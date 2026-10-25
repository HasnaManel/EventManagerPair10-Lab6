import importlib
from datetime import date, timedelta
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.database import Base, get_db
from app.models import Event, Participant, Registration
from app.schemas import ParticipantCreate
from app.registration_logic import (
    has_available_capacity,
    check_duplicate_registration,
)
from app.routers.participants import (
    create_participant,
    list_participants,
    get_participant,
    delete_participant,
)
from app.routers.registrations import (
    register_participant,
    list_event_participants,
)


# Import the app while preventing create_all() from running here.
with patch.object(Base.metadata, "create_all"):
    app = importlib.import_module("app.main").app


# ============================================================
# Fixtures for FastAPI TestClient
# ============================================================

@pytest.fixture
def api_mock_db():
    return MagicMock()


@pytest.fixture
def api_client(api_mock_db):
    app.dependency_overrides[get_db] = lambda: api_mock_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


# ============================================================
# Helper functions for mocking the database
# ============================================================

def mock_db_for(model, result):
    db = MagicMock()
    query = MagicMock()

    db.query.return_value = query
    query.filter.return_value.first.return_value = result
    query.order_by.return_value.all.return_value = (
        result if isinstance(result, list) else []
    )

    return db


def mock_query_results(results):
    db = MagicMock()
    queries = {}

    for model, result in results.items():
        query = MagicMock()
        query.filter.return_value.first.return_value = result
        query.order_by.return_value.all.return_value = (
            result if isinstance(result, list) else []
        )
        queries[model] = query

    db.query.side_effect = lambda model: queries[model]
    return db


def make_participant(**overrides):
    values = {
        "id": 1,
        "name": "Lina",
        "email": "lina@example.com",
    }
    values.update(overrides)

    participant = MagicMock(spec=Participant)

    for key, value in values.items():
        setattr(participant, key, value)

    return participant


def make_event(**overrides):
    values = {
        "id": 1,
        "title": "Python Workshop",
        "description": "Learn Python",
        "date": date.today() + timedelta(days=10),
        "location": "Algiers",
        "capacity": 10,
        "registrations": [],
    }
    values.update(overrides)

    event = MagicMock(spec=Event)

    for key, value in values.items():
        setattr(event, key, value)

    return event


# ============================================================
# 1. Participant name and email validation
# ============================================================

def test_valid_participant(sample_participant_dict):
    participant = ParticipantCreate(**sample_participant_dict)

    assert participant.name == "Lina"
    assert participant.email == "lina@example.com"


def test_participant_name_too_short(sample_participant_dict):
    data = sample_participant_dict.copy()
    data["name"] = "A"

    with pytest.raises(ValidationError):
        ParticipantCreate(**data)


def test_invalid_participant_email(sample_participant_dict):
    data = sample_participant_dict.copy()
    data["email"] = "not-an-email"

    with pytest.raises(ValidationError):
        ParticipantCreate(**data)


# ============================================================
# 2. Capacity check logic
# ============================================================

def test_capacity_available():
    assert has_available_capacity(5, 10) is True


def test_capacity_one_slot_remaining():
    assert has_available_capacity(9, 10) is True


def test_capacity_exactly_full():
    assert has_available_capacity(10, 10) is False


def test_capacity_exceeded():
    assert has_available_capacity(11, 10) is False


# ============================================================
# 3. Duplicate registration logic
# ============================================================

def test_duplicate_registration_raises_error():
    registered_ids = [1, 2, 3]

    with pytest.raises(ValueError) as exc:
        check_duplicate_registration(registered_ids, 3)

    assert str(exc.value) == "Participant is already registered."


def test_new_registration_is_not_duplicate():
    registered_ids = [1, 2, 3]

    assert check_duplicate_registration(registered_ids, 4) is None


# ============================================================
# 4. Participant route tests with mocked database sessions
# ============================================================

def test_create_participant_mocked():
    db = mock_db_for(Participant, None)

    data = ParticipantCreate(
        name="Lina",
        email="lina@example.com",
    )

    result = create_participant(participant=data, db=db)

    assert result.name == "Lina"
    assert result.email == "lina@example.com"
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(result)


def test_create_participant_rejects_duplicate_email():
    existing = make_participant()
    db = mock_db_for(Participant, existing)

    data = ParticipantCreate(
        name="Another Person",
        email="lina@example.com",
    )

    with pytest.raises(HTTPException) as exc:
        create_participant(participant=data, db=db)

    assert exc.value.status_code == 409
    db.add.assert_not_called()


