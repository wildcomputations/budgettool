# budgettool
model future money flow

Inspired by: [CBB's recur.pl](http://doc.gnu-darwin.org/cbb-man/cbb-man.html#SECTION00064000000000000000)

To use this, you need to write a json file describing your predicted
transactions. See example.json.

To run the budget:
```
./run_forecast.py <budget file>
```
By default this will open a matplotlib plot of the budget. See --help for other options.

# Testing
To check the code style and some static error analysis, run
```
pylint budgettool
```

To run the unit tests run
```
python3 -m unittest
```

[Kanban board](https://waffle.io/wildcomputations/budgettool)
