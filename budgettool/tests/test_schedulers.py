#!/usr/bin/env python3
"""Unit test for schedulers
"""

from collections import namedtuple
from datetime import date, timedelta
import math
import unittest

from .. import schedulers

class TestSchedulers(unittest.TestCase):
    """Test cases for all the schedulers.
    """
    def test_once(self):
        """Test Once schedule
        """
        earlier = date(2015, 10, 3)
        later = date(2016, 2, 15)

        sched = schedulers.Once(later)
        out = list(sched.view(earlier, duration=timedelta(600)))
        self.assertEqual(out, [later])

        sched = schedulers.Once(earlier)
        out = list(sched.view(later, duration=timedelta(600)))
        self.assertEqual(out, [])

        sched = schedulers.Once(date(2016, 1, 6))
        out = list(sched.view(later, earlier))
        self.assertEqual(out, [])

        sched = schedulers.Once(earlier)
        out = list(sched.view(start=earlier, duration=timedelta(5)))
        self.assertEqual(out, [earlier])

        sched = schedulers.Once(earlier)
        out = list(sched.view(start=earlier, duration=timedelta(0)))
        self.assertEqual(out, [])

        sched = schedulers.Once(later)
        out = list(sched.view(earlier, end=later+timedelta(1)))
        self.assertEqual(out, [later])

    def test_every_n_week(self):
        """Test events that repeat on multi-week interval
        """
        TestItem = namedtuple("TestItem",
                              ['start',
                               'end',
                               'step',
                               'iter_start',
                               'iter_end'])
        # Test cases must generate at least one event for the subsequent loop
        # to run
        test_items = [
            TestItem(date(2011, 5, 20), date(2012, 1, 1),
                     None, date(2011, 5, 20), date(2012, 1, 1)),
            TestItem(date(2012, 3, 1), date(2040, 12, 31),
                     52, date(2012, 3, 1), date(2040, 12, 31)),
            TestItem(date(2011, 5, 20), date(2012, 1, 1),
                     3, date(2011, 1, 1), date(2012, 1, 1)),
            TestItem(date(2010, 3, 8), date(2012, 1, 1),
                     4, date(2011, 5, 20), date(2012, 1, 1)),
            TestItem(date(2011, 5, 20), None,
                     None, date(2011, 5, 20), date(2012, 1, 1)),
            TestItem(date(2012, 3, 1), None,
                     52, date(2012, 3, 1), date(2040, 12, 31)),
            TestItem(date(2011, 5, 20), None,
                     3, date(2011, 1, 1), date(2012, 1, 1)),
            TestItem(date(2010, 3, 8), None,
                     4, date(2011, 5, 20), date(2012, 1, 1)),
            TestItem(date(2010, 3, 3), date(2011, 12, 18),
                     5, date(2011, 5, 20), date(2012, 1, 1)),
            ]

        for test in test_items:
            if test.step is None:
                days_per_step = 7
                sched = schedulers.EveryNWeek(test.start, end=test.end)
            else:
                days_per_step = 7 * test.step
                sched = schedulers.EveryNWeek(test.start, test.step, test.end)

            out = list(sched.view(start=test.iter_start, end=test.iter_end))
            self.assertGreaterEqual(out[0], test.start)
            self.assertGreaterEqual(out[0], test.iter_start)
            delta_to_start = out[0] - test.start
            self.assertEqual(delta_to_start.days % days_per_step, 0)

            prev = out[0]
            for event in out[1:]:
                self.assertEqual((event - prev).days, days_per_step)
                if test.end is not None:
                    self.assertLess(event, test.end)
                if test.iter_end is not None:
                    self.assertLess(event, test.iter_end)
                prev = event

        # test durations
        starts = [date(2011, 1, 2),
                  date(2011, 3, 4),
                  date(2011, 5, 6),
                  date(2011, 7, 8)
                 ]
        for start in starts:
            sched = schedulers.EveryNWeek(start)

            out = list(sched.view(sched.start, duration=timedelta(7 * 5)))
            self.assertEqual(len(out), 5)

        # test special cases that the general loop above can't handle
        # end == start
        sched = schedulers.EveryNWeek(date(2015, 3, 2))
        out = list(sched.view(start=date(2015, 1, 1), end=date(2015, 3, 2)))
        self.assertEqual(out, [])

        # end < start
        sched = schedulers.EveryNWeek(date(2015, 10, 30))
        out = list(sched.view(end=date(2015, 8, 1), start=date(2015, 1, 1)))
        self.assertEqual(out, [])

        # iter_start < end
        sched = schedulers.EveryNWeek(date(2015, 3, 2))
        out = list(sched.view(end=date(2015, 10, 30), start=date(2016, 1, 1)))
        self.assertEqual(out, [])

    def test_every_n_month(self):
        TestCase = namedtuple("TestCase",
                              ['start',
                               'step',
                               'view_start',
                               'view_duration'])

        test_cases = []
        for year in range(2000, 2003):
            for start_day in range(1, 365, 17):
                for step in range(1, 4):
                    for view_start in range(-100, 100, 27):
                        for view_duration in range(step * 2, step * 10, 6):
                            start_date = date(
                                year,
                                math.ceil(start_day / 31),
                                start_day % 28)

                            test_cases.append(TestCase(
                                start_date,
                                step,
                                start_date + timedelta(view_start),
                                timedelta(view_duration * 31)))

        for test in test_cases:
            sched = schedulers.EveryNMonth(
                test.start, test.step)
            out = list(sched.view(test.view_start, duration=test.view_duration))

            for x in out:
                self.assertEqual(x.day, test.start.day)

                self.assertLessEqual(x, test.view_start + test.view_duration)
                self.assertGreaterEqual(x, test.view_start)
                self.assertGreaterEqual(x, test.start)

        # specific cases
        sched = schedulers.EveryNMonth(
            date(2000, 5, 12), 4)
        out = list(sched.view(date(2000, 6, 14), date(2000, 12, 1)))
        self.assertEqual(out, [date(2000, 9, 12)])

    def test_weekly(self):
        monday = date(2016, 3, 14)
        tuesday = date(2016, 3, 15)
        wednesday = date(2016, 3, 16)
        thursday = date(2016, 3, 17)
        friday = date(2016, 3, 18)
        saturday = date(2016, 3, 19)
        sunday = date(2016, 3, 20)

        start = date(2016, 3, 14)
        num = 5
        # inclusive of end date
        end = start + timedelta(num * 7 - 1)

        weekdays = {
            0:monday,
            1:tuesday,
            2:wednesday,
            3:thursday,
            4:friday,
            5:saturday,
            6:sunday
            }

        for day_id, first_date in weekdays.items():
            sched = schedulers.Weekly(day_id)
            out = list(sched.view(end=end, start=start))
            self.assertEqual(len(out), num)
            for index in range(num):
                self.assertEqual(out[index], first_date + index * timedelta(7))

        TestRanges = namedtuple("TestRanges",
                                ["sched_start",
                                 "sched_end",
                                 "view_start",
                                 "view_end"])
        test_cases = (
            # view inside schedule
            TestRanges(date(2015, 1, 15), date(2015, 6, 15),
                       date(2015, 2, 15), date(2015, 5, 15)),
            # view greater than schedule
            TestRanges(date(2016, 3, 1), date(2016, 5, 1),
                       date(2016, 1, 1), date(2016, 6, 1)),
            # view before & overlapping
            TestRanges(date(2015, 8, 20), date(2017, 4, 23),
                       date(2014, 9, 30), date(2015, 12, 28)),
            # view after and overlapping
            TestRanges(date(2015, 8, 20), date(2017, 4, 23),
                       date(2016, 9, 30), date(2017, 12, 28)),
            # no intersection
            TestRanges(date(2015, 1, 15), date(2015, 6, 15),
                       date(2016, 9, 30), date(2017, 4, 23))
            )
        for test in test_cases:
            sched = schedulers.Weekly(2, test.sched_start, test.sched_end)
            view_with_end = sched.view(test.view_start, test.view_end)
            for event in view_with_end:
                self.assertEqual(event.weekday(), 2)
                self.assertGreaterEqual(event, test.sched_start)
                self.assertGreaterEqual(event, test.view_start)
                self.assertLess(event, test.sched_end)
                self.assertLess(event, test.view_end)

            view_with_duration = sched.view(test.view_start,
                                            duration=test.view_end - test.view_start)
            self.assertEqual(list(view_with_end), list(view_with_duration))

    def test_monthly(self):
        TestItem = namedtuple("TestItem", ['year', 'month', 'day', 'start_day'])

        test_cases = []
        for year in range(2010, 2017):
            for month in range(1, 12):
                for day_of_month in range(1, 28, 2):
                    for start_day in range(1, 28, 3):
                        test_cases.append(
                            TestItem(year, month, day_of_month, start_day))
        for test in test_cases:
            sched = schedulers.Monthly(test.day)
            out = list(sched.view(
                start=date(test.year, test.month, test.start_day),
                end=date(test.year + 1, test.month, 28)))

            if test.start_day <= test.day:
                # 13 because end is included
                self.assertEqual(len(out), 13)
            else:
                self.assertEqual(len(out), 12)
            for x in out:
                self.assertEqual(x.day, test.day)

            start = out[0]
            for x, item in enumerate(out):
                self.assertGreater((item - start).days, x * 30.4 - 3)
                self.assertLess((item - start).days, x * 30.4 + 3)


if __name__ == '__main__':
    unittest.main()
