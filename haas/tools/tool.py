"""
Base Tool class, all tools should inherit from this class.

Has methods returning appropriate metadata to instruct an llm how to use the tool:
- gpt4_assistants_tool
As llms are supported, more methods will be added to this class to support the new llm types.

Method `do_it` executes the tool's functionality. Arguments are determined by the tool and should match what is defined in the llm instruction metadata.
"""

import os
from inflection import underscore

class Tool:
    def __init__(self, *args, **kwargs):
        # Set the tool name to the subclass name by default underscored
        self.name = kwargs.get('name', underscore(self.__class__.__name__))
        self.agent = kwargs.get('agent', None)

    def set_name(self, name):
        """
        Set the name of the tool.
        """
        self.name = name

    def set_agent(self, agent):
        """
        Set the agent for the tool.
        """
        self.agent = agent

    def gpt4_assistants_tool(self):
        """
        Return metadata for the tool.
        """
        raise NotImplementedError(f"GPT 4 Assitants Tool metadata not implemented. ({__class__.__name__})")

    def gpt4_prompt_instructions(self):
        """
        Return the prompt for the tool.
        """
        raise NotImplementedError(f"GPT 4 Prompt not implemented. ({__class__.__name__})")

    def do_it(self, *args, **kwargs):
        """
        Execute the tool's functionality.
        """
        raise NotImplementedError(f"Tool functionality not implemented. ({__class__.__name__})")

    def set_agent(self, agent):
        """
        Set the agent for the tool.
        """
        self.agent = agent
