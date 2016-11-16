#!/usr/bin/env python3

import argparse
import budgettool as bt

class ArgToDate(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(ArgToDate, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        date = bt.str_to_date(values)
        setattr(namespace, self.dest, date)

def cmdline_args():
    """ parse the commandline arguments and return them.
    """
    parser = argparse.ArgumentParser(description="generate csv file of transactions from budget")
    parser.add_argument("in_budget", metavar="budget", help="file containing a budget")
    parser.add_argument("-o", dest="out_csv", metavar="out", help="filename for output csv")
    parser.add_argument("--start", help="start date for budget. (Requires --balance)",
                        action=ArgToDate)
    parser.add_argument("--end", help="end date for budget", action=ArgToDate)
    parser.add_argument("--balance", help="starting balance for budget",
                        type=float)

    args = parser.parse_args()

    if args.start and not args.balance:
        parser.exit("must specify a starting balance when specifying a start date")

    return args

if __name__ == "__main__":
    args = cmdline_args()

    budget = bt.budget_from_json(args.in_budget)
    forecast = budget.forecast(args.start, args.balance, args.end)
    if args.out_csv is None:
        bt.plot_forecast(forecast)
    else:
        bt.save_forecast_to_csv(forecast, args.out_csv)

