import datetime
from . import schedulers
from .fileutils import str_to_date, date_to_str, dict_to_duration, duration_to_dict, get_default

class Item:
    @staticmethod
    def from_dict(data):
        name     = data['name']
        category = data['category']
        amount   = data['amount']
        schedule = schedulers.get_schedule(data['schedule'])
        return Item(name=name, category=category, amount=amount, schedule=schedule)

    def __init__(self, name=None, category=None, amount=None, schedule=None):
        self.name = name
        self.category = category
        self.amount = amount
        self.schedule = schedule

    def __iter__(self):
        return iter((
            ('name',     self.name),
            ('category', self.category),
            ('amount',   self.amount),
        ))

    def __repr__(self):
        return repr(dict(self))

    def __str__(self):
        return ''.join(('    ', '\n    '.join(('{:8s} : {}'.format(*x) for x in self))))

class Budget:
    @staticmethod
    def from_dict(data, filename=None):
        assert data['filetype'] == 'budgettool'
        assert data['version'] == 1
        start_balance = data['start_balance']
        start_date = get_default('start_date', data, None, str_to_date)
        duration = dict_to_duration(data['duration'])
        budget = [ Item.from_dict(item) for item in data['budget'] ]
        return Budget(start_balance=start_balance,
                      start_date=start_date,
                      duration=duration,
                      budget=budget,
                      filename=filename)

    def __init__(self, start_balance=None, start_date=None,
                 duration=None, budget=[], filename=None):
        self.filename=filename
        self.start_balance=start_balance
        self.start_date=start_date
        self.duration=duration
        self.budget=budget

    def add_item(self, item):
        self.budget.append(item)

    def modify(self, **kwargs):
        keys = ('start_balance', 'start_date', 'duration', 'budget', 'filename')
        for k, v in kwargs.items():
            if k in keys:
                setattr(self, k, v)
            else:
                raise KeyError

    # XXX delete modfy0() after modify() has been tested
    def modify0(self, start_balance=None, start_date=None,
               duration=None, budget=None, filename=None):
        self.start_balance = self.start_balance if start_balance is None else start_balance
        self.start_date    = self.start_date    if start_date    is None else start_date
        self.duration      = self.duration      if duration      is None else duration
        self.budget        = self.budget        if budget        is None else budget
        self.filename      = self.filename      if filename      is None else filename

    def __iter__(self):
        return iter((
            ('filetype',     'budgettool'),
            ('version',      1),
            ('start_blance', self.start_balance),
            ('start_date',   date_to_str(self.start_date)),
            ('duration',     duration_to_dict(self.duration)),
            ('budget',       [dict(item) for item in self.budget]),
        ))

    def __repr__(self):
        return repr(dict(self))

    def _str_budget(self):
        return ''.join(('\n', '\n\n'.join(('{:s}'.format(str(item)) for item in self.budget))))

    def __str__(self):
        strdata = (
            ('filetype',     'budgettool'),
            ('version',      1),
            ('start_blance', self.start_balance),
            ('start_date',   date_to_str(self.start_date)),
            ('duration',     str(duration_to_dict(self.duration))),
            ('budget',       self._str_budget()),
        )
        return '\n'.join(('{:12s} : {}'.format(*x) for x in strdata))
