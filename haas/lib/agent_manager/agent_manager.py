import uuid
from haas.lib.agent_manager.agent_state_machine import AgentStateMachine

class AgentManager(object):
    def __init__(self):
        self.agent_registry = {}

    def list_agents(self):
        return [{'id': agent_id, 'state': agent.state} for agent_id, agent in self.agent_registry.items()]

    def create_agent(self, agent_definition, prompt_definition, tool_definitions):
        new_agent_id = str(uuid.uuid4())
        new_agent = AgentStateMachine()
        self.agent_registry[new_agent_id] = new_agent
        return new_agent_id

    def get_agent(self, agent_id):
        return self.agent_registry.get(agent_id, None)

    def transition_state(self, agent_id, transition, *args, **kwargs):
        agent = self.get_agent(agent_id)
        if not agent:
            return f"Agent with ID {agent_id} not found."
        try:
            trigger = getattr(agent, transition)
            trigger(*args, **kwargs)
            return f"Transition {transition} triggered for agent {agent_id}."
        except AttributeError:
            return f"Invalid transition {transition} for agent {agent_id}."