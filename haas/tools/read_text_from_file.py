import os
import inspect
from .tool import Tool

class ReadTextFromFile(Tool):
    def gpt4_assistants_tool(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Read text from a file with optional start offset and max return",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "relative_path": {"type": "string", "description": "Relative path to the file to read"},
                        "start_offset": {"type": "string", "description": "Start character offset for the read"},
                        "max_return": {"type": "string", "description": "Maximum number of characters to return"},
                    },
                    "required": ["path"]
                }
            }
        }

    def gpt4_prompt_instructions(self):
        return inspect.cleandoc("""
            # Read Text from a File (read_text_from_file):

            You have the capability to read text from files using this function. This includes selecting the file through its relative path and optionally setting a start offset and a maximum number of characters to return.

            ## Parameters:

            * relative_path: Indicate the file's relative path from which you wish to read, relative to the current directory (./).
            * start_offset: (Optional) Start reading from a specific character offset.
            * max_return: (Optional) Designate the maximum number of characters to be read from the file.
        """)

    def do_it(self, relative_path, start_offset=0, max_return=-1):
        # Enforce that all paths are within the current directory
        full_path = self.enforce_relative_path(relative_path)

        # Check if the path is a file
        if not os.path.isfile(relative_path):
            raise ValueError(f"The path {relative_path} is not a file.")

        with open(relative_path, 'rt', encoding='utf-8') as file:
            text = file.read()

        # Apply start offset and max return
        if max_return != -1:
            text = text[start_offset:start_offset + max_return]
        else:
            text = text[start_offset:]

        return text
