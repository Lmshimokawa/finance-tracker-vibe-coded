import datetime
from utils import date_utils


def test_get_date_range_today(monkeypatch):
    fake_today = datetime.date(2024, 4, 10)
    monkeypatch.setattr(date_utils, "get_today", lambda: fake_today)
    start, end = date_utils.get_date_range("today")
    assert start == fake_today and end == fake_today


def test_get_date_range_this_week(monkeypatch):
    fake_today = datetime.date(2024, 4, 10)  # Wednesday
    monkeypatch.setattr(date_utils, "get_today", lambda: fake_today)
    start, end = date_utils.get_date_range("this_week")
    assert start == datetime.date(2024, 4, 8)
    assert end == datetime.date(2024, 4, 14)


def test_get_date_range_last_30_days(monkeypatch):
    fake_today = datetime.date(2024, 4, 10)
    monkeypatch.setattr(date_utils, "get_today", lambda: fake_today)
    start, end = date_utils.get_date_range("last_30_days")
    assert start == datetime.date(2024, 3, 12)
    assert end == fake_today
