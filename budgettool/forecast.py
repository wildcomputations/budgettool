"""Predict future balances and transactions."""
class ForecastEntry:
    """Transaction at a specific date in a forecast."""
    def __init__(self, date, amount, transaction, balance):
        self.date = date
        self.amount = amount
        self.transaction = transaction
        self.balance = balance

    def __eq__(self, other):
        return (self.date == other.date
                and self.amount == other.amount
                and self.transaction == other.transaction
                and self.balance == other.balance)
    def __str__(self):
        return "ForecastEntry(date={}, amount={}, transaction={}, balance={})".format(
            self.date, self.amount, self.transaction.name, self.balance)


def forecast(starting_balance, transactions, start, end=None, duration=None):
    """Take a starting balance and a list of TemplateTransactions and compute
    the future balances.
    """
    # generate all entries
    entries = [
        ForecastEntry(date, amount, template.transaction, 0)
        for template in transactions
        for date, amount in template.view(start, end, duration)]

    # sort by date
    entries = sorted(entries, key=lambda entry: entry.date)

    # compute the balance
    balance = starting_balance
    for entry in entries:
        entry.balance = balance + entry.amount
        balance = entry.balance

    return entries
