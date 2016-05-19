#!/usr/bin/env python3
"""Unit test for forecasting
"""

import datetime as dt
import unittest

from ..transaction import TemplateTransaction
from .. import schedulers
from ..forecast import forecast, ForecastEntry


class TestForecast(unittest.TestCase):
    """Unit test for forecast method."""
    def test_one(self):
        """Test a forecast with one scheduled transaction."""
        a_day = dt.date(2015, 4, 1)
        templates = [
            TemplateTransaction("foo",
                                "category_x",
                                100,
                                schedulers.Weekly(a_day.weekday()))
        ]

        output = forecast(
            10, templates, a_day, duration=dt.timedelta(5 * 7))

        self.assertEqual(
            output,
            [ForecastEntry(a_day,
                           templates[0].transaction.amount,
                           templates[0].transaction,
                           110),
             ForecastEntry(a_day + dt.timedelta(7),
                           templates[0].transaction.amount,
                           templates[0].transaction,
                           210),
             ForecastEntry(a_day + dt.timedelta(2 * 7),
                           templates[0].transaction.amount,
                           templates[0].transaction,
                           310),
             ForecastEntry(a_day + dt.timedelta(3 * 7),
                           templates[0].transaction.amount,
                           templates[0].transaction,
                           410),
             ForecastEntry(a_day + dt.timedelta(4 * 7),
                           templates[0].transaction.amount,
                           templates[0].transaction,
                           510)
            ]
        )

    def test_three(self):
        """Test a forecast with three different types of scheduled transactions."""
        # two monthly schedules and one weekly
        a_date = dt.date(2000, 1, 1)
        monthly_1 = TemplateTransaction("monthy_1",
                                        "category",
                                        1,
                                        schedulers.Monthly(15))
        monthly_2 = TemplateTransaction("monthly_2",
                                        "category",
                                        10,
                                        schedulers.EveryNMonth(
                                            a_date, 2)
                                       )
        weekly_1 = TemplateTransaction("weekly",
                                       "category",
                                       100,
                                       schedulers.Weekly(
                                           3,
                                           start=dt.date(2000, 2, 1),
                                           end=dt.date(2000, 3, 12))
                                      )
        templates = [monthly_1, monthly_2, weekly_1]

        output = forecast(
            1000, templates, a_date, end=dt.date(2000, 5, 31))

        self.assertEqual(
            output,
            [ForecastEntry(dt.date(2000, 1, 1),
                           monthly_2.transaction.amount,
                           monthly_2.transaction,
                           1010),
             ForecastEntry(dt.date(2000, 1, 15),
                           monthly_1.transaction.amount,
                           monthly_1.transaction,
                           1011),
             ForecastEntry(dt.date(2000, 2, 3),
                           weekly_1.transaction.amount,
                           weekly_1.transaction,
                           1111),
             ForecastEntry(dt.date(2000, 2, 10),
                           weekly_1.transaction.amount,
                           weekly_1.transaction,
                           1211),
             ForecastEntry(dt.date(2000, 2, 15),
                           monthly_1.transaction.amount,
                           monthly_1.transaction,
                           1212),
             ForecastEntry(dt.date(2000, 2, 17),
                           weekly_1.transaction.amount,
                           weekly_1.transaction,
                           1312),
             ForecastEntry(dt.date(2000, 2, 24),
                           weekly_1.transaction.amount,
                           weekly_1.transaction,
                           1412),
             ForecastEntry(dt.date(2000, 3, 1),
                           monthly_2.transaction.amount,
                           monthly_2.transaction,
                           1422),
             ForecastEntry(dt.date(2000, 3, 2),
                           weekly_1.transaction.amount,
                           weekly_1.transaction,
                           1522),
             ForecastEntry(dt.date(2000, 3, 9),
                           weekly_1.transaction.amount,
                           weekly_1.transaction,
                           1622),
             ForecastEntry(dt.date(2000, 3, 15),
                           monthly_1.transaction.amount,
                           monthly_1.transaction,
                           1623),
             ForecastEntry(dt.date(2000, 4, 15),
                           monthly_1.transaction.amount,
                           monthly_1.transaction,
                           1624),
             ForecastEntry(dt.date(2000, 5, 1),
                           monthly_2.transaction.amount,
                           monthly_2.transaction,
                           1634),
             ForecastEntry(dt.date(2000, 5, 15),
                           monthly_1.transaction.amount,
                           monthly_1.transaction,
                           1635),
            ]
        )


if __name__ == '__main__':
    unittest.main()
