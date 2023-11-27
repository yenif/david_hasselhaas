import os
from .filter import Filter
import shlex

class ShellCommandFilter(Filter):
    def __init__(self, allowed_command, tool_description, tool, name=None):
        super().__init__(tool)
        self.allowed_command = allowed_command
        self.tool_description = tool_description
        self.tool.set_name(name or f'{self.tool.name}-{self.allowed_command}')

    def gpt4_assistants_tool(self):
        tool_info = self.tool.gpt4_assistants_tool()
        # Override tool's description and usage instruction
        tool_info['function']['description'] = self.tool_description.get('description', tool_info['function']['description'])
        tool_info['function']['parameters'] = {
            'type': 'object',
            'properties': {
                'args': {'type': 'string', 'description': 'Arguments for the allowed command'}
            },
            'required': ['args']
        }
        return tool_info

    def gpt4_prompt_instructions(self):
        # Basic instructions with a suggestion to use --help for more information
        return f"This tool allows you to use the '{self.allowed_command}' command within the HAAS system. For further information on how to use the available command, you can pass '--help' or the equivalent to the allowed command.\n\n" + \
               f"Basic usage: {self.allowed_command} [options] [arguments]\n" + \
               self.tool_description.get('usage', '')

    def do_it(self, args):
        # Construct the full command with the allowed command and provided arguments
        full_command = f'{self.allowed_command} {shlex.quote(args)}'
        # Call the shell_execute tool's do_it function with the constructed command
        return self.tool.do_it(full_command)
