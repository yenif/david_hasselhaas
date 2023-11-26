from haas.tools.tool import Tool


class Filter(Tool):
    def __init__(self, tool):
        self.tool = tool

    def __getattribute__(self, item):
        # Allow normal attribute access for 'tool' and '__dict__'
        if item in ['tool', '__dict__']:
            return object.__getattribute__(self, item)

        try:
            # Check if 'item' is a special method or exists in this class
            if item.startswith('__') and item.endswith('__') or item in self.__dict__:
                attr = object.__getattribute__(self, item)
            else:
                raise AttributeError
        except AttributeError:
            # Delegate to the 'tool' if 'item' is not found
            attr = getattr(self.tool, item)

        return attr

    def gpt4_assistants_tool(self):
        """
        Return metadata for the tool.
        """
        # The 'gpt4_assistants_tool' method can be overridden by subclasses to adjust the metadata if needed to support modifications to the tool's functionality
        return self.tool.gpt4_assistants_tool()

    def gpt4_prompt_instructions(self):
        """
        Return the prompt for the tool.
        """
        # The 'gpt4_prompt_instructions' method can be overridden by subclasses to adjust the prompt if needed to support modifications to the tool's functionality
        return self.tool.gpt4_prompt_instructions()

    def do_it(self, *args, **kwargs):
        """
        Execute the tool's functionality.
        """
        # The 'do_it' method can be overridden by subclasses to adjust the Tool's arguments or output as needed
        return self.tool.do_it(*args, **kwargs)
