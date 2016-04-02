class Transaction:
    def __init__(self, name, category, amount):
        self.name = name
        self.category = category
        self.amount = amount


class TemplateTransaction:
    @staticmethod
    def from_dict(data):
        name     = data['name']
        category = data['category']
        amount   = data['amount']
        schedule = schedulers.get_schedule(data['schedule'])
        return TemplateTransaction(
            name=name, category=category, amount=amount, schedule=schedule)

    def __init__(self, name=None, category=None, amount=None, schedule=None):
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

