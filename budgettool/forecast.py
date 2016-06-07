"""Predict future balances and transactions."""
class ForecastEntry:
    """Transaction at a specific date in a forecast."""
    def __init__(self, date, transaction, balance):
        self.date = date
        self.transaction = transaction
        self.balance = balance

    def __eq__(self, other):
        return (self.date == other.date
                and self.transaction == other.transaction
                and self.balance == other.balance)
    def __str__(self):
        return "ForecastEntry(date={}, transaction={}, balance={})".format(
            self.date, self.transaction, self.balance)


def forecast(starting_balance, transactions, start, end=None, duration=None):
    """Take a starting balance and a list of TemplateTransactions and compute
    the future balances.
    """
    # generate all entries
    entries = [
        ForecastEntry(date, template.transaction, 0)
        for template in transactions
        for date in template.schedule.view(start, end, duration)]

    # sort by date
    entries = sorted(entries, key=lambda entry: entry.date)

    # compute the balance
    balance = starting_balance
    for entry in entries:
        entry.balance = balance + entry.transaction.amount
        balance = entry.balance

    return entries
