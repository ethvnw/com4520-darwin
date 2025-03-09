import pytest
from walks.random_walk import RandomWalk
from fsm_gen.machine import Machine

### MAKE FSMs FOR TESTING WITH DIFFERENT PROPERTIES ###

@pytest.fixture
def simple_fsm():
    """ A simple FSM for testing """
    states = ["S0", "S1"]
    triggers = ["A", "B"]
    transitions = [
        {"source": "S0", "trigger": "A", "dest": "S1"},
        {"source": "S1", "trigger": "B", "dest": "S0"},
    ]
    return Machine(states=states, initial="S0", transitions=transitions)

@pytest.fixture
def loop_fsm():
    """ A FSM with a loop for testing """
    states = ["S0", "S1", "S2"]
    triggers = ["A", "B", "C"]
    transitions = [
        {"source": "S0", "trigger": "A", "dest": "S1"},
        {"source": "S1", "trigger": "B", "dest": "S2"},
        {"source": "S2", "trigger": "C", "dest": "S1"},
    ]
    return Machine(states=states, initial="S0", transitions=transitions)

@pytest.fixture
def blocked_fsm():
    """ A FSM with a state with no outgoing transitions """
    states = ["S0", "S1", "S2"]
    triggers = ["A", "B", "C"]
    transitions = [
        {"source": "S0", "trigger": "A", "dest": "S1"},
        {"source": "S1", "trigger": "B", "dest": "S2"},
    ]
    return Machine(states=states, initial="S0", transitions=transitions)


### TESTS ###

