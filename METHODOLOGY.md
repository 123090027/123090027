# Methodology: Extracting Distribution Moments from Options

## Overview

This document explains the mathematical methodology used to extract distributional moments from S&P 500 options data.

## Risk-Neutral Distribution (from Options)

### Theoretical Foundation

The risk-neutral distribution is extracted using the **Bakshi, Kapadia, and Madan (2003)** method, which leverages the relationship between option prices and the risk-neutral probability distribution.

### Key Formulas

#### 1. Forward Price

The forward price is calculated using put-call parity:

```
F = K₀ + exp(rT) × (C_ATM - P_ATM)
```

Where:
- `K₀` = ATM strike price
- `r` = risk-free rate
- `T` = time to maturity
- `C_ATM`, `P_ATM` = ATM call and put prices

#### 2. First Moment (Mean)

```
μ_Q = exp(rT) - 1 - (exp(rT)/2) × ∫ Q(K)/K² dK
```

Where `Q(K)` is the price of an OTM option at strike K.

#### 3. Second Moment (Variance)

```
σ²_Q = exp(rT) × ∫ Q(K)/K² dK - μ²_Q
```

#### 4. Third Moment (Skewness)

```
W = exp(rT) × ∫ [6×ln(K/F) - 3×ln²(K/F)] × Q(K)/K² dK

Skewness = (W - 3×μ_Q×σ²_Q - μ³_Q) / σ³_Q
```

#### 5. Fourth Moment (Kurtosis)

```
X = exp(rT) × ∫ [12×ln²(K/F) - 4×ln³(K/F)] × Q(K)/K² dK

Excess Kurtosis = (X - 4×W×μ_Q + 6×σ²_Q×μ²_Q + 3×μ⁴_Q) / σ⁴_Q - 3
```

### Implementation Steps

1. **Data Preparation**
   - Separate calls and puts
   - Filter for liquid options (Volume > 0, Open Interest > 0)
   - Identify ATM strike

2. **Calculate Forward Price**
   - Use put-call parity at ATM
   - This gives the risk-neutral expected future spot price

3. **Select OTM Options**
   - OTM puts: K ≤ F
   - OTM calls: K > F
   - OTM options are more liquid and have cleaner prices

4. **Numerical Integration**
   - Use trapezoidal integration across strikes
   - Compute integrals for each moment
   - Extract moments from the integrals

5. **Convert to Log Returns**
   - Mean of log returns: `E[ln(S_T/S_t)] ≈ μ_Q - σ²_Q/2`
   - Std of log returns: `√σ²_Q`

## Real-World Distribution (from Historical Data)

### Methodology

The real-world distribution is estimated from historical S&P 500 returns.

### Steps

1. **Download Historical Data**
   - Source: Yahoo Finance (^GSPC)
   - Frequency: Monthly (for comparability with short-term options)
   - Period: 5+ years (sufficient sample size)

2. **Calculate Log Returns**
   ```
   r_t = ln(S_t / S_{t-1})
   ```

3. **Compute Sample Moments**
   - Mean: `μ = (1/n) × Σ r_t`
   - Variance: `σ² = (1/n) × Σ (r_t - μ)²`
   - Skewness: `(1/n) × Σ [(r_t - μ)/σ]³`
   - Excess Kurtosis: `(1/n) × Σ [(r_t - μ)/σ]⁴ - 3`

4. **Scale to Option Horizon**

   For horizon T (in years):
   ```
   μ_T = μ_monthly × T × 12
   σ_T = σ_monthly × √(T × 12)
   ```

   Note: Skewness and kurtosis don't scale with time (they're shape parameters)

## Comparison and Interpretation

### Why Compare These Two Distributions?

The risk-neutral and real-world distributions reveal different information:

