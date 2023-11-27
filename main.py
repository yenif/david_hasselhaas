import logging
from autogen import UserProxyAgent
from haas.agents.gpt4_agent import Gpt4Agent
from haas.tools.shell_execute import ShellExecute
from haas.filters.shell_command_filter import ShellCommandFilter

# Tools
from haas.tools.create_agent import CreateAgent
from haas.tools.list_agents import ListAgents
from haas.tools.list_directory import ListDirectory
from haas.tools.read_code_from_file import ReadCodeFromFile
from haas.tools.read_text_from_file import ReadTextFromFile
from haas.tools.receive_from_agent import ReceiveFromAgent
from haas.tools.run_python_test import RunPythonTest
from haas.tools.send_to_agent import SendToAgent
from haas.tools.web_retrieve import WebRetrieve
from haas.tools.write_text_to_file import WriteTextToFile
from haas.tools.write_whole_text_file import WriteWholeTextFile

# Filters
from haas.filters.restrict_path_to_dir import RestrictPathToDir
from haas.filters.shell_command_filter import ShellCommandFilter

# Directory to restrict the operation of filesystem tools
restricted_directory = './'

# Initialize tools with directory restrictions applied
list_dir_tool = RestrictPathToDir(restricted_directory, ListDirectory())
read_code_tool = RestrictPathToDir(restricted_directory, ReadCodeFromFile())
read_file_tool = RestrictPathToDir(restricted_directory, ReadTextFromFile())
run_python_test_tool = RestrictPathToDir(restricted_directory, RunPythonTest())
write_file_tool = RestrictPathToDir(restricted_directory, WriteTextToFile())
write_whole_file_tool = RestrictPathToDir(restricted_directory, WriteWholeTextFile())

# Create restricted tools for 'git' and 'gh' commands
restricted_git_tool = ShellCommandFilter(
    'git',
    {
        'description': 'Execute git commands within the HAAS system.',
        'usage': "For more information on usage, pass '--help' as an argument to git."
    },
    ShellExecute()
)
restricted_gh_tool = ShellCommandFilter(
    'gh',
    {
        'description': 'Execute gh GitHub CLI commands within the HAAS system. You should use this tool to interact with GitHub, Repositories, Pull Requests, Documentation, and many other functions.',
        'usage': "For more information on usage, pass '--help' as an argument to gh."
    },
    ShellExecute()
)

logging.basicConfig(level=logging.INFO)

# Initialize the Gpt4Agent with name, instructions, and tools
sab_agent = Gpt4Agent(
    name='Autonomous Swarm Agent Builder (SAB) Agent',
    instructions=open('haas/prompts/autonomous_swarm_agent_builder.md').read(),
    tools=[
        list_dir_tool,
        read_code_tool,
        read_file_tool,
        run_python_test_tool,
        write_file_tool,
        write_whole_file_tool,
        CreateAgent(),
        ListAgents(),
        ReceiveFromAgent(),
        SendToAgent(),
        WebRetrieve(),
        restricted_git_tool,  # Add restricted git capability
        restricted_gh_tool   # Add restricted gh capability
    ]
)

# Create a UserProxyAgent and initiate a chat with the SABAgent
user_proxy = UserProxyAgent(name='user_proxy')
user_proxy.initiate_chat(sab_agent, message='start up', silent=False)
