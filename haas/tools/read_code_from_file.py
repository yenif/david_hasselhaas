import os
import subprocess
import tree_sitter
from tree_sitter_languages import get_language, get_parser
import inspect
from .tool import Tool


class ReadCodeFromFile(Tool):
    LANGUAGES = {
        '.py': 'python',
        '.js': 'javascript',
        '.rb': 'ruby',
        # More languages and their corresponding file extensions can be added here
    }

    def gpt4_assistants_tool(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Read a specified component from a code file using an AST path.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "relative_path": {
                            "type": "string", "description": "Relative path to the code file"
                        },
                        "ast_path": {
                            "type": "string", "description": "AST path referencing the component to read"
                        }
                    },
                    "required": ["relative_path", "ast_path"]
                }
            }
        }

    def gpt4_prompt_instructions(self):
        return inspect.cleandoc("""
            # Read From Code File (read_from_code_file):
            This tool uses Tree-sitter to read and return the text of a specific code component based on an AST path. It requires information on where the file is located and what portion of the code to extract.

            ## How to use this tool:
            Specify the relative path to the source code file and the AST path referencing the component to read. The tool will determine the file type, use the appropriate Tree-sitter grammar, and return the text of the code at or matching the AST path.

            ## Parameters:
            - relative_path: The path to the code file from which you want to read, relative to the current working directory.
            - ast_path: A string that represents the AST path to query. This path should conform to the syntax of Tree-sitter queries and will be used to locate the code component to read.

            ## Example:
            If you want to read the function named 'main' from a Python file 'example.py', specify the relative path as 'example.py' and an AST path that finds the function definition named 'main'.

            ## AST Path Example for Python:
            (function_definition
            name: (identifier) @function
            (#eq? @function "main")
            )

            # Note:
            Ensure that the AST path is correctly formatted for the language of the code file and is specific enough to match only the intended part of the code.
        """)

    def do_it(self, relative_path, ast_path):
        full_path = self.enforce_relative_path(relative_path)

        # Ensure the file exists
        if not os.path.isfile(full_path):
            raise ValueError(f"The path {relative_path} is not a valid file.")

        # Determine the file type and select the correct language for tree-sitter
        file_extension = os.path.splitext(full_path)[1]
        if file_extension not in self.LANGUAGES:
            raise ValueError(f"Unsupported file type: {file_extension}")
        language_name = self.LANGUAGES[file_extension]

        # Load and set the language for tree-sitter
        language = get_language(language_name)
        parser = get_parser(language_name)

        # Read the file and parse it
        with open(full_path, 'rb') as file:
            code = file.read()
        tree = parser.parse(code)

        # Create a query using the provided AST path
        query = language.query(ast_path)
        captures = query.captures(tree.root_node)

        # Use the query captures to extract text from the code
        result = []
        for _, node in captures:
            start = node.start_byte
            end = node.end_byte
            result.append(code[start:end].decode('utf8'))

        return result
