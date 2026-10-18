def filter_events_by_location(events, location):
    return [
        event for event in events
        if event.location.lower() == location.lower()
    ]


def filter_events_by_title(events, title):
    return [
        event for event in events
        if title.lower() in event.title.lower()
    ]