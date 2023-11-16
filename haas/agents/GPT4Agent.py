import logging
from autogen import UserProxyAgent
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent

from haas.tools.list_directory import ListDirectory
from haas.tools.read_text_from_file import ReadTextFromFile
from haas.tools.write_text_to_file import WriteTextToFile

logger = logging.getLogger(__name__)

class GPT4Agent(GPTAssistantAgent):
    """Autonomous Swarm Agent Builder (SAB) Agent"""

    DEFAULT_LLM_CONFIG = dict(
        model="gpt-4-1106-preview",
        tools=[
            {"type": "retrieval"},
            {"type": "code_interpreter"}
        ]
    )

    def __init__(self,
                 name,
                 instructions,
                 tools=[]):

        self.llm_config = self.DEFAULT_LLM_CONFIG.copy()
        self.llm_config.setdefault("tools", []).extend([tool.gpt4_assistants_tool() for tool in tools]) # type: ignore
        self.instructions = instructions
        self.tools = self.llm_config["tools"]

        super().__init__(
            name=name,
            instructions=instructions,
            llm_config=self.llm_config
        )

        self.register_function(dict([(tool.name, tool.do_it) for tool in tools]))

        logger.info(f"""
GPT4Agent {self.name} initialized with tools: {", ".join([tool.name for tool in tools])}

Instructions:
{self.instructions}
""")
