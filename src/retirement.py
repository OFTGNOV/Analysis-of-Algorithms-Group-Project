def fixedInvestor(principal, rate, years):
    """
    Simulates compound growth of retirement savings over a fixed interest rate and time period.
    
    Args:
        principal (float): The annual contribution amount.
        rate (float): The annual interest rate (e.g., 0.05 for 5%).
        years (int): The number of years until retirement.
        
    Returns:
        float: Total accumulated balance after all contributions and compounding.
    """
    balance = 0.0
    for _ in range(years):
        balance = (balance * (1 + rate)) + principal
    return balance

def variableInvestor(principal, rateList):
    """
    Models the effect of varying annual interest rates over time.
    
    Args:
        principal (float): The annual contribution amount.
        rateList (list of float): List of annual percentage growth rates.
        
    Returns:
        float: Final accumulated balance after applying each year's rate sequentially.
    """
    balance = 0.0
    for rate in rateList:
        balance = (balance * (1 + rate)) + principal
    return balance

def finallyRetired(balance, expense, rate, max_years=200):
    """
    Recursively determine how many years retirement funds last.
    
    balance: initial retirement savings (must be >= 0)
    expense: yearly withdrawal (must be > 0)
    rate: yearly interest rate (cannot be < -1)
    max_years: safety cap to prevent infinite recursion
    """

    # type checks
    if not isinstance(balance, (int, float)):
        raise TypeError("balance must be a numeric value")
    if not isinstance(expense, (int, float)):
        raise TypeError("expense must be a numeric value")
    if not isinstance(rate, (int, float)):
        raise TypeError("rate must be a numeric value")

    # logical validity checks
    if balance < 0:
        raise ValueError("balance cannot be negative")
    if expense <= 0:
        raise ValueError("expense must be a positive number")
    if rate < -1:
        raise ValueError("rate cannot be less than -1 (−100%)")

    # safety cap: avoid infinite recursion
    if max_years <= 0:
        # This means the money lasted beyond our safety limit
        # so we return the upper bound.
        return 0

    # BASE CASE
    if balance <= 0:
        return 0

    # RECURSIVE STEP
    new_balance = balance * (1 + rate) - expense

    return 1 + finallyRetired(new_balance, expense, rate, max_years - 1)
