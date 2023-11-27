import os
from .tool import Tool


class WriteWholeTextFile(Tool):
    def gpt4_assistants_tool(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Replace the entire content of a file with new_text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "relative_path": {"type": "string", "description": "Relative path to the file to write"},
                        "new_text": {"type": "string", "description": "New text to replace the entire content of the file"}
                    },
                    "required": ["relative_path", "new_text"]
                }
            }
        }

    def gpt4_prompt_instructions(self):
        return '''
            ## Write Whole Text to a File (write_whole_text_file):

            Use this tool to replace the entire content of a file with new text. This is particularly useful when you want to start with a clean slate or update a file's content completely.

            ### Parameters:

            * relative_path: The path to the file whose content will be replaced.
            * new_text: The text to write into the file, replacing all existing content.
        '''

    def do_it(self, relative_path, new_text):
        # Check if the path exists and is a file
        if not os.path.exists(relative_path):
            os.makedirs(os.path.dirname(relative_path), exist_ok=True)

        # Write new_text to the file, replacing all existing content
        with open(relative_path, 'w', encoding='utf-8') as file:
            file.write(new_text)

        return True
