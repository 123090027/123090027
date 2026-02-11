# Quick Start Guide

## Problem 6: Distribution Analysis

This guide shows you how to solve Problem 6 step by step.

## Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Prepare Your Data

Place your S&P 500 options data file in the `./data/` directory:
- Filename: `spx-options-exp-2025-03-13-weekly.csv`
- See `./data/README.md` for required columns

**OR** use the included sample data for testing.

### Step 3: Run the Analysis

```bash
python problem6_distribution_analysis.py
```

This will:
1. Load the options data
2. Calculate risk-neutral moments from options
3. Download historical S&P 500 data (or use cached data if offline)
4. Compare the distributions
5. Generate visualizations and save results

### Step 4: View Results

The script generates:
- **comparison_results.csv** - Comparison table
- **detailed_results.csv** - Detailed results
- **distribution_comparison.pdf** - Visual comparison (4 plots)
- **Console output** - Full analysis with interpretation

## Understanding the Results

### Risk-Neutral Distribution
Extracted from options prices using the Bakshi-Kapadia-Madan (2003) method:
- Reflects market's forward-looking expectations
- Incorporates risk aversion and crash risk premiums
- Shows what the market "prices in" for future returns

### Real-World Distribution
Calculated from historical S&P 500 monthly returns:
- Reflects actual historical behavior
- Backward-looking measure
- Based on realized returns

### Key Insights

**Mean Difference**:
- Risk-neutral mean is typically lower than real-world mean
- This difference is the **equity risk premium** - compensation for bearing equity risk

**Skewness**:
- Negative risk-neutral skewness indicates **crash risk premium**
- Market pays more for downside protection (puts)
- Reflects investor fear of large negative movements

**Kurtosis**:
- Higher risk-neutral kurtosis indicates **fat tails**
- Market prices in extreme events through options
- Higher probability of large moves (up or down)

## Customization

### Using Your Own Options Data

Replace the sample data with your actual data:
1. Place CSV file in `./data/` directory
2. Update parameters in `problem6_distribution_analysis.py`:
   ```python
   CURRENT_DATE = pd.Timestamp('2025-02-13')
   MATURITY_DATE = pd.Timestamp('2025-03-13')
   SPX_PRICE = 6051.0
   RISK_FREE_RATE = 0.04
   ```

### Changing Historical Data Period

Edit the parameters in the script:
```python
rw_results = calculate_real_world_moments(
    start_date='2020-01-01',  # Change this
    end_date='2025-02-13',    # Change this
    freq='monthly',           # or 'weekly', 'daily'
    T_years=T
)
```

### Working Offline

If you can't access Yahoo Finance:
1. Generate sample data: `python create_sample_historical_data.py`
2. The script automatically falls back to sample data

## Interpreting the Output

### Console Output Structure

1. **Part 1**: Options data loading and validation
2. **Part 2**: Risk-neutral moments from options
3. **Part 3**: Real-world moments from historical data
4. **Part 4**: Side-by-side comparison with interpretation

### Visualization

The PDF contains 4 plots:
1. **Distribution curves**: Visual comparison of the two distributions
2. **Mean and Std Dev**: Bar chart comparison
3. **Skewness**: Comparison of asymmetry
4. **Excess Kurtosis**: Comparison of tail behavior

## Troubleshooting

### "No module named 'pandas'"
Install dependencies: `pip install -r requirements.txt`

### "Options data file not found"
Place your CSV file in `./data/` directory or use sample data

### "No data retrieved from yfinance"
The script will automatically use sample data. To generate fresh sample data:
```bash
python create_sample_historical_data.py
```

### Network/DNS errors
Normal in sandboxed environments. Script falls back to sample data automatically.

## Academic Reference

This implementation uses the methodology from:

**Bakshi, G., Kapadia, N., & Madan, D. (2003).** "Stock Return Characteristics, Skew Laws, and the Differential Pricing of Individual Equity Options." *Review of Financial Studies*, 16(1), 101-143.

## File Structure

```
.
├── problem6_distribution_analysis.py    # Main script - START HERE
├── risk_neutral_moments.py              # Risk-neutral calculations
├── real_world_moments.py                # Real-world calculations (online)
├── real_world_moments_offline.py        # Real-world calculations (offline)
├── comparison.py                        # Comparison and visualization
├── create_sample_historical_data.py     # Generate sample data
├── requirements.txt                     # Dependencies
├── README.md                            # Full documentation
├── USAGE.md                             # This file
└── data/
    ├── README.md                        # Data format info
    ├── spx-options-exp-2025-03-13-weekly.csv  # Sample options data
    └── sample_historical_returns.csv    # Sample historical data
```

## Support

For issues or questions, please refer to the main README.md or open an issue on GitHub.
