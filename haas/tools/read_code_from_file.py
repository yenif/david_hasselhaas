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
            # Read Code File Tool (read_code_from_file):

            This tool uses Tree-sitter, a parser generator tool and an incremental parsing library, to read and return text from a code file based on an AST (Abstract Syntax Tree) path.

            An AST path is a query language used by Tree-sitter to identify and locate specific code constructs within the source file's parsed tree structure. 

            ## How to Construct an AST Path:

            1. Identify the language of the source code file you will be querying.
            2. Refer to the language's Tree-sitter grammar documentation for the syntax and node types defined within it.
            3. Construct the AST path using the syntax constructs provided by Tree-sitter, targeting the code section of interest.

            ## Examples of Valid AST Paths:

            ```plaintext
            # Python Function Definition AST Path:
            (function_definition
            name: (identifier) @function
            (#eq @function "function_name")
            ) @function

            # JavaScript Method Definition in a Class AST Path:
            (method_definition
            name: (property_identifier) @method
            (#eq @method "methodName")
            ) @function-body
            ```

            ### Example:

            To read the 'main' function from a file named `example.py`, provide these arguments to the tool:

            Relative Path: "example.py"
            AST Path: 
            ```plaintext
            (function_definition
            name: (identifier) @function
            (#eq @function "main")
            ) @function
            ```

            ### Note on Query Specificity:

            Ensure that the AST path is specific enough to match only the intended part of the code. Ambiguities in the query might lead to multiple matches or incorrect excerpts being returned.

            ### Additional Resources:

            For detailed Tree-sitter query syntax for supported languages, please refer to [Tree-sitter documentation](https://tree-sitter.github.io/tree-sitter/using-parsers#pattern-matching-with-queries).

            By following these instructions and utilizing appropriate examples and resources, users can construct effective AST path queries tailored to their specific needs when working with the `read_code_from_file` tool.
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
        for node, _type in captures:
            start = node.start_byte
            end = node.end_byte
            result.append(code[start:end].decode('utf8'))

        return result
