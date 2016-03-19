""" Classes which generate transactions based on repeating schedules.
Dates are returned as instances of datetime.date
"""

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

class _FixedIncrIter:
    """Fixed increment in days
    """
    def __init__(self, next_date, end_date, increment):
        """Increment up to, but excluding end_date
        """
        self.next_date = next_date
        self.end_date = end_date
        self.increment = increment
    def __iter__(self):
        return self
    def __next__(self):
        if self.next_date >= self.end_date:
            raise StopIteration
        out = self.next_date
        self.next_date += self.increment
        return out

class EveryNWeek:
    """ Repeating schedule on weekly increments.
    For example, repeat every 2 weeks starting on Jan 1.
    """
    def __init__(self, start, end, step=1, iter_start=datetime.date.today()):
        """Create the schedule. By default it will repeat every week and won't
        generate old dates before today.

        Params
        -----
        start - datetime.date object for the first instance of this event
        end - cuttoff for last event to generate
        step - the number of weeks between events
        iter_start - cutoff for earliest event to generate.
        """
        self.start = start
        self.step = step * datetime.timedelta(days=7)
        self.end = end
        self.iter_start = iter_start

    def __iter__(self):
        if self.start < self.iter_start:
            delta = self.iter_start - self.start
            num_steps = math.ceil(delta / self.step)
            next_date = self.start + num_steps * self.step
        else:
            next_date = self.start

        return _FixedIncrIter(next_date, self.end, self.step)

class Weekly:
    """ Repeat every week on a specifc day of the week.
    For example, repeat every Tuesday.
    """
    def __init__(self, day_of_week, end, iter_start=datetime.date.today()):
        """ Repeat every week on the specified day of the week.
        Defaults to only generating events in the future.

        Params
        _______
        day_of_week: integer representation of day of the week. Monday is 0,
                 Sunday is 6.
        end - cuttoff for last event to generate
        iter_start: cuttoff for earliest event to generate.
        """
        offset = (day_of_week - iter_start.weekday()) % 7
        self.start = iter_start + datetime.timedelta(offset)
        self.end = end

    def __iter__(self):
        return _FixedIncrIter(self.start, self.end, datetime.timedelta(days=7))

