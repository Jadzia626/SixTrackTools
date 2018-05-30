#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""SixTrackTools Plot Beam Distribution

  SixTrack Tools - Plot Beam Distribution
 =========================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import sys
import numpy as np
import matplotlib.pyplot as plt

from os import path
from scipy.optimize import curve_fit

# Variables and Flags
useHDF5 = False
useFORT = False
useCOLL = False

nBins   = 50

# Parse Arguments
if len(sys.argv) == 3:
    fileType = sys.argv[1]
    fileName = sys.argv[2]
    dataPath = ""
elif len(sys.argv) == 4:
    fileType = sys.argv[1]
    fileName = sys.argv[2]
    dataPath = sys.argv[3]
else:
    print("ERROR plotBeamDist expected two parameters:")
    print(" - fileType: HDF5, FORT13, COLL")
    print(" - fileName: Path to file")
    print(" - dataPath: Path to HDF5 dataset if fileType is HDF5")
    sys.exit(1)

if not path.isfile(fileName):
    print("ERROR File not found: '%s'" % fileName)
    sys.exit(1)

if fileType == "HDF5":
    if dataPath == "":
        print("ERROR A dataset path is required when using HDF5.")
        sys.exit(1)
    useHDF5 = True
elif fileType == "FORT13":
    useFORT = True
elif fileType == "COLL":
    useCOLL = True
else:
    print("ERROR Unknown fileType '%s'" % fileType)
    sys.exit(1)

# Gather All the Data
if useCOLL:
    dIN = np.loadtxt(fileName)
if useFORT:
    dTMP  = np.loadtxt(fileName)
    nBits = len(dTMP)
    nPart = int(nBits/15)
    dIN   = np.zeros((nPart*2,6))
    for i in range(nPart):
        dIN[2*i+0,0] = dTMP[15*i+0]
        dIN[2*i+0,1] = dTMP[15*i+1]
        dIN[2*i+0,2] = dTMP[15*i+2]
        dIN[2*i+0,3] = dTMP[15*i+3]
        dIN[2*i+0,4] = dTMP[15*i+4]
        dIN[2*i+0,5] = dTMP[15*i+5]
        dIN[2*i+1,0] = dTMP[15*i+6]
        dIN[2*i+1,1] = dTMP[15*i+7]
        dIN[2*i+1,2] = dTMP[15*i+8]
        dIN[2*i+1,3] = dTMP[15*i+9]
        dIN[2*i+1,4] = dTMP[15*i+10]
        dIN[2*i+1,5] = dTMP[15*i+11]

# Gaussian Fit
def fitGauss(x, *p):
    amp, mu, sigma = p
    return amp*np.exp(-(x-mu)**2/(2.*sigma**2))

p0 = [1.0, 0.0, 1.0]

# Plot
fig1 = plt.figure(1,figsize=(14, 10),dpi=100)
fig1.clf()

cTitle = ["x","y","z","x'","y'","dP/P"]

for i in range(6):
    dHist, binEdges   = np.histogram(dIN[:,i], bins=nBins, density=True)
    binCentres        = (binEdges[:-1] + binEdges[1:])/2
    fCoeff, varMatrix = curve_fit(fitGauss, binCentres, dHist, p0=p0)
    hFit              = fitGauss(binCentres, *fCoeff)
    
    sFig1 = plt.subplot(2,3,i+1)
    plt.step(binCentres,dHist,where="mid")
    plt.plot(binCentres,hFit)
    plt.title("Distribution of %s" % cTitle[i])
    plt.xlabel("mu = %.2f, sigma = %.2f" % (fCoeff[1],fCoeff[2]))

plt.show(block=True)
