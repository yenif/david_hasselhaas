import unittest
from haas.tools.web_retrieve import WebRetrieve

class TestWebRetrieve(unittest.TestCase):
    def test_retrieval(self):
        # Create an instance of the WebRetrieve tool
        web_retrieve_tool = WebRetrieve()

        # Use a known URL for testing
        test_url = 'http://example.com'
        result = web_retrieve_tool.do_it(test_url)

        # Check if the result contains expected content from example.com
        self.assertIn('Example Domain', result, 'The retrieved content does not contain the expected text.')

if __name__ == '__main__':
    unittest.main()
