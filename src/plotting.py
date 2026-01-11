import matplotlib.pyplot as plt
import numpy as np

def plot_lightcurve(time, flux, title="Light Curve", filename=None):
    """Plot a simple light curve."""
    plt.figure(figsize=(10, 5))
    plt.scatter(time, flux, s=1, c='k', alpha=0.5)
    plt.title(title)
    plt.xlabel("Time (BJD - 2457000)")
    plt.ylabel("Normalized Flux")
    if filename:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()

def plot_periodogram(periodogram, title="BLS Periodogram", filename=None):
    """Plot the BLS power spectrum."""
    plt.figure(figsize=(10, 5))
    plt.plot(periodogram.period, periodogram.power, c='k', lw=1)
    plt.title(title)
    plt.xlabel("Period (days)")
    plt.ylabel("Power")
    
    # Mark best peak
    best_period = periodogram.period_at_max_power
    max_power = periodogram.max_power
    plt.axvline(best_period.value, color='r', linestyle='--', alpha=0.5, label=f"Best Period: {best_period.value:.4f} d")
    plt.legend()
    
    if filename:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()

def plot_folded(folded_lc, model_lc=None, title="Folded Light Curve", filename=None):
    """Plot phase-folded light curve."""
    plt.figure(figsize=(10, 5))
    plt.scatter(folded_lc.time.value, folded_lc.flux.value, s=1, c='k', alpha=0.5, label="Data")
    
    if model_lc:
        # If we had a model, we'd plot it here. 
        # For now, just plotting data.
        pass
        
    plt.title(title)
    plt.xlabel("Phase")
    plt.ylabel("Normalized Flux")
    
    if filename:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()
