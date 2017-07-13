import glob as g
import os
import time
from ds9 import *


def setupDs9(ds9_name):
    ds9Set(ds9_name, 'scale mode zscale')
    ds9Set(ds9_name, 'preserve scale yes')
    ds9Set(ds9_name, 'preserve pan yes')
    # set up frames
    ds9Set(ds9_name, 'frame new')
    ds9Set(ds9_name, 'frame new')
    ds9Set(ds9_name, 'frame new')
    ds9Set(ds9_name, 'tile')

startDs9('GOTO')
setupDs9('GOTO')

os.chdir('/data/images/')
nights = g.glob('2017*')
if len(nights) > 0:
    os.chdir(nights[-1])
    old_img_id = ""
    while True:
        imgs = g.glob('*.fits')
        if len(imgs) > 0:
            img_id = imgs[-1].split('_')[0]
            if img_id != old_img_id:
                print('Displaying {}*'.format(img_id))
                # UT1
                ds9Set('GOTO', 'frame 1')
                ds9Display('GOTO', '{}_UT1.fits')
                ds9Set('GOTO', 'zoom to fit')
                # UT2
                ds9Set('GOTO', 'frame 2')
                ds9Display('GOTO', '{}_UT2.fits')
                ds9Set('GOTO', 'zoom to fit')
                # UT3
                #ds9Set('GOTO', 'frame 3')
                #ds9Display('GOTO', '{}_UT3.fits')
                #ds9Set('GOTO', 'zoom to fit')
                # UT4
                ds9Set('GOTO', 'frame 4')
                ds9Display('GOTO', '{}_UT4.fits')
                ds9Set('GOTO', 'zoom to fit')
                old_img_id = img_id
        time.sleep(1)
