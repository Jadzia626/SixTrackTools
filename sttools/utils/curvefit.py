# -*- coding: utf-8 -*
"""SixTrack Tools - Curve Fitting

  SixTrack Tools - Curve Fitting
 ================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import logging
import sttools

import numpy as np

from scipy.optimize import curve_fit

logger = logging.getLogger(__name__)

class CurveFit():

    def __init__(self, inData, inRes=[], inAxes=[]):

        self.theData  = inData
        self.theShape = np.shape(inData)
        self.theDims  = len(self.theShape)

        if np.shape(inAxes)[0] == self.theDims:
            self.theAxes = inAxes
        else:
            self.theAxes = np.zeros((self.theDims,2),dtype=float)
            for d in range(self.theDims):
                self.theAxes[d,0] = np.amin(self.theData,d)
                self.theAxes[d,1] = np.amax(self.theData,d)

        if len(inRes) == self.theDims:
            self.theRes = inRes
        else:
            self.theRes = np.ones(self.theDims,dtype=int)*200

        # Gaussian fit initial values
        self.gaussInit    = np.zeros((self.theDims,3),dtype=float)
        self.gaussInitSet = False

        return

    #
    # Set Methods
    #

    def setGaussInit(self, gOrder, *gParam):
        if gOrder < 1 or gOrder > 2:
            logger.error("Gauss order out of range. Valid range is 1:2.")
            exit(1)
        if len(gParam) != 3*gOrder:
            logger.error("Gauss seeds require 3*order values.")
            exit(1)
        for i in range(gOrder):
            self.gaussInit[i][:] = gParam[3*i:3*i+2]
        self.gaussInitSet = True
        return True

    #
    # Fit Methods
    #

    def fitGauss1(self):
        if not self.gaussInitSet:
            self.gaussInit[0][0] = np.maximum(max(self.theData),-min(self.theData))
            self.gaussInit[0][1] = np.mean(self.theData)
            self.gaussInit[0][2] = np.std(self.theData)

        hData, binEdges = np.histogram(self.theData, density=True, bins=self.theRes[0])
        binCentres      = (binEdges[:-1] + binEdges[1:])/2
        fCoeff, varMat  = curve_fit(self.funcGauss1D, binCentres, hData, p0=self.gaussInit[0])

        print(fCoeff)
        print(varMat)

    #
    # Fit Functions
    #

    @staticmethod
    def funcGauss1D(data, *par):
        if len(par)%3 > 0:
            return None
        retVal = np.zeros(len(data))
        for n in range(len(par)%3):
            retVal += par[3*n]*np.exp(-(data-par[3*n+1])**2 / 2.0*par[3*n+2]**2)
        return retVal

# END Class CurveFit
