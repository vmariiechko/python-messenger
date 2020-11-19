import sys
import unittest

sys.path.append("../../messenger/client")

from style_sheet import load_stylesheet


class TestStyleSheet(unittest.TestCase):

    def test_load_stylesheet(self):
        stylesheet = load_stylesheet()
        self.assertIs(type(stylesheet), str)


if __name__ == '__main__':
    unittest.main()
