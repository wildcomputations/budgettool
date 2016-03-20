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

jsonparser.save(dict(b), filename='save_'+filename)
