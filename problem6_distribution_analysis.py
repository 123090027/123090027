"""
Problem 6: Extract and Compare Distribution Moments

This script extracts mean, standard deviation, skewness, and kurtosis of the log returns
of the S&P 500 index under both risk-neutral and real-world probability measures.

Usage:
    python problem6_distribution_analysis.py

Requirements:
    - S&P 500 options data CSV file in ./data/ directory
    - Internet connection for downloading historical data
"""

import pandas as pd
import numpy as np
import warnings
import os

# Import custom modules
from risk_neutral_moments import calculate_risk_neutral_moments, print_risk_neutral_results
from real_world_moments import calculate_real_world_moments, print_real_world_results
from real_world_moments_offline import calculate_real_world_moments_from_file
from comparison import compare_distributions, print_comparison_table, plot_distribution_comparison, generate_interpretation

warnings.filterwarnings('ignore')

# ============================================================================
# Configuration
# ============================================================================

# Data file path
DATA_FILE = './data/spx-options-exp-2025-03-13-weekly.csv'

# Market parameters
CURRENT_DATE = pd.Timestamp('2025-02-13')
MATURITY_DATE = pd.Timestamp('2025-03-13')
SPX_PRICE = 6051.0  # S&P 500 level on 2025-02-13
RISK_FREE_RATE = 0.04  # 4% annual risk-free rate

# Time to maturity
T = (MATURITY_DATE - CURRENT_DATE).days / 365.0

print("="*80)
print("PROBLEM 6: DISTRIBUTION ANALYSIS OF S&P 500 LOG RETURNS")
print("="*80)
print(f"Current Date        : {CURRENT_DATE.date()}")
print(f"Option Maturity Date: {MATURITY_DATE.date()}")
print(f"Time to Maturity    : {T:.4f} years ({(MATURITY_DATE - CURRENT_DATE).days} days)")
print(f"S&P 500 Level       : {SPX_PRICE:.2f}")
print(f"Risk-Free Rate      : {RISK_FREE_RATE*100:.2f}%")
print("="*80)


# ============================================================================
# Part 1: Load and Prepare Options Data
# ============================================================================

print("\n" + "="*80)
print("PART 1: LOADING OPTIONS DATA")
print("="*80)

if not os.path.exists(DATA_FILE):
    print(f"\nERROR: Options data file not found: {DATA_FILE}")
    print("Please place the file 'spx-options-exp-2025-03-13-weekly.csv' in the ./data/ directory")
    print("\nTo create sample data for testing, you can use the following format:")
    print("Type,Strike,Bid,Mid,Ask,IV,Delta,Volume,Open Int")
    print("Call,6100,50,52,54,0.15,0.52,1000,5000")
    print("Put,6000,48,50,52,0.14,0.48,1000,5000")
    exit(1)

# Load options data
options_data = pd.read_csv(DATA_FILE)

# Clean data - remove footer rows if present
options_data = options_data[~options_data['Strike'].astype(str).str.contains('Downloaded', na=False)].copy()

# Clean and convert to numeric
for col in ['Strike', 'Bid', 'Mid', 'Ask']:
    options_data[col] = pd.to_numeric(options_data[col].astype(str).str.replace(',', ''), errors='coerce')

# Handle IV column (might be percentage)
if options_data['IV'].dtype == 'object':
    options_data['IV'] = pd.to_numeric(options_data['IV'].str.rstrip('%'), errors='coerce') / 100
else:
    options_data['IV'] = pd.to_numeric(options_data['IV'], errors='coerce')

# Convert Volume and Open Interest
for col in ['Volume', 'Open Int']:
    if col in options_data.columns:
        options_data[col] = pd.to_numeric(options_data[col].replace('unch', '0'), errors='coerce').fillna(0)

# Remove rows with NaN
options_data = options_data.dropna(subset=['Strike', 'Bid', 'Mid', 'Ask', 'IV'])

