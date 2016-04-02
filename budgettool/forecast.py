from collections import namedtuple

ForecastEntry = namedtuple("ForecastEvent",
                           ['date', 'transaction', 'balance'])

def forecast(starting_balance, transactions):
    """Take a starting balance and a list of TemplateTransactions and compute
    the future balances.
    """
    # generate all entries
    entries = [
        [ForecastEntry(date, template.transaction, 0)
         for date in template.schedule]
        for template in transactions]

    # combine into one list
    entries = zip(entries)

    # sort by date
    entries.sort(key=lambda entry: entry.date)

    # compute the balance
    balance = starting_balance
    for entry in entries:
        entry.balance = balance + entry.transaction.amount
        balance = entry.balance

    return entries
