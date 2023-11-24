from haas.tools.tool import Tool
from typing import Optional, Union, Dict

class SendToAgent(Tool):
    def gpt4_assistants_tool(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Sends a message to a specified agent within the agent manager.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agent_name": {"type": "string", "description": "Name of the agent to send the message to."},
                        "message": {"type": "string", "description": "The message to send."},
                    },
                    "required": ["agent_name", "message"]
                },
            }
        }

    def gpt4_prompt_instructions(self):
        return (
            "## Send To Agent (send_to_agent):\n" +
            "Send a message to a specified agent. You need to provide the agent_name and the message you want to send.\n" +
            "Optionally, you can specify request_reply to expect a reply, and silent to send without notifying the sender agent.\n"
        )

    def do_it(self, agent_name: str, message: str, request_reply: Optional[bool] = True, silent: Optional[bool] = False):
        if not self.agent or not hasattr(self.agent, 'agent_manager'):
            raise ValueError('Agent manager not found')

        return self.agent.agent_manager.send_to_agent(agent_name, message, request_reply, silent)
