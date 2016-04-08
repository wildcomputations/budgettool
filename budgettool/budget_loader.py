"""File with top level helper to import a budget.
"""
from . import jsonparser
from . import budget

def budget_from_json(filename):
    """Create a Budget object from a file.

    Parameters
    =====
    filename - path to a json file with a budget
    """
    # note, if we start supporting multiple file encodings, we would add that here.
    storage_dict = jsonparser.load(filename)
    budget_obj = budget.Budget.from_dict(storage_dict, filename)
    return budget_obj
