"""
Helper script to create sample historical data for testing when network is unavailable.
"""

import pandas as pd
import numpy as np

# Generate synthetic historical monthly returns for S&P 500
# Based on typical characteristics: ~1% monthly return, ~4% monthly std
np.random.seed(42)

dates = pd.date_range(start='2020-01-31', end='2025-02-28', freq='ME')
n_months = len(dates)

# Generate returns with realistic properties
# Mean: ~1% monthly (12% annualized)
# Std: ~4% monthly
# Slight negative skewness (typical for equity returns)
monthly_returns = np.random.normal(0.01, 0.04, n_months)

# Add some negative skewness by including a few larger negative returns
monthly_returns[10] = -0.08
monthly_returns[25] = -0.12
monthly_returns[45] = -0.10

# Create DataFrame
historical_data = pd.DataFrame({
    'Date': dates,
    'Log_Return': monthly_returns
})

# Save to CSV
historical_data.to_csv('./data/sample_historical_returns.csv', index=False)

print(f"Created sample historical data with {len(historical_data)} monthly observations")
print(f"Mean: {monthly_returns.mean():.6f}")
print(f"Std: {monthly_returns.std():.6f}")
print(f"\nSaved to: ./data/sample_historical_returns.csv")
