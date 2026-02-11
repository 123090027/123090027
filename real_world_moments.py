"""
Real-World Distribution Moments from Historical Data

This module calculates the mean, standard deviation, skewness, and kurtosis
of log returns under the real-world (physical) probability measure using
historical S&P 500 price data.
"""

import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis
import yfinance as yf


def calculate_real_world_moments(start_date='2020-01-01', end_date='2025-02-13',
                                   freq='monthly', T_years=None):
    """
    Calculate real-world moments from historical S&P 500 data.

    Parameters:
    -----------
    start_date : str
        Start date for historical data (YYYY-MM-DD)
    end_date : str
        End date for historical data (YYYY-MM-DD)
    freq : str
        Frequency of returns: 'daily', 'weekly', or 'monthly'
    T_years : float, optional
        Time horizon in years for annualization. If None, uses the frequency period.

    Returns:
    --------
    dict : Dictionary containing mean, std, skewness, kurtosis
    """

    print(f"\nDownloading S&P 500 historical data from {start_date} to {end_date}...")

    # Download S&P 500 data
    spx = yf.download('^GSPC', start=start_date, end=end_date, progress=False)

    if spx.empty:
        raise ValueError("No data retrieved from yfinance")

    # Resample based on frequency
    if freq == 'monthly':
        spx_resampled = spx['Adj Close'].resample('ME').last()
        period_label = "Monthly"
    elif freq == 'weekly':
        spx_resampled = spx['Adj Close'].resample('W').last()
        period_label = "Weekly"
    else:  # daily
        spx_resampled = spx['Adj Close']
        period_label = "Daily"

    # Calculate log returns
    log_returns = np.log(spx_resampled / spx_resampled.shift(1)).dropna()

    # Calculate moments
    mean_log_return = log_returns.mean()
    std_log_return = log_returns.std()
    skewness_log_return = skew(log_returns)
    kurtosis_log_return = kurtosis(log_returns, fisher=True)  # Excess kurtosis

    # If T_years is provided, annualize/scale to that horizon
    if T_years is not None:
        if freq == 'monthly':
            periods_per_year = 12
        elif freq == 'weekly':
            periods_per_year = 52
        else:  # daily
            periods_per_year = 252

        n_periods = T_years * periods_per_year

        # Scale mean and std
        mean_scaled = mean_log_return * n_periods
        std_scaled = std_log_return * np.sqrt(n_periods)

        results = {
            'mean': mean_log_return,
            'std': std_log_return,
            'skewness': skewness_log_return,
            'kurtosis': kurtosis_log_return,
            'mean_scaled': mean_scaled,
            'std_scaled': std_scaled,
            'freq': freq,
            'period_label': period_label,
            'n_observations': len(log_returns),
            'start_date': log_returns.index[0].strftime('%Y-%m-%d'),
            'end_date': log_returns.index[-1].strftime('%Y-%m-%d'),
            'T_years': T_years
        }
    else:
        results = {
            'mean': mean_log_return,
            'std': std_log_return,
            'skewness': skewness_log_return,
            'kurtosis': kurtosis_log_return,
            'freq': freq,
            'period_label': period_label,
            'n_observations': len(log_returns),
            'start_date': log_returns.index[0].strftime('%Y-%m-%d'),
            'end_date': log_returns.index[-1].strftime('%Y-%m-%d')
        }

    return results


def print_real_world_results(results):
    """Print the real-world distribution moments."""
    print("\n" + "="*70)
    print("REAL-WORLD DISTRIBUTION MOMENTS")
    print("="*70)
    print(f"Data Frequency                 : {results['period_label']}")
    print(f"Number of Observations         : {results['n_observations']}")
    print(f"Start Date                     : {results['start_date']}")
    print(f"End Date                       : {results['end_date']}")
    print("-"*70)
    print(f"Mean of ln(S_T/S_t)            : {results['mean']:.6f}")
    print(f"Std Dev of ln(S_T/S_t)         : {results['std']:.6f}")
    print(f"Skewness                       : {results['skewness']:.6f}")
    print(f"Excess Kurtosis                : {results['kurtosis']:.6f}")

    if 'T_years' in results and results['T_years'] is not None:
        print("-"*70)
        print(f"Scaled to T = {results['T_years']:.4f} years:")
        print(f"Mean (scaled)                  : {results['mean_scaled']:.6f}")
        print(f"Std Dev (scaled)               : {results['std_scaled']:.6f}")

    print("="*70)
