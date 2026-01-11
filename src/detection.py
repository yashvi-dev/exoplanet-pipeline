import numpy as np
import lightkurve as lk
import logging
import astropy.units as u

def run_bls_search(lc, min_period=0.5, max_period=20, duration=np.linspace(0.05, 0.3, 10)):
    """
    Run Box Least Squares (BLS) periodogram search.
    
    Args:
        lc (lightkurve.LightCurve): Detrended light curve.
        min_period (float): Minimum period to search (days).
        max_period (float): Maximum period to search (days).
    
    Returns:
        lightkurve.periodogram.BoxLeastSquaresPeriodogram: The computed periodogram.
    """
    logging.info(f"Running BLS search from {min_period} to {max_period} days...")
    # Create periodogram
    periodogram = lc.to_periodogram(method='bls', period=np.linspace(min_period, max_period, 10000), duration=duration)
    return periodogram

def find_best_transit(periodogram):
    """
    Identify the most significant transit signal.
    
    Args:
        periodogram: BLS periodogram.
        
    Returns:
        dict: Parameters of the best fit (period, t0, duration, depth, snr).
    """
    best_period = periodogram.period_at_max_power
    best_t0 = periodogram.transit_time_at_max_power
    best_duration = periodogram.duration_at_max_power
    best_depth = periodogram.depth_at_max_power
    max_power = periodogram.max_power
    
    logging.info(f"Best Period: {best_period:.4f} d, t0: {best_t0.value:.4f}, Depth: {best_depth:.4f}")
    
    return {
        "period": best_period.value,
        "t0": best_t0.value,
        "duration": best_duration.value,
        "depth": best_depth.value,
        "power": max_power.value
    }
