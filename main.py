import argparse
import sys
import os
import logging
from src import data_loader, preprocessing, detection, modeling, plotting

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Exoplanet Transit Detection Pipeline")
    parser.add_argument("--tic", type=str, required=True, help="TESS Input Catalog ID (e.g., 261136679)")
    parser.add_argument("--sector", type=int, default=None, help="TESS Sector to download")
    parser.add_argument("--out", type=str, default="output", help="Output directory for plots")
    
    args = parser.parse_args()
    
    # Create output dir
    os.makedirs(args.out, exist_ok=True)
    
    logging.info("Starting pipeline...")
    
    # 1. Download
    try:
        lcs = data_loader.download_tess_data(args.tic, sector=args.sector)
        # Stitch if multiple sectors (simple stitch for now)
        if hasattr(lcs, 'stitch'):
             lc = lcs.stitch()
        else:
             lc = lcs[0] # Take first if collection but not switchable (rare with download_all)
             
        logging.info("Data downloaded and stitched.")
    except Exception as e:
        logging.error(f"Failed to load data: {e}")
        return

    # 2. Preprocess
    lc_clean = preprocessing.clean_lightcurve(lc)
    lc_flat = preprocessing.detrend_lightcurve(lc_clean)
    
    # Plot Raw vs Flat
    plotting.plot_lightcurve(lc.time.value, lc.flux.value, title="Raw Light Curve", filename=os.path.join(args.out, "raw_lc.png"))
    plotting.plot_lightcurve(lc_flat.time.value, lc_flat.flux.value, title="Detrended Light Curve", filename=os.path.join(args.out, "flat_lc.png"))
    logging.info("Preprocessing complete.")
    
    # 3. Detection (BLS)
    periodogram = detection.run_bls_search(lc_flat)
    plotting.plot_periodogram(periodogram, filename=os.path.join(args.out, "periodogram.png"))
    
    best_params = detection.find_best_transit(periodogram)
    logging.info(f"Detection results: {best_params}")
    
    # 4. Modeling / Folding
    folded_lc, params = modeling.fit_transit_model(lc_flat, best_params['period'], best_params['t0'], best_params['duration'])
    plotting.plot_folded(folded_lc, title=f"Folded (P={best_params['period']:.4f} d)", filename=os.path.join(args.out, "folded_lc.png"))
    
    logging.info(f"Pipeline finished. Results in {args.out}/")

if __name__ == "__main__":
    main()
