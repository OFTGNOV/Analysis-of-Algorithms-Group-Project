# Retirement Investment Functions Explained

## **fixedInvestor** – Compound Growth with Constant Rate

### How It Works

`fixedInvestor` simulates **annual contributions** that grow at a **fixed interest rate** over multiple years.

```python
def fixedInvestor(principal, rate, years):
    balance = 0.0
    for _ in range(years):
        balance = (balance * (1 + rate)) + principal
    return balance
```

**Each iteration:**

1. Multiply current balance by $(1 + \text{rate})$ to apply compound interest
2. Add the annual contribution (`principal`)

### Example Walkthrough

With `principal=7500`, `rate=0.05`, `years=3`:

| Year | Opening Balance | After Interest | After Contribution | Closing Balance |
|------|-----------------|-----------------|-------------------|-----------------|
| 1    | $0              | $0 × 1.05 = $0  | $0 + $7500        | $7,500          |
| 2    | $7,500          | $7,500 × 1.05 = $7,875 | $7,875 + $7,500   | $15,375         |
| 3    | $15,375         | $15,375 × 1.05 = $16,143.75 | $16,143.75 + $7,500 | $23,643.75      |

### The Algorithm

This is an **iterative simulation** that applies the recurrence relation:

$$B_n = B_{n-1} \cdot (1 + r) + P$$

where $B_n$ is balance after year $n$, $r$ is the rate, and $P$ is the principal contribution.

---

## **variableInvestor** – Compound Growth with Varying Rates

### How It Works

`variableInvestor` does the **same calculation** as `fixedInvestor`, but the interest rate **changes each year**.

```python
def variableInvestor(principal, rateList):
    balance = 0.0
    for rate in rateList:
        balance = (balance * (1 + rate)) + principal
    return balance
```

**Key difference:** Instead of a constant `rate`, you pass a `rateList` of different rates—one per year.

### Example Walkthrough

With `principal=1000`, `rateList=[0.10, 0.05]`:

| Year | Rate | Opening Balance | After Interest | After Contribution | Closing Balance |
|------|------|-----------------|-----------------|-------------------|-----------------|
| 1    | 10%  | $0              | $0 × 1.10 = $0  | $0 + $1000        | $1,000          |
| 2    | 5%   | $1,000          | $1,000 × 1.05 = $1,050 | $1,050 + $1000   | $2,050          |

### The Algorithm

This applies the **same recurrence relation** but with a **time-varying rate**:

$$B_n = B_{n-1} \cdot (1 + r_n) + P$$

where $r_n$ is the rate for year $n$.

---

## Key Differences

| Aspect | fixedInvestor | variableInvestor |
|--------|---------------|------------------|
| **Rate** | Same every year | Changes each year |
| **Use Case** | Predictable, stable markets | Realistic market conditions |
| **Flexibility** | Simple, one parameter | More granular control |

### 💡 Gotcha

Both functions assume you contribute **at the end of each year** (after interest is applied). If you need **beginning-of-year contributions**, the math changes slightly.