import unittest
from haas.filters.pager_filter import PagerFilter

# Mock tool class to use with the PagerFilter for testing purposes
class MockTool:
    def do_it(self, *args, **kwargs):
        return ' '.join(['Line ' + str(i) for i in range(1, 101)])  # Returns a string with 100 lines

# Test case for the PagerFilter
class TestPagerFilter(unittest.TestCase):
    def test_pagination(self):
        mock_tool = MockTool()
        pager_filter = PagerFilter(mock_tool, page_length=160) # Page length reduced for test purposes

        # Run the tool the first time (should retrieve the first page)
        first_page_result = pager_filter.do_it(continue_paginate=False)
        self.assertIn('Line 1', first_page_result['content'])
        self.assertNotIn('Line 41', first_page_result['content'])  # Assuming each line is approx 40 characters
        self.assertEqual(first_page_result['page_number'], 1)
        self.assertGreater(first_page_result['total_pages'], 1)  # There should be more than one page

        # Run the tool again, with continue_paginate=True (should retrieve the second page)
        second_page_result = pager_filter.do_it(continue_paginate=True)
        self.assertNotIn('Line 1', second_page_result['content'])
        self.assertIn('Line 41', second_page_result['content'])
        self.assertEqual(second_page_result['page_number'], 2)

if __name__ == '__main__':
    unittest.main()
