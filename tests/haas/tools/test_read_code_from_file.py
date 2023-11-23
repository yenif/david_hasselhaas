import unittest
import os
from haas.tools.read_code_from_file import ReadCodeFromFile

# A sample code for testing purposes
SAMPLE_CODE = """
def hello_world():
    print(\"Hello, world!\")

class Greeter:
    def greet(self, name):
        return \"Hello, \" + name
"""

class TestReadCodeFromFile(unittest.TestCase):
    tool = ReadCodeFromFile()

    def setUp(self):
        # Create a temporary directory if it doesn't exist
        if not os.path.isdir('./tests/tmp'):
            os.makedirs('./tests/tmp')
        # Write the sample code to a temporary file for testing
        with open('./tests/tmp/sample.py', 'w') as file:
            file.write(SAMPLE_CODE)

    def tearDown(self):
        # Clean up the temporary file and directory after tests
        if os.path.exists('./tests/tmp/sample.py'):
            os.remove('./tests/tmp/sample.py')
        if os.path.isdir('./tests/tmp'):
            os.rmdir('./tests/tmp')

    def test_read_function(self):
        # Test if the tool can read a simple function
        result = self.tool.do_it('./tests/tmp/sample.py', "(function_definition name: (identifier) @function (#eq @function \"hello_world\"))")
        self.assertIn('hello_world', result)

    def test_read_class(self):
        # Test if the tool can read a class definition
        result = self.tool.do_it('./tests/tmp/sample.py', "(class_definition name: (identifier) @class (#eq @class \"Greeter\"))")
        self.assertIn('Greeter', result)

    def test_read_method_within_class(self):
        # Test if the tool can read a method within a class
        result = self.tool.do_it('./tests/tmp/sample.py', '(class_definition body: (block (function_definition name: (identifier) @method (#eq @method \"greet\"))))')
        self.assertIn('greet', result)

    def test_invalid_file(self):
        # Test the response when the provided file path is invalid
        with self.assertRaises(ValueError):
            self.tool.do_it('./tests/tmp/nonexistent.py', "(function_definition)")

    def test_invalid_ast_path(self):
        # Test the response when the provided AST path is invalid
        with self.assertRaises(NameError):
            self.tool.do_it('./tests/tmp/sample.py', "(not_a_node)")

# Run the tests
if __name__ == '__main__':
    unittest.main()
