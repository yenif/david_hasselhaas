from haas.tools.tool import Tool
from typing import Optional, Union, Dict

class ReceiveFromAgent(Tool):
    def gpt4_assistants_tool(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Receives any messages from a specified agent within the agent manager.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agent_name": {"type": "string", "description": "Name of the agent to receive the message from."}
                    },
                    "required": ["agent_name"]
                },
            }
        }

    def gpt4_prompt_instructions(self):
        return (
            "# Receive From Agent (receive_from_agent):\n" +
            "Receives a message from a specified agent. " +
            "You need to provide the agent_name from which you want to receive messages."
        )

    def do_it(self, agent_name):
        if not self.agent or not hasattr(self.agent, 'agent_manager'):
            raise ValueError('Agent manager not found')

        return self.agent.agent_manager.receive_from_agent(agent_name)
