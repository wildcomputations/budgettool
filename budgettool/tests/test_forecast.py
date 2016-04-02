#!/usr/bin/env python3
"""Unit test for forecasting
"""

import datetime
import unittest

from ..transaction import TemplateTransaction
from .. import schedulers
from ..forecast import forecast, ForecastEntry


class TestForecast(unittest.TestCase):
    def test_one(self):
        a_day = datetime.date(2015, 4, 1)
        templates = [
            TemplateTransaction("foo",
                                "category_x",
                                100,
                                schedulers.Weekly(a_day.weekday()))
        ]

        output = forecast(
            10, templates, a_day, duration=datetime.timedelta(5 * 7))

        self.assertEqual(
            output,
            [ForecastEntry(a_day,
                           templates[0].transaction,
                           110),
             ForecastEntry(a_day + datetime.timedelta(7),
                           templates[0].transaction,
                           210),
             ForecastEntry(a_day + datetime.timedelta(2 * 7),
                           templates[0].transaction,
                           310),
             ForecastEntry(a_day + datetime.timedelta(3 * 7),
                           templates[0].transaction,
                           410),
             ForecastEntry(a_day + datetime.timedelta(4 * 7),
                           templates[0].transaction,
                           510)
            ]
        )


if __name__ == '__main__':
    unittest.main()
