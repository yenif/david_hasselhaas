import os
import subprocess
from .tool import Tool
import shlex
import logging

logger = logging.getLogger(__name__)

class WebRetrieve(Tool):
    def gpt4_assistants_tool(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Retrieve live internet web page content using `lynx --dump`.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL of the web page to retrieve. Example: https://www.google.com/search?q=I+can+search+the+web+with+lynx"
                        }
                    },
                    "required": ["url"]
                }
            }
        }

    def gpt4_prompt_instructions(self):
        return '''
            ## Web Page Retrieval Tool (web_retrieve):

            This tool is designed to retrieve the full text content of a oive internet web page. It operates using `lynx --dump`, providing a text-based representation of the web page specified by the given URL followed by the url links from the page.

            ### Parameters:

            * url: The full HTTP or HTTPS URL of the web page to retrieve content from.
        '''

    def do_it(self, url):
        # Sanitize the URL
        url = shlex.quote(url)

        # Execute the lynx command in an isolated environment
        lynx_dump_command = f'lynx --display_charset=utf8 --dump {url}'

        # Adding logging to capture lynx command output
        logger.info(f'Lynx command: {lynx_dump_command}')

        result = subprocess.run(
            lynx_dump_command, shell=True, text=True, capture_output=True,
            #env={'PATH': '/usr/sbin:/usr/bin'},
            #cwd='/tmp'
        )

        logger.debug(f'Command output: {result.stdout}')
        logger.debug(f'Command error: {result.stderr}')

        if result.stderr:
            raise RuntimeError("Web page retrieval error:\n" + result.stderr)

        return result.stdout
