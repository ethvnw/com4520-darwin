import collections
from pathlib import Path
import pickle

import pytest

from fsm_gen.generator import FSMGenerator


@pytest.fixture
def fsm():
    return FSMGenerator(num_states=6, num_inputs=4, num_outputs=4)


def is_connected(fsm):
    def dfs(start_state):
        visited = set()
        stack = [start_state]
        while stack:
            state = stack.pop()
            if state not in visited:
                visited.add(state)
                for transition in fsm.transitions:
                    if transition["source"] == state:
                        stack.append(transition["dest"])
        return visited

    all_states = set(fsm.states)
    for state in fsm.states:
        if dfs(state) != all_states:
            return False

    return True

def is_deterministic(fsm):
    events = collections.Counter(fsm.events)

    for state in fsm.states:
        transitions = [t for t in fsm.transitions if t["source"] == state]
        triggers = [t["trigger"].split(" / ")[0] for t in transitions]

        if collections.Counter(triggers) != events:
            return False

    return True

def test_fsm_creation(fsm: FSMGenerator):
    """Test that the generator creates a FSM with correct numbers of states, events, and transitions."""
    assert len(fsm.states) == 6
    assert len(fsm.events) == 4
    assert len(fsm.transitions) == len(fsm.states) * len(
        fsm.events
    )  # each state has a transition for each event
    assert fsm.states[0] == "S0"
    assert all(state.startswith("S") for state in fsm.states)


def test_fsm_zero_states():
    """Raise an error if the number of states is zero."""
    with pytest.raises(IndexError):
        FSMGenerator(num_states=0, num_inputs=3, num_outputs=3)


def test_fsm_zero_inputs():
    """Raise an error if the number of inputs is zero."""
    with pytest.raises(ValueError):
        FSMGenerator(num_states=4, num_inputs=0, num_outputs=3)


def test_fsm_zero_outputs():
    """Raise an error if the number of outputs is zero."""
    with pytest.raises(IndexError):
        FSMGenerator(num_states=4, num_inputs=3, num_outputs=0)


def test_fsm_negative_states():
    """Raise an error if the number of states is negative."""
    with pytest.raises(IndexError):
        FSMGenerator(num_states=-1, num_inputs=3, num_outputs=3)


def test_fsm_negative_inputs():
    """Raise an error if the number of inputs is negative."""
    with pytest.raises(ValueError):
        FSMGenerator(num_states=4, num_inputs=-1, num_outputs=3)


def test_fsm_negative_outputs():
    """Raise an error if the number of outputs is negative."""
    with pytest.raises(IndexError):
        FSMGenerator(num_states=4, num_inputs=3, num_outputs=-1)


def test_fsm_single_state():
    """Test that the generator creates a FSM with a single state."""
    fsm = FSMGenerator(num_states=1, num_inputs=3, num_outputs=3)
    assert len(fsm.states) == 1
    assert len(fsm.events) == 3
    assert len(fsm.transitions) == len(fsm.states) * len(fsm.events)
    assert fsm.states[0] == "S0"


def test_no_reachable_states():
    """Test that the FSM is not connected if there are no transitions."""
    fsm = FSMGenerator(num_states=3, num_inputs=3, num_outputs=3)
    fsm.transitions = []  # Removing transitions
    assert not is_connected(fsm)


def test_generate_transitions(fsm: FSMGenerator):
    """Test that transitions are generated correctly and have the required fields."""
    assert isinstance(fsm.transitions, list)
    assert len(fsm.transitions) > 0
    for transition in fsm.transitions:
        assert "trigger" in transition
        assert "source" in transition
        assert "dest" in transition
        assert transition["source"] in fsm.states
        assert transition["dest"] in fsm.states
    transi = fsm._generate_transitions()
    for trans in transi:
        assert "trigger" in trans
        assert "source" in trans
        assert "dest" in trans


def test_is_reachable_from():
    """Test the function to check if a state is reachable from another."""
    fsm = FSMGenerator(num_states=4, num_inputs=3, num_outputs=3)
    for state in fsm.states:
        for target in fsm.states:
            assert fsm._is_reachable_from(state, target) or (state == target)


def test_try_generate_connected_machine(fsm: FSMGenerator):
    """Test that the FSM generator can create a connected machine."""
    fsm._try_generate_connected_machine()
    assert is_connected(fsm)


def test_fsm_connected():
    """Test that the FSM is connected."""
    fsm = FSMGenerator(num_states=6, num_inputs=4, num_outputs=4)
    assert is_connected(fsm)


def test_no_duplicate_transitions():
    """Test that there are no duplicate transitions in the FSM."""
    fsm = FSMGenerator(num_states=6, num_inputs=4, num_outputs=4)
    transitions = [(t["source"], t["dest"], t["trigger"]) for t in fsm.transitions]
    assert len(transitions) == len(set(transitions))


def test_fsm_deterministic():
    """Test that the FSM is deterministic."""
    fsm = FSMGenerator(num_states=5, num_inputs=3, num_outputs=3)
    assert is_deterministic(fsm)


