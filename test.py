import unittest
from datetime import datetime
import main


class TestGetSheet(unittest.TestCase):
    def test(self):
        ss = main.get_spread_sheet(main.SPREAD_TITLE)
        now = datetime(2024, 1, 6)
        sheet = main.get_worksheet(ss, now)
        self.assertEqual('01/05', sheet.title)


if __name__ == '__main__':
    unittest.main()
