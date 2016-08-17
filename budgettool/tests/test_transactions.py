#!/usr/bin/env python3
"""Unit test for transactions
"""

import datetime
import unittest

from .. import transaction, schedulers

class TestTransactions(unittest.TestCase):
    """Test cases for TemplateTransaction
    """
    def test_monthly_exception(self):
        name = "test transaction"
        category = "TEST_CATEGORY"
        template = transaction.TemplateTransaction(
            name,
            category,
            100.00,
            schedulers.Monthly(31, start=datetime.date(2016, 6, 1)),
            exceptions={datetime.date(2016, 6, 30):200.0}
        )
        view = template.view(start = datetime.date(2016, 6, 1),
                             duration=datetime.timedelta(4 * 30))
        expected = [
            (datetime.date(2016, 6, 30), transaction.Transaction(name, category, 200.00)),
            (datetime.date(2016, 7, 31), transaction.Transaction(name, category, 100.00)),
            (datetime.date(2016, 8, 31), transaction.Transaction(name, category, 100.00))
        ]
        actual = list(view)
        print("Expected transactions", expected)
        print("Actual transactions  ", actual)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
