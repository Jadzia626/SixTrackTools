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
from matplotlib.ticker import MaxNLocator

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
    print(" - dataFiles:  Optionally, a list of files.")
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


##################
#  COLLECT DATA  #
##################

lenLHC = [
    26658.8832, # LHC Length
    19994.1624, # IP1
    23326.5990, # IP2
        0.0000, # IP3
     3332.2842, # IP4
     6664.5684, # IP5
     9997.0050, # IP6
    13329.4416, # IP7
    16650.6582, # IP8
]
collList = None
collHits = {"IMP":{}, "ABS":{}}
collImp  = 0
collAbs  = 0
lostTurn = []
lostSPos = []
nSurvive = []
scatT    = []
scatDEE  = []
nParts   = 0
nTurns   = 0
for inFile in dataFiles:

    filePath = path.join(dataFolder,inFile)
    print("Reading file: %s" % inFile)
    if not path.isfile(filePath):
        print("ERROR File not found: %s" % filePath)
        sys.exit(1)

    h5File  = h5py.File(filePath,mode="r")
    nParts += int(h5File["/"].attrs["Particles"])
    if nTurns == 0:
        nTurns   = int(h5File["/"].attrs["Turns"])
        nSurvive = np.zeros((nTurns+1,),dtype=int)

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
        collImp += nImp
        collAbs += nAbs

    # Survival
    dSet = h5File["/scatter/scatter_log"]
    for sT, sDEE, sTheta, sPhi in dSet["T","dE/E","THETA","PHI"]:
        scatT.append(sT*1e-6)
        scatDEE.append(sDEE)

    # Scatter Log
    dSet = h5File["/collimation/survival"]
    for iTurn, nSurv in dSet["TURN","NSURV"]:
        nSurvive[iTurn] += nSurv

    # Aperture Data
    dSet = h5File["/aperture/losses"]
    for iTurn, sLoss in dSet["TURN","SLOS"]:
        if iTurn == 0: continue
        if sLoss < lenLHC[5] or sLoss > lenLHC[6]: continue
        lostTurn.append(iTurn)
        lostSPos.append(sLoss)

    h5File.close()


#############
#  SUMMARY  #
#############


# Print summaries
print("")
print("###################")
print("# ~o~ SUMMARY ~o~ #")
print("###################")
print("")
print(" Particles: %d" % nParts)
print(" Turns:     %d" % nTurns)

# Collimation
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
        100*collHits["IMP"][iColl]/collImp,
        collHits["ABS"][iColl],
        100*collHits["ABS"][iColl]/collAbs,
    ))
print("-------+----------------------+--------+-------+--------+-------")
print(" %5d |                      | %6d | %5.2f | %6d | %5.2f " % (
    len(collList["ID"]),
    collImp,
    100*collImp/nParts,
    collAbs,
    100*collAbs/nParts,
))

# Survival
print("")
print(" Survival")
print("==========")
print("")
print(" TURN |  COUNT ")
print("------+--------")
for iTurn in range(1,len(nSurvive)):
    print(" %4d | %6d " % (
        iTurn,
        nSurvive[iTurn]
    ))
print("------+--------")


###########
#  PLOTS  #
###########


# Plot Collimation Losses
fig1, ax1 = plt.subplots(figsize=(7, 8),dpi=100)
plt.ion()

pLabels = []
pImp    = []
pAbs    = []
for iColl in collList["ID"].keys():
    nImp = collHits["IMP"][iColl]
    nAbs = collHits["ABS"][iColl]
    if nImp > 0 or nAbs > 0:
        pLabels.append(collList["ID"][iColl])
        pImp.append(collHits["IMP"][iColl])
        pAbs.append(collHits["ABS"][iColl])

yPos = np.arange(len(pLabels))

ax1.barh(yPos-0.2, pImp, height=0.4, align="center", color="green")
ax1.barh(yPos+0.2, pAbs, height=0.4, align="center", color="red")
ax1.set_yticks(yPos)
ax1.set_yticklabels(pLabels)
ax1.invert_yaxis()
ax1.set_xlabel("Particle Count")
ax1.set_title("Collimation Hits and Absorbtions")
ax1.legend(("Impacts","Absorbtions"))

plt.subplots_adjust(left=0.22, right=0.95, top=0.95, bottom=0.07)

# Plot Aperture Losses
fig2, ax2 = plt.subplots(figsize=(12, 6),dpi=100)
plt.ion()

