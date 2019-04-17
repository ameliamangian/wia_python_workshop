#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 12:23:32 2018

@author: johnmangian
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd    

sig_2 = 1.3
sig_1_4 = 3.4

'''
1. Source ID: the IAU designation for the SPT-detected source.
2. RA: right ascension (J2000) in degrees.
3. DEC: declination (J2000) in degrees.
4. S/N (2.0 mm): detection significance (signal-to-noise ratio) in the 2.0 mm band.
5. Sraw (2.0 mm): raw flux (uncorrected for flux boosting) in the 2.0 mm band.
6. Sbest (2.0 mm): median value of de-boosted flux at 2.0 mm.
7. dSup (2.0 mm): upper error bar (1-sigma normal equivalent) of de-boosted flux at 2.0 mm.
8. dSdown (2.0 mm): lower error bar (1-sigma normal equivalent) of de-boosted flux at 2.0 mm.
9. S/N (1.4 mm): detection significance (signal-to-noise ratio) in the 1.4 mm band.
10. Sraw (1.4 mm): raw flux (uncorrected for flux boosting) in the 1.4 mm band.
11. Sbest (1.4 mm): median value of de-boosted flux at 1.4 mm.
12. dSup (1.4 mm): upper error bar (1-sigma normal equivalent) of de-boosted flux at 1.4 mm.
13. dSdown (1.4 mm): lower error bar (1-sigma normal equivalent) of de-boosted flux at 1.4 mm.
14. alpharaw: estimate (from the raw flux in each band) of the 2.0 mm-1.4 mm spectral index alpha
15. alphabest: median value of spectral index.
16. d_alphaup: upper error bar (1-sigma normal equivalent) of spectral index.
17. d_alphadown (2.0 mm): lower error bar (1-sigma normal equivalent) of spectral index.
18. P(alpha > 1.66): fraction of the spectral index posterior probability distribution above the threshold value of 1.66. A higher value of P means the source is more likely to be dust-dominated.
19. Type: source classification (synchrotron- or dust-dominated).
20. Nearest SUMSS source: angular distance (in arseconds) from the nearest source in the 36 cm (843 MHz) Sydney University Molongolo Sky Survey.
21. Nearest RASS source: angular distance (in arseconds) from the nearest source in the ROSAT All-Sky Survey (RASS) Bright Source Catalog or Faint Source Catalog.
22. Nearest IRAS source: angular distance (in arseconds) from the nearest source in the IRAS Faint-Source Catalog.
'''

with open('source_table_vieira09_3sigma.dat','r') as f:
    next(f) # skip first row
    df = pd.DataFrame(l.rstrip().split()[1:] for l in f)

df_rem = df

for index, row in df_rem.iterrows():
    if float(row[3]) < 4.5 and float(row[8]) < 4.5:
        df_rem = df_rem.drop([index])

df_rem_all = df_rem
 
for index, row in df_rem.iterrows():
    if float(row[19]) < 60 or float(row[20]) < 60 or float(row[21]) < 60:
        df_rem = df_rem.drop([index])

flux_2 = []
flux_1_4 = []
err_flux_2l = []
err_flux_1_4l = []
err_flux_2h = []
err_flux_1_4h = []
flux_2a = []
flux_1_4a = []
err_flux_2la = []
err_flux_1_4la = []
err_flux_2ha = []
err_flux_1_4ha = []

for index, row in df_rem.iterrows():
    flux_2.append(float(row[4]))
    flux_1_4.append(float(row[9]))
    err_flux_2l.append(float(row[7]))
    err_flux_1_4l.append(float(row[6]))
    err_flux_2h.append(float(row[12]))
    err_flux_1_4h.append(float(row[11]))

for index, row in df_rem_all.iterrows():
    flux_2a.append(float(row[4]))
    flux_1_4a.append(float(row[9]))
    err_flux_2la.append(float(row[7]))
    err_flux_1_4la.append(float(row[6]))
    err_flux_2ha.append(float(row[12]))
    err_flux_1_4ha.append(float(row[11]))

asymmetric_error_x = [err_flux_2l, err_flux_2h]
asymmetric_error_y = [err_flux_1_4l, err_flux_1_4h]

fig, ax = plt.subplots(figsize = (8,6))      
ax.scatter(flux_2a, flux_1_4a, edgecolor = 'red', facecolor = 'None', marker = 'o', label = 'All Sources')
ax.scatter(flux_2, flux_1_4, edgecolor = 'green', facecolor = 'green', marker = 'x', label = 'Sources with no Counterpart')
#ax.errorbar(flux_2, flux_1_4, xerr=asymmetric_error_x, yerr = asymmetric_error_y, fmt='None', ecolor='k')
plt.scatter(float(df.iloc[2986][4]), float(df.iloc[2986][9]), color = 'blue', label = 'Selected Dusty')
plt.scatter(float(df.iloc[2356][4]), float(df.iloc[2356][9]), color = 'orange', label = 'Selected Synchrotron')
plt.scatter(float(df.iloc[1690][4]), float(df.iloc[1690][9]), color = 'purple', marker = 'x', label = 'Selected Lensed')
ax.axvline(4.5*sig_2, ls = '--', c = 'k', label =r'Flux Cut (4.5$\sigma$)')
ax.axhline(4.5*sig_1_4, ls = '--', c = 'k')
ax.set_yscale('log')
ax.set_xscale('log')
plt.xlim(.1,1000)
plt.ylim(.1,1000)
ax.set_xlabel(r'S$_{2.0 mm}$ (mJy)', fontsize = 12)
ax.set_ylabel(r'S$_{1.4 mm}$ (mJy)', fontsize = 12)
plt.legend()

plt.savefig('spt_cut.png')