import os
import subprocess
import inspect
from .tool import Tool

class ListDirectory(Tool):
    def gpt4_assistants_tool(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "List directory contents with optional start offset and max return. Includes item type, size, mime type, and name.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "relative_path": {"type": "string", "description": "Relative path to the directory to list"},
                        "start_offset": {"type": "string", "description": "Start character offset for the list"},
                        "max_return": {"type": "string", "description": "Maximum number of characters to return"},
                    },
                    "required": ["relative_path"]
                }
            }
        }

    def gpt4_prompt_instructions(self):
        return inspect.cleandoc("""
            # List Directory Contents (list_directory):
            Utilize this function to list the contents of a directory. You can specify the directory path, an optional character offset to start the listing, and define a maximum number of characters for the return.
            ## Parameters:
            * relative_path: Provide the directory's relative path you wish to inspect, relative to the current directory (./).
            * start_offset: (Optional) Define the character offset where the listing should start.
            * max_return: (Optional) Limit the characters in the returned listing.
        """)
    
    def do_it(self, relative_path, start_offset=0, max_return=-1):
        # Enforce that all paths are within the current directory
        full_path = self.enforce_relative_path(relative_path)

        # Check if the path is a directory
        if not os.path.isdir(relative_path):
            raise ValueError(f"The path {relative_path} is not a directory.")

        items = os.listdir(relative_path)
        items.sort()  # Sort alphabetically

        # Get details for each item
        items_detail = []
        for item in items:
            item_path = os.path.join(relative_path, item)
            item_type = "directory" if os.path.isdir(item_path) else "file"
            size = os.path.getsize(item_path) if item_type == "file" else None
            mime_type = subprocess.check_output(['file', '--mime-type', '-b', item_path]).strip() if item_type == "file" else None
            items_detail.append((item_type, size, mime_type, item))

        # Apply start offset and max return
        if start_offset != 0 or max_return != -1:
            items_detail = items_detail[start_offset:max_return]

        return items_detail
