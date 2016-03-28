""" Classes which generate transactions based on repeating schedules.
Dates are returned as instances of datetime.date
"""

import datetime
import math

def _check_calc_date_range(default_start,
        user_start,
        default_end,
        user_end,
        user_duration):
    """ Helper function to compute an end date from a start and an end date or
    duration which may be none.
    """
    if user_start is None:
        start = default_start
    else:
        start = user_start

    if start is None:
        raise ValueError("No start specified")
    if default_start is not None:
        start = max(default_start, start)

    if user_end is not None:
        end = user_end
    elif user_duration is not None:
        end = user_start + user_duration
    else:
        end = default_end

    if end is None:
        raise ValueError("No end specified")

    if default_end is not None:
        end = min(end, default_end)

    return start, end

class Once:
    """ One time transaction. Generates a single event on the specified date.
    """
    def __init__(self, date):
        self.date = date

    def view(self, start=datetime.date.today(), end=None, duration=None):
        start, end = _check_calc_date_range(
                self.date, start,
                self.date + datetime.timedelta(1), end, duration)
        if start <= self.date and self.date < end:
            return [self.date]
        else:
            return []

class _FixedIncrIter:
    """Fixed increment in days
    """
    def __init__(self, container):
        """Increment up to, but excluding end_date
        """
        self.container = container
        self.next_date = container.start_date
    def __iter__(self):
        return self
    def __next__(self):
        if self.next_date >= self.container.end_date:
            raise StopIteration
        out = self.next_date
        self.next_date += self.container.increment
        return out

class _FixedIncrContainer:
    """Fixed increment in days
    """
    def __init__(self, start_date, end_date, increment):
        """Increment up to, but excluding end_date
        """
        self.start_date = start_date
        self.end_date = end_date
        self.increment = increment
    def __iter__(self):
        return _FixedIncrIter(self)

class EveryNWeek:
    """ Repeating schedule on weekly increments.
    For example, repeat every 2 weeks starting on Jan 1.
    """
    def __init__(self, start, step=1, end=None):
        """Create the schedule. By default it will repeat every week and won't
        generate old dates before today.

        Params
        -----
        start - datetime.date object for the first instance of this event
        step - the number of weeks between events
        end - cuttoff for last event to generate
        """
        self.start = start
        self.step = step
        self.end = end

    def view(self, start=datetime.date.today(), end=None, duration=None):
        iter_start, iter_end = _check_calc_date_range(
                self.start, start,
                self.end, end, duration)
        if iter_start >= iter_end:
            return []

        step = self.step * datetime.timedelta(days=7)

        if self.start < iter_start:
            delta = iter_start - self.start
            num_steps = math.ceil(delta / step)
            next_date = self.start + num_steps * step
        else:
            next_date = self.start

        return _FixedIncrContainer(next_date, iter_end, step)

class Weekly:
    """ Repeat every week on a specifc day of the week.
    For example, repeat every Tuesday.
    """
    def __init__(self, day_of_week, start=None, end=None):
        """ Repeat every week on the specified day of the week.
        Defaults to only generating events in the future.

        Params
        _______
        day_of_week: integer representation of day of the week. Monday is 0,
                 Sunday is 6.
        end - cuttoff for last event to generate
        iter_start: cuttoff for earliest event to generate.
        """
        self.day_of_week = day_of_week
        self.start = start
        self.end = end

    def view(self, start=datetime.date.today(), end=None, duration=None):
        iter_start, iter_end = _check_calc_date_range(
                self.start, start,
                self.end, end, duration)
        if iter_start >= iter_end:
            return []

        offset = (self.day_of_week - iter_start.weekday()) % 7
        iter_start = iter_start + datetime.timedelta(offset)

        return _FixedIncrContainer(iter_start, iter_end, datetime.timedelta(days=7))

