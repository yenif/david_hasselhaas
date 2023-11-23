from transitions import Machine

class AgentStateMachine(object):
    states = ['initializing', 'running', 'waiting', 'suspended', 'terminated']
    transitions = [
        {'trigger': 'start', 'source': ['initializing', 'suspended'], 'dest': 'running', 'after': 'send_initialize_agent_message'},
        {'trigger': 'send_message', 'source': ['waiting', 'suspended'], 'dest': 'running'},
        {'trigger': 'receive_message', 'source': 'running', 'dest': 'waiting'},
        {'trigger': 'suspend', 'source': ['initializing', 'running', 'waiting'], 'dest': 'suspended'},
        {'trigger': 'terminate', 'source': '*', 'dest': 'terminated'}
    ]

    def __init__(self, agent):
        self.name = agent.name
        self.agent = agent
        self.machine = Machine(model=self, states=AgentStateMachine.states, transitions=AgentStateMachine.transitions, initial='initializing')
        self.start()