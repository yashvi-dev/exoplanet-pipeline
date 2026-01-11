import numpy as np
import lightkurve as lk

def clean_lightcurve(lc):
    """
    Remove NaNs, outliers, and normalize the light curve.
    
    Args:
        lc (lightkurve.LightCurve): Input light curve.
        
    Returns:
        lightkurve.LightCurve: Cleaned light curve.
    """
    # Remove NaN flux values
    lc = lc.remove_nans()
    
    # Remove outliers using basic sigma clipping
    lc = lc.remove_outliers(sigma=5)
    
    return lc

def detrend_lightcurve(lc, window_length_days=0.5):
    """
    Remove stellar variability using the flatten method (Savitzky-Golay filter).
    
    Args:
        lc (lightkurve.LightCurve): Input light curve.
        window_length_days (float): Window length in days for the detrender.
        
    Returns:
        lightkurve.LightCurve: Flattened (detrended) light curve.
    """
    # Convert window length to number of cadences (approximately)
    # TESS cadence is usually 2 min or 30 mins. Lightkurve handles units if passed correctly,
    # but flatten takes window_length in POINTS, not time, usually, unless we use units.
    # Actually lc.flatten(window_length=...) takes integer points.
    # We need to estimate points.
    
    # Estimate cadence
    if len(lc) > 1:
        cadence_days = np.nanmedian(np.diff(lc.time.value))
        window_length = int(window_length_days / cadence_days)
        # Ensure odd
        if window_length % 2 == 0:
            window_length += 1
    else:
        window_length = 101 # Fallback
        
    return lc.flatten(window_length=window_length)
