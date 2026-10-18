

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
