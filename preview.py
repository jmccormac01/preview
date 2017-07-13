import glob as g
import os
import time
from collections import OrderedDict
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
            HFD = OrderedDict()
            if len(imgs) > 0:
                img_id = imgs[-1].split('_')[0]
                if img_id != old_img_id:
                    time.sleep(4)
                    print('Displaying {}*'.format(img_id))
                    # loop over UTs
                    for i in range(1, 5):
                        # skip UT3 for now, broken
                        if i != 3:
                            ds9Set('GOTO', 'frame {}'.format(i))
                            ut_img_id = '{}_UT{}.fits'.format(img_id, i)
                            ds9Display('GOTO', ut_img_id)
                            HFD[i] = [measureHfd(ut_img_id)]
                            if img_num == 0:
                                ds9Set('GOTO', 'zoom to fit')
                    for j in HFD:
                        print('{}: {}'.format(j, HFD[j]))
                    old_img_id = img_id
                    img_num += 1
            time.sleep(1)
