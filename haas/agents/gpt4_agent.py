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
        self.llm_config.setdefault("tools", []).extend([tool.gpt4_assistants_tool() for tool in tools]) # type: ignore
        self.instructions = instructions
        self.tools = self.llm_config["tools"]

        tool_functions = dict()
        tool_instructions = []
        for tool in tools:
            tool.set_agent(self)
            tool_functions[tool.name] = tool.do_it
            tool_instructions.append(tool.gpt4_prompt_instructions())
        
        instructions = "\n\n".join((instructions, *tool_instructions))

        super().__init__(
            name=name,
            instructions=instructions,
            llm_config=self.llm_config
        )

        self.register_function(tool_functions)

        self.agent_manager = AgentManager()

        logger.info(inspect.cleandoc(f"""
            GPT4Agent {self.name} initialized with tools: {", ".join([tool.name for tool in tools])}

            Instructions:
            """) + instructions)
