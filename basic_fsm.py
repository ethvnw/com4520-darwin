from machine import Machine


class Basic_FSM(object):

    states = ['S0', 'S1', 'S2']

    def __init__(self, name):

        self.name = name
        self.machine = Machine(model=self, states=Basic_FSM.states, initial='S0')

        self.machine.add_transition(trigger='b / 0', source='S0', dest='S0')
        self.machine.add_transition(trigger='a / 0', source='S0', dest='S1')
        self.machine.add_transition(trigger='a / 1', source='S1', dest='S1')
        self.machine.add_transition(trigger='b / 1', source='S1', dest='S2')
        self.machine.add_transition(trigger='b / 1', source='S2', dest='S0')
        self.machine.add_transition(trigger='a / 0', source='S2', dest='S1')



if __name__ == "__main__":
    basic = Basic_FSM("testing")
    basic.get_graph().draw('state.svg', prog='dot')