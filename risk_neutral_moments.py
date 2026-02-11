"""
Risk-Neutral Distribution Moments from Options Data

This module calculates the mean, standard deviation, skewness, and kurtosis
of log returns under the risk-neutral probability measure using S&P 500 options data.

The method is based on Bakshi, Kapadia, and Madan (2003) which uses option prices
to extract moments of the risk-neutral distribution.
"""

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d, UnivariateSpline
from scipy.integrate import simpson, trapezoid


def calculate_risk_neutral_moments(options_data, spx_price, T, r=0.04):
    """
    Calculate risk-neutral moments from options data.

    Parameters:
    -----------
    options_data : pd.DataFrame
        Options data with columns: Strike, Mid, Type, IV, Volume, Open Int
    spx_price : float
        Current S&P 500 index level
    T : float
        Time to maturity in years
    r : float
        Risk-free rate

    Returns:
    --------
    dict : Dictionary containing mean, std, skewness, kurtosis
    """

    # Separate calls and puts
    calls = options_data[options_data['Type'] == 'Call'].copy()
    puts = options_data[options_data['Type'] == 'Put'].copy()

    # Filter for liquid options (Volume > 0 and Open Interest > 0)
    calls = calls[(calls['Volume'] > 0) & (calls['Open Int'] > 0)].copy()
    puts = puts[(puts['Volume'] > 0) & (puts['Open Int'] > 0)].copy()

    # Find common strikes
    common_strikes = np.intersect1d(calls['Strike'].values, puts['Strike'].values)

    # Find ATM strike and calculate forward price
    atm_strike = common_strikes[np.argmin(np.abs(common_strikes - spx_price))]
    c_atm = calls[calls['Strike'] == atm_strike]['Mid'].values[0]
    p_atm = puts[puts['Strike'] == atm_strike]['Mid'].values[0]
    F = atm_strike + np.exp(r * T) * (c_atm - p_atm)

    print(f"Forward Price F: {F:.2f}")
    print(f"ATM Strike K₀: {atm_strike:.2f}")

    # Filter OTM options
    otm_puts = puts[puts['Strike'] <= F].copy()
    otm_calls = calls[calls['Strike'] > F].copy()

    # Combine OTM options
    otm_chain = pd.concat([otm_puts, otm_calls], ignore_index=True).sort_values('Strike').reset_index(drop=True)

    # Calculate the moments using Bakshi-Kapadia-Madan method
    exp_rt = np.exp(r * T)

    # Calculate V(K) - the integral component
    def calculate_v_k(K_values, Q_values, r, T):
        """Calculate V(K) = ∫ max(0, K-K_i) * Q(K_i) dK_i"""
        exp_rt = np.exp(r * T)
        v_k = np.zeros_like(K_values, dtype=float)

        for i, K in enumerate(K_values):
            # Integrate over all strikes less than K
            mask = K_values < K
            if np.any(mask):
                integrand = (K - K_values[mask]) * Q_values[mask] * exp_rt
                # Use trapezoidal integration
                v_k[i] = trapezoid(integrand, K_values[mask])

        return v_k

    # Extract strikes and option prices
    K = otm_chain['Strike'].values
    Q = otm_chain['Mid'].values

    # Calculate integrals for moments
    # μ_Q = exp(rT) - 1 - (exp(rT)/2) * ∫ (1/K²) * Q(K) dK
    integral_0 = trapezoid(Q / (K**2), K)
    mu_Q = exp_rt - 1 - (exp_rt / 2) * integral_0

    # σ²_Q = exp(rT) * ∫ (1/K²) * Q(K) dK - (μ_Q)²
    sigma2_Q = exp_rt * integral_0 - mu_Q**2

    # For skewness and kurtosis, we need higher order moments
    # W = exp(rT) * ∫ (6*ln(K/F) - 3*ln²(K/F)) * (1/K²) * Q(K) dK
    ln_ratio = np.log(K / F)
    integrand_W = (6 * ln_ratio - 3 * ln_ratio**2) * Q / (K**2)
    W = exp_rt * trapezoid(integrand_W, K)

    # X = exp(rT) * ∫ (12*ln²(K/F) - 4*ln³(K/F)) * (1/K²) * Q(K) dK
    integrand_X = (12 * ln_ratio**2 - 4 * ln_ratio**3) * Q / (K**2)
    X = exp_rt * trapezoid(integrand_X, K)

    # Calculate skewness
    skewness_Q = (W - 3 * mu_Q * sigma2_Q - mu_Q**3) / (sigma2_Q**(3/2))

    # Calculate kurtosis (excess kurtosis)
    kurtosis_Q = (X - 4 * W * mu_Q + 6 * sigma2_Q * mu_Q**2 + 3 * mu_Q**4) / (sigma2_Q**2) - 3

    # Convert to log return moments
    # E[ln(S_T/S_t)] ≈ μ_Q - σ²_Q/2
    mean_log_return = mu_Q - sigma2_Q / 2
    std_log_return = np.sqrt(sigma2_Q)

    results = {
        'mean': mean_log_return,
        'std': std_log_return,
        'skewness': skewness_Q,
        'kurtosis': kurtosis_Q,
        'forward_price': F,
        'atm_strike': atm_strike,
        'num_options': len(otm_chain)
    }

    return results


def print_risk_neutral_results(results):
    """Print the risk-neutral distribution moments."""
    print("\n" + "="*70)
    print("RISK-NEUTRAL DISTRIBUTION MOMENTS")
    print("="*70)
    print(f"Forward Price (F)              : {results['forward_price']:.2f}")
    print(f"ATM Strike (K₀)                : {results['atm_strike']:.2f}")
    print(f"Number of OTM Options Used     : {results['num_options']}")
    print("-"*70)
    print(f"Mean of ln(S_T/S_t)            : {results['mean']:.6f}")
    print(f"Std Dev of ln(S_T/S_t)         : {results['std']:.6f}")
    print(f"Skewness                       : {results['skewness']:.6f}")
    print(f"Excess Kurtosis                : {results['kurtosis']:.6f}")
    print("="*70)