def test_fsm_minimal():
    """Test that the FSM is minimal after minimization."""
    fsm = FSMGenerator(num_states=7, num_inputs=4, num_outputs=4)
    initial_state_count = len(fsm.states)
    fsm._make_minimal()
    assert is_connected(fsm)
    assert is_deterministic(fsm)
    assert len(fsm.states) <= initial_state_count


def test_get_triggers():
    """Test getting triggers from a state."""
    fsm = FSMGenerator(num_states=5, num_inputs=3, num_outputs=3)
    state = fsm.states[0]
    triggers = fsm._get_triggers(state)
    assert isinstance(triggers, list)
    assert all(isinstance(trigger, str) for trigger in triggers)


def test_add_leftover_transitions():
    """Test adding transitions that are missing to make the FSM complete."""
    fsm = FSMGenerator(num_states=6, num_inputs=4, num_outputs=4)
    initial_transitions = len(fsm.transitions)
    fsm._add_leftover_transitions()
    assert len(fsm.transitions) >= initial_transitions
    for state in fsm.states:
        triggers = [trigger[0] for trigger in fsm._get_triggers(state)]
        assert sorted(triggers) == sorted(fsm.events)


def test_find_1_equivalent(fsm: FSMGenerator):
    """Test finding 1-equivalent states in the FSM."""
    equivalence_sets = fsm._find_1_equivalent()
    assert isinstance(equivalence_sets, dict)
    for key, value in equivalence_sets.items():
        assert isinstance(value, set)


def test_get_dest_from_trigger():
    """Test getting the destination state from a trigger."""
    fsm = FSMGenerator(num_states=6, num_inputs=4, num_outputs=4)
    state = fsm.states[0]
    trigger = fsm._get_triggers(state)[0]
    dest = fsm._get_dest_from_trigger(state, trigger)
    assert dest in fsm.states or dest is None


def test_invalid_transition(fsm: FSMGenerator):
    """Test that an error is raised if the transition is invalid."""
    with pytest.raises(LookupError):
        fsm._get_dest_from_trigger("S0", "INVALID_TRIGGER")


def test_get_transitions():
    """Test getting all transitions from a state."""
    fsm = FSMGenerator(num_states=6, num_inputs=4, num_outputs=4)
    state = fsm.states[0]
    transitions = fsm._get_transitions(source=state)
    assert isinstance(transitions, list)
    for transition in transitions:
        assert "trigger" in transition
        assert "source" in transition
        assert "dest" in transition


def test_find_equivalent_states():
    """Test finding equivalent states in the FSM."""
    fsm = FSMGenerator(num_states=6, num_inputs=4, num_outputs=4)
    equivalent_states = fsm._find_equivalent_states()
    assert isinstance(equivalent_states, list)
    for eqviv_set in equivalent_states:
        assert isinstance(eqviv_set, set)


def test_cleanup_transitions():
    """Test removing duplicate transitions from the FSM."""
    fsm = FSMGenerator(num_states=6, num_inputs=4, num_outputs=4)
    initial_transitions = len(fsm.transitions)
    fsm._cleanup_transitions()
    assert len(fsm.transitions) <= initial_transitions


def test_save(tmp_path: Path):
    """Test saving the FSM and loading it from a file."""
    fsm = FSMGenerator(num_states=3, num_inputs=2, num_outputs=2)
    file_path = tmp_path / "fsm.pkl"

    fsm.save(str(file_path))
    loaded_fsm = pickle.load(open(file_path, "rb"))

    assert loaded_fsm.states == fsm.states
    assert loaded_fsm.events == fsm.events
    assert loaded_fsm.transitions == fsm.transitions


def test_load_corrupted_file(tmp_path: Path):
    """Test that loading a corrupted file raises an UnpicklingError."""
    file_path = tmp_path / "corrupted_fsm.pkl"
    with open(file_path, "wb") as f:
        f.write(b"corrupted_data")

    with pytest.raises(pickle.UnpicklingError):
        pickle.load(open(file_path, "rb"))


def test_apply_input_sequence(fsm: FSMGenerator):
    """Test applying an input sequence to the FSM."""
    state = fsm.states[0]
    sequence = "".join(fsm.events)  # Using all possible events

    final_state, output_seq = fsm.apply_input_sequence(state, sequence)

    assert final_state in fsm.states
    assert isinstance(output_seq, tuple)
    assert len(output_seq) == len(sequence)


def test_apply_invalid_sequence(fsm: FSMGenerator):
    """Test that applying an invalid input sequence raises a ValueError."""
    state = fsm.states[0]
    with pytest.raises(ValueError):
        fsm.apply_input_sequence(state, "INVALID_EVENT")


def test_draw_invalid_path(fsm: FSMGenerator):
    """Test that drawing to an invalid path raises an OSError."""
    with pytest.raises(OSError):
        fsm.draw("/invalid/path/image.png")
