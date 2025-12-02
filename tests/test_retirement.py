import pytest
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from retirement import fixedInvestor, variableInvestor, finallyRetired

def test_fixedInvestor_example():
    # Example from PDF:
    # Year 1: 7500
    # Year 2: 15375
    # Year 3: 23643.75
    principal = 7500
    rate = 0.05
    years = 3
    expected = 23643.75
    assert fixedInvestor(principal, rate, years) == pytest.approx(expected, rel=1e-9)

def test_fixedInvestor_zero_years():
    assert fixedInvestor(1000, 0.05, 0) == 0.0

def test_fixedInvestor_zero_rate():
    # If rate is 0, it's just principal * years
    assert fixedInvestor(1000, 0.0, 5) == 5000.0

def test_variableInvestor_constant_rate():
    # Should match fixedInvestor if rates are all the same
    principal = 7500
    rate = 0.05
    years = 3
    rateList = [rate] * years
    expected = fixedInvestor(principal, rate, years)
    assert variableInvestor(principal, rateList) == pytest.approx(expected, rel=1e-9)

def test_variableInvestor_varying_rates():
    # Year 1: rate 0.10. Bal = 0*1.1 + 1000 = 1000
    # Year 2: rate 0.05. Bal = 1000*1.05 + 1000 = 1050 + 1000 = 2050
    principal = 1000
    rateList = [0.10, 0.05]
    expected = 2050.0
    assert variableInvestor(principal, rateList) == pytest.approx(expected, rel=1e-9)

def test_variableInvestor_negative_rates():
    # Year 1: rate -0.10. Bal = 0*0.9 + 1000 = 1000
    # Year 2: rate 0.10. Bal = 1000*1.1 + 1000 = 1100 + 1000 = 2100
    principal = 1000
    rateList = [-0.10, 0.10]
    expected = 2100.0
    assert variableInvestor(principal, rateList) == pytest.approx(expected, rel=1e-9)

def test_finallyRetired_basic_case():
    # Balance grows by 4%, then expense is withdrawn each year
    # We just check that it returns the correct number of years (approx)
    balance = 100000
    expense = 12000
    rate = 0.04
    years = finallyRetired(balance, expense, rate)
    assert years == 10 or years == 11  # depends on exact rounding


def test_finallyRetired_zero_balance():
    # If balance starts at 0 → funds already depleted
    assert finallyRetired(0, 10000, 0.05) == 0


def test_finallyRetired_exact_one_year():
    # Withdraw exactly the whole balance → lasts only 1 year
    assert finallyRetired(50000, 50000, 0.07) == 1


def test_finallyRetired_expense_greater_than_balance():
    # You overspend on year 1 → still lasts only 1 year
    assert finallyRetired(30000, 50000, 0.03) == 1


def test_finallyRetired_negative_interest():
    # Money shrinks by 10% per year before expenses
    years = finallyRetired(100000, 12000, -0.10)
    assert 8 <= years <= 10  # expected window based on typical depletion


def test_finallyRetired_low_expense_long_life():
    # Low expense → should hit safety cap
    years = finallyRetired(100000, 1, 0.04)
    assert years == 200  # matches the default max_years safeguard


def test_finallyRetired_high_interest_makes_money_last_longer():
    years = finallyRetired(100000, 2000, 0.12)
    assert years == 200   # hits safety cap due to high growth


def test_finallyRetired_invalid_negative_balance():
    # Should raise a ValueError
    with pytest.raises(ValueError):
        finallyRetired(-1000, 5000, 0.04)


def test_finallyRetired_invalid_negative_expense():
    # Should raise a ValueError
    with pytest.raises(ValueError):
        finallyRetired(50000, -1000, 0.04)


def test_finallyRetired_invalid_rate_less_than_negative_one():
    # Less than -100% is impossible
    with pytest.raises(ValueError):
        finallyRetired(50000, 10000, -1.5)


def test_finallyRetired_non_numeric_inputs():
    with pytest.raises(TypeError):
        finallyRetired("10000", 1000, 0.05)
