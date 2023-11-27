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
                        "new_text": {"type": "string", "description": "New text to insert into the file"},
                        "text_to_replace": {"type": "string", "description": "If present, the first instance of text_to_replace after start_offset will be replaced with new_text, remember that any text being replaced must be replicated in new_text if you want to keep it. If text_to_replace is '', then new_text will be inserted at start_offset. If text_to_replace is None, then file will be truncated to start_offset and new_text will be appended to the file."},
                        "start_offset": {"type": "string", "description": "Start character offset for the write, defaults to 0, negative start_offset indexes from the end of the file"},
                        "append": {"type": "boolean", "description": "If true and text_to_replace is an empty string, new_text will be inserted after the character at the position of start_offset."}
                    },
                    "required": ["relative_path", "new_text"]
                }
            }
        }

    def gpt4_prompt_instructions(self):
        return inspect.cleandoc('''
            ## Write Text to a File (write_text_to_file):

            This tool allows you to write new text to a specified file. You can either add text, insert it at a particular offset, or replace existing text based on provided parameters.

            This tool is more complex than simply overwriting the whole file. You should generally use write_whole_text_file instead. However this tool is useful for prepend, append, and replace operations, especially on larger files or logs. Make sure to work step by step to read the part of the file you are modifying before and after editing to ensure the edit is applied correctly!

            ### Parameters:

            * relative_path: Specify the file's relative path where the new text will be written, relative to the current directory (./).
            * new_text: The new content you intend to write into the file.
            * text_to_replace: (Optional) Use text_to_replace to control the editing mode of writing to a file. None or "" string inserts new_text at start_offset, where as a string provides explicit text to replace. Remember that any text being replaced must be replicated in new_text if you want to keep it.
            * start_offset: (Optional) Choose the positional character offset for the new text. Default is zero and negative values count from the end of the file. For example, a start_offset of -1 will insert new_text just before the last character of the file.
            * append: (Optional) If true and text_to_replace is an empty string, new_text will be inserted after the character at the position of start_offset (+=1).

            ### Example:

            The default is to prepend new_text to the file. For example:
            ```python
            write_text_to_file(
                relative_path="example.txt",
                new_text="Prepended text\n"
            )
            ```

            To append text to the end of the file, you can set start_offset to the file's length minus one and set append to true. For example:
            ```python
            write_text_to_file(
                relative_path="example.txt",
                new_text="Appended text\n",
                start_offset=-1,
                append=True
            )
            ```
        ''')

    def do_it(self, relative_path, new_text, text_to_replace=None, start_offset=0, append=False):
        # Create path if it doesn't exist
        if not os.path.exists(os.path.dirname(relative_path)):
            os.makedirs(os.path.dirname(relative_path), exist_ok=True)

        # Open file with read & write permissions
        with open(relative_path, 'r+', encoding='utf-8') as file:
            content = file.read()

            # Adjust the start_offset if it's negative
            if start_offset < 0:
                start_offset += len(content)

            # Determine where to insert new_text
            if append and text_to_replace in [None, ""]:
                start_offset += 1  # Move to the character after the current index

            # Replace the specified text if any
            if text_to_replace in [None, ""]:
                content = content[:start_offset] + new_text + content[start_offset:]
            else:
                content = content[:start_offset] + content[start_offset:].replace(text_to_replace, new_text, 1)  # Replace the first instance of text_to_replace

            file.seek(0)
            file.truncate()
            file.write(content)

        return True
