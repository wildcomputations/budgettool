from . import jsonparser
from . import budget

def budget_from_json(filename):
    storage_dict = jsonparser.load(filename)
    budget_obj = budget.Budget.from_dict(storage_dict, filename)
    return budget_obj