def test_list_participants_mocked():
    participants = [make_participant()]
    db = mock_db_for(Participant, participants)

    result = list_participants(db=db)

    assert result == participants


def test_get_participant_missing():
    db = mock_db_for(Participant, None)

    with pytest.raises(HTTPException) as exc:
        get_participant(participant_id=999, db=db)

    assert exc.value.status_code == 404


def test_delete_participant_missing():
    db = mock_db_for(Participant, None)

    with pytest.raises(HTTPException) as exc:
        delete_participant(participant_id=999, db=db)

    assert exc.value.status_code == 404
    db.delete.assert_not_called()


# ============================================================
# 5. Registration route tests with mocked database sessions
# ============================================================

def test_register_participant_event_missing():
    db = mock_query_results({Event: None})

    with pytest.raises(HTTPException) as exc:
        register_participant(
            event_id=1,
            participant_id=1,
            db=db,
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Event not found."


def test_register_participant_missing_participant():
    event = make_event()

    db = mock_query_results({
        Event: event,
        Participant: None,
    })

    with pytest.raises(HTTPException) as exc:
        register_participant(
            event_id=1,
            participant_id=2,
            db=db,
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Participant not found."


def test_register_participant_duplicate():
    event = make_event()
    existing = MagicMock(spec=Registration)

    db = mock_query_results({
        Event: event,
        Participant: make_participant(),
        Registration: existing,
    })

    with pytest.raises(HTTPException) as exc:
        register_participant(
            event_id=1,
            participant_id=1,
            db=db,
        )

    assert exc.value.status_code == 409
    assert exc.value.detail == "Participant is already registered."
    db.add.assert_not_called()


def test_register_participant_capacity_reached():
    event = make_event(
        capacity=1,
        registrations=[MagicMock()],
    )

    db = mock_query_results({
        Event: event,
        Participant: make_participant(),
        Registration: None,
    })

    with pytest.raises(HTTPException) as exc:
        register_participant(
            event_id=1,
            participant_id=1,
            db=db,
        )

    assert exc.value.status_code == 409
    assert exc.value.detail == "Event capacity has been reached."
    db.add.assert_not_called()


def test_register_participant_success():
    db = mock_query_results({
        Event: make_event(),
        Participant: make_participant(),
        Registration: None,
    })

    result = register_participant(
        event_id=1,
        participant_id=1,
        db=db,
    )

    assert result.event_id == 1
    assert result.participant_id == 1
    db.add.assert_called_once_with(result)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(result)


def test_list_event_participants_missing_event():
    db = mock_db_for(Event, None)

    with pytest.raises(HTTPException) as exc:
        list_event_participants(event_id=999, db=db)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Event not found."


def test_list_event_participants_success():
    participant = make_participant()

    registration = MagicMock(spec=Registration)
    registration.participant = participant

    event = make_event(registrations=[registration])
    db = mock_db_for(Event, event)

    result = list_event_participants(event_id=1, db=db)

    assert result == [
        {
            "id": 1,
            "name": "Lina",
            "email": "lina@example.com",
        }
    ]


# ============================================================
# 6. FastAPI TestClient API tests
# ============================================================

def test_create_participant_api(api_client, api_mock_db):
    query = MagicMock()
    api_mock_db.query.return_value = query
    query.filter.return_value.first.return_value = None

    def set_id(participant):
        participant.id = 1

    api_mock_db.refresh.side_effect = set_id

    response = api_client.post(
        "/participants/",
        json={
            "name": "Lina",
            "email": "lina@example.com",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Lina"
    assert response.json()["email"] == "lina@example.com"
    api_mock_db.add.assert_called_once()
    api_mock_db.commit.assert_called_once()


def test_create_participant_duplicate_email_api(
    api_client, api_mock_db
):
    query = MagicMock()
    api_mock_db.query.return_value = query
    query.filter.return_value.first.return_value = make_participant()

    response = api_client.post(
        "/participants/",
        json={
            "name": "Another Person",
            "email": "lina@example.com",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email is already registered."
    api_mock_db.add.assert_not_called()


def test_create_participant_invalid_email_api(
    api_client, api_mock_db
):
    response = api_client.post(
        "/participants/",
        json={
            "name": "Lina",
            "email": "not-an-email",
        },
    )

    assert response.status_code == 422
    api_mock_db.query.assert_not_called()


def test_get_missing_participant_api(api_client, api_mock_db):
    query = MagicMock()
    api_mock_db.query.return_value = query
    query.filter.return_value.first.return_value = None

    response = api_client.get("/participants/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found."