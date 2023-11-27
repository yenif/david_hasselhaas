import os
import io
import sys
import unittest
from haas.tools.tool import Tool

class RunPythonTest(Tool):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def gpt4_assistants_tool(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Runs a Python test file using the unittest framework.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "The path to the Python test file to be run."}
                    },
                    "required": ["path"]
                }
            }
        }

    def gpt4_prompt_instructions(self):
        return '''
            ## Run Python Test (run_python_test):

            This tool is designed to run Python test files using the unittest test framework. It executes a specified test file and returns the results.

            ### Parameters:

            * path: Provide the path to the Python test file that you want to execute.
        '''

    def do_it(self, path, *args, **kwargs):
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Test file does not exist: {path}")

        # Set up a buffer to capture test output
        buffer = io.StringIO()
        runner = unittest.TextTestRunner(stream=buffer, verbosity=2)

        # Find and run tests
        suite = unittest.defaultTestLoader.discover(start_dir=os.path.dirname(path), pattern=os.path.basename(path))
        result = runner.run(suite)

        # Capture the results from the buffer
        test_output = buffer.getvalue()
        buffer.close()

        # Return structured test results
        return {
            "success": result.wasSuccessful(),
            "run": result.testsRun,
            "failures": len(result.failures),
            "errors": len(result.errors),
            "output": test_output
        }