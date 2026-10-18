
import pytest
from pydantic import ValidationError

from app.schemas import ParticipantCreate
from app.registration_logic import (
    has_available_capacity,
    check_duplicate_registration,
)


# 1. Name and email rules

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


# 2. Capacity check logic

def test_capacity_available():
    assert has_available_capacity(5, 10) is True


def test_capacity_one_slot_remaining():
    assert has_available_capacity(9, 10) is True


def test_capacity_exactly_full():
    assert has_available_capacity(10, 10) is False


def test_capacity_exceeded():
    assert has_available_capacity(11, 10) is False


# 3. Duplicate registration guard

def test_duplicate_registration_raises_error():
    registered_ids = [1, 2, 3]

    with pytest.raises(ValueError):
        check_duplicate_registration(registered_ids, 3)


def test_new_registration_is_not_duplicate():
    registered_ids = [1, 2, 3]

    # No exception should be raised for a new participant.
    check_duplicate_registration(registered_ids, 4)
