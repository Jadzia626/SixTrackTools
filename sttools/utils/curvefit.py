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

logger = logging.getLogger(__name__)

class GaussianFit():

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
        if len(inres) == self.theDims:
            self.theRes = inRes
        else:
            self.theRes = np.ones(self.theDims,dtype=int)*100

        return

# END Class GaussianFit
