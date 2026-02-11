"""
Comparison and Visualization of Risk-Neutral vs Real-World Distributions

This module provides functions to compare and visualize the distributional
properties under risk-neutral and real-world probability measures.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm


def compare_distributions(rn_results, rw_results):
    """
    Compare risk-neutral and real-world distribution moments.

    Parameters:
    -----------
    rn_results : dict
        Risk-neutral moments from risk_neutral_moments.py
    rw_results : dict
        Real-world moments from real_world_moments.py

    Returns:
    --------
    pd.DataFrame : Comparison table
    """

    # Determine which real-world mean and std to use
    if 'mean_scaled' in rw_results:
        rw_mean = rw_results['mean_scaled']
        rw_std = rw_results['std_scaled']
        rw_label = f"Real-World (scaled to T={rw_results['T_years']:.4f}y)"
    else:
        rw_mean = rw_results['mean']
        rw_std = rw_results['std']
        rw_label = f"Real-World ({rw_results['period_label']})"

    comparison = pd.DataFrame({
        'Metric': ['Mean', 'Std Dev', 'Skewness', 'Excess Kurtosis'],
        'Risk-Neutral': [
            rn_results['mean'],
            rn_results['std'],
            rn_results['skewness'],
            rn_results['kurtosis']
        ],
        rw_label: [
            rw_mean,
            rw_std,
            rw_results['skewness'],
            rw_results['kurtosis']
        ]
    })

    # Calculate differences
    comparison['Difference'] = comparison['Risk-Neutral'] - comparison[rw_label]
    comparison['Relative Diff (%)'] = (comparison['Difference'] / comparison[rw_label].abs() * 100)

    return comparison


def print_comparison_table(comparison_df):
    """Print formatted comparison table."""
    print("\n" + "="*90)
    print("COMPARISON: RISK-NEUTRAL vs REAL-WORLD DISTRIBUTION")
    print("="*90)
    print(comparison_df.to_string(index=False))
    print("="*90)


def plot_distribution_comparison(rn_results, rw_results, save_path='distribution_comparison.pdf'):
    """
    Plot comparison of risk-neutral and real-world distributions.

    Parameters:
    -----------
    rn_results : dict
        Risk-neutral moments
    rw_results : dict
        Real-world moments
    save_path : str
        Path to save the plot
    """

    # Create a range of returns for plotting
    rn_mean = rn_results['mean']
    rn_std = rn_results['std']

    # Use scaled values if available
    if 'mean_scaled' in rw_results:
        rw_mean = rw_results['mean_scaled']
        rw_std = rw_results['std_scaled']
        rw_label = f"Real-World (scaled to T={rw_results['T_years']:.4f}y)"
    else:
        rw_mean = rw_results['mean']
        rw_std = rw_results['std']
        rw_label = f"Real-World ({rw_results['period_label']})"

    # Generate x-axis (log returns)
    x_min = min(rn_mean - 4*rn_std, rw_mean - 4*rw_std)
    x_max = max(rn_mean + 4*rn_std, rw_mean + 4*rw_std)
    x = np.linspace(x_min, x_max, 1000)

    # For visualization, we approximate using normal distributions
    # (Note: actual distributions may have different skewness and kurtosis)
    rn_pdf = norm.pdf(x, loc=rn_mean, scale=rn_std)
    rw_pdf = norm.pdf(x, loc=rw_mean, scale=rw_std)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Distribution curves
    ax1 = axes[0, 0]
    ax1.plot(x, rn_pdf, 'b-', linewidth=2, label='Risk-Neutral', alpha=0.8)
    ax1.plot(x, rw_pdf, 'r-', linewidth=2, label=rw_label, alpha=0.8)
    ax1.axvline(rn_mean, color='b', linestyle='--', alpha=0.5, linewidth=1)
    ax1.axvline(rw_mean, color='r', linestyle='--', alpha=0.5, linewidth=1)
    ax1.set_xlabel('Log Return ln(S_T/S_t)', fontsize=11)
    ax1.set_ylabel('Probability Density', fontsize=11)
    ax1.set_title('Distribution Comparison (Normal Approximation)', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)

    # Plot 2: Mean and Std Dev comparison
    ax2 = axes[0, 1]
    metrics = ['Mean', 'Std Dev']
    rn_values = [rn_mean, rn_std]
    rw_values = [rw_mean, rw_std]
    x_pos = np.arange(len(metrics))
    width = 0.35

    ax2.bar(x_pos - width/2, rn_values, width, label='Risk-Neutral', color='blue', alpha=0.7)
    ax2.bar(x_pos + width/2, rw_values, width, label=rw_label, color='red', alpha=0.7)
    ax2.set_ylabel('Value', fontsize=11)
    ax2.set_title('Mean and Standard Deviation', fontsize=12, fontweight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(metrics)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3, axis='y')

    # Plot 3: Skewness comparison
    ax3 = axes[1, 0]
    skew_metrics = ['Skewness']
    rn_skew = [rn_results['skewness']]
    rw_skew = [rw_results['skewness']]

    x_pos = np.arange(len(skew_metrics))
    ax3.bar(x_pos - width/2, rn_skew, width, label='Risk-Neutral', color='blue', alpha=0.7)
    ax3.bar(x_pos + width/2, rw_skew, width, label=rw_label, color='red', alpha=0.7)
    ax3.axhline(y=0, color='k', linestyle='-', linewidth=0.8)
    ax3.set_ylabel('Skewness', fontsize=11)
    ax3.set_title('Skewness Comparison', fontsize=12, fontweight='bold')
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(skew_metrics)
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3, axis='y')

    # Plot 4: Kurtosis comparison
    ax4 = axes[1, 1]
    kurt_metrics = ['Excess Kurtosis']
    rn_kurt = [rn_results['kurtosis']]
    rw_kurt = [rw_results['kurtosis']]

    x_pos = np.arange(len(kurt_metrics))
    ax4.bar(x_pos - width/2, rn_kurt, width, label='Risk-Neutral', color='blue', alpha=0.7)
    ax4.bar(x_pos + width/2, rw_kurt, width, label=rw_label, color='red', alpha=0.7)
    ax4.axhline(y=0, color='k', linestyle='-', linewidth=0.8)
    ax4.set_ylabel('Excess Kurtosis', fontsize=11)
    ax4.set_title('Excess Kurtosis Comparison', fontsize=12, fontweight='bold')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(kurt_metrics)
    ax4.legend(fontsize=10)
    ax4.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"\nPlot saved to: {save_path}")
    plt.show()


def generate_interpretation(comparison_df):
    """
    Generate interpretation of the comparison results.

    Parameters:
    -----------
    comparison_df : pd.DataFrame
        Comparison table

    Returns:
    --------
    str : Interpretation text
    """

    interpretation = "\n" + "="*90 + "\n"
    interpretation += "INTERPRETATION OF RESULTS\n"
    interpretation += "="*90 + "\n\n"

    mean_diff = comparison_df[comparison_df['Metric'] == 'Mean']['Difference'].values[0]
    skew_rn = comparison_df[comparison_df['Metric'] == 'Skewness']['Risk-Neutral'].values[0]
    kurt_rn = comparison_df[comparison_df['Metric'] == 'Excess Kurtosis']['Risk-Neutral'].values[0]

    # Mean interpretation
    interpretation += "1. MEAN (Expected Return):\n"
    if mean_diff < 0:
        interpretation += f"   - Risk-neutral mean ({mean_diff:.6f}) is LOWER than real-world mean\n"
        interpretation += "   - This reflects the RISK PREMIUM: investors demand higher expected returns\n"
        interpretation += "     in the real world to compensate for bearing equity risk\n"
    else:
        interpretation += f"   - Risk-neutral mean ({mean_diff:.6f}) is HIGHER than real-world mean\n"

    interpretation += "\n2. VOLATILITY (Standard Deviation):\n"
    interpretation += "   - Volatility differences reflect market expectations vs historical behavior\n"
    interpretation += "   - Risk-neutral volatility is forward-looking (implied from options)\n"
    interpretation += "   - Real-world volatility is backward-looking (historical data)\n"

    interpretation += "\n3. SKEWNESS:\n"
    if skew_rn < 0:
        interpretation += f"   - Risk-neutral skewness ({skew_rn:.6f}) is NEGATIVE\n"
        interpretation += "   - This indicates LEFT TAIL RISK (crash risk)\n"
        interpretation += "   - Investors pay premium for downside protection (put options)\n"
        interpretation += "   - Reflects market's fear of large negative movements\n"
    else:
        interpretation += f"   - Risk-neutral skewness ({skew_rn:.6f}) is POSITIVE\n"

    interpretation += "\n4. KURTOSIS:\n"
    if kurt_rn > 0:
        interpretation += f"   - Risk-neutral excess kurtosis ({kurt_rn:.6f}) is POSITIVE\n"
        interpretation += "   - Distribution has FATTER TAILS than normal distribution\n"
        interpretation += "   - Indicates higher probability of extreme events\n"
        interpretation += "   - Market prices in tail risk through options\n"
    else:
        interpretation += f"   - Risk-neutral excess kurtosis ({kurt_rn:.6f}) is NEGATIVE\n"
        interpretation += "   - Distribution has THINNER TAILS than normal distribution\n"

    interpretation += "\n5. KEY INSIGHTS:\n"
    interpretation += "   - Risk-neutral measure reflects MARKET EXPECTATIONS and RISK AVERSION\n"
    interpretation += "   - Real-world measure reflects ACTUAL HISTORICAL BEHAVIOR\n"
    interpretation += "   - Differences reveal RISK PREMIUMS and MARKET SENTIMENT\n"
    interpretation += "   - Options market incorporates forward-looking information\n"

    interpretation += "\n" + "="*90 + "\n"

    return interpretation
