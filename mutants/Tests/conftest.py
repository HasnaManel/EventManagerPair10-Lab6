
import pytest
#from app.models import Event
from app.models import Event

@pytest.fixture
def sample_event_dict():
    return {
        "title": "Python Workshop",
        "description": "Learn Python basics",
        "date": "2027-05-15",
        "location": "Algiers",
        "capacity": 50,
    }


@pytest.fixture
def sample_participant_dict():
    return {
        "name": "Lina",
        "email": "lina@example.com",
    }


@pytest.fixture
def mock_event_store():
    store = []

    yield store

    store.clear()


@pytest.fixture
def prepopulated_event_store(
    mock_event_store,
    sample_event_dict
):
    for i in range(3):
        event = sample_event_dict.copy()
        event["title"] = f"Event {i + 1}"
        mock_event_store.append(event)

    return mock_event_store

#ChatGPT changed this  not me
@pytest.fixture
def prepopulated_event_store(mock_event_store, sample_event_dict):
    for i in range(3):
        event_data = sample_event_dict.copy()
        event_data["title"] = f"Event {i + 1}"

        event = Event(**event_data)
        mock_event_store.append(event)

    return mock_event_store



@pytest.fixture(autouse=True)
def global_environment_logger():
    print("\n--- Test setup ---")

    yield

    print("\n--- Test teardown ---")
