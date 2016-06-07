#!/usr/bin/env python3

import argparse
import budgettool as bt

def cmdline_args():
    """ parse the commandline arguments and return them.
    """
    parser = argparse.ArgumentParser(description="generate csv file of transactions from budget")
    parser.add_argument("in_budget", metavar="budget", help="file containing a budget")
    parser.add_argument("out_csv", metavar="out", help="filename for output csv")

    return parser.parse_args()

if __name__ == "__main__":
    args = cmdline_args()

    budget = bt.budget_from_json(args.in_budget)
    forecast = budget.forecast()
    bt.save_forecast_to_csv(forecast, args.out_csv)

