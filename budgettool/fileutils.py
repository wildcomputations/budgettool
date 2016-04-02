import datetime

def str_to_date(datestr):
    """TODO: expand this to support other formats automatically?"""
    return datetime.datetime.strptime(datestr, '%d %B %Y').date()

def date_to_str(date):
    return date.strftime('%d %B %Y')

def str_to_weekday(daystr):
    try:
        return int(daystr)
    except ValueError:
        return {
            'sunday'    : 0,
            'monday'    : 1,
            'tuesday'   : 2,
            'wednesday' : 3,
            'thursday'  : 4,
            'friday'    : 5,
            'saturday'  : 6,
            'sun'       : 0,
            'mon'       : 1,
            'tue'       : 2,
            'wed'       : 3,
            'thu'       : 4,
            'fri'       : 5,
            'sat'       : 6,
        }[daystr.lower()]

def weekday_to_str(weekday):
    return ('sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')[weekday]

def dict_to_duration(data):
    return datetime.timedelta(**data)

def duration_to_dict(duration):
    days = duration.days
    if days % 7:
        return { 'days' : days }
    else:
        return { 'weeks' : days // 7 }

def get_default(key, values, default, func=None):
    if key in values:
        if func:
            return func(values[key])
        else:
            return values[key]
    else:
        return default
