# -*- coding: utf-8 -*
"""Python Toolbox for SixTrack, Beam Analysis

  SixTrack Tools - Beam Analysis
 ================================
  Tools for analysing beams
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging
import numpy as np
import matplotlib.pyplot as plt

from sttools.dataset   import DataSet
from sttools.functions import symmetricRange, parseKeyWordArgs

# Logging
logger = logging.getLogger(__name__)

class Beams():

    def __init__(self, simData):
        self.simData = simData
        return

    def histSixDim(self, dataSet, nBins=100):

        # Check if the data is from collimation or dump module
        if dataSet in ("dist0","distn"):
            isDump    = False
            colNames  = ["X", "XP",  "Y", "YP",  "S", "P"]
            colLabels = ["x", "x'",  "y", "y'",  "s", "p"]
            colUnits  = ["mm","mrad","mm","mrad","mm","MeV"]
            colScales = [-3,  -3,    -3,  -3,    -3,  6]
        else:
            isDump    = True
            colNames  = ["X", "XP",  "Y", "YP",  "Z", "dE/E"]
            colLabels = ["x", "x'",  "y", "y'",  "z", "dE/E"]
            colUnits  = ["mm","mrad","mm","mrad","mm","MeV"]
            colScales = [-3,  -3,    -3,  -3,    -3,  6]

        accuData = [np.array([])]*6
        dSet = DataSet(dataSet,self.simData)
        for aSet in dSet:
            for i in range(6):
                accuData[i] = np.append(accuData[i],aSet[colNames[i]])

        meanVals = [0.0]*6
        stdVals  = [0.0]*6
        minVals  = [0.0]*6
        maxVals  = [0.0]*6
        limVals  = [0.0]*6
        for i in range(6):
            meanVals[i] = np.mean(accuData[i])
            stdVals[i]  = np.std(accuData[i])
            minVals[i]  = np.min(accuData[i])
            maxVals[i]  = np.max(accuData[i])
            limVals[i]  = symmetricRange(minVals[i],maxVals[i],meanVals[i])

        histVals = [(0.0,0.0)]*6
        retVals = {
            "histData"   : [],
            "binEdges"   : [],
            "binCentres" : [],
            "colName"    : [],
            "colLabel"   : [],
            "colUnit"    : [],
            "colScale"   : [],
        }
        for i in range(6):
            hData,bEdges = np.histogram(accuData[i],bins=nBins,range=limVals[i])
            bCentres     = (bEdges[:-1] + bEdges[1:])/2.0
            retVals["histData"].append(hData)
            retVals["binEdges"].append(bEdges)
            retVals["binCentres"].append(bCentres)
            retVals["colName"].append(colNames[i])
            retVals["colLabel"].append(colLabels[i])
            retVals["colUnit"].append(colUnits[i])
            retVals["colScale"].append(colScales[i])

        return retVals

    def plotSixDim(self, dataSet, **theArgs):

        valArgs = {
            "bins"   : 100,
            "figure" : 1,
        }
        kwArgs = parseKeyWordArgs(valArgs, theArgs)

        hSixD = self.histSixDim(dataSet,nBins=kwArgs["bins"])
        print(hSixD)

        fMain  = plt.figure(kwArgs["figure"],figsize=(17,9),dpi=100)
        sOrder = [1,4,2,5,3,6]
        for a in range(6):
            ax = fMain.add_subplot(2,3,sOrder[a])
            yData = hSixD["histData"][a]
            xData = hSixD["binCentres"][a]
            ax.step(xData,yData)
            ax.set_title("Distribution of %s" % hSixD["colLabel"][a])
            ax.set_xlabel("%s" % hSixD["colUnit"][a])

        plt.draw()
        plt.show(block=True)

        return

# END Class Beams
