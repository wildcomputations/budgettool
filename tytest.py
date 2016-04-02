#! /usr/bin/env python3

import datetime as dt

from importlib import reload
from budgettool import jsonparser
from budgettool import budget

import budgettool.schedulers
import budgettool.fileutils

reload(budgettool.schedulers)
reload(budgettool.fileutils)

filename = 'example.json'

reload(jsonparser)
d = jsonparser.load(filename)

reload(budget)
b = budget.Budget.from_dict(d, filename)

print(dict(b))
print(repr(b))
print(b._str_budget())
print(b)

b.modify(start_balance=5432.10, duration=dt.timedelta(weeks=26))

print(b)

jsonparser.save(dict(b), filename='save_'+filename)
