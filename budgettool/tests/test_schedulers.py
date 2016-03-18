#!/usr/bin/env python3
from ..schedulers import *

import datetime
import unittest

class _TestSchedulers(unittest.TestCase):
    def test_once(self):
        earlier = datetime.date(2015, 10, 3)
        later = datetime.date(2016, 2, 15)

        sched = Once(later, earlier)
        out = [x for x in sched]
        self.assertEqual(out, [later])

        sched = Once(earlier, later)
        out = [x for x in sched]
        self.assertEqual(out, [])

        today = datetime.date.today()
        tomorrow = datetime.date.today() + datetime.timedelta(1)
        yesterday = datetime.date.today() - datetime.timedelta(1)

        sched = Once(tomorrow)
        out = [x for x in sched]
        self.assertEqual(out, [tomorrow])

        sched = Once(today)
        out = [x for x in sched]
        self.assertEqual(out, [today])

        sched = Once(yesterday)
        out = [x for x in sched]
        self.assertEqual(out, [])

if __name__ == '__main__':
    unittest.main()
