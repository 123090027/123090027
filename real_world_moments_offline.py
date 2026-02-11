"""
Alternative real-world moments calculation that can use cached/sample data
"""

import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis
import os


def calculate_real_world_moments_from_file(filepath, T_years=None):
    """
    Calculate real-world moments from a pre-saved CSV file containing log returns.

    Parameters:
    -----------
    filepath : str
        Path to CSV file with columns: Date, Log_Return
    T_years : float, optional
        Time horizon in years for scaling

    Returns:
    --------
    dict : Dictionary containing mean, std, skewness, kurtosis
    """

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Historical data file not found: {filepath}")

    # Load data
    data = pd.read_csv(filepath)
    log_returns = data['Log_Return'].values

    # Calculate moments
    mean_log_return = log_returns.mean()
    std_log_return = log_returns.std()
    skewness_log_return = skew(log_returns)
    kurtosis_log_return = kurtosis(log_returns, fisher=True)  # Excess kurtosis

    # Assuming monthly data
    freq = 'monthly'
    period_label = "Monthly"
    periods_per_year = 12

    # If T_years is provided, scale to that horizon
    if T_years is not None:
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
            'start_date': data['Date'].iloc[0] if 'Date' in data.columns else 'N/A',
            'end_date': data['Date'].iloc[-1] if 'Date' in data.columns else 'N/A',
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
            'start_date': data['Date'].iloc[0] if 'Date' in data.columns else 'N/A',
            'end_date': data['Date'].iloc[-1] if 'Date' in data.columns else 'N/A'
        }

    return results
