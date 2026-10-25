

from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_filter_events_by_location__mutmut: MutantDict = {}  # type: ignore
@_mutmut_mutated(mutants_x_filter_events_by_location__mutmut)
def filter_events_by_location(events, location):
    return [
        event for event in events
        if event.location.lower() == location.lower()
    ]
def x_filter_events_by_location__mutmut_orig(events, location):
    return [
        event for event in events
        if event.location.lower() == location.lower()
    ]
def x_filter_events_by_location__mutmut_1(events, location):
    return [
        event for event in events
        if event.location.upper() == location.lower()
    ]
def x_filter_events_by_location__mutmut_2(events, location):
    return [
        event for event in events
        if event.location.lower() != location.lower()
    ]
def x_filter_events_by_location__mutmut_3(events, location):
    return [
        event for event in events
        if event.location.lower() == location.upper()
    ]

mutants_x_filter_events_by_location__mutmut['_mutmut_orig'] = x_filter_events_by_location__mutmut_orig # type: ignore # mutmut generated
mutants_x_filter_events_by_location__mutmut['x_filter_events_by_location__mutmut_1'] = x_filter_events_by_location__mutmut_1 # type: ignore # mutmut generated
mutants_x_filter_events_by_location__mutmut['x_filter_events_by_location__mutmut_2'] = x_filter_events_by_location__mutmut_2 # type: ignore # mutmut generated
mutants_x_filter_events_by_location__mutmut['x_filter_events_by_location__mutmut_3'] = x_filter_events_by_location__mutmut_3 # type: ignore # mutmut generated
mutants_x_filter_events_by_title__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_filter_events_by_title__mutmut)
def filter_events_by_title(events, title):
    return [
        event for event in events
        if title.lower() in event.title.lower()
    ]


def x_filter_events_by_title__mutmut_orig(events, title):
    return [
        event for event in events
        if title.lower() in event.title.lower()
    ]


def x_filter_events_by_title__mutmut_1(events, title):
    return [
        event for event in events
        if title.upper() in event.title.lower()
    ]


def x_filter_events_by_title__mutmut_2(events, title):
    return [
        event for event in events
        if title.lower() not in event.title.lower()
    ]


def x_filter_events_by_title__mutmut_3(events, title):
    return [
        event for event in events
        if title.lower() in event.title.upper()
    ]

mutants_x_filter_events_by_title__mutmut['_mutmut_orig'] = x_filter_events_by_title__mutmut_orig # type: ignore # mutmut generated
mutants_x_filter_events_by_title__mutmut['x_filter_events_by_title__mutmut_1'] = x_filter_events_by_title__mutmut_1 # type: ignore # mutmut generated
mutants_x_filter_events_by_title__mutmut['x_filter_events_by_title__mutmut_2'] = x_filter_events_by_title__mutmut_2 # type: ignore # mutmut generated
mutants_x_filter_events_by_title__mutmut['x_filter_events_by_title__mutmut_3'] = x_filter_events_by_title__mutmut_3 # type: ignore # mutmut generated