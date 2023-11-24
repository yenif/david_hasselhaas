import uuid
import importlib
from inflection import camelize

from haas.lib.agent_manager.agent_state_machine import AgentStateMachine

class AgentManager(object):
    def __init__(self, owning_agent: 'Agent'):
        self.owning_agent = owning_agent
        self.agent_registry = {}

    def list_agents(self):
        return [
            {"name": agent_name, "state": agent.state, "received_messages": agent.message_count()}
            for agent_name, agent in self.agent_registry.items()
        ]

    def new_agent(self, name, agent_definition, prompt_definition, tool_definitions):
        return agent_definition(
            name=name,
            instructions=prompt_definition,
            tools=tool_definitions
        )

    def create_agent(self, name, agent_definition, prompt_definition, tool_definitions):
        agent = self.new_agent(name, agent_definition, prompt_definition, tool_definitions)
        agent_state = AgentStateMachine(agent=agent, agent_manager=self)
        self.agent_registry[agent_state.name] = agent_state
        return agent_state.name

    def get_agent(self, agent_id):
        return self.agent_registry.get(agent_id, None)

    def send_to_agent(self, agent_id, message):
        agent = self.get_agent(agent_id)
        if not agent:
            raise ValueError(f'Agent with id {agent_id} not found.')
        agent.send(message)

    def receive_from_agent(self, agent_id):
        agent = self.get_agent(agent_id)
        if not agent:
            raise ValueError(f'Agent with id {agent_id} not found.')
        return agent.get_all_messages()
