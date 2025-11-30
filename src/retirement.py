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
