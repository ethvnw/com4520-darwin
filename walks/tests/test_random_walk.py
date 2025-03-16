import pytest
from unittest.mock import MagicMock
from fsm_gen.generator import FSMGenerator
from walks.random_walk import RandomWalk
from fsm_gen.machine import Machine

@pytest.fixture
def simple_fsm():
    mock_fsm = MagicMock(spec=FSMGenerator)
    mock_machine = MagicMock()
    mock_machine.initial = 'S0'
    mock_machine.state = 'S0'
    
    # Mock triggers and transitions
    mock_fsm._get_triggers.return_value = ['a', 'b']
    mock_fsm.machine = mock_machine
    mock_fsm.transitions = [
        {"source": "S0", "trigger": "a", "dest": "S1"},
        {"source": "S1", "trigger": "b", "dest": "S0"}
    ]
    
    return mock_fsm

@pytest.fixture
def loop_fsm():
    mock_fsm = MagicMock(spec=FSMGenerator)
    mock_machine = MagicMock()
    mock_machine.initial = 'S0'
    mock_machine.state = 'S0'

    # Mock triggers and transitions
    mock_fsm._get_triggers.return_value = ['a', 'b', 'c']
    mock_fsm.machine = mock_machine
    mock_fsm.transitions = [
        {"source": "S0", "trigger": "a", "dest": "S1"},
        {"source": "S1", "trigger": "b", "dest": "S2"},
        {"source": "S2", "trigger": "c", "dest": "S1"}
    ]

    return mock_fsm

@pytest.fixture
def sample_hsi_suite():
    return {
        'a': ('0',),
        'ab': ('0', '1'),
        'abc': ('0', '1', '0')
    }


def test_random_walk(simple_fsm, sample_hsi_suite):
    """ Tests that the walk actually walks """
    walk = RandomWalk(simple_fsm, target_coverage=100, HSI_suite=sample_hsi_suite)
    walk_length = walk.random_walk()
    assert walk_length > 0

def test_random_walk_no_coverage(simple_fsm, sample_hsi_suite):
    """ Tests that the walk doesnt walk if target coverage is 0 """
    walk = RandomWalk(simple_fsm, target_coverage=0, HSI_suite=sample_hsi_suite)
    walk_length = walk.random_walk()
    assert walk_length == 0

def test_random_walk_loop(loop_fsm, sample_hsi_suite):
    """ Test that it doesnt get stuck in a loop """
    walk = RandomWalk(loop_fsm, target_coverage=100, HSI_suite=sample_hsi_suite)
    walk_length = walk.random_walk()
    assert walk_length > 0
    assert walk_length < 1000 # Should not be too long/ no infinite loop


def test_random_walk_reset(simple_fsm, sample_hsi_suite):
    """ Test that the walk resets after a certain number of steps """
    walk = RandomWalk(simple_fsm, target_coverage=100, HSI_suite=sample_hsi_suite)
    simple_fsm.machine.state = 'S0'
    simple_fsm._get_triggers.side_effect = [['a'], ['b']]
    steps = walk.random_walk_with_reset(1)
    # ensure that the fsm does at least one step and then resets
    assert steps >= 1
    assert simple_fsm.machine.state == simple_fsm.machine.initial
    # make sure walk continues after until coverage reached
    assert steps >= (len(simple_fsm.transitions))


# @pytest.fixture
# def blocked_fsm():
#     """ A FSM with a state with no outgoing transitions """
#     states = ["S0", "S1", "S2"]
#     triggers = ["A", "B", "C"]
#     transitions = [
#         {"source": "S0", "trigger": "A", "dest": "S1"},
#         {"source": "S1", "trigger": "B", "dest": "S2"},
#     ]
#     return Machine(states=states, initial="S0", transitions=transitions)


# ### TESTS ###



# def test_blocked_random_walk(blocked_fsm):
#     """ Test a random walk with a FSM with a blocked state """
#     rand_walk = RandomWalk(blocked_fsm, RandomWalk.WalkType.RANDOM, 100)
#     walk_length = rand_walk.walk()
#     assert walk_length > 0
#     assert walk_length < 100 # Should not be too long/ no infinite loop

# ### THIS MAKES THE THING GO INTO AN INFINITE LOOP ###
# ### CHNAGE CODE SO CANT DO GOAL THAT IS IMPOSSIBLE ###
# # def test_impossible_coverage(simple_fsm):
# #     """ Test a random walk with a target coverage that is impossible """
# #     rand_walk = RandomWalk(simple_fsm, RandomWalk.WalkType.RANDOM, 200)
# #     walk_length = rand_walk.walk()
# #     assert walk_length > 0 # Should still try walk
# #     assert walk_length < 200 # Should not be too long/ no infinite loop


# ### TEST FAILS, RETURNS 1 not 0 ###
# def test_empty_fsm():
#     """ Test a random walk with an empty FSM """
#     empty_fsm = Machine(states=["S0"], initial="S0", transitions=[])
#     rand_walk = RandomWalk(empty_fsm, RandomWalk.WalkType.RANDOM, 100)
#     walk_length = rand_walk.walk()
#     # fsm becomes complete so one transition is added 
#     assert walk_length == 1 


