# S&P 500 Distribution Analysis - Problem 6

This repository contains the solution to Problem 6: Extract and compare the distributional properties of S&P 500 log returns under risk-neutral and real-world probability measures.

## Problem Statement

Extract mean, standard deviation, skewness, and kurtosis of the log returns of the S&P 500 index `ln(S_T/S_t)` (with T being the maturity date of the option and t being the current date) under:
1. **Risk-neutral probability measure** (from options data)
2. **Real-world probability measure** (from historical monthly returns)

Compare the distributional properties between the two measures.

## Repository Structure

```
.
├── problem6_distribution_analysis.py   # Main script
├── risk_neutral_moments.py             # Risk-neutral moment calculations
├── real_world_moments.py               # Real-world moment calculations
├── comparison.py                       # Comparison and visualization
├── requirements.txt                    # Python dependencies
├── data/
│   ├── README.md                       # Data directory info
│   └── spx-options-exp-2025-03-13-weekly.csv  # Options data
└── README.md                           # This file
```

## Installation

1. Clone the repository
2. Install required packages:

```bash
pip install -r requirements.txt
```

Required packages:
- pandas
- numpy
- scipy
- matplotlib
- yfinance

## Usage

### Basic Usage

Simply run the main script:

```bash
python problem6_distribution_analysis.py
```

This will:
1. Load S&P 500 options data from `./data/spx-options-exp-2025-03-13-weekly.csv`
2. Calculate risk-neutral distribution moments from options
3. Download historical S&P 500 data and calculate real-world moments
4. Compare the two distributions
5. Generate visualizations and save results

### Expected Output

The script generates:
1. **Console output**: Detailed results and interpretation
2. **comparison_results.csv**: Side-by-side comparison table
3. **detailed_results.csv**: Detailed results with data sources
4. **distribution_comparison.pdf**: Visual comparison plots

## Data Requirements

### Options Data

Place the S&P 500 options data file in the `./data/` directory. The CSV file should have the following columns:

- `Type`: "Call" or "Put"
- `Strike`: Strike price
- `Bid`: Bid price
- `Mid`: Mid price (or average of bid and ask)
- `Ask`: Ask price
- `IV`: Implied volatility (as decimal or percentage)
- `Delta`: Option delta
- `Volume`: Trading volume
- `Open Int`: Open interest

Sample data is included for testing purposes.

### Historical Data

Historical S&P 500 data is automatically downloaded from Yahoo Finance using the `yfinance` library. No manual data collection is needed.

## Methodology

### Risk-Neutral Distribution

The risk-neutral moments are extracted using the **Bakshi, Kapadia, and Madan (2003)** method, which uses out-of-the-money (OTM) option prices to compute:

1. **Mean**: E^Q[ln(S_T/S_t)]
2. **Variance**: Var^Q[ln(S_T/S_t)]
3. **Skewness**: Calculated from third moment
4. **Kurtosis**: Calculated from fourth moment

Key steps:
- Calculate forward price from put-call parity
- Filter for OTM options with good liquidity
- Integrate option prices across strikes
- Extract moments from the integrals

### Real-World Distribution

The real-world moments are calculated from historical S&P 500 monthly returns:

1. Download historical data using yfinance
2. Calculate log returns: ln(S_t / S_{t-1})
3. Compute sample moments
4. Scale to match the option's time horizon

## Key Insights

The comparison reveals important differences between market expectations (risk-neutral) and historical behavior (real-world):

1. **Mean**: Risk-neutral mean is typically lower due to the equity risk premium
2. **Volatility**: Forward-looking (options) vs backward-looking (historical)
3. **Skewness**: Negative skewness in options reflects crash risk premium
4. **Kurtosis**: Fat tails in options indicate extreme event pricing

## Configuration

You can modify the following parameters in `problem6_distribution_analysis.py`:

```python
# Market parameters
CURRENT_DATE = pd.Timestamp('2025-02-13')
MATURITY_DATE = pd.Timestamp('2025-03-13')
SPX_PRICE = 6051.0
RISK_FREE_RATE = 0.04

# Historical data parameters (in real_world_moments.py)
start_date='2020-01-01'
end_date='2025-02-13'
freq='monthly'  # or 'daily', 'weekly'
```

## Academic Reference

This implementation is based on the methodology from:

**Bakshi, G., Kapadia, N., & Madan, D. (2003).** "Stock Return Characteristics, Skew Laws, and the Differential Pricing of Individual Equity Options." *Review of Financial Studies*, 16(1), 101-143.

## Troubleshooting

### Missing Data File

If you get an error about missing data file:
1. Ensure the CSV file is in the `./data/` directory
2. Check that the filename matches: `spx-options-exp-2025-03-13-weekly.csv`
3. Verify the CSV has the required columns

### Network Issues

If yfinance fails to download data:
1. Check your internet connection
2. Try running the script again (sometimes Yahoo Finance has temporary issues)
3. Consider using a proxy if behind a firewall

### Import Errors

If you get import errors:
```bash
pip install --upgrade -r requirements.txt
```

## License

This code is provided for educational purposes.

## Contact

For questions or issues, please open an issue on GitHub.
