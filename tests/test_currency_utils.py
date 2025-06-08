import pytest
from utils.currency_utils import format_currency


def test_format_currency_brl_default():
    assert format_currency(1234.56, "BRL") == "R$ 1.234,56"


def test_format_currency_usd():
    assert format_currency(1234.56, "USD") == "$ 1,234.56"


def test_format_currency_eur():
    assert format_currency(1234.56, "EUR") == "€ 1.234,56"


def test_format_currency_generic_no_symbol():
    assert format_currency(1234.56, "GBP", show_symbol=False) == "1,234.56"
