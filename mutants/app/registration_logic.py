


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_has_available_capacity__mutmut: MutantDict = {}  # type: ignore
@_mutmut_mutated(mutants_x_has_available_capacity__mutmut)
def has_available_capacity(current_count, max_capacity):
    return current_count < max_capacity
def x_has_available_capacity__mutmut_orig(current_count, max_capacity):
    return current_count < max_capacity
def x_has_available_capacity__mutmut_1(current_count, max_capacity):
    return current_count <= max_capacity

mutants_x_has_available_capacity__mutmut['_mutmut_orig'] = x_has_available_capacity__mutmut_orig # type: ignore # mutmut generated
mutants_x_has_available_capacity__mutmut['x_has_available_capacity__mutmut_1'] = x_has_available_capacity__mutmut_1 # type: ignore # mutmut generated
mutants_x_check_duplicate_registration__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_check_duplicate_registration__mutmut)
def check_duplicate_registration(registered_ids, new_id):
    if new_id in registered_ids:
        raise ValueError("Participant is already registered.")


def x_check_duplicate_registration__mutmut_orig(registered_ids, new_id):
    if new_id in registered_ids:
        raise ValueError("Participant is already registered.")


def x_check_duplicate_registration__mutmut_1(registered_ids, new_id):
    if new_id not in registered_ids:
        raise ValueError("Participant is already registered.")


def x_check_duplicate_registration__mutmut_2(registered_ids, new_id):
    if new_id in registered_ids:
        raise ValueError(None)


def x_check_duplicate_registration__mutmut_3(registered_ids, new_id):
    if new_id in registered_ids:
        raise ValueError("XXParticipant is already registered.XX")


def x_check_duplicate_registration__mutmut_4(registered_ids, new_id):
    if new_id in registered_ids:
        raise ValueError("participant is already registered.")


def x_check_duplicate_registration__mutmut_5(registered_ids, new_id):
    if new_id in registered_ids:
        raise ValueError("PARTICIPANT IS ALREADY REGISTERED.")

mutants_x_check_duplicate_registration__mutmut['_mutmut_orig'] = x_check_duplicate_registration__mutmut_orig # type: ignore # mutmut generated
mutants_x_check_duplicate_registration__mutmut['x_check_duplicate_registration__mutmut_1'] = x_check_duplicate_registration__mutmut_1 # type: ignore # mutmut generated
mutants_x_check_duplicate_registration__mutmut['x_check_duplicate_registration__mutmut_2'] = x_check_duplicate_registration__mutmut_2 # type: ignore # mutmut generated
mutants_x_check_duplicate_registration__mutmut['x_check_duplicate_registration__mutmut_3'] = x_check_duplicate_registration__mutmut_3 # type: ignore # mutmut generated
mutants_x_check_duplicate_registration__mutmut['x_check_duplicate_registration__mutmut_4'] = x_check_duplicate_registration__mutmut_4 # type: ignore # mutmut generated
mutants_x_check_duplicate_registration__mutmut['x_check_duplicate_registration__mutmut_5'] = x_check_duplicate_registration__mutmut_5 # type: ignore # mutmut generated
