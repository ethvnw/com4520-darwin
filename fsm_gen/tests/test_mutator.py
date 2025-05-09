import pytest

from fsm_gen.case_studies import LocalisationSystem
from fsm_gen.mutator import Mutator


@pytest.fixture
def mutator():
    """
    Create a fresh Mutator instance with a new FSM for each test.
    """
    fsm = LocalisationSystem()
    return Mutator(fsm)


@pytest.fixture
def fsm():
    """
    Create a fresh FSM.
    """
    return LocalisationSystem()


def test_add_state(mutator):
    """
    Test that the add_state function increases the number of states in the FSM.
    """
    initial_state_count = len(mutator.fsm.states)
    mutator._add_state()
    assert len(mutator.fsm.states) == initial_state_count + 1


def test_remove_state(mutator):
    """
    Test that the remove_state function decreases the number of states in the FSM.
    """
    initial_state_count = len(mutator.fsm.states)
    mutator._remove_state()
    assert len(mutator.fsm.states) == initial_state_count - 1


def test_change_trigger_output(mutator):
    """
    Test that the change_trigger_output function changes the output of a trigger.
    """
    initial_triggers = [t["trigger"] for t in mutator.fsm.transitions]
    initial_sources = [t["source"] for t in mutator.fsm.transitions]
    initial_destinations = [t["dest"] for t in mutator.fsm.transitions]

    mutator._change_trigger_output()

    changed_triggers = sum(
        t["trigger"].split(" / ")[1] != initial_triggers[i].split(" / ")[1]
        for i, t in enumerate(mutator.fsm.transitions)
    )
    assert changed_triggers == 1

    # Check that all sources remain the same
    assert all(
        t["source"] == initial_sources[i] for i, t in enumerate(mutator.fsm.transitions)
    )
    # Check that all destinations remain the same
    assert all(
        t["dest"] == initial_destinations[i]
        for i, t in enumerate(mutator.fsm.transitions)
    )


def test_change_trans_dest(mutator):
    """
    Test that the change_trans_dest function changes the destination of a transition.
    """
    initial_triggers = [t["trigger"] for t in mutator.fsm.transitions]
    initial_sources = [t["source"] for t in mutator.fsm.transitions]
    initial_destinations = [t["dest"] for t in mutator.fsm.transitions]

    mutator._change_trans_dest()

    # Check that only one destination has changed
    changed_destinations = sum(
        t["dest"] != initial_destinations[i]
        for i, t in enumerate(mutator.fsm.transitions)
    )
    assert changed_destinations == 1

    # Check that all triggers remain the same
    assert all(
        t["trigger"] == initial_triggers[i]
        for i, t in enumerate(mutator.fsm.transitions)
    )
    # Check that all sources remain the same
    assert all(
        t["source"] == initial_sources[i] for i, t in enumerate(mutator.fsm.transitions)
    )


def test_get_num_transitions_exclude_loops(mutator):
    """
    Test that the get_num_transitions function excludes loops from the count.
    """
    # S0 has 2 self-loops, 2 outgoing and 3 incoming transitions
    assert mutator._get_num_transitions_exclude_loops("S0", incoming=True) == 3
    assert mutator._get_num_transitions_exclude_loops("S0", incoming=False) == 2


def test_check_determinsism(mutator):
    """
    Test that the check_determinsism function correctly identifies a non-deterministic FSM.
    """
    assert mutator._check_determinism() is True
    # Add a non-deterministic transition
    mutator.fsm.transitions.append({"trigger": "N / a", "source": "S0", "dest": "S1"})
    assert mutator._check_determinism() is False


def test_check_connectivity(mutator, fsm):
    """
    Test that the check_connectivity function correctly identifies a connected FSM.
    """
    assert mutator._check_connectivity() is True
    # Add a disconnected state
    mutator.fsm.states.append("S3")
    assert mutator._check_connectivity() is False
    # Remove outbound transitions from S2
    mutator.fsm.transitions = [
        t for t in mutator.fsm.transitions if t["source"] != "S2"
    ]
    assert mutator._check_connectivity() is False


def test_create_mutated_fsm(mutator, fsm):
    """
    Test that the create_mutated_fsm function creates a mutated FSM that is different from the original.
    """
    mutated_fsm = mutator.create_mutated_fsm()
    assert mutated_fsm != fsm

    for mutation_applied in mutator.mutations_applied:
        if mutation_applied == "add_state":
            assert len(mutated_fsm.states) == len(fsm.states) + 1
        elif mutation_applied == "remove_state":
            assert len(mutated_fsm.states) == len(fsm.states) - 1
        elif mutation_applied == "change_trigger_output":
            assert len(mutated_fsm.transitions) == len(fsm.transitions)
            assert mutated_fsm.transitions != fsm.transitions
        elif mutation_applied == "change_trans_dest":
            assert len(mutated_fsm.transitions) == len(fsm.transitions)
            assert mutated_fsm.transitions != fsm.transitions
