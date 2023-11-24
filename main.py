import logging
from autogen import UserProxyAgent

from haas.agents.gpt4_agent import Gpt4Agent
from haas.tools.list_directory import ListDirectory
from haas.tools.read_text_from_file import ReadTextFromFile
from haas.tools.write_text_to_file import WriteTextToFile
from haas.tools.read_code_from_file import ReadCodeFromFile
from haas.tools.create_agent import CreateAgent
from haas.tools.list_agents import ListAgents
from haas.tools.send_to_agent import SendToAgent
from haas.tools.receive_from_agent import ReceiveFromAgent

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # Initialize SABAgent
    sab_agent = Gpt4Agent(
        name = 'Autonomous Swarm Agent Builder (SAB) Agent',
        instructions = open('./haas/prompts/autonomous_swarm_agent_builder.md').read(),
        tools = [
            ListDirectory(),
            ReadTextFromFile(),
            WriteTextToFile(),
            ReadCodeFromFile(),
            CreateAgent(),
            ListAgents(),
            SendToAgent(),
            ReceiveFromAgent(),
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