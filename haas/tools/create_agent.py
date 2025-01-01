import inspect
import importlib
from inflection import camelize
from .tool import Tool
from haas.lib.agent_manager.agent_state_machine import AgentStateMachine


class CreateAgent(Tool):
    def gpt4_assistants_tool(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Create a new agent in the agent_manager with provided agent, prompt, and tool definitions.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Name of the new agent to create."},
                        "agent_definition": {"type": "string", "description": "Reference to an existing agent definition"},
                        "prompt_definition": {"type": "string", "description": "Reference to an existing prompt definition"},
                        "tool_definitions": {"type": "array", "description": "List of references to existing tool definitions", "items": {"type": "string"}},
                    },
                    "required": ["agent_definition", "prompt_definition", "tool_definitions"]
                }
            }
        }

    def gpt4_prompt_instructions(self):
        return inspect.cleandoc("""
            ## Create Agent (create_agent):

            This tool requires references to existing agent, prompt, and tool definitions to create a new agent within the agent_manager.
            Provide the necessary information for the agent_definition, prompt_definition, and tool_definitions.

            The tool ensures that only valid definitions are used when creating a new agent.

            ### Parameters:

            * name: Provide the name of the new agent to create.
            * agent_definition: Provide the reference to an existing agent definition. This is a module from `haas.agents.`.
            * prompt_definition: Provide the reference to an existing prompt definition. This is a filename from "./haas/prompts/".
            * tool_definitions: Provide the references to existing tool definitions. This is a list of tool names from the list of tools you have access to.

            ### Example:

            ```psuedocode
                create_agent(
                    name="bob_the_developer",
                    agent_definition="gpt4_agent",
                    prompt_definition="developer_agent_instructions.md",
                    tool_definitions=["list_directory", "read_text_from_file", "write_whole_text_file", "run_python_test"]
                )
            ```

            ```psuedocode
                create_agent(
                    name="bob_the_developer",
                    agent_definition="gpt4_agent",
                    prompt_definition="developer_agent_instructions.md",
                    tool_definitions=[
                        {"name": "list_directory", "filters": [{"name": "restrict_path_to_dir", "args": ["/home/bob/"]}]},
                        "list_directory",
                        "read_text_from_file",
                        "write_whole_text_file",
                        "run_python_test"
                    ]
                )
            ```
        """)

    def do_it(self, name, agent_definition, prompt_definition, tool_definitions):
        # Dynamically load the agent class using the full agent class name from the definition
        agent_module_name = f"haas.agents.{agent_definition}"
        agent_class_name = camelize(agent_definition)

        agent_module = importlib.import_module(agent_module_name)
        agent_class = getattr(agent_module, agent_class_name)

        # Fetch the prompt contents from the provided definition
        with open(f'./haas/prompts/{prompt_definition}', 'r') as prompt_file:
            prompt_contents = prompt_file.read()

        # Get the tools for the new agent
        tools = []
        for tool_name in tool_definitions:
            tools.append(self.agent.tools[tool_name])
            # TODO: figure out how add additional filters to a tool to restrict sub agent access

        # Create the new agent with the agent's agent_manager
        agent_manager = self.agent.agent_manager
        return agent_manager.create_agent(name, agent_class, prompt_contents, tools)