# lostSPos = np.asarray(lostSPos)*1.0e-3
# lhcIPPos = np.asarray(lenLHC)*1.0e-3
mElements = {
    "IP5"           : 6.664568432756251e+03, # MARKER
    "TAXS.1R5"      : 6.685418432756253e+03, # TAS
#   "MQXFA.A1R5"    : 6.691768432756252e+03, # QUADRUPOLE
    "MQXFA.B1R5"    : 6.696614432756251e+03, # QUADRUPOLE
#   "MQXFB.A2R5"    : 6.707392432756250e+03, # QUADRUPOLE
    "MQXFB.B2R5"    : 6.716650432756250e+03, # QUADRUPOLE
#   "MQXFA.A3R5"    : 6.724478432756249e+03, # QUADRUPOLE
    "MQXFA.B3R5"    : 6.729324432756250e+03, # QUADRUPOLE
    "MBXF.4R5"      : 6.745507473049764e+03, # RBEND
    "TAXN.4R5"      : 6.795035232756250e+03, # TAN
    "TCLX.4R5.B1"   : 6.800809232756248e+03, # COLLIMATOR
    "MQYY.4R5.B1"   : 6.844083432756253e+03, # QUADRUPOLE
    "TCL.5R5.B1"    : 6.866258432756254e+03, # COLLIMATOR
    "MQY.5R5.B1"    : 6.873758432756253e+03, # QUADRUPOLE
    "TCL.6R5.B1"    : 6.885875432756256e+03, # COLLIMATOR
    "MQML.6R5.B1"   : 6.895358432756256e+03, # QUADRUPOLE
#   "MQM.A7R5.B1"   : 6.927972432756256e+03, # QUADRUPOLE
    "MQM.B7R5.B1"   : 6.931739432756256e+03, # QUADRUPOLE
#   "MCS.A8R5.B1"   : 6.948781927455099e+03, # SEXTUPOLE
    "MCS.B8R5.B1"   : 6.964442422153944e+03, # SEXTUPOLE
    "MQML.8R5.B1"   : 6.970811422153944e+03, # QUADRUPOLE
#   "MB.A9R5.B1"    : 6.987518669503365e+03, # SBEND
#   "MCS.A9R5.B1"   : 6.987847916852788e+03, # SEXTUPOLE
    "MB.B9R5.B1"    : 7.003179164202210e+03, # SBEND
#   "MCS.B9R5.B1"   : 7.003508411551631e+03, # SEXTUPOLE
#   "MQMC.9R5.B1"   : 7.007509411551630e+03, # QUADRUPOLE
#   "MQM.9R5.B1"    : 7.011275411551630e+03, # QUADRUPOLE
#   "MB.A10R5.B1"   : 7.027984658901053e+03, # SBEND
#   "MCS.A10R5.B1"  : 7.028313906250474e+03, # SEXTUPOLE
    "MB.B10R5.B1"   : 7.043645153599896e+03, # SBEND
#   "MCS.B10R5.B1"  : 7.043974400949317e+03, # SEXTUPOLE
#   "MQML.10R5.B1"  : 7.050343400949317e+03, # QUADRUPOLE
#   "MS.10R5.B1"    : 7.050872900949317e+03, # SEXTUPOLE
#   "MB.A11R5.B1"   : 7.067050648298738e+03, # SBEND
#   "MCS.A11R5.B1"  : 7.067379895648160e+03, # SEXTUPOLE
    "MB.B11R5.B1"   : 7.082711142997581e+03, # SBEND
#   "MCS.B11R5.B1"  : 7.083040390347002e+03, # SEXTUPOLE
#   "MQ.11R5.B1"    : 7.101678090347002e+03, # QUADRUPOLE
#   "MQTLI.11R5.B1" : 7.103147090347001e+03, # QUADRUPOLE
#   "MS.11R5.B1"    : 7.103693590347001e+03, # SEXTUPOLE
#   "MB.A12R5.B1"   : 7.119833337696422e+03, # SBEND
#   "MCS.A12R5.B1"  : 7.120162585045843e+03, # SEXTUPOLE
#   "MB.B12R5.B1"   : 7.135493832395267e+03, # SBEND
#   "MCS.B12R5.B1"  : 7.135823079744688e+03, # SEXTUPOLE
    "MB.C12R5.B1"   : 7.151154327094109e+03, # SBEND
#   "MCS.C12R5.B1"  : 7.151483574443530e+03, # SEXTUPOLE
#   "MQT.12R5.B1"   : 7.153221574443530e+03, # QUADRUPOLE
#   "MQ.12R5.B1"    : 7.156619574443530e+03, # QUADRUPOLE
#   "MS.12R5.B1"    : 7.157149074443530e+03, # SEXTUPOLE
#   "MB.A13R5.B1"   : 7.173284821792950e+03, # SBEND
#   "MCS.A13R5.B1"  : 7.173614069142371e+03, # SEXTUPOLE
#   "MB.B13R5.B1"   : 7.188945316491794e+03, # SBEND
#   "MCS.B13R5.B1"  : 7.189274563841215e+03, # SEXTUPOLE
    "MB.C13R5.B1"   : 7.204605811190637e+03, # SBEND
#   "MCS.C13R5.B1"  : 7.204935058540058e+03, # SEXTUPOLE
#   "MQT.13R5.B1"   : 7.206673058540057e+03, # QUADRUPOLE
#   "MQ.13R5.B1"    : 7.210071058540057e+03, # QUADRUPOLE
#   "MS.13R5.B1"    : 7.210600558540057e+03, # SEXTUPOLE
#   "MB.A14R5.B1"   : 7.226736305889477e+03, # SBEND
#   "MCS.A14R5.B1"  : 7.227065553238900e+03, # SEXTUPOLE
#   "MB.B14R5.B1"   : 7.242396800588322e+03, # SBEND
#   "MCS.B14R5.B1"  : 7.242726047937743e+03, # SEXTUPOLE
    "MB.C14R5.B1"   : 7.258057295287164e+03, # SBEND
#   "MCS.C14R5.B1"  : 7.258386542636586e+03, # SEXTUPOLE
#   "MQT.14R5.B1"   : 7.260124542636585e+03, # QUADRUPOLE
#   "MQ.14R5.B1"    : 7.263522542636585e+03, # QUADRUPOLE
#   "MS.14R5.B1"    : 7.264052042636585e+03, # SEXTUPOLE
}

