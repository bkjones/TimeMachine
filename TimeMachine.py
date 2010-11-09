import datetime
import calendar

class TimeMachine(object):
    def __init__(self):
        # maps weekdays, using Sunday as day 0. To map daystring to number, call weekdays.index(daystring)
        self.weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    def get_next_byday(self, daystring, startdate, fmt=None):
        """
        Pass in a daystring like 'Monday' or 'Wednesday' and a start date, and this
        should return the date of the daystring following the startdate. If fmt is given, it
        should be a strftime()-compatible format string.

        >>> tm = TimeMachine()
        >>> n = datetime.datetime(2010, 7, 5)
        >>> tm.get_next_byday('Monday', n)
        datetime.datetime(2010, 7, 12, 0, 0)
        >>> tm.get_next_byday('Sunday', n)
        datetime.datetime(2010, 7, 11, 0, 0)
        >>> n = datetime.datetime(2010, 7, 13)
        >>> tm.get_next_byday('Wednesday', n)
        datetime.datetime(2010, 7, 14, 0, 0)
        >>> n = datetime.datetime(2010, 7, 14)
        >>> tm.get_next_byday('Tuesday', n)
        datetime.datetime(2010, 7, 20, 0, 0)
        """

        # decimal number day of the week we're starting from. %w formats using Sunday as day 0.
        dow_start = int(datetime.datetime.strftime(startdate, '%w'))


        # decimal number day of week we're trying to get.
        dow_target = self.weekdays.index(daystring)

        # len - ((start + (len - target)) % len)
        days_ahead = 7 - ((dow_start + (7 - dow_target)) % 7)
        res = startdate + datetime.timedelta(days=days_ahead)
        return res


    def get_previous_byday(self, daystring, startdate, fmt=None):
        """
        Pass in a daystring and startdate, and this returns the date of the closest
        daystring prior to startdate. If fmt is given, it should be a strftime()-compatible format string.

        >>> tm = TimeMachine()
        >>> n = datetime.datetime(2010, 7, 6)
        >>> tm.get_previous_byday('Sunday', n)
        datetime.datetime(2010, 7, 4, 0, 0)
        >>> tm.get_previous_byday('Thursday', n)
        datetime.datetime(2010, 7, 1, 0, 0)
        >>> n = datetime.datetime(2010, 7, 13)
        >>> tm.get_previous_byday('Monday', n)
        datetime.datetime(2010, 7, 12, 0, 0)
        >>> tm.get_previous_byday('Wednesday', n)
        datetime.datetime(2010, 7, 7, 0, 0)
        >>> n = datetime.datetime(2010, 7, 11)
        >>> tm.get_previous_byday('Sunday', n)
        datetime.datetime(2010, 7, 4, 0, 0)
        """
        # decimal number day of the week we're starting from. %w formats using Sunday as day 0.
        dow_start = int(datetime.datetime.strftime(startdate, '%w'))

        # decimal number day of week we're trying to get.
        dow_target = self.weekdays.index(daystring)

        days_back = 7 - ((dow_target + (7 - dow_start)) % 7)

        res = startdate - datetime.timedelta(days=days_back)
        return res

    def get_current_week_range(self, currdate):
        """
        Pass in a datetime object, returns a tuple of two datetime objects,
        representing the start/end dates of the week containing currdate.

        >>> tm = TimeMachine()
        >>> n = datetime.datetime(2010, 7, 9)
        >>> tm.get_current_week_range(n)
        (datetime.datetime(2010, 7, 4, 0, 0), datetime.datetime(2010, 7, 10, 0, 0))
        >>> n = datetime.datetime(2010, 7, 11)
        >>> tm.get_current_week_range(n)
        (datetime.datetime(2010, 7, 11, 0, 0), datetime.datetime(2010, 7, 17, 0, 0))
        """
        dow_start = datetime.datetime.strftime(currdate, '%w')
        if dow_start == '0':
            week_start = currdate
        else:
            week_start = self.get_previous_byday('Sunday', currdate)

        week_end = week_start + datetime.timedelta(days=6)
        return (week_start, week_end)

    def get_previous_week(self, startdate):
        """
        Pass in a datetime object, and get back a tuple of two
        datetime objects representing the start/end dates for the
        whole week prior to the start date. Weeks start on Sun. and end on Sat.
        If fmt is given, it should be a strftime()-compatible format string.


        >>> tm = TimeMachine()
        >>> n = datetime.datetime(2010, 7, 5)
        >>> tm.get_previous_week(n)
        (datetime.datetime(2010, 6, 27, 0, 0), datetime.datetime(2010, 7, 3, 0, 0))
        >>> n = datetime.datetime(2010, 7, 4)
        >>> tm.get_previous_week(n)
        (datetime.datetime(2010, 6, 27, 0, 0), datetime.datetime(2010, 7, 3, 0, 0))
        """
        # day 0 is Monday. Sunday is 6.
        dow_today = startdate.weekday()

        if dow_today == 6:
            days_ago_saturday = 1
        else:
            # To get last saturday, we need to go to day 0 (Monday), then two more days.
            days_ago_saturday = dow_today + 2

        # Make a timedelta object so we can do date arithmetic.
        delta_saturday = datetime.timedelta(days=days_ago_saturday)
        # saturday is now a date object representing last saturday
        saturday = startdate - delta_saturday
        # timedelta object representing '6 days'...
        delta_prevsunday = datetime.timedelta(days=6)
        # Making a date object. Subtract the 6 days from saturday to get "the Sunday before that".
        prev_sunday = saturday - delta_prevsunday

        last_week = (prev_sunday, saturday)
        return last_week

    def get_next_week(self, startdate):
        """
        Just like get_previous_week...

        >>> tm = TimeMachine()
        >>> n = datetime.datetime(2010, 7, 5)
        >>> tm.get_next_week(n)
        (datetime.datetime(2010, 7, 11, 0, 0), datetime.datetime(2010, 7, 17, 0, 0))
        >>> n = datetime.datetime(2010, 4, 25) # a sunday
        >>> tm.get_next_week(n)
        (datetime.datetime(2010, 5, 2, 0, 0), datetime.datetime(2010, 5, 8, 0, 0))
        """
        dow_today = int(datetime.datetime.strftime(startdate, '%w'))
        days_until_sunday = 7 - ((dow_today + 7) % 7)
        #days_until_sunday = 7 - (dow_today + 1)
        sunday = startdate + datetime.timedelta(days=days_until_sunday)
        following_saturday = sunday + datetime.timedelta(days=6)
        next_week = (sunday, following_saturday)
        return next_week

    def get_current_month_range(self, currdate):
        """
        Pass a datetime object for currdate and get back a tuple with two
        datetime objects, representing the start and end dates of the month
        that currdate is contained within.

        >>> tm = TimeMachine()
        >>> n = datetime.datetime(2010, 7, 12)
        >>> tm.get_current_month_range(n)
        (datetime.datetime(2010, 7, 1, 0, 0), datetime.datetime(2010, 7, 31, 0, 0))
        """
        days_curr_month = calendar.monthrange(currdate.year, currdate.month)[1]
        first_day_this_month = datetime.datetime(currdate.year, currdate.month, 1)
        last_day_this_month = datetime.datetime(currdate.year, currdate.month, days_curr_month)

        this_month = (first_day_this_month, last_day_this_month)
        return this_month


    def get_previous_month(self, startdate):
        """
        Pass a datetime object for startdate, and get back a tuple with two
        datetime objects, representing the start/end dates of the month before
        startdate. If fmt is given, it should be a strftime()-compatible format string.

        >>> tm = TimeMachine()
        >>> n = datetime.datetime(2010, 7, 5)
        >>> tm.get_previous_month(n)
        (datetime.datetime(2010, 6, 1, 0, 0), datetime.datetime(2010, 6, 30, 0, 0))
        """
        first_day_current = datetime.datetime(startdate.year, startdate.month, 1)
        last_day_previous = first_day_current - datetime.timedelta(days=1)
        first_day_previous = datetime.datetime(last_day_previous.year, last_day_previous.month, 1)

        last_month = (first_day_previous, last_day_previous)
        return last_month

    def get_next_month(self, startdate, fmt=None):
        """
        Just like 'get_previous_month'...

        >>> tm = TimeMachine()
        >>> n = datetime.datetime(2010, 7, 5)
        >>> tm.get_next_month(n)
        (datetime.datetime(2010, 8, 1, 0, 0), datetime.datetime(2010, 8, 31, 0, 0))
        """
        days_in_start_month = calendar.monthrange(startdate.year, startdate.month)[1]
        first_day_next_month = startdate + datetime.timedelta(days=(days_in_start_month - startdate.day + 1))
        days_in_next_month = calendar.monthrange(first_day_next_month.year, first_day_next_month.month)[1]
        last_day_next_month = first_day_next_month + datetime.timedelta(days=(days_in_next_month - 1))
        next_month = (first_day_next_month, last_day_next_month)
        return next_month

    def get_n_days_ago(self, startdate, n):
        """
        Pass in a datetime object for startdate, and an integer n, and get back
        a datetime object for the date n days prior to startdate.

        >>> tm = TimeMachine()
        >>> n = datetime.datetime(2010, 7, 5)
        >>> tm.get_n_days_ago(n, 3)
        datetime.datetime(2010, 7, 2, 0, 0)
        """
        return startdate - datetime.timedelta(days=n)

    def get_n_days_ahead(self, startdate, n, fmt=None):
        """
        Just like get_n_days_ago, but goes forward instead of back.

        >>> tm = TimeMachine()
        >>> n = datetime.datetime(2010, 7, 5)
        >>> tm.get_n_days_ahead(n, 2)
        datetime.datetime(2010, 7, 7, 0, 0)
        """
        return startdate + datetime.timedelta(days=n)

    def get_date_from_string(self, datestr, fmt):
        """
        Given a string and format string, return a datetime object.

        >>> tm = TimeMachine()
        >>> n = '2010-07-05'
        >>> tm.get_date_from_string(n, '%Y-%m-%d')
        datetime.datetime(2010, 7, 5, 0, 0)
        """
        return datetime.datetime.strptime(datestr, fmt)

    def get_period_range(self, period, start, end):
        """
        Given a start date, end date, and period type ('week' or 'month' right now),
        return a list of tuples which contain the start and end dates of each period
        in the range (start date, end date).

        >>> tm = TimeMachine()
        >>> s = '2010-07-05'
        >>> e = '2010-11-05'
        >>> tm.get_period_range('month', s, e)
        [(datetime.datetime(2010, 7, 1, 0, 0), datetime.datetime(2010, 7, 31, 0, 0)), (datetime.datetime(2010, 8, 1, 0, 0), datetime.datetime(2010, 8, 31, 0, 0)), (datetime.datetime(2010, 9, 1, 0, 0), datetime.datetime(2010, 9, 30, 0, 0)), (datetime.datetime(2010, 10, 1, 0, 0), datetime.datetime(2010, 10, 31, 0, 0)), (datetime.datetime(2010, 11, 1, 0, 0), datetime.datetime(2010, 11, 30, 0, 0))]
        >>> s = '2010-01-01'
        >>> e = '2010-01-30'
        >>> tm.get_period_range('week', s, e)
        [(datetime.datetime(2009, 12, 27, 0, 0), datetime.datetime(2010, 1, 2, 0, 0)), (datetime.datetime(2010, 1, 3, 0, 0), datetime.datetime(2010, 1, 9, 0, 0)), (datetime.datetime(2010, 1, 10, 0, 0), datetime.datetime(2010, 1, 16, 0, 0)), (datetime.datetime(2010, 1, 17, 0, 0), datetime.datetime(2010, 1, 23, 0, 0)), (datetime.datetime(2010, 1, 24, 0, 0), datetime.datetime(2010, 1, 30, 0, 0))]
        """
        if not isinstance(start, datetime.datetime):
            start = self.get_date_from_string(start, '%Y-%m-%d')
        if not isinstance(end, datetime.datetime):
            end = self.get_date_from_string(end, '%Y-%m-%d')

        if period == 'month':
            get_period = self.get_current_month_range
            get_next_period = self.get_next_month
        if period == 'week':
            get_period = self.get_current_week_range
            get_next_period = self.get_next_week

        returnvals = []


        firstper = get_period(start)
        returnvals.append(firstper)
        per = firstper
        while per[1] < end:
            # goes as long as the *end* of the period is < our end date.
            # the intent is that if end is 2010-10-04, the last period will be
            # (2010-10-01, 2010-10-31)
            per = get_next_period(per[1])
            returnvals.append(per)

        return returnvals



def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
