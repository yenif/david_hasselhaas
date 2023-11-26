import os
import inspect
from .tool import Tool

class WriteTextToFile(Tool):
    def gpt4_assistants_tool(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Write new_text to a file specified by relative_path. Optionally specify start_offset as the character offset index to insert new_text, defaults to 0, negative start_offset indexes from the end of the file. If text_to_replace is not blank, then the first instance of text_to_replace after start_offset will be replaced with new_text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "relative_path": {"type": "string", "description": "Relative path to the file to write"},
                        "new_text": {"type": "string", "description": "New text to insert in to the file"},
                        "text_to_replace": {"type": "string", "description": 'If present, the first instance of text_to_replace after start_offset will be replaced with new_text, remember that any text being replaced must be replicated in new_text if you want to keep it. If text_to_replace is "", then new_text will be inserted at start_offset. If text_to_replace is None, then file will be truncated to start_offset and new_text will be appended to the file.'},
                        "start_offset": {"type": "string", "description": "Start character offset for the write, defaults to 0, negative start_offset indexes from the end of the file"}
                    },
                    "required": ["relative_path", "new_text"]
                }
            }
        }

    def gpt4_prompt_instructions(self):
        return inspect.cleandoc("""
            ## Write Text to a File (write_text_to_file):

            This tool allows you to write new text to a specified file. You can either add text, insert it at a particular offset, or replace existing text based on provided parameters.

            ### Parameters:

            * relative_path: Specify the file's relative path where the new text will be written, relative to the current directory (./).
            * new_text: The new content you intend to write into the file.
            * text_to_replace: (Optional) Use text_to_replace to control the editting mode of writing to a file. Blank str inserts at start_offset, None truncates and appends at start_offset, and a str gives explicit text to replace. Remember that any text being replaced must be replicated in new_text if you want to keep it.
            * start_offset: (Optional) Choose the positional character offset for the new text. Default is zero and negative values count from the end of the file.

            Thus, by default, if you provide a relative_path and new_text, the file will be truncated to 0 and new text will be inserted as the new content of the file.
        """)

    def do_it(self, relative_path, new_text, text_to_replace=None, start_offset=0):
        # Create path if it doesn't exist
        if not os.path.exists(relative_path):
            os.makedirs(os.path.dirname(relative_path), exist_ok=True)
            open(relative_path, 'w').close()

        # Check if the path is a file
        if not os.path.isfile(relative_path):
            raise ValueError(f"The path {relative_path} is not a file.")

        with open(relative_path, 'r+t', encoding='utf-8') as file:
            content = file.read()
            if start_offset < 0:
                start_offset += len(content)  # Negative indexing from the end

            # Replace the specified text if any
            if text_to_replace == None:
                content = content[:start_offset] + new_text
            elif text_to_replace == "":
                content = content[:start_offset] + new_text + content[start_offset:]
            else:
                content = content[:start_offset] + content[start_offset:].replace(text_to_replace, new_text)

            file.seek(0)
            file.truncate()
            file.write(content)

        return True
