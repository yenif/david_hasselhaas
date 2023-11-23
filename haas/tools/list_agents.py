import inspect
from .tool import Tool

class ListAgents(Tool):
    def gpt4_assistants_tool(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "List agents in the calling agent's agent_manager and their current state.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }

    def gpt4_prompt_instructions(self):
        return inspect.cleandoc("""
            ## List Agents (list_agents):

            Utilize this function to list the agents in the calling agent's agent_manager along with their current state.
        """)
    
    def do_it(self):
        # Assuming the agent manager is accessible via self.agent.agent_manager
        if not self.agent or not hasattr(self.agent, 'agent_manager'):
            raise ValueError("Agent manager not found.")
        return self.agent.agent_manager.list_agents()
