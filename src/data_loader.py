import lightkurve as lk
import logging

def download_tess_data(tic_id, sector=None):
    """
    Download TESS light curve data for a given TIC ID.
    
    Args:
        tic_id (str or int): The TESS Input Catalog ID (e.g., 'TIC 261136679').
        sector (int, optional): Specific sector to download. If None, downloads all available.
        
    Returns:
        lightkurve.LightCurveCollection or lightkurve.LightCurve: The downloaded light curve(s).
    """
    search_str = f"TIC {tic_id}"
    logging.info(f"Searching for {search_str}...")
    
    try:
        search_result = lk.search_lightcurve(search_str, mission="TESS", sector=sector, author="SPOC")
        if len(search_result) == 0:
            logging.warning("No SPOC light curves found. Trying QLP...")
            search_result = lk.search_lightcurve(search_str, mission="TESS", sector=sector, author="QLP")
            
        if len(search_result) == 0:
            raise ValueError(f"No light curves found for {search_str}")
            
        logging.info(f"Found {len(search_result)} light curves. Downloading...")
        lc_collection = search_result.download_all()
        return lc_collection
    except Exception as e:
        logging.error(f"Error downloading data: {e}")
        raise
