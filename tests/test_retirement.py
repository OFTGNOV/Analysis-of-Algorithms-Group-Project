import pytest
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from retirement import fixedInvestor, variableInvestor

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
