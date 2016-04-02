import datetime
from . import schedulers
from . import forecast
from .transaction import TemplateTransaction
from .fileutils import str_to_date, date_to_str, dict_to_duration, duration_to_dict, get_default

class Budget:
    @staticmethod
    def from_dict(data, filename=None):
        assert data['filetype'] == 'budgettool'
        assert data['version'] == 1
        start_balance = data['start_balance']
        start_date = get_default('start_date', data, None, str_to_date)
        duration = dict_to_duration(data['duration'])
        budget = [ TemplateTransaction.from_dict(item) for item in data['budget'] ]
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

    def forecast(self):
        """Generate a list of transactions and predicted balance from this budget."""
        return forecast.forecast(
            self.start_balance,
            self.budget,
            self.start_date,
            duration=self.duration)

    def __iter__(self):
        return iter((
            ('filetype',     'budgettool'),
            ('version',      1),
            ('start_blance', self.start_balance),
            ('start_date',   date_to_str(self.start_date)),
            ('duration',     duration_to_dict(self.duration)),
            ('budget',       [dict(item) for item in self.budget]),
        ))
