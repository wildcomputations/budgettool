""" Classes which generate transactions based on repeating schedules.
Dates are returned as instances of datetime.date
"""

from calendar import monthrange
import datetime
import math

def _check_calc_date_range(schedule_start,
                           user_start,
                           schedule_end,
                           user_end,
                           user_duration):
    """ Helper function to compute an end date from a start and an end date or
    duration which may be none.
    """
    if schedule_start is None:
        start = user_start
    else:
        start = max(schedule_start, user_start)

    if user_end is not None:
        end = user_end
    elif user_duration is not None:
        end = user_start + user_duration - datetime.timedelta(1)
    else:
        raise ValueError("No end specified")

    if schedule_end is not None:
        end = min(end, schedule_end)

    return start, end


class _DayIncrIter:
    """Fixed increment in days
    """
    def __init__(self, container):
        """Increment up to, and including end_date
        """
        self.container = container
        self.next_date = container.start_date
    def __iter__(self):
        return self
    def __next__(self):
        if self.next_date > self.container.end_date:
            raise StopIteration
        out = self.next_date
        self.next_date += self.container.increment
        return out

class _DayIncrContainer:
    """Fixed increment in days
    """
    def __init__(self, start_date, end_date, increment):
        """Increment up to, and including end_date
        """
        self.start_date = start_date
        self.end_date = end_date
        self.increment = increment
    def __iter__(self):
        return _DayIncrIter(self)

class _MonthIncrIter:
    """Increment in months."""

    def __init__(self, container):
        """Increment through the virtual container of _MonthIncrContainer."""
        self.container = container
        self.next_month = container.start_month
    def __iter__(self):
        return self
    def __next__(self):
        out = self.next_month.replace(
                day = min(self.container.day,
                    monthrange(self.next_month.year, self.next_month.month)[1]))
        if out > self.container.end_date:
            raise StopIteration

        next_month = self.next_month.month + self.container.increment
        next_year = self.next_month.year + (next_month - 1) // 12
        self.next_month = datetime.date(next_year, (next_month - 1) % 12 + 1, 1)

        return out

class _MonthIncrContainer:
    """Increment in months."""

    def __init__(self, start_month, day, end_date, increment):
        """Start at next_date, increment up to and including end_date.

        Increment by 'increment' months.
        """
        self.start_month = start_month
        self.day = day
        self.end_date = end_date
        self.increment = increment

    def __iter__(self):
        return _MonthIncrIter(self)


class Once:
    """ One time transaction. Generates a single event on the specified date.
    """
    def __init__(self, date):
        self.date = date

    def view(self, start, end=None, duration=None):
        """Generate the subset of events within a date window.

        Must specify either an end or a duration.

        Parameters
        ---
        start - start date
        end - (optional) the last day in the window.
        duration - (optional) duration for the window.
        """
        start, end = _check_calc_date_range(self.date,
                                            start,
                                            self.date + datetime.timedelta(1),
                                            end,
                                            duration)
        if start <= self.date and self.date <= end:
            return [self.date]
        else:
            return []

class EveryNWeek:
    """ Repeating schedule on weekly increments.
    For example, repeat every 2 weeks starting on Jan 1.
    """
    def __init__(self, start, step=1, end=None):
        """Create the schedule. By default it will repeat every week.

        Params
        -----
        start - datetime.date object for the first instance of this event
        step - the number of weeks between events
        end - cuttoff for last event to generate
        """
        self.start = start
        self.step = step
        self.end = end

    def view(self, start, end=None, duration=None):
        """The subset of events which fall within a window.

        Parameters
        -----
        start - start of the window
        end - (optional) the last day in the window
        duration - (optional) the length of the window as a timedelta.

        Must specify either an end or a duration.
        """
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

        return _DayIncrContainer(next_date, iter_end, step)

class EveryNMonth:
    """Event repeats on the same day every month.
    """

    def __init__(self, start, step=1, end=None):
        """
        Specify how often this schedule repeats and the day of month to repeat on.

        Params
        ------
        day_of_month - day of the month.
        step - how many months between repeats
        end - cuttoff for last date to generate (non-inclusive)
        """
        self.start = start
        self.step = step
        self.end = end

    def view(self, start, end=None, duration=None):
        """The subset of events which fall within a window.

        Parameters
        -----
        start - start of the window
        end - (optional) the last day in the window
        duration - (optional) the length of the window as a timedelta.

        Must specify either an end or a duration here or in constructor.
        """
        iter_start, iter_end = _check_calc_date_range(
            self.start, start,
            self.end, end, duration)
        if iter_start >= iter_end:
            return []

        day = self.start.day
        start = self.start

        if start < iter_start:
            print("initial start", start,
                    "iter_start", iter_start)
            delta_year = iter_start.year - start.year
            delta_month = iter_start.month - start.month + 12 * delta_year
            if iter_start.day > start.day:
                delta_month += 1
            print("delta month", delta_month)

            extra_months_needed = (-delta_month) % self.step
            print("extra months", extra_months_needed,
                    "step", self.step)
            
            start_month_0 = iter_start.month + extra_months_needed - 1
            start_year = iter_start.year + start_month_0 // 12
            start_month = 1 + (start_month_0 % 12)

            start = datetime.date(start_year, start_month, 1)
            print("computed start", start)

        return _MonthIncrContainer(start, day, iter_end, self.step)

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

    def view(self, start, end=None, duration=None):
        """The subset of events which fall within a window.

        Parameters
        -----
        start - start of the window
        end - (optional) the last day in the window
        duration - (optional) the length of the window as a timedelta.

        Must specify either an end or a duration.
        """
        iter_start, iter_end = _check_calc_date_range(
            self.start, start,
            self.end, end, duration)
        if iter_start > iter_end:
            return []

        offset = (self.day_of_week - iter_start.weekday()) % 7
        iter_start = iter_start + datetime.timedelta(offset)

        return _DayIncrContainer(iter_start, iter_end, datetime.timedelta(days=7))

class Monthly:
    """Repeat every month on the specified day"""

    def __init__(self, day_of_month, start=None, end=None):
        """Create a schedule which repeats every month on a specific day.

        Parameters
        ---------
        day_of_month - integer day of the month (0-31)
        end - end date. No events generated past this date.
        iter_start - first day to consider generating an event.
        """
        self.day_of_month = day_of_month
        self.start = start
        self.end = end

    def view(self, start, end=None, duration=None):
        """The subset of events which fall within a window.

        Parameters
        -----
        start - start of the window
        end - (optional) the last day in the window
        duration - (optional) the length of the window as a timedelta.

        Must specify either an end or a duration here or in constructor.
        """
        iter_start, iter_end = _check_calc_date_range(
            self.start, start,
            self.end, end, duration)
        if iter_start >= iter_end:
            return []

        start = iter_start
        if iter_start.day > self.day_of_month:
            start.replace(day=1)
            start += datetime.timedelta(31)
        start.replace(day=1)

        return _MonthIncrContainer(start, self.day_of_month, end, 1)
