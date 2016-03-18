#!/usr/bin/env python3
"""Unit test for schedulers
"""

import datetime
import unittest

from .. import schedulers

class _TestSchedulers(unittest.TestCase):
    def test_once(self):
        """Test Once schedule
        """
        earlier = datetime.date(2015, 10, 3)
        later = datetime.date(2016, 2, 15)

        sched = schedulers.Once(later, earlier)
        out = [x for x in sched]
        self.assertEqual(out, [later])

        sched = schedulers.Once(earlier, later)
        out = [x for x in sched]
        self.assertEqual(out, [])

        today = datetime.date.today()
        tomorrow = datetime.date.today() + datetime.timedelta(1)
        yesterday = datetime.date.today() - datetime.timedelta(1)

        sched = schedulers.Once(tomorrow)
        out = [x for x in sched]
        self.assertEqual(out, [tomorrow])

        sched = schedulers.Once(today)
        out = [x for x in sched]
        self.assertEqual(out, [today])

        sched = schedulers.Once(yesterday)
        out = [x for x in sched]
        self.assertEqual(out, [])

if __name__ == '__main__':
    unittest.main()
