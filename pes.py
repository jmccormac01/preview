"""
Code to measure image stats
"""
import numpy as np
import sep
from astropy.io import fits
from astropy.stats.sigma_clipping import sigma_clipped_stats

def measureHfd(img):
    data = fits.open(img)[0].data
    y, x = data.shape
    xcen = int(x/2)
    ycen = int(y/2)
    # grab the middle 2k x 2k
    stats_area = np.array(data[ycen-1024: ycen+1024, \
                               xcen-1024: xcen+1024]).astype(np.int32).copy(order='C')
    bkg = sep.Background(stats_area)
    thresh = 3 * bkg.globalrms
    objects = sep.extract(stats_area-bkg, thresh)
    # taken from g-tecs autoFocus.py
    hfr, mask = sep.flux_radius(stats_area,
                                objects['x'],
                                objects['y'],
                                30*np.ones_like(objects['x']),
                                0.5,
                                normflux=objects['cflux'])
    mask = np.logical_and(mask == 0, objects['peak'] < 40000)
    hfd = 2*hfr[mask]
    if hfd.size > 3:
        mean, median, std = sigma_clipped_stats(hfd, sigma=2.5, iters=10)
        return median, std
    return 0.0, 0.0




