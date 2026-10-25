

import pytest
from pydantic import ValidationError


#def test_event_title_length(sample_event_dict):
#    assert  len(sample_event_dict['title']) >= 3


from app.schemas import EventCreate

# Change this import to the module where your search helpers are defined.
from app.utils.event_search import (
    filter_events_by_location,
    filter_events_by_title,
)


'''
#Strong tests
# HAPPY PATH TEST 1: Valid event creation
def test_valid_event_instantiation(sample_event_dict):
    event = EventCreate(**sample_event_dict)

    assert event.title == "Python Workshop"
    assert event.capacity == 50


# HAPPY PATH TEST 2: Filter events by location
def test_filter_events_by_location(prepopulated_event_store):
    results = filter_events_by_location(
        prepopulated_event_store,
        "aLgIeRs"
    )


    assert len(results) == 3
    assert all(event.location.lower() == "algiers" for event in results)

'''


# Weak tests:
# HAPPY PATH TEST 2: Filter events by location (weak version)
def test_filter_events_by_location(prepopulated_event_store):
    results = filter_events_by_location(prepopulated_event_store, "algiers")
    assert isinstance(results, list)

'''
# HAPPY PATH TEST 3: Filter events by title (weak version)
def test_filter_events_by_title(prepopulated_event_store):
    results = filter_events_by_title(prepopulated_event_store, "event 1")
    assert isinstance(results, list)
'''    
# HAPPY PATH TEST 3: Filter events by title (very weak version)
def test_filter_events_by_title(prepopulated_event_store):
    results = filter_events_by_title(prepopulated_event_store, "event 1")
    assert results is not None
    
    
    
    
# HAPPY PATH TEST 3: Filter events by title
def test_filter_events_by_title(prepopulated_event_store):
    results = filter_events_by_title(
        prepopulated_event_store,
        "eVeNt 1"
    )

    assert len(results) == 1
    assert results[0].title == "Event 1"


# BOUNDARY TEST 1: Minimum valid capacity
def test_capacity_minimum(sample_event_dict):
    data = sample_event_dict.copy()
    data["capacity"] = 1

    event = EventCreate(**data)

    assert event.capacity == 1


# BOUNDARY TEST 2: Maximum valid capacity
def test_capacity_maximum(sample_event_dict):
    data = sample_event_dict.copy()
    data["capacity"] = 10000

    event = EventCreate(**data)

    assert event.capacity == 10000


# BOUNDARY TEST 3: Minimum valid title length
def test_title_minimum_length(sample_event_dict):
    data = sample_event_dict.copy()
    data["title"] = "ABC"

    event = EventCreate(**data)

    assert event.title == "ABC"


# NEGATIVE TEST 1: Title shorter than 3 characters
def test_short_title_raises_validation_error(sample_event_dict):
    data = sample_event_dict.copy()
    data["title"] = "AB"

    with pytest.raises(ValidationError):
        EventCreate(**data)


# NEGATIVE TEST 2: Invalid capacities
@pytest.mark.parametrize("capacity", [0, -1])
def test_invalid_capacity_raises_validation_error(
    sample_event_dict,
    capacity
):
    data = sample_event_dict.copy()
    data["capacity"] = capacity

    with pytest.raises(ValidationError):
        EventCreate(**data)

#----------------------Tests added to improve coverage -------------------
from unittest.mock import MagicMock
from fastapi import HTTPException

from app.routers.events import get_event


def test_get_missing_event_without_database():
    mock_db = MagicMock()

    # Simulate a database query that finds no event
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        get_event(event_id=999, db=mock_db)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Event not found."
    

from unittest.mock import MagicMock
from app.routers.events import get_event


def test_get_existing_event():
    mock_db = MagicMock()

    fake_event = MagicMock()
    fake_event.id = 1

    mock_db.query.return_value.filter.return_value.first.return_value = fake_event

    result = get_event(event_id=1, db=mock_db)

    assert result == fake_event
    
    
from app.routers.events import delete_event


def test_delete_existing_event():
    mock_db = MagicMock()

    fake_event = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = fake_event

    result = delete_event(event_id=1, db=mock_db)

    mock_db.delete.assert_called_once_with(fake_event)
    mock_db.commit.assert_called_once()
    assert result is None
    
from app.routers.events import update_event
from app.schemas import EventUpdate


def test_update_missing_event():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    update_data = EventUpdate(
        title="Updated Workshop",
        description="Updated description",
        date="2027-06-15",
        location="Algiers",
        capacity=30,
    )

    with pytest.raises(HTTPException) as exc_info:
        update_event(event_id=999, event_data=update_data, db=mock_db)

    assert exc_info.value.status_code == 404
    

from app.routers.events import list_events


def test_list_events_without_search():
    mock_db = MagicMock()
    fake_events = [MagicMock(), MagicMock()]

    mock_db.query.return_value.order_by.return_value.all.return_value = fake_events

    result = list_events(search=None, db=mock_db)

    assert result == fake_events


def test_list_events_with_search():
    mock_db = MagicMock()
    fake_events = [MagicMock()]

    query_mock = mock_db.query.return_value
    query_mock.filter.return_value.order_by.return_value.all.return_value = fake_events

    result = list_events(search="Python", db=mock_db)

    query_mock.filter.assert_called_once()
    assert result == fake_events