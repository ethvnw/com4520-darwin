from fsm_gen.machine import Machine
from fsm_gen.generator import FSMGenerator

class CoffeeMachine(FSMGenerator):

    def __init__(self):
        self.states = ["a", "b", "c", "d", "e", "f"]
        self.events = ["clean", "button", "pod", "water"]
        self.outputs = ["ok", "coffee", "error"]
		self.transitions = [
            {"trigger": "", "source": "", "dest": ""},
            {"trigger": "", "source": "", "dest": ""},
            {"trigger": "", "source": "", "dest": ""},
            {"trigger": "", "source": "", "dest": ""},
            {"trigger": "", "source": "", "dest": ""},
            {"trigger": "", "source": "", "dest": ""},
            {"trigger": "", "source": "", "dest": ""},
            {"trigger": "", "source": "", "dest": ""},
            {"trigger": "", "source": "", "dest": ""},
            {"trigger": "", "source": "", "dest": ""},
            {"trigger": "", "source": "", "dest": ""},
        ]