print(f"\nLoaded {len(options_data)} options from {DATA_FILE}")
print(f"  - Call options: {len(options_data[options_data['Type'] == 'Call'])}")
print(f"  - Put options : {len(options_data[options_data['Type'] == 'Put'])}")


# ============================================================================
# Part 2: Calculate Risk-Neutral Distribution Moments
# ============================================================================

print("\n" + "="*80)
print("PART 2: RISK-NEUTRAL DISTRIBUTION (from Options Data)")
print("="*80)

try:
    rn_results = calculate_risk_neutral_moments(
        options_data=options_data,
        spx_price=SPX_PRICE,
        T=T,
        r=RISK_FREE_RATE
    )
    print_risk_neutral_results(rn_results)
except Exception as e:
    print(f"\nERROR calculating risk-neutral moments: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)


# ============================================================================
# Part 3: Calculate Real-World Distribution Moments
# ============================================================================

print("\n" + "="*80)
print("PART 3: REAL-WORLD DISTRIBUTION (from Historical Data)")
print("="*80)

try:
    # Try to calculate with monthly frequency from yfinance
    print("\nAttempting to download historical data from Yahoo Finance...")
    try:
        rw_results = calculate_real_world_moments(
            start_date='2020-01-01',
            end_date='2025-02-13',
            freq='monthly',
            T_years=T
        )
        print_real_world_results(rw_results)
    except Exception as e_online:
        print(f"\nWarning: Could not download data from Yahoo Finance: {str(e_online)}")
        print("Falling back to sample historical data...")

        # Fall back to sample data
        sample_file = './data/sample_historical_returns.csv'
        if os.path.exists(sample_file):
            rw_results = calculate_real_world_moments_from_file(
                filepath=sample_file,
                T_years=T
            )
            print_real_world_results(rw_results)
            print("\n*** Note: Using sample/cached historical data ***")
        else:
            raise FileNotFoundError(f"Sample historical data not found at {sample_file}. "
                                  "Run 'python create_sample_historical_data.py' to generate it.")

except Exception as e:
    print(f"\nERROR calculating real-world moments: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)


# ============================================================================
# Part 4: Compare Risk-Neutral vs Real-World
# ============================================================================

print("\n" + "="*80)
print("PART 4: COMPARISON OF DISTRIBUTIONS")
print("="*80)

try:
    comparison_df = compare_distributions(rn_results, rw_results)
    print_comparison_table(comparison_df)

    # Generate interpretation
    interpretation = generate_interpretation(comparison_df)
    print(interpretation)

    # Create visualization
    plot_distribution_comparison(
        rn_results=rn_results,
        rw_results=rw_results,
        save_path='distribution_comparison.pdf'
    )

except Exception as e:
    print(f"\nERROR during comparison: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)


# ============================================================================
# Save Results to CSV
# ============================================================================

print("\n" + "="*80)
print("SAVING RESULTS")
print("="*80)

# Save comparison table
comparison_df.to_csv('comparison_results.csv', index=False)
print("Comparison table saved to: comparison_results.csv")

# Save detailed results
detailed_results = pd.DataFrame({
    'Measure': ['Risk-Neutral', 'Real-World (Monthly)'],
    'Mean': [rn_results['mean'], rw_results['mean_scaled']],
    'Std Dev': [rn_results['std'], rw_results['std_scaled']],
    'Skewness': [rn_results['skewness'], rw_results['skewness']],
    'Excess Kurtosis': [rn_results['kurtosis'], rw_results['kurtosis']],
    'Data Source': [f"{rn_results['num_options']} OTM options",
                    f"{rw_results['n_observations']} monthly observations"]
})
detailed_results.to_csv('detailed_results.csv', index=False)
print("Detailed results saved to: detailed_results.csv")

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print("\nGenerated files:")
print("  1. comparison_results.csv      - Side-by-side comparison")
print("  2. detailed_results.csv        - Detailed results")
print("  3. distribution_comparison.pdf - Visual comparison plots")
print("="*80)
