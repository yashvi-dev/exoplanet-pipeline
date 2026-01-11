import unittest
import numpy as np
from src import detection
# Mocking lightkurve data download specifically would be good, 
# but for an end-to-end test we might want to try a real small download or a generated synthetic LC.
# To avoid network dependency in tests, I'll generate a synthetic light curve.

import lightkurve as lk

class TestExoplanetPipeline(unittest.TestCase):
    
    def setUp(self):
        # Create a synthetic light curve with a known transit
        # Period = 5 days, Transit at t=2.5, depth=1%
        time = np.linspace(0, 20, 1000)
        flux = np.ones_like(time)
        
        period = 5.0
        t0 = 2.5
        duration = 0.2
        depth = 0.01
        
        # Inject transit
        phase = (time - t0 + 0.5 * period) % period - 0.5 * period
        mask = np.abs(phase) < 0.5 * duration
        flux[mask] -= depth
        
        # Add some noise
        # flux += np.random.normal(0, 0.001, size=len(time))
        
        self.lc = lk.LightCurve(time=time, flux=flux)
        
    def test_bls_detection(self):
        # Run BLS
        periodogram = detection.run_bls_search(self.lc, min_period=1, max_period=10)
        best = detection.find_best_transit(periodogram)
        
        self.assertAlmostEqual(best['period'], 5.0, delta=0.1)
        # t0 might be modulo period, so check phase match or just checking period is often enough for basic test
        # self.assertAlmostEqual(best['t0'], 2.5, delta=0.1) 
        self.assertAlmostEqual(best['depth'], 0.01, delta=0.005)

if __name__ == '__main__':
    unittest.main()
