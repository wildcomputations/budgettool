"""Containers for metadata associated with a transaction
or entry in the ledger.
"""
from . import schedulers

class Transaction:
    """Minimum data associated with all transactions.
    """
    def __init__(self, name, category, amount):
        self.name = name
        self.category = category
        self.amount = amount


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
        return TemplateTransaction(
            name=name, category=category, amount=amount, schedule=schedule)

    def __init__(self, name, category, amount, schedule):
        self.transaction = Transaction(name, category, amount)
        self.schedule = schedule

    def __iter__(self):
        return iter((
            ('name',     self.transaction.name),
            ('category', self.transaction.category),
            ('amount',   self.transaction.amount),
        ))

    def __repr__(self):
        return repr(dict(self))

    def __str__(self):
        return ''.join(('    ', '\n    '.join(('{:8s} : {}'.format(*x) for x in self))))

