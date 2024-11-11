from transitions import Machine
from transitions.extensions import GraphMachine

class Basic_FSM(object):

    # states = ['S0', 'S1', 'S2', 'S3', 'S4']
    states = ['A', 'B', 'C']

    def __init__(self, name):

        self.name = name
        self.machine = GraphMachine(model=self, states=Basic_FSM.states, initial='A')

        # self.machine.add_transition(trigger='a / 0', source='S0', dest='S4')
        # self.machine.add_transition(trigger='b / 0', source='S0', dest='S3')
        # self.machine.add_transition(trigger='b / 0', source='S3', dest='S0')
        # self.machine.add_transition(trigger='a / 1', source='S3', dest='S4')
        # self.machine.add_transition(trigger='a / 1', source='S4', dest='S2')
        # self.machine.add_transition(trigger='b / 0', source='S4', dest='S2')
        # self.machine.add_transition(trigger='a / 1', source='S2', dest='S1')
        # self.machine.add_transition(trigger='b / 1', source='S2', dest='S4')
        # self.machine.add_transition(trigger='b / 1', source='S1', dest='S3')
        # self.machine.add_transition(trigger='a / 0', source='S1', dest='S3')

        self.machine.add_transition(trigger='h', source='A', dest='B')
        self.machine.add_transition(trigger='e', source='B', dest='C')
        self.machine.add_transition(trigger='e', source='C', dest='A')



if __name__ == "__main__":
    hero = Basic_FSM("testing")
    hero.get_graph().draw('state.svg', prog='dot')