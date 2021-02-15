import re
import datetime as dtime

class ParseDateApproximate(object):
    months = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'may': 5,
        'june': 6,
        'july': 7,
        'aug': 8,
        'sept': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12,
    }

    regex_months = r'({})'.format('|'.join(months))
    regex_date = r'{} ([0-9]+), ([0-9]+)'.format(regex_months)

    # https://www.programiz.com/python-programming/examples/leap-year
    # (adapted)
    @staticmethod
    def is_leap(y: int):
        """Checks whether `y` is a leap year.

        Args:
            y (int): year to be checked

        Returns:
            bool: `True` if `y` is a leap year, False otherwise
        """
        return bool(
            not y % 4 and 
            (y % 100 or not y % 400)
        )

    @classmethod
    def parse(cls, s: str, today=dtime.datetime, debug=False):
        """Parses the date at most on day-level.

        The granularity depends on the information received. For example:

        - "3 (minutes|hours) ago": is this case its possible to know (considering
            syncronous processing) the exact minute at which an item was
            created. However as this is not the case for old comments 
            the majority of time
        - "1 month ago": this case show the unavoidable limited information
            that can be appear
        - "on Feb 13, 2020": this situation happens for old comments.
        WARNING:
            There may be some light innacuracy when time passed is defined
            in terms of "months"/"years" ago since the exact amount of days
            passed is not available. Also, newer comments may have a one-day
            innacuracy.

            
        Args:
            s (str): string containing the date
        Returns:
            datetime.datetime: object representing the date present in `s`
                considering month-level granularity.
        """
        s = s.lower()
        m, d, y = None, None, None
        if debug:
            print(f"[{__name__}.ParseDateApproximate.parse] TODAY:", today)
        if 'ago' in s:
            date = None
            delta = int(re.search(r'([0-9]+)', s).group(1))
            if 'day' in s:
                date = today - dtime.timedelta(delta)
                m, d, y = date.month, date.day, date.year
            elif 'month' in s:
                d = today.day
                m = today.month - delta
                y = today.year
                if m <= 0:
                    m = (m + 12) % 13
                    y = today.year - 1
                if m == 2:
                    d = min(d, (29 if cls.is_leap(y) else 28))
            elif 'year' in s:
                date = today
                m, d, y = date.month, date.day, date.year - delta
            elif 'minute' in s or 'hour' in s:
                date = today
                m, d, y = date.month, date.day, date.year
            else:
                raise ValueError("Innapropriate value of s: {}".format(s))
        else:  # easy case
            m, d, y = re.search(cls.regex_date, s, re.IGNORECASE).groups()
            m, d, y = cls.months[m], int(d), int(y)
        date = dtime.datetime(month=m, day=d, year=y)
        if debug:
            print(f'[{__name__}.ParseDateApproximate.parse] WAS:', date, end='\n\n')
        return date

