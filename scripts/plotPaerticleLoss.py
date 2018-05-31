#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""SixTrackTools Plot Particle Loss

  SixTrack Tools - Plot Particle Loss
 =====================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt

from os import path, listdir

# Variables and Flags

# Parse Arguments
if len(sys.argv) == 2:
    dataFolder = sys.argv[1]
    dataFiles  = None
elif len(sys.argv) > 2:
    dataFolder = sys.argv[1]
    dataFiles  = sys.argv[2:]
else:
    print("ERROR plotParticleLoss expected one or two parameters:")
    print(" - dataFolder: The data storage folder")
    print(" - dataFiles:  Optional. A list of files.")
    sys.exit(1)

if not path.isdir(dataFolder):
    print("ERROR Path not found: '%s'" % dataFolder)
    sys.exit(1)

if dataFiles is None:
    tmpList   = listdir(dataFolder)
    extList   = (".hdf5",".h5",".hdf")
    dataFiles = []
    for elem in tmpList:
        fName, fExt = path.splitext(elem)
        if fExt in extList:
            dataFiles.append(elem)

collList = None
collHits = {"IMP":{}, "ABS":{}}
tImp = 0
tAbs = 0
for inFile in dataFiles:
    
    filePath = path.join(dataFolder,inFile)
    print("Reading file: %s" % inFile)
    if not path.isfile(filePath):
        print("ERROR File not found: %s" % filePath)
        sys.exit(1)
    
    h5File = h5py.File(filePath,mode="r")
    
    # Collimation Data
    dSet = h5File["/collimation/coll_summary"]
    
    # If first, create collimation index
    if collList is None:
        collList = {"ID":{}, "NAME":{}}
        for iColl, nColl in dSet["ICOLL","COLLNAME"]:
            # Build index
            print("Collimator %2d : '%s'" % (iColl,nColl.decode("utf-8")))
            collList["ID"][iColl]   = nColl.decode("utf-8")
            collList["NAME"][nColl] = iColl
            # Initialise hits data
            collHits["IMP"][iColl] = 0
            collHits["ABS"][iColl] = 0
    
    # Sum up hits
    for iColl, nImp, nAbs in dSet["ICOLL","NIMP","NABS"]:
        collHits["IMP"][iColl] += nImp
        collHits["ABS"][iColl] += nAbs
        tImp += nImp
        tAbs += nAbs
    
    h5File.close()

# Print summaries
print("")
print(" Collimation Summary")
print("=====================")
print("")
print("       |                      |      NIMP      |      NABS      ")
print(" ICOLL | COLLNAME             |  COUNT | RAT % |  COUNT | RAT % ")
print("-------+----------------------+--------+-------+--------+-------")
for iColl in collList["ID"].keys():
    print(" %5d | %-20s | %6d | %5.2f | %6d | %5.2f " % (
        iColl,
        collList["ID"][iColl],
        collHits["IMP"][iColl],
        100*collHits["IMP"][iColl]/tImp,
        collHits["ABS"][iColl],
        100*collHits["ABS"][iColl]/tAbs,
    ))
print("-------+----------------------+--------+-------+--------+-------")
print(" %5d |                      | %6d |       | %6d |       " % (
    len(collList["ID"]),
    tImp,
    tAbs,
))

# fig1 = plt.figure(1,figsize=(5, 15),dpi=100)
# fig1.clf()

# plt.rcdefaults()
fig1, ax1 = plt.subplots(figsize=(7, 9),dpi=100)
plt.ion()

# Example data
pLabels = []
pImp    = []
pAbs    = []
for iColl in collList["ID"].keys():
    pLabels.append(collList["ID"][iColl])
    pImp.append(collHits["IMP"][iColl])
    pAbs.append(collHits["ABS"][iColl])
    
# people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')
yPos = np.arange(len(pLabels))

ax1.barh(yPos-0.2, pImp, height=0.4, align="center", color="green")
ax1.barh(yPos+0.2, pAbs, height=0.4, align="center", color="red")
ax1.set_yticks(yPos)
ax1.set_yticklabels(pLabels)
ax1.invert_yaxis()
ax1.set_title("Collimation Hits and Absorbtions")
ax1.legend(("Impacts","Absorbtions"))

plt.subplots_adjust(left=0.20, right=0.95, top=0.95, bottom=0.05)
plt.draw()
plt.show(block=True)
