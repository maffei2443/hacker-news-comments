from tutorial.tutorial.spiders.helper import ParseDateApproximate
import datetime as dtime
import pytest

YEARS = [
    2014, 
    1900, 
    2012, 
    2000,
]




def test_leap_1():
    assert ParseDateApproximate.is_leap(YEARS[0]) == False


def test_leap_2():
    assert ParseDateApproximate.is_leap(YEARS[1]) == False


def test_leap_3():
    assert ParseDateApproximate.is_leap(YEARS[2]) == True


def test_leap_4():
    assert ParseDateApproximate.is_leap(YEARS[3]) == True


DATES = [
    'Jan 1, 2021',
    '8 days ago',
    '2 months ago',
    '3 years ago',
    'Mar 30, 2008',
]


@pytest.fixture(scope='module')
def day_to_test():
    return  dtime.datetime(month=2, day=15, year=2021)


def test_date_parse_0(day_to_test):
    assert (
        ParseDateApproximate.parse(DATES[0], today=day_to_test)
        == dtime.datetime(month=1, day=1, year=2021)
    )


def test_date_parse_1(day_to_test):
    assert (
        ParseDateApproximate.parse(DATES[1], today=day_to_test)
        == dtime.datetime(month=2, day=7, year=2021)
    )


def test_date_parse_2(day_to_test):
    assert (
        ParseDateApproximate.parse(DATES[2], today=day_to_test)
        == dtime.datetime(month=12, day=15, year=2020)
    )


def test_date_parse_3(day_to_test):
    assert (
        ParseDateApproximate.parse(DATES[3], today=day_to_test)
        == dtime.datetime(month=2, day=15, year=2018)
    )


def test_date_parse_4(day_to_test):
    assert (
        ParseDateApproximate.parse(DATES[4], today=day_to_test)
        == dtime.datetime(month=3, day=30 , year=2008)
    )


@pytest.fixture(scope='module')
def date_leap_years():
    return  [
        ('1 month ago', dtime.datetime(month=3, day=31, year=2020)),
        ('1 month ago', dtime.datetime(month=3, day=31, year=2021)) , 
    ]


def test_date_leap_0(date_leap_years):
    date, today = date_leap_years[0]
    assert (
        ParseDateApproximate.parse(date, today=today)
        == dtime.datetime(month=2, day=29, year=2020)
    )


def test_date_leap_1(date_leap_years):
    date, today = date_leap_years[1]
    assert (
        ParseDateApproximate.parse(date, today=today)
        == dtime.datetime(month=2, day=28, year=2021)
    )
