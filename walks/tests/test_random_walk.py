from typing import Any
from unittest.mock import MagicMock

import pytest

from fsm_gen.generator import FSMGenerator
from fsm_gen.machine import Machine
from fsm_gen.mutator import Mutator
from walks.random_walk import RandomWalk


@pytest.fixture
def simple_fsm():
    fsm = MagicMock(spec=FSMGenerator)
    mock_machine = MagicMock()
    mock_machine.initial = "S0"
    mock_machine.state = "S0"

    # Mock triggers and transitions
    fsm._get_triggers.return_value = ["a", "b", "c"]
    fsm.machine = mock_machine
    fsm.events = ["a", "b", "c"]
    fsm.transitions = [
        {"source": "S0", "trigger": "a", "dest": "S1"},
        {"source": "S1", "trigger": "b", "dest": "S2"},
        {"source": "S2", "trigger": "c", "dest": "S0"},
    ]
    fsm.states = ["S0", "S1", "S2"]
    fsm.apply_input_sequence = MagicMock(
        side_effect=lambda state, seq: (state, tuple("0" for _ in seq))
    )

    return fsm


@pytest.fixture
def mutated_fsm2():
    fsm = MagicMock(spec=FSMGenerator)
    mock_machine = MagicMock()
    mock_machine.initial = "S0"
    mock_machine.state = "S0"

    # Mock triggers and transitions
    fsm.machine = mock_machine
    fsm.events = ["a", "b", "c"]
    fsm.transitions = [
        {"source": "S0", "trigger": "a", "dest": "S1"},
        {"source": "S1", "trigger": "b", "dest": "S2"},
        {"source": "S2", "trigger": "c", "dest": "S0"},
    ]
    fsm.states = ["S0", "S1", "S2"]

    # Apply mutations using the Mutator
    mutator = Mutator(fsm)
    mutated_fsm2 = mutator.create_mutated_fsm()

    return mutated_fsm2


@pytest.fixture
def mutated_fsm1():
    mutated_fsm1 = MagicMock(spec=FSMGenerator)
    mock_machine = MagicMock()
    mock_machine.initial = "S0"
    mock_machine.state = "S0"

    # Mock triggers and transitions
    mutated_fsm1.events = ["a", "b", "c"]
    mutated_fsm1._get_triggers.return_value = ["a", "b", "c"]
    mutated_fsm1.machine = mock_machine
    mutated_fsm1.transitions = [
        {"source": "S0", "trigger": "a", "dest": "S1"},
        {"source": "S1", "trigger": "a", "dest": "S2"},
        {"source": "S2", "trigger": "c", "dest": "S0"},
    ]

    return mutated_fsm1


@pytest.fixture
def loop_fsm():
    mock_fsm = MagicMock(spec=FSMGenerator)
    mock_machine = MagicMock()
    mock_machine.initial = "S0"
    mock_machine.state = "S0"

    # Mock triggers and transitions
    mock_fsm._get_triggers.return_value = ["a", "b", "c"]
    mock_fsm.machine = mock_machine
    mock_fsm.events = ["a", "b", "c"]
    mock_fsm.transitions = [
        {"source": "S0", "trigger": "a", "dest": "S1"},
        {"source": "S1", "trigger": "b", "dest": "S0"},
        {"source": "S1", "trigger": "a", "dest": "S2"},
        {"source": "S2", "trigger": "c", "dest": "S1"},
    ]
    mock_fsm.states = ["S0", "S1", "S2"]

    return mock_fsm


@pytest.fixture
def loop_fsm_mutated():
    mock_fsm = MagicMock(spec=FSMGenerator)
    mock_machine = MagicMock()
    mock_machine.initial = "S0"
    mock_machine.state = "S0"

    # Mock triggers and transitions
    mock_fsm._get_triggers.return_value = ["a", "b", "c"]
    mock_fsm.events = ["a", "b", "c"]
    mock_fsm.machine = mock_machine
    mock_fsm.transitions = [
        {"source": "S0", "trigger": "a", "dest": "S1"},
        {"source": "S1", "trigger": "b", "dest": "S0"},
        {"source": "S1", "trigger": "a", "dest": "S2"},
        {"source": "S2", "trigger": "b", "dest": "S1"},
    ]

    return mock_fsm


@pytest.fixture
def sample_hsi_suite():
    return {"a": ("0",), "ab": ("0", "1"), "abc": ("0", "1", "0")}


@pytest.fixture
def random_walk(
    simple_fsm: MagicMock, mutated_fsm1: MagicMock, sample_hsi_suite: dict[str, Any]
):
    return RandomWalk(simple_fsm, mutated_fsm1, 70, sample_hsi_suite)


def test_random_walk(random_walk: RandomWalk):
    """Tests that the walk actually walks for a random walk"""
    walk = random_walk.walk(RandomWalk.WalkType.RANDOM)
    assert len(walk) > 0


def test_random_walk_no_coverage(
    simple_fsm: MagicMock, mutated_fsm1: MagicMock, sample_hsi_suite: dict[str, Any]
):
    """Tests that the random walk doesnt walk if target coverage is 0"""
    random_walk = RandomWalk(simple_fsm, mutated_fsm1, 0, sample_hsi_suite)
    walk = random_walk.walk(RandomWalk.WalkType.RANDOM)
    assert len(walk) == 0


def test_random_walk_loop(
    loop_fsm: MagicMock, sample_hsi_suite: dict[str, Any], loop_fsm_mutated: MagicMock
):
    """Test that it doesnt get stuck in a loop"""
    random_walk = RandomWalk(loop_fsm, loop_fsm_mutated, 60, sample_hsi_suite)
    walk = random_walk.walk(RandomWalk.WalkType.RANDOM)
    assert len(walk) > 0
    assert len(walk) < 100  # Should not be too long/ no infinite loop


