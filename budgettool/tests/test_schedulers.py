#!/usr/bin/env python3
"""Unit test for schedulers
"""

from collections import namedtuple
from datetime import date, timedelta
import unittest

from .. import schedulers

class _TestSchedulers(unittest.TestCase):
    def test_once(self):
        """Test Once schedule
        """
        earlier = date(2015, 10, 3)
        later = date(2016, 2, 15)

        sched = schedulers.Once(later, earlier)
        out = [x for x in sched]
        self.assertEqual(out, [later])

        sched = schedulers.Once(earlier, later)
        out = [x for x in sched]
        self.assertEqual(out, [])

        today = date.today()
        tomorrow = date.today() + timedelta(1)
        yesterday = date.today() - timedelta(1)

        sched = schedulers.Once(tomorrow)
        out = [x for x in sched]
        self.assertEqual(out, [tomorrow])

        sched = schedulers.Once(today)
        out = [x for x in sched]
        self.assertEqual(out, [today])

        sched = schedulers.Once(yesterday)
        out = [x for x in sched]
        self.assertEqual(out, [])

    def test_every_n_week(self):
        """Test events that repeat on multi-week interval
        """
        TestItem = namedtuple("TestItem",
                ['start', 'end', 'step', 'iter_start'])
        # Test cases must generate at least one event for the subsequent loop
        # to run
        test_items = [
                TestItem(date(2011, 5, 20), date(2012, 1, 1),
                    None, date(2011, 5, 20)),
                TestItem(date(2012, 3, 1), date(2040, 12, 31),
                    52, date(2012, 3, 1)),
                TestItem(date(2011, 5, 20), date(2012, 1, 1),
                    3, date(2011, 1, 1)),
                TestItem(date(2010, 3, 8), date(2012, 1, 1),
                    4, date(2011, 5, 20)),
                ]

        for test in test_items:
            if test.step == None:
                sched = schedulers.EveryNWeek(
                        test.start, test.end, iter_start=test.iter_start)
                days_per_step = 7
            else:
                sched = schedulers.EveryNWeek(
                        test.start, test.end, test.step, iter_start=test.iter_start)
                days_per_step = 7 * test.step

            out = [x for x in sched]
            self.assertGreaterEqual(out[0], test.start)
            self.assertGreaterEqual(out[0], test.iter_start)
            delta_to_start = out[0] - test.start
            self.assertEqual(delta_to_start.days % days_per_step, 0)

            prev = out[0]
            for event in out[1:]:
                self.assertEqual((event - prev).days, days_per_step)
                self.assertLess(event, test.end)
                prev = event

        # test special cases that the general loop above can't handle
        # end == start
        sched = schedulers.EveryNWeek(
                date(2015, 3, 2), date(2015, 3, 2), iter_start=date(2015, 1, 1))
        out = [x for x in sched]
        self.assertEqual(out, [])

        # end < start
        sched = schedulers.EveryNWeek(
                date(2015, 10, 30), date(2015, 8, 1), iter_start=date(2015, 1, 1))
        out = [x for x in sched]
        self.assertEqual(out, [])

        # iter_start < end
        sched = schedulers.EveryNWeek(
                date(2015, 3, 2), date(2015, 10, 30), iter_start=date(2016, 1, 1))
        out = [x for x in sched]
        self.assertEqual(out, [])

        # test default value for iter_start. Should be today
        sched = schedulers.EveryNWeek(
                date.today() - timedelta(7 * 100 + 1),
                date.today() + timedelta(365))
        event = next(iter(sched))
        self.assertEqual(event, date.today() + timedelta(6))

if __name__ == '__main__':
    unittest.main()
