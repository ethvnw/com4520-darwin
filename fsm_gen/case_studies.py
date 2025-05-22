from fsm_gen.generator import FSMGenerator
from fsm_gen.machine import Machine


class CoffeeMachine(FSMGenerator):
    """
    Representation of a coffee machine.
    Derived from M. Merten, 'Active automata learning for real life applications'. doi: 10.17877/DE290R-5169.
    """

    def __init__(self):
        self.states = ["S0", "S1", "S2", "S3", "S4", "S5"]
        self.events = ["C", "B", "P", "W", "R"]
        self.outputs = ["t", "c", "f"]
        self.transitions = [
            {"trigger": "C / t", "source": "S0", "dest": "S0"},
            {"trigger": "B / f", "source": "S0", "dest": "S5"},
            {"trigger": "P / t", "source": "S0", "dest": "S1"},
            {"trigger": "W / t", "source": "S0", "dest": "S2"},
            {"trigger": "P / t", "source": "S1", "dest": "S1"},
            {"trigger": "C / t", "source": "S1", "dest": "S0"},
            {"trigger": "B / f", "source": "S1", "dest": "S5"},
            {"trigger": "W / t", "source": "S1", "dest": "S3"},
            {"trigger": "C / t", "source": "S3", "dest": "S0"},
            {"trigger": "B / c", "source": "S3", "dest": "S4"},
            {"trigger": "C / t", "source": "S4", "dest": "S0"},
            {"trigger": "C / t", "source": "S2", "dest": "S0"},
            {"trigger": "W / t", "source": "S3", "dest": "S3"},
            {"trigger": "P / t", "source": "S3", "dest": "S3"},
            {"trigger": "W / t", "source": "S2", "dest": "S2"},
            {"trigger": "P / t", "source": "S2", "dest": "S3"},
            {"trigger": "B / f", "source": "S4", "dest": "S5"},
            {"trigger": "P / f", "source": "S4", "dest": "S5"},
            {"trigger": "W / f", "source": "S4", "dest": "S5"},
            {"trigger": "B / f", "source": "S2", "dest": "S5"},
            {"trigger": "C / f", "source": "S5", "dest": "S5"},
            {"trigger": "B / f", "source": "S5", "dest": "S5"},
            {"trigger": "P / f", "source": "S5", "dest": "S5"},
            {"trigger": "W / f", "source": "S5", "dest": "S5"},
            {"trigger": "R / t", "source": "S5", "dest": "S0"},
        ]

        self.machine = Machine(
            states=self.states,
            initial=self.states[0],
            graph_engine="pygraphviz",
            auto_transitions=False,
            transitions=self.transitions,
        )

    def __str__(self):
        return "Coffee Machine"


class LocalisationSystem(FSMGenerator):
    """
    Simple localisation system.
    Derived from S. Plambeck, J. Schyga, J. Hinckeldeyn, J. Kreutzfeldt, and G. Fey,
    'Automata Learning for Automated Test Generation of Real Time Localization Systems', May, 2021,
    doi: 10.48550/arXiv.2105.11911.
    """

    def __init__(self):
        self.states = ["S0", "S1", "S2"]
        self.events = ["N", "E", "S", "W"]
        self.outputs = ["a", "b"]
        self.transitions = [
            {"trigger": "N / a", "source": "S0", "dest": "S0"},
            {"trigger": "W / a", "source": "S0", "dest": "S0"},
            {"trigger": "S / b", "source": "S0", "dest": "S1"},
            {"trigger": "S / a", "source": "S1", "dest": "S0"},
            {"trigger": "N / a", "source": "S1", "dest": "S0"},
            {"trigger": "E / b", "source": "S1", "dest": "S2"},
            {"trigger": "E / a", "source": "S2", "dest": "S1"},
            {"trigger": "N / a", "source": "S2", "dest": "S2"},
            {"trigger": "S / a", "source": "S2", "dest": "S0"},
            {"trigger": "E / a", "source": "S0", "dest": "S2"},
        ]

        self.machine = Machine(
            states=self.states,
            initial=self.states[0],
            graph_engine="pygraphviz",
            auto_transitions=False,
            transitions=self.transitions,
        )

    def __str__(self):
        return "Localisation System"


class Phone(FSMGenerator):
    """
    Authentication and key management on an Android phone.
    Derived from F. Vaandrager, M. Ebrahimi, and R. Bloem, 'Learning Mealy machines with one timer',
    Information and Computation, vol. 295, p. 105013, Dec. 2023, doi: 10.1016/j.ic.2023.105013.
    """

    def __init__(self):
        self.states = ["S0", "S1", "S2", "S3"]
        self.events = ["A", "D", "E", "P", "T", "O"]
        self.outputs = ["a, d, e, p, t, o"]
        self.transitions = [
            {"trigger": "D / v", "source": "S0", "dest": "S0"},
            {"trigger": "P / p", "source": "S0", "dest": "S0"},
            {"trigger": "O / d", "source": "S0", "dest": "S0"},
            {"trigger": "A / a", "source": "S1", "dest": "S1"},
            {"trigger": "A / a", "source": "S0", "dest": "S1"},
            {"trigger": "P / p", "source": "S1", "dest": "S0"},
            {"trigger": "D / v", "source": "S1", "dest": "S0"},
            {"trigger": "T / d", "source": "S1", "dest": "S0"},
            {"trigger": "E / v", "source": "S0", "dest": "S3"},
            {"trigger": "E / v", "source": "S1", "dest": "S3"},
            {"trigger": "A / a", "source": "S3", "dest": "S1"},
            {"trigger": "D / v", "source": "S3", "dest": "S3"},
            {"trigger": "E / v", "source": "S3", "dest": "S3"},
            {"trigger": "P / p", "source": "S3", "dest": "S3"},
            {"trigger": "O / d", "source": "S3", "dest": "S3"},
            {"trigger": "O / o", "source": "S1", "dest": "S2"},
            {"trigger": "A / a", "source": "S2", "dest": "S1"},
            {"trigger": "E / v", "source": "S2", "dest": "S3"},
            {"trigger": "O / o", "source": "S2", "dest": "S2"},
            {"trigger": "T / e", "source": "S2", "dest": "S0"},
            {"trigger": "P / p", "source": "S2", "dest": "S0"},
            {"trigger": "D / v", "source": "S2", "dest": "S0"},
        ]

        self.machine = Machine(
            states=self.states,
            initial=self.states[0],
            graph_engine="pygraphviz",
            auto_transitions=False,
            transitions=self.transitions,
        )

    def __str__(self):
        return "Phone"
