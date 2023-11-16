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

    def gpt4_assistants_tool(self):
        """
        Return metadata for the tool.
        """
        raise NotImplementedError(f"GPT 4 Assitants Tool metadata not implemented. ({__class__.__name__})")

    def do_it(self, *args, **kwargs):
        """
        Execute the tool's functionality.
        """
        raise NotImplementedError(f"Tool functionality not implemented. ({__class__.__name__})")

    def enforce_relative_path(self, relative_path):
        full_path = os.path.abspath(relative_path)
        if not full_path.startswith(os.getcwd()):
            raise ValueError(f"Access to the path outside the current directory is not allowed. ({relative_path})")
        return full_path