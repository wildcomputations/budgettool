#! /usr/bin/env python3

import datetime as dt
import json

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

b.modify(start_balance=5432.10, duration=dt.timedelta(weeks=26))

print(json.dumps(dict(b), sort_keys=True, indent=4))

jsonparser.save(dict(b), filename='save_'+filename)
