import pytest

from fsm_gen.generator import FSMGenerator
from walks.hsi import HSI

@pytest.fixture
def fsm():
    """ A FSM for testing """
    return FSMGenerator(num_states=6, num_inputs=4)

@pytest.fixture
def hsi(fsm):
    """ A HSI for testing """
    return HSI(fsm)

def test_find_shortest_path(hsi):
    """ Ensure a valid list is returned """
    fsm = hsi.fsm
    state = fsm.states[-1] # the last state
    path = hsi._find_shortest_path(state) # the shortest path to the last state
    assert isinstance(path, list) # the path should be a list
    assert len(path) > 0 # the path should not be empty
    assert all(isinstance(event, str) for event in path) # all elements should be strings


def test_generate_state_cover(hsi):
    """ Ensure a valid dict is returned """


def test_generate_transition_cover(hsi):
    """ Ensure a valid non-empty set is returned """


def test_compute_w_set(hsi):
    """ Checks if the W set differentiates states  """


def test_compute_w_set_empty(hsi):
    """ Checks if the W set is empty for a FSM with no transitions """


def test_compute_w_set_no_states(hsi):
    """ Checks if the W set is empty for a FSM with no states """


def test_compute_hsi_sets(hsi):
    """ Checks if the HSI sets are computed correctly """