elPos    = np.asarray(list(mElements.values()))-lenLHC[5]
elName   = list(mElements.keys())
lostSPos = np.asarray(lostSPos)

print("")
print(" Losses Up To")
print("===============")
print("")
for elCount in elName:
    print("%-16s : %d" % (elCount,(lostSPos < mElements[elCount]).sum()))
print("")

ax2.hist(lostSPos-lenLHC[5], bins=3333)
ax2.set_xticks(elPos)
ax2.set_xticks(elPos, minor=True)
ax2.set_xticklabels(elName)
for tick in ax2.get_xticklabels():
    tick.set_rotation(90)
# ax2.set_xticks(lhcIPPos)
# ax2.set_xticklabels(["IP3","IP1","IP2","IP3","IP4","IP5","IP6","IP7","IP8"])
# ax2.set_xlim([0,lhcIPPos[0]])
# ax2.set_xlim([lhcIPPos[5],lhcIPPos[6]])
ax2.set_xlim([0.0,600.0])
ax2.set_xlabel("Right of IP5")
ax2.set_ylabel("Count/m")
ax2.set_title("Aperture Losses")

plt.subplots_adjust(left=0.08, right=0.95, top=0.92, bottom=0.22)

# Plot Survival
fig3, ax3 = plt.subplots(figsize=(7, 4),dpi=100)
plt.ion()

ax3.plot(range(1,nTurns), nSurvive[1:nTurns], color="blue")
ax3.xaxis.set_major_locator(MaxNLocator(integer=True))
ax3.set_xlim([1,nTurns])
ax3.set_xlabel("Turn")
ax3.set_ylabel("Particle Count")
ax3.set_title("Survival")

plt.subplots_adjust(left=0.13, right=0.97, top=0.92, bottom=0.13)

# Plot Scatter Log T
fig4, ax4 = plt.subplots(figsize=(7, 4),dpi=100)
plt.ion()
ax4.hist(scatT, bins=100, histtype="step", log=True)
ax4.set_xlabel("|t| [GeV^2]")
ax4.set_xlim([0,2])
ax4.set_ylim([1,1e6])
ax4.set_title("Scatter Angle")

plt.subplots_adjust(left=0.08, right=0.95, top=0.91, bottom=0.15)

# Plot Scatter Log dE/E
fig5, ax5 = plt.subplots(figsize=(7, 4),dpi=100)
plt.ion()
ax5.hist(scatDEE, bins=100, histtype="step", log=True)
ax5.set_xlabel("dE/E")
# ax5.set_xlim([0,2])
ax5.set_ylim([1,1e6])
ax5.set_title("Energy Loss")

# plt.subplots_adjust(left=0.08, right=0.95, top=0.91, bottom=0.15)


plt.draw()
plt.show(block=True)
