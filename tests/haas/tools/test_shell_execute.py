import unittest
from haas.tools.shell_execute import ShellExecute

class TestShellExecute(unittest.TestCase):

    def setUp(self):
        self.shell_execute = ShellExecute()

    def test_execute_echo(self):
        """Test executing an echo command."""
        command = 'echo Hello, World!'
        result = self.shell_execute.do_it(command)
        self.assertIn('out: Hello, World!', result['output'])
        self.assertEqual(result['returncode'], 0)

    def test_execute_stderr(self):
        """Test executing a command that generates stderr."""
        command = 'ls non_existent_file'
        result = self.shell_execute.do_it(command)
        self.assertIn('err:', result['output'])
        self.assertNotEqual(result['returncode'], 0)

    def test_combined_output_order(self):
        """Test that stdout and stderr are interleaved in the correct order."""
        command = '/bin/bash -c "echo out1; >&2 echo err1; echo out2; >&2 echo err2"'
        result = self.shell_execute.do_it(command)
        expected_output = '\n'.join(['out: out1', 'err: err1', 'out: out2', 'err: err2'])
        self.assertEqual(result['output'], expected_output)
        self.assertEqual(result['returncode'], 0)

if __name__ == '__main__':
    unittest.main()
