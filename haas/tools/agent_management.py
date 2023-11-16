from haas.tools.tool import Tool

from haas.lib.agent_manager import AgentManager

class AgentManagementTool(Tool):
    def __init__(self, **kwargs):
        super(AgentManagementTool, self).__init__(**kwargs)
        self.manager = AgentManager()

    def gpt4_assistants_tool(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Tool to manage the lifecycle and states of agents",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "Action to perform: 'list_agents', 'create_agent', or 'transition_state'."
                        },
                        "agent_id": {
                            "type": "string",
                            "description": "The ID of the agent to manage (required for 'transition_state')."
                        },
                        "transition": {
                            "type": "string",
                            "description": "The transition to trigger (required for 'transition_state')."
                        },
                        "agent_definition": {
                            "type": "string",
                            "description": "The definition of the agent (required for 'create_agent')."
                        },
                        "prompt_definition": {
                            "type": "string",
                            "description": "The prompt to be used by the agent (required for 'create_agent')."
                        },
                        "tool_definitions": {
                            "type": "array",
                            "description": "List of tools to be used by the agent (required for 'create_agent')."
                        }
                    },
                    "required": ["command"]
                }
            }
        }

    def do_it(self, command, agent_id=None, transition=None, agent_definition=None, prompt_definition=None, tool_definitions=None):
        if command == 'list_agents':
            return self.manager.list_agents()
        elif command == 'create_agent':
            return self.manager.create_agent(agent_definition, prompt_definition, tool_definitions)
        elif command == 'transition_state':
            return self.manager.transition_state(agent_id, transition)
        else:
            raise ValueError(f"Unknown command: {command}")