def test_random_walk_max_length_exceeded(random_walk: RandomWalk):
    """Test that the random walk stops if the maximum walk length is exceeded."""
    # override the max length to test
    random_walk.max_walk_length = 1
    walk = random_walk.walk(RandomWalk.WalkType.RANDOM)
    # return -1 if max length exceeded
    assert walk == -1


def test_detected_fault(simple_fsm: MagicMock, mutated_fsm1: MagicMock):
    """Test that the detected_fault method identifies faults correctly."""
    random_walk = RandomWalk(simple_fsm, mutated_fsm1, 100, {})
    mutated_walk = ["a / 0", "b / 1", "c / 0"]
    simple_fsm.apply_input_sequence = MagicMock(return_value=(None, ("0", "1", "1")))
    fault_index = random_walk.detected_fault(mutated_walk)
    # detect the fault at correct index
    assert fault_index == 3


def test_detected_fault_no_fault(simple_fsm: MagicMock, mutated_fsm1: MagicMock):
    """Test that the detected_fault method returns -1 if no fault is found."""
    random_walk = RandomWalk(simple_fsm, mutated_fsm1, 100, {})
    mutated_walk = ["a / 0", "b / 1", "c / 0"]
    simple_fsm.apply_input_sequence = MagicMock(return_value=(None, ("0", "1", "0")))
    fault_index = random_walk.detected_fault(mutated_walk)
    assert fault_index == -1


def test_random_walk_reaches_target_coverage(
    simple_fsm: MagicMock, mutated_fsm1: MagicMock, sample_hsi_suite: dict[str, Any]
):
    """Test that the random walk reaches the target coverage."""
    target_coverage = 100
    random_walk = RandomWalk(
        simple_fsm, mutated_fsm1, target_coverage, sample_hsi_suite
    )
    walk = random_walk.walk(RandomWalk.WalkType.RANDOM)
    assert len(walk) > 0
    assert random_walk.target_coverage == 100


def test_random_reset_walk_doesnt_walk_with_no_coverage(
    simple_fsm: MagicMock, mutated_fsm1: MagicMock, sample_hsi_suite: dict[str, Any]
):
    """Tests that the walk doesnt walk if target coverage is 0"""
    random_walk = RandomWalk(simple_fsm, mutated_fsm1, 0, sample_hsi_suite)
    walk = random_walk.walk(RandomWalk.WalkType.RANDOM_WITH_RESET, 5)
    assert len(walk) == 0


def test_random_walk_with_empty_triggers(mutated_fsm1: MagicMock):
    """Test that the random walk raises an error if there are no triggers."""
    mock_fsm = MagicMock(spec=FSMGenerator)
    mock_fsm.machine = MagicMock()
    mock_fsm.initial = "S0"
    mock_fsm.state = "S0"
    mock_fsm.transitions = []
    mock_fsm._get_triggers = MagicMock(return_value=[])
    mock_fsm.states = ["S0", "S1", "S2"]
    mock_fsm.events = ["a", "b", "c"]
    walk = RandomWalk(mock_fsm, mock_fsm, target_coverage=100, HSI_suite={})
    with pytest.raises(IndexError):
        walk.walk(RandomWalk.WalkType.RANDOM)


def test_impossible_coverage(
    simple_fsm: MagicMock, mutated_fsm1: MagicMock, sample_hsi_suite: dict[str, Any]
):
    """Test a random walk with a target coverage that is impossible"""
    random_walk = RandomWalk(simple_fsm, mutated_fsm1, 200, sample_hsi_suite)
    walk = random_walk.walk(RandomWalk.WalkType.RANDOM)
    assert len(walk) > 0
    assert random_walk.target_coverage == 100


def test_statistical_walk(random_walk: RandomWalk):
    """Tests that the walk actually walks for a statistical walk"""
    walk = random_walk.walk(RandomWalk.WalkType.STATISTICAL)
    assert isinstance(walk, list)
    assert len(walk) > 0


def test_statistical_walk_no_coverage(
    simple_fsm: MagicMock, mutated_fsm1: MagicMock, sample_hsi_suite: dict[str, Any]
):
    """Tests that the statistical walk doesnt walk if target coverage is 0"""
    random_walk = RandomWalk(simple_fsm, mutated_fsm1, 0, sample_hsi_suite)
    walk = random_walk.walk(RandomWalk.WalkType.STATISTICAL)
    assert len(walk) == 0


def test_statistical_walk_max_length_exceeded(random_walk: RandomWalk):
    """Test that the statistical walk stops if the maximum walk length is exceeded."""
    random_walk.max_walk_length = 1  # low max length to test
    walk = random_walk.walk(RandomWalk.WalkType.STATISTICAL)
    # return -1 if max length exceeded
    assert walk == -1


def test_limited_self_loop_walk(random_walk: RandomWalk):
    """Tests that the walk actually walks for a limited self loop walk"""
    walk = random_walk.walk(RandomWalk.WalkType.LIMITED_SELF_LOOP)
    assert len(walk) > 0
    assert isinstance(walk, list)


def test_limited_self_loop_walk_no_coverage(random_walk: RandomWalk):
    """Tests that it doesn't walk if the target coverage is 0"""
    random_walk.target_coverage = 0
    walk = random_walk.walk(RandomWalk.WalkType.LIMITED_SELF_LOOP)
    assert len(walk) == 0


def test_limited_self_loop_walk_max_length_exceeded(random_walk: RandomWalk):
    """Test that the limited self loop walk stops if the maximum walk length is exceeded."""
    random_walk.max_walk_length = 1  # low max length to test
    walk = random_walk.walk(RandomWalk.WalkType.LIMITED_SELF_LOOP)
    # return -1 if max length exceeded
    assert walk == -1
