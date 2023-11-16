from transitions import Machine

class AgentStateMachine(object):
    states = ['initializing', 'active', 'suspended', 'terminated']
    transitions = [
        {'trigger': 'activate', 'source': 'initializing', 'dest': 'active'},
        {'trigger': 'suspend', 'source': 'active', 'dest': 'suspended'},
        {'trigger': 'terminate', 'source': '*', 'dest': 'terminated'}
    ]

    def __init__(self):
        self.machine = Machine(model=self, states=AgentStateMachine.states, transitions=AgentStateMachine.transitions, initial='initializing')