| Measure | Risk-Neutral (Q) | Real-World (P) |
|---------|------------------|----------------|
| **Source** | Options prices | Historical returns |
| **Time horizon** | Forward-looking | Backward-looking |
| **Reflects** | Market expectations + risk aversion | Actual realized behavior |
| **Incorporates** | Risk premiums | Historical patterns |

### Expected Differences

#### 1. Mean

```
μ_Q < μ_P
```

**Reason**: The equity risk premium. Investors demand higher expected returns (under P) to compensate for bearing equity risk. The risk-neutral measure (Q) doesn't include this premium.

**Formula**: `Equity Risk Premium ≈ μ_P - μ_Q`

#### 2. Volatility

Can go either way, but often:
```
σ_Q > σ_P
```

**Reason**: Markets may price in higher volatility than historically realized, especially during uncertain times (volatility risk premium).

#### 3. Skewness

Typically:
```
Skew_Q < Skew_P < 0
```

**Reason**: Crash risk premium. Investors pay extra for downside protection (puts), making the risk-neutral distribution more negatively skewed. This reflects fear of large negative moves.

#### 4. Kurtosis

Often:
```
Kurt_Q > Kurt_P > 0
```

**Reason**: Tail risk premium. Options markets price in higher probability of extreme events (fat tails) than what's observed historically. Investors pay for protection against black swan events.

### Economic Interpretation

The differences between Q and P measures reveal:

1. **Risk Premiums**: How much investors pay for protection
2. **Market Sentiment**: Fear, uncertainty, and risk aversion
3. **Forward vs Backward**: Market expectations vs historical reality
4. **Structural Breaks**: Changes in market regime

## Implementation Details

### Numerical Considerations

1. **Integration Method**: Trapezoidal rule
   - Simple and robust
   - Works well for discrete strike data
   - More sophisticated methods (splines) can be used for smoother curves

2. **Strike Range**:
   - Use strikes covering 0.85 to 1.15 of forward price
   - Avoid deep OTM options (low liquidity, wide spreads)

3. **Option Filtering**:
   - Remove options with zero volume/open interest
   - Filter out options with wide bid-ask spreads

### Data Quality Issues

Common issues and solutions:

| Issue | Solution |
|-------|----------|
| Missing strikes | Interpolation (carefully) |
| Wide spreads | Use mid price, filter if spread > 15% |
| Low liquidity | Filter by volume and open interest |
| Stale quotes | Use recent data only |

## References

1. **Bakshi, G., Kapadia, N., & Madan, D. (2003).** "Stock Return Characteristics, Skew Laws, and the Differential Pricing of Individual Equity Options." *Review of Financial Studies*, 16(1), 101-143.

2. **Breeden, D. T., & Litzenberger, R. H. (1978).** "Prices of State-Contingent Claims Implicit in Option Prices." *Journal of Business*, 51(4), 621-651.

3. **Carr, P., & Madan, D. (2001).** "Towards a Theory of Volatility Trading." In *Volatility*, pp. 417-427. Risk Books.

4. **Jiang, G. J., & Tian, Y. S. (2005).** "The Model-Free Implied Volatility and Its Information Content." *Review of Financial Studies*, 18(4), 1305-1342.

## Code Structure

```
risk_neutral_moments.py:
├── calculate_risk_neutral_moments()
│   ├── Filter OTM options
│   ├── Calculate forward price
│   ├── Compute integrals
│   └── Extract moments

real_world_moments.py:
├── calculate_real_world_moments()
│   ├── Download historical data
│   ├── Calculate log returns
│   ├── Compute sample moments
│   └── Scale to horizon

comparison.py:
├── compare_distributions()
│   └── Side-by-side comparison
├── plot_distribution_comparison()
│   └── Visualization
└── generate_interpretation()
    └── Economic interpretation
```

## Further Reading

For deeper understanding:
- Option pricing theory (Black-Scholes-Merton)
- Risk-neutral valuation
- Implied volatility and volatility smiles/skews
- Risk premiums in equity markets
- Higher-moment risk premia
