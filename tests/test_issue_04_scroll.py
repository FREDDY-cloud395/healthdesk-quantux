import unittest
import os

class TestIssue04Scroll(unittest.TestCase):
    def test_requester_portal_overflow_scroll(self):
        with open('frontend/index.html', 'r', encoding='utf-8') as f:
            html = f.read()

        self.assertIn('id="view-requester-portal" style="overflow-y: auto !important;"', html)
        self.assertIn('id="requester-clinical-portal"', html)
        self.assertIn('overflow-y: auto !important;', html)
        self.assertIn('id="requester-typeahead-dropdown"', html)
        self.assertIn('overscroll-behavior: contain', html)

    def test_css_scrollbar_styling(self):
        with open('frontend/css/styles.css', 'r', encoding='utf-8') as f:
            css = f.read()

        self.assertIn('#requester-typeahead-dropdown::-webkit-scrollbar', css)
        self.assertIn('#requester-typeahead-dropdown', css)
        self.assertIn('overscroll-behavior: contain', css)

    def test_typeahead_keyboard_navigation(self):
        with open('frontend/js/typeahead.js', 'r', encoding='utf-8') as f:
            js = f.read()

        self.assertIn('window.handleRequesterTypeaheadKeydown = handleRequesterTypeaheadKeydown;', js)
        self.assertIn('highlightRequesterTypeaheadItem', js)
        self.assertIn('scrollIntoView', js)

    def test_app_js_delegation(self):
        with open('frontend/js/app.js', 'r', encoding='utf-8') as f:
            js = f.read()

        self.assertIn('handleRequesterTypeaheadKeydown', js)
        self.assertIn('reqPortal.style.overflowY = \'auto\'', js)

if __name__ == '__main__':
    unittest.main()
