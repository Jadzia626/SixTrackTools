# -*- coding: utf-8 -*
"""SixTrack Tools - Particle Generator 

  SixTrack Tools - Particle Generator
 =====================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

  Generate a particle distribution file for SixTrack
  
"""

import logging
import sttools
import numpy as np

from sttools.constants import Const
from sttools.physics   import calcGammaBeta

logger = logging.getLogger(__name__)

class Dist():
    
    partMass = None
    
    def __init__(self, initData):
        
        keyVals = initData.keys()
        
        self.partArrays = {
            "x"    : [],
            "xp"   : [],
            "y"    : [],
            "yp"   : [],
            "z"    : [],
            "d/dP" : [],
            "E"    : [],
            "dE/E" : [],
        }
        
        if "energy" in keyVals:
            self.beamEnergy = initData["energy"]
        else:
            self.beamEnergy = 7.0e12
        
        if "mass" in keyVals:
            self.partMass = initData["mass"]
        else:
            self.partMass = Const.ProtonMass
        
        if "nemit" in keyVals:
            self.normEmit = initData["nemit"]
        else:
            self.normEmit = [0.0, 0.0]
        
        if "gemit" in keyVals:
            self.geomEmit = initData["gemit"]
        else:
            self.geomEmit = [0.0, 0.0]
        
        if "twalpha" in keyVals:
            self.twissAlpha = initData["twalpha"]
        else:
            self.twissAlpha = [0.0, 0.0]
        
        if "twbeta" in keyVals:
            self.twissBeta = initData["twbeta"]
        else:
            self.twissBeta = [1.0, 1.0]
        
        if "offset" in keyVals:
            self.beamOffset = initData["offset"]
        else:
            self.beamOffset = [0.0, 0.0, 0.0, 0.0]
        
        # Check Values
        self.hasError = False
        if not len(self.normEmit) == 2:
            logger.error("Value 'nemit' must be a vector of [x,y] values")
            self.hasError = True
        
        if not len(self.geomEmit) == 2:
            logger.error("Value 'gemit' must be a vector of [x,y] values")
            self.hasError = True
        
        if not len(self.twissAlpha) == 2:
            logger.error("Value 'twalpha' must be a vector of [x,y] values")
            self.hasError = True
        
        if not len(self.twissBeta) == 2:
            logger.error("Value 'twbeta' must be a vector of [x,y] values")
            self.hasError = True
        
        if not len(self.beamOffset) == 4:
            logger.error("Value 'offset' must be a vector of [x,xp,y,yp] values")
            self.hasError = True
        
        bG, bB, bP0 = calcGammaBeta(self.beamEnergy,self.partMass)
        self.beamGamma = bG
        self.beamBeta  = bB
        self.beamMom   = bP0
        
        if not "gemit" in keyVals:
            gEmitX = self.normEmit[0]/(self.beamGamma*self.beamBeta)
            gEmitY = self.normEmit[1]/(self.beamGamma*self.beamBeta)
            self.geomEmit = [gEmitX,gEmitY]
        
        return
    
    def genDist(self, nPairs):
        
        self.genTransverseDist(nPairs)
        
        return
    
    def genTransverseDist(self, nPairs):
        """Generate x,xp and y,yp bivariate distributions via covariance matrices
        See: http://se.mathworks.com/help/matlab/ref/randn.html
        """
        
        nPart  = nPairs * 2
        
        gEmitX = self.geomEmit[0]
        gEmitY = self.geomEmit[1]
        alphaX = self.twissAlpha[0]
        alphaY = self.twissAlpha[1]
        betaX  = self.twissBeta[0]
        betaY  = self.twissBeta[1]
        gammaX = 1+alphaX**2 / betaX
        gammaY = 1+alphaY**2 / betaY
        
        covX   = np.matrix([[betaX, alphaX], [-alphaX, gammaX]])
        covY   = np.matrix([[betaX, alphaY], [-alphaY, gammaY]])
        
        cholX  = np.linalg.cholesky(covX*gEmitX)
        cholY  = np.linalg.cholesky(covY*gEmitY)
        
        distX  = np.random.normal(0, 1, (nPart,2))
        distY  = np.random.normal(0, 1, (nPart,2))
        
        phspX  = distX*cholX
        phspY  = distY*cholY
        
        print(phspX)
        print(phspY)
        
        return
        
# End Class Dist
