import subprocess
from .tool import Tool

class ShellExecute(Tool):
    def gpt4_assistants_tool(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Execute shell commands in a secure and unrestricted manner within the HAAS system environment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "Shell command to execute"}
                    },
                    "required": ["command"]
                }
            }
        }

    def gpt4_prompt_instructions(self):
        return "The ShellExecute tool executes a supplied shell command using the environment as it exists. This tool does not impose any restrictions on the commands that can be run."

    def do_it(self, command):
        # Execute the command in the system environment capturing output as it happens
        process = subprocess.Popen(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_lines = []
        while True:
            # Read one line from stdout/stderr respectively
            out_line = process.stdout.readline()
            err_line = process.stderr.readline()
            if out_line:
                output_lines.append(f'out: {out_line.strip()}')
            if err_line:
                output_lines.append(f'err: {err_line.strip()}')
            # Break from loop if process is done and no lines are received
            if not out_line and not err_line and process.poll() is not None:
                break
        # Include any remaining lines from stdout
        while True:
            out_line = process.stdout.readline()
            if out_line:
                output_lines.append(f'out: {out_line.strip()}')
            else:
                break
        # Include any remaining lines from stderr
        while True:
            err_line = process.stderr.readline()
            if err_line:
                output_lines.append(f'err: {err_line.strip()}')
            else:
                break
        # Get return code
        return_code = process.poll()
        return {
            'returncode': return_code,
            'output': '\n'.join(output_lines)
        }