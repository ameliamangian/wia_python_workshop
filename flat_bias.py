#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 10:48:49 2018

@author: johnmangian
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from astropy.io import fits

field_d = fits.getdata('DECam_00380036_09.fits', ext = 0)
bias_d = fits.getdata('D_n20131112t1127_c13_r1472p01_biascor.fits', ext = 0)
flat_d = fits.getdata('D_n20131112t1127_r_c13_r1472p01_dflatcor.fits', ext = 0)


fig, ax = plt.subplots()
histogram_bias = plt.hist([field_d.flatten(), bias_d.flatten(), flat_d.flatten()], 30, density = True, 
                           label = ['Science', 'Bias', 'Flat'], color = ['purple', 'red', 'cyan'])

ax.legend()
ax.set_yscale('log')
ax.set_xlabel('Counts')
ax.set_ylabel('Normalized Number')
plt.savefig('counts_hist.png')
plt.close()

plt.imshow(field_d, cmap ='gray', norm=LogNorm())
plt.axis('off')
plt.savefig('field.png')
plt.close()


plt.imshow(bias_d, cmap ='gray', norm=LogNorm())
plt.axis('off')
plt.savefig('bias.png')
plt.close()

plt.imshow(flat_d, cmap ='gray', norm=LogNorm())
plt.axis('off')
plt.savefig('flat.png')
plt.close()

##########################################################################

field_all = fits.open('DECam_00380036_09.fits')
header = fits.getheader('DECam_00380036_09.fits')
oScanA_beg = 2105; oScanA_end = 2154;
oScanB_beg = 7; oScanB_end = 56;
sciB_beg = 57; sciB_end = 1080;
sciA_beg = 1081; sciA_end= 2104;
subField = np.zeros([4096, 2048])
y_start = 51

i = 0
for row in field_d:
    medB = np.median(row[oScanB_beg-1:oScanB_end])
    medA = np.median(row[oScanA_beg-1:oScanA_end])
    subRow = np.zeros([2048])
    if i > y_start-1:
        for j in range(len(row)):
            if j < sciB_end and j > sciB_beg +1:
                subRow[j-57] = row[j] - medB
            elif j < sciA_end:
                subRow[j-57] = row[j] - medA
        subField[i- 51] = subRow
    i+=1
    
plt.plot(range(56,2104), subRow, color = 'purple', label = 'Subtracted')
plt.plot(range(0,2160), row, color = 'cyan', label = 'Raw')
plt.xlabel('Pixel')
plt.ylabel('Count')
plt.legend()
plt.savefig('ampBias.png')
plt.close()

finData = (subField - bias_d)/flat_d

hdu = fits.PrimaryHDU()
hdu.data = finData
hdu.header = header
hdu.writeto('subtractedDES.fits', overwrite=True)

#############################################################################
radio = fits.getdata('skv7351605255062_4.fits', ext = 0)
noise = np.std(radio)