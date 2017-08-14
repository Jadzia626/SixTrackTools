# -*- coding: utf-8 -*
"""Twiss Class

  SixTrack Tools - Twiss Class
 ==============================
  Twiss (emittance) related calculations
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging
import numpy   as np

from math import *

logger = logging.getLogger(__name__)


class Twiss:

    STData = None # STData object

    def __init__(self, inData):

        self.STData = inData

        if not self.STData.isNumPy:
            self.STData.convertToNumpy()

        return

    def getTwiss(self, psDir, turnID=-1):

        if   psDir.lower() == "x":
            idxPos = "X"
            idxAng = "XP"
        elif psDir.lower() == "y":
            idxPos = "Y"
            idxAng = "YP"
        else:
            logger.error("Unreckognised direction '%s'" % psDir)
            return None

        self.STData.filterTurn(turnID)
        partPos = self.STData.fData[idxPos]
        partAng = self.STData.fData[idxAng]

        mCov  = np.cov(np.vstack((partPos,partAng)))
        gEmit = sqrt(np.linalg.det(mCov))
        mCov  = mCov / gEmit

        tAlpha = mCov[0,1]
        tBeta  = mCov[0,0]
        tGamma = mCov[1,1]
        
        retVals = {
            "Count" : 0,
            "Alpha" : tAlpha,
            "Beta"  : tBeta,
            "Gamma" : tGamma,
            "GEmit" : gEmit,
        }

        return retVals

## End Class Twiss    
