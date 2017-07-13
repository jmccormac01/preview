import glob as g
import os
import time
from ds9 import (
    setupDs9,
    ds9Set,
    ds9Display
    )
from pes import measureHfd

if __name__ == "__main__":
    setupDs9('GOTO')
    os.chdir('/data/images/')
    nights = g.glob('2017*')
    if len(nights) > 0:
        os.chdir(nights[-1])
        old_img_id = ""
        img_num = 0
        while True:
            imgs = g.glob('*.fits')
            if len(imgs) > 0:
                img_id = imgs[-1].split('_')[0]
                if img_id != old_img_id:
                    time.sleep(4)
                    print('Displaying {}*'.format(img_id))
                    # UT1
                    ds9Set('GOTO', 'frame 1')
                    ut1_img_id = '{}_UT1.fits'.format(img_id)
                    ds9Display('GOTO', ut1_img_id)
                    if img_num == 0:
                        ds9Set('GOTO', 'zoom to fit')
                    ut1_hfd, ut1_std = measureHfd(ut1_img_id)
                    print('UT1: {} {}'.format(ut1_hfd, ut1_std))
                    # UT2
                    ds9Set('GOTO', 'frame 2')
                    ds9Display('GOTO', '{}_UT2.fits'.format(img_id))
                    if img_num == 0:
                        ds9Set('GOTO', 'zoom to fit')
                    # UT3
                    #ds9Set('GOTO', 'frame 3')
                    #ds9Display('GOTO', '{}_UT3.fits'.format(img_id))
                    #if img_num == 0:
                    #   ds9Set('GOTO', 'zoom to fit')
                    # UT4
                    ds9Set('GOTO', 'frame 4')
                    ds9Display('GOTO', '{}_UT4.fits'.format(img_id))
                    if img_num == 0:
                        ds9Set('GOTO', 'zoom to fit')
                    old_img_id = img_id
                    img_num += 1
            time.sleep(1)
