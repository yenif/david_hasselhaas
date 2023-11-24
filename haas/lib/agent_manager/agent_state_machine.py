import logging
from transitions import Machine
from typing import Union, Optional, Dict
from autogen import Agent

logger = logging.getLogger(__name__)

class AgentStateMachine(object):
    states = ['initializing', 'running', 'waiting', 'suspended', 'terminated']
    transitions = [
        {'trigger': 'start', 'source': 'initializing', 'dest': 'running', 'after': 'send_initialize_agent_message'},
        {'trigger': 'send', 'source': 'waiting', 'dest': 'running', 'after': 'send_message'},
        {'trigger': 'receive', 'source': 'running', 'dest': 'waiting', 'after': 'receive_message'},
        {'trigger': 'suspend', 'source': 'running', 'dest': 'suspended'},
        {'trigger': 'terminate', 'source': '*', 'dest': 'terminated'}
    ]

    def __init__(self, agent: Agent):
        self.name = agent.name
        self.agent = agent
        self.machine = Machine(model=self, states=AgentStateMachine.states, transitions=AgentStateMachine.transitions, initial='initializing')
        self.answering_machine = []
        self.start()

    def send_initialize_agent_message(self):
        """Send initialize message to the agent."""
        self.agent.receive('start up', self)

    def send_message(self, message: Union[Dict, str], request_reply: Optional[bool] = True, silent: Optional[bool] = False):
        """Send message to the agent."""
        self.agent.receive(message, self, request_reply, silent)

    def receive_message(self, message: Union[Dict, str], sender: 'Agent', request_reply: Optional[bool] = None, silent: Optional[bool] = False):
        """Handle message received from the agent."""
        self.answering_machine.append(message)
        self.receive_message()

    def message_count(self):
        """Check if the answering machine has messages."""
        return len(self.answering_machine)

    def get_next_message(self):
        """Get the next message from the answering machine."""
        return self.answering_machine.pop(0)

    def get_all_messages(self):
        """Get all messages from the answering machine."""
        messages = self.answering_machine
        self.answering_machine = []
        return messages
