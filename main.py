import logging
from autogen import UserProxyAgent
from haas.agents.gpt4_agent import Gpt4Agent

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

from haas.filters.restrict_path_to_dir import RestrictPathToDir

# Directory to restrict the operation of filesystem tools
restricted_directory = './'

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # Initialize tools with directory restrictions applied
    list_dir_tool = RestrictPathToDir(restricted_directory, ListDirectory())
    read_code_tool = RestrictPathToDir(restricted_directory, ReadCodeFromFile())
    read_file_tool = RestrictPathToDir(restricted_directory, ReadTextFromFile())
    run_python_test_tool = RestrictPathToDir(restricted_directory, RunPythonTest())
    write_file_tool = RestrictPathToDir(restricted_directory, WriteTextToFile())
    write_whole_file_tool = RestrictPathToDir(restricted_directory, WriteWholeTextFile())

    # Initialize SABAgent
    sab_agent = Gpt4Agent(
        name = 'Autonomous Swarm Agent Builder (SAB) Agent',
        instructions = open('./haas/prompts/autonomous_swarm_agent_builder.md').read(),
        tools = [
            list_dir_tool,
            read_code_tool,
            read_file_tool,
            run_python_test_tool,
            write_whole_file_tool,
            write_file_tool,
            CreateAgent(),
            ListAgents(),
            ReceiveFromAgent(),
            SendToAgent(),
            WebRetrieve(),
        ]
    )

    # Create a UserProxyAgent instance named 'user_proxy'
    user_proxy = UserProxyAgent(name='user_proxy')

    # Initiate chat between the user proxy and the SABAgent
    user_proxy.initiate_chat(
        sab_agent,
        message='start up',
        silent=False,
    )
