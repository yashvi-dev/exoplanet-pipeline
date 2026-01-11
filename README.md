# Exoplanet Transit Detection Pipeline

This project implements a pipeline to detect exoplanet transits in TESS light curve data.

## Features
- **Data Acquisition**: Download light curves from the TESS mission using `lightkurve`.
- **Preprocessing**: Remove outliers and detrend stellar variability.
- **Detection**: Use Box Least Squares (BLS) periodogram to find periodic transit signals.
- **Modeling**: Estimate transit parameters (Period, T0, Duration, Depth).
- **Visualization**: Generate plots for raw/processed data and phase-folded transits.

## Installation
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install lightkurve scipy pandas matplotlib astropy
   ```

## Usage
Run the pipeline for a specific TESS Input Catalog (TIC) ID:

```bash
python main.py --tic 261136679
```

(TIC 261136679 is Pi Mensae, a known exoplanet host).

## Output
Results are saved to the `output/` directory:
- `raw_lc.png`: Raw light curve.
- `flat_lc.png`: Detrended light curve.
- `periodogram.png`: BLS power spectrum.
- `folded_lc.png`: Phase-folded light curve at the detected period.

## Science Concepts
- **Transit Photometry**: Detecting the dip in brightness as a planet passes in front of its star.
- **BLS**: An algorithm optimized for finding box-like periodic signals (transits) in time-series data.
