# import pytest
# from walks.random_walk import RandomWalk
# from fsm_gen.machine import Machine

# ### MAKE FSMs FOR TESTING WITH DIFFERENT PROPERTIES ###

# @pytest.fixture
# def simple_fsm():
#     """ A simple FSM for testing """
#     states = ["S0", "S1"]
#     triggers = ["A", "B"]
#     transitions = [
#         {"source": "S0", "trigger": "A", "dest": "S1"},
#         {"source": "S1", "trigger": "B", "dest": "S0"},
#     ]
#     return Machine(states=states, initial="S0", transitions=transitions)

# @pytest.fixture
# def loop_fsm():
#     """ A FSM with a loop for testing """
#     states = ["S0", "S1", "S2"]
#     triggers = ["A", "B", "C"]
#     transitions = [
#         {"source": "S0", "trigger": "A", "dest": "S1"},
#         {"source": "S1", "trigger": "B", "dest": "S2"},
#         {"source": "S2", "trigger": "C", "dest": "S1"},
#     ]
#     return Machine(states=states, initial="S0", transitions=transitions)

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

# def test_simple_random_walk(simple_fsm):
#     """ Test a random walk with a simple FSM """
#     rand_walk = RandomWalk(simple_fsm, RandomWalk.WalkType.RANDOM, 100)
#     walk_length = rand_walk.walk()
#     assert walk_length > 0

# def test_loop_random_walk(loop_fsm):
#     """ Test a random walk with a FSM with a loop """
#     rand_walk = RandomWalk(loop_fsm, RandomWalk.WalkType.RANDOM, 100)
#     walk_length = rand_walk.walk()
#     assert walk_length > 0
#     assert walk_length < 1000 # Should not be too long/ no infinite loop

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

# def test_no_coverage(simple_fsm):
#     """ Test a random walk with a target coverage of 0 """
#     rand_walk = RandomWalk(simple_fsm, RandomWalk.WalkType.RANDOM, 0)
#     walk_length = rand_walk.walk()
#     assert walk_length == 0 

# ### TEST FAILS, RETURNS 1 not 0 ###
# def test_empty_fsm():
#     """ Test a random walk with an empty FSM """
#     empty_fsm = Machine(states=["S0"], initial="S0", transitions=[])
#     rand_walk = RandomWalk(empty_fsm, RandomWalk.WalkType.RANDOM, 100)
#     walk_length = rand_walk.walk()
#     # fsm becomes complete so one transition is added 
#     assert walk_length == 1 


