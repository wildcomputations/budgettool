"""Containers for metadata associated with a transaction
or entry in the ledger.
"""
from . import schedulers
from . import fileutils

class Transaction:
    """Minimum data associated with all transactions.
    """
    def __init__(self, name, category, amount):
        self.name = name
        self.category = category
        self.amount = amount

class _TransactionIterator:
    def __init__(self, default_transaction, schedule_iterator, exceptions):
        self.default_transaction = default_transaction
        self.schedule_iterator = schedule_iterator
        self.exceptions = exceptions

    def __iter__(self):
        return self

    def __next__(self):
        next_date = next(self.schedule_iterator)
        if next_date in self.exceptions:
            except_transaction = Transaction(
                self.default_transaction.name,
                self.default_transaction.category,
                self.exceptions[next_date])
            return (next_date, except_transaction)
        return (next_date, self.default_transaction)

class _TransactionView:
    def __init__(self, transaction, schedule_view, exceptions):
        self.transaction = transaction
        self.schedule_view = schedule_view
        self.exceptions = exceptions

    def __iter__(self):
        return _TransactionIterator(self.transaction,
                                    iter(self.schedule_view),
                                    self.exceptions)

class TemplateTransaction:
    """Template from which transactions can be generated on a schedule.
    """
    @staticmethod
    def from_dict(data):
        """Generate a transaction template from the standard dictionary storage format.
        """
        name     = data['name']
        category = data['category']
        amount   = data['amount']
        schedule = schedulers.from_dict(data['schedule'])
        exceptions = {}
        if 'except' in data:
            for pair in data['except']:
                date = fileutils.str_to_date(pair['date'])
                amount = pair['amount']
                exceptions[date] = amount
        return TemplateTransaction(
            name=name, category=category, amount=amount,
            schedule=schedule, exceptions=exceptions)

    def __init__(self, name, category, amount, schedule, exceptions={}):
        self.transaction = Transaction(name, category, amount)
        self.schedule = schedule
        self.exceptions = exceptions

    def view(self, start, end=None, duration=None):
        return _TransactionView(self.transaction,
                                self.schedule.view(start, end, duration),
                                self.exceptions)

    def __iter__(self):
        encoded = [
            ('name',     self.transaction.name),
            ('category', self.transaction.category),
            ('amount',   self.transaction.amount),
            ('schedule', { 'type': self.schedule.schedule_type,
                         'data': dict(self.schedule) }),
        ]
        if self.exceptions != {}:
            encoded.append( ('except',
                             [
                                 {'date': fileutils.date_to_str(date),
                                  'amount': amount} 
                                 for date, amount in self.exceptions.items()
                             ]
                            ) )
        return iter(encoded)
