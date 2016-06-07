"""View for a generated forecast that prints out the transactions and balances as csv"""


def save_forecast_to_csv(transactions, filename):
    """Save forecasted account balances to a csv file.

    The file format is
    date, transaction name, transaction amount, balance.

    Parameters
    ========
    transactions - list of ForecastEntry transactions.
    filename - path to filename to write the values out.
    """
    with open(filename, 'w') as out:
        print('date YYYY-MM-dd,name,amount,balance', file=out)

        for entry in transactions:
            print(
                "{},{},${:.2f},${:.2f}".format(
                    entry.date.isoformat(),
                    entry.transaction.name,
                    entry.transaction.amount,
                    entry.balance),
                file=out)
