import uuid
import importlib
from inflection import classify

from haas.lib.agent_manager.agent_state_machine import AgentStateMachine

class AgentManager(object):
    def __init__(self):
        self.agent_registry = {}

    def list_agents(self):
        return [{"name": agent_name, "state": agent.state} for agent_name, agent in self.agent_registry.items()]

    def new_agent(self, agent_definition, prompt_definition, tool_definitions):
        if agent_definition['type'] == 'gpt4':
            return GPT4Agent(
                name=agent_definition['name'],
                instructions=prompt_definition,
                tools=[init_tool(tool_definition) for tool_definition in tool_definitions]
            )
        else:
            raise ValueError(f"Unknown agent type: {agent_definition['type']}")

    def init_tool(self, tool_name):
        import_path = f"haas.tools.{tool_name}"
        tool = importlib.import_module(import_path)
        tool_class = getattr(tool, classify(tool_name))
        return tool_class()


    def create_agent(self, agent_definition, prompt_definition, tool_definitions):
        agent = self.new_agent(agent_definition, prompt_definition, tool_definitions)
        agent_state = AgentStateMachine(agent=agent)
        self.agent_registry[agent_state.name()] = agent_state
        return agent_state.name()

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