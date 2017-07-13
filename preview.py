import os
import time
from collections import OrderedDict
import glob as g
from ds9 import (
    setupDs9,
    ds9Set,
    ds9Display
    )
from pes import measureHfd

if __name__ == "__main__":
    # set up a new DS9 session
    setupDs9('GOTO')
    # go to the data directory
    os.chdir('/data/images/')
    nights = g.glob('2017*')
    # if there are nights in there, continue
    if len(nights) > 0:
        # most recent night
        os.chdir(nights[-1])
        old_img_id = ""
        img_num = 0
        # loop forever getting list of images each time
        while True:
            imgs = g.glob('*.fits')
            # store the HFDs for each round
            HFD = OrderedDict()
            if len(imgs) > 0:
                # get the image prefix
                img_id = imgs[-1].split('_')[0]
                # if new images, do stuff, if not, dont't
                if img_id != old_img_id:
                    # wait for a few sec for files to finish writing
                    time.sleep(4)
                    # loop over UTs
                    for i in range(1, 5):
                        # skip UT3 for now, broken
                        if i != 3:
                            # activate UT DS9 frame
                            ds9Set('GOTO', 'frame {}'.format(i))
                            # display the UT's image, if it exists
                            ut_img_id = '{}_UT{}.fits'.format(img_id, i)
                            res = ds9Display('GOTO', ut_img_id)
                            # if it existed, do some stats
                            if res:
                                HFD[i] = [measureHfd(ut_img_id)]
                                if img_num == 0:
                                    ds9Set('GOTO', 'zoom to fit')
                    # print a stats summary
                    out_str = "{} ".format(img_id)
                    for j in HFD:
                        out_str = out_str + "{}: {:.3f} {:.3f} ".format(j,
                                                                       HFD[j][0][0],
                                                                       HFD[j][0][1])
                    print(out_str)
                    old_img_id = img_id
                    img_num += 1
            time.sleep(1)
