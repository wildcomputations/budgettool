# Classes which generate transactions based on repeating schedules.
# dates are returned as instances of datetime.date

import datetime
import math

class Once:
    """ One time transaction. Generates a single event on the specified date.
    """
    def __init__(self, date, iter_start=datetime.date.today()):
        self.date = date
        self.iter_start = iter_start

    def __iter__(self):
        if self.iter_start <= self.date:
            return [self.date].__iter__()
        else:
            return [].__iter__()

class _FixedIncrItr:
    def __init__(self, next_date, increment):
        self.next_date = next_date
        self.increment = increment
    def __iter__(self):
        return self
    def next(self):
        out = self.next_date
        self.next_date += self.increment
        return out

class EveryNWeek:
    def __init__(self, start, step=1, iter_start = datetime.date.today()):
        """ Repeating schedule on weekly increments.

        Params
        -----
        start - datetime.date object for the first instance of this event
        step - the number of weeks between events
        iter_start - cutoff for earliest event to generate.
        """
        self.start = start
        self.step = step * datetime.timedelta(days=7)
        self.iter_start = iter_start

    def __iter__(self):
        if self.start < self.iter_start:
            delta = self._iter_start - self._start
            num_steps = math.ceil(delta / self.step)
            next_date = self.start + num_steps * self.step
        else:
            next_date = self.start

        return _FixedIncrIter(next_date, self.step)

class Weekly:
    def __init__(self, day_of_week, iter_start=datetime.date.today()):
        """ Repeat every week on the specified day of the week.

        Params
        _______
        day_of_week: integer representation of day of the week. Monday is 0,
                 Sunday is 6.
        iter_start: cuttoff for earliest event to generate.
        """
        offset = (day_of_week - iter_start.weekday()) % 7
        self.start = iter_start + offset
            

    def __iter__(self):
        return _FixedIncrIter(self.start, datetime.timedelta(days=7))

