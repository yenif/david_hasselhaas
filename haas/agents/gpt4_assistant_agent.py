import logging
import inspect
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from haas.lib.agent_manager.agent_manager import AgentManager

logger = logging.getLogger(__name__)

class Gpt4Agent(GPTAssistantAgent):
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
                 tools=[]
                 ):

        self.llm_config = self.DEFAULT_LLM_CONFIG.copy()
        self.instructions = instructions

        self.tools = dict()
        self.tool_functions = tool_functions = dict()
        self.tool_instructions = tool_instructions = []
        self.llm_config.setdefault("tools", [])
        for tool in tools:
            tool.set_agent(self)
            self.tools[tool.name] = tool
            tool_functions[tool.name] = tool.do_it
            tool_instructions.append(inspect.cleandoc(tool.gpt4_prompt_instructions()))
            self.llm_config["tools"].append(tool.gpt4_assistants_tool()) # type: ignore

        instructions = "\n\n".join((instructions, *tool_instructions))

        super().__init__(
            name=name,
            instructions=instructions,
            llm_config=self.llm_config
        )

        self.register_function(tool_functions)

        self.agent_manager = AgentManager(self)

        logger.info(inspect.cleandoc(f"""
            GPT4Agent {self.name} initialized with tools: {", ".join([tool.name for tool in tools])}

            Instructions:
            """) + f"\n{instructions}")
