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
import timeit
import numpy as np

from os         import path
from .constants import Const
from .physics   import calcGammaBeta

logger = logging.getLogger(__name__)

class PartDist():
    
    partMass = None
    randSeed = None
    
    def __init__(self, initData):
        
        keyVals = initData.keys()
        
        # Distributions
        self.genXXP = None
        self.genYYP = None
        self.genZ   = None
        self.genP   = None
        self.genDDP = None
        self.genE   = None
        
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
        
        if "sigmaz" in keyVals:
            self.sigmaZ = initData["sigmaz"]
        else:
            self.sigmaZ = 0.0
        
        if "spreade" in keyVals:
            self.spreadE = initData["spreade"]
        else:
            self.spreadE = 0.0
        
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
    
    def setSeed(self, newSeed, seedFile=None):
        
        if seedFile is not None:
            if not path.isdir(path.dirname(seedFile)):
                logger.error("Path not found: %s" % path.dirname(seedFile))
                return False
            with open(seedFile,"a+") as outFile:
                outFile.write(str(newSeed)+"\n")
        
        np.random.seed(newSeed)
        
        return True
    
    #
    # Particle Generators
    #
    
    def genDist(self, nPairs):
        
        startTime = timeit.default_timer()
        self.genTransverseDist(nPairs)
        self.genLongitudinalDist(nPairs)
        timePassed = timeit.default_timer() - startTime
        
        logger.info("Generated %d particle pairs in %.4f sec" % (nPairs,timePassed))
        
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
        
        # Covariant matrices
        covX   = np.matrix([[betaX, alphaX], [-alphaX, gammaX]])
        covY   = np.matrix([[betaX, alphaY], [-alphaY, gammaY]])
        
        # Cholesky decomposition
        cholX  = np.linalg.cholesky(covX*gEmitX)
        cholY  = np.linalg.cholesky(covY*gEmitY)
        
        # Generate uncorrelated distributions
        distX  = np.random.normal(0, 1, (nPart,2))
        distY  = np.random.normal(0, 1, (nPart,2))
        
        # Apply the Cholesky decomposition
        self.genXXP = distX*cholX*1e3 # Unit mm, mrad
        self.genYYP = distY*cholY*1e3 # Unit mm, mrad
        
        return
    
    def genLongitudinalDist(self, nPairs):
        
        nPart = nPairs * 2
        
        self.genZ   = np.random.normal(0, 1, nPart) * self.sigmaZ
        self.genE   = self.beamEnergy * (1 + np.random.normal(0, 1, nPart)*self.spreadE)
        self.genP   = np.sqrt((self.genE - self.partMass) * (self.genE + self.partMass))
        self.genDDP = (self.genP - self.beamMom) / self.beamMom
        
        self.genZ  *= 1e3  # Unit mm
        self.genE  *= 1e-6 # Unit MeV
        
        return
    
    #
    # Write Files
    #
    
    def writeFort13(self, outPath, nPairs):
        
        startTime = timeit.default_timer()
        
        if not path.isdir(outPath):
            logger.error("Path not found: %s" % outPath)
            return False
        
        if nPairs*2 > len(self.genXXP):
            logger.error("Cannot output more particle pairs than has been generated")
            return False
        
        beamEnergy = self.beamEnergy * 1e-6 # Unit MeV
        outFile = path.join(outPath, "fort.13")
        with open(outFile, "w") as fort13:
            for i in range(nPairs):
                p1 = i*2
                p2 = p1+1
                
                # Particle 1
                fort13.write("%22.15e\n" % self.genXXP[p1,0])
                fort13.write("%22.15e\n" % self.genXXP[p1,1])
                fort13.write("%22.15e\n" % self.genYYP[p1,0])
                fort13.write("%22.15e\n" % self.genYYP[p1,1])
                fort13.write("%22.15e\n" % self.genZ[p1])
                fort13.write("%22.15e\n" % self.genDDP[p1])
                
                # Particle 2
                fort13.write("%22.15e\n" % self.genXXP[p2,0])
                fort13.write("%22.15e\n" % self.genXXP[p2,1])
                fort13.write("%22.15e\n" % self.genYYP[p2,0])
                fort13.write("%22.15e\n" % self.genYYP[p2,1])
                fort13.write("%22.15e\n" % self.genZ[p2])
                fort13.write("%22.15e\n" % self.genDDP[p2])
                
                # Energy
                fort13.write("%22.15e\n" % beamEnergy)
                fort13.write("%22.15e\n" % self.genE[p1])
                fort13.write("%22.15e\n" % self.genE[p2])
                
        timePassed = timeit.default_timer() - startTime
        
        logger.info("Wrote %d particle pairs to file in %.4f sec" % (nPairs,timePassed))
        
        return True
        
    def writeCollDist(self, outPath, nPairs):
        
        startTime = timeit.default_timer()
        
        if not path.isdir(outPath):
            logger.error("Path not found: %s" % outPath)
            return False
        
        if nPairs*2 > len(self.genXXP):
            logger.error("Cannot output more particle pairs than has been generated")
            return False
        
        beamEnergy = self.beamEnergy * 1e-6 # Unit MeV
        outFile = path.join(outPath, "partDist.dat")
        with open(outFile, "w") as outFile:
            for i in range(2*nPairs):
                outFile.write((("{: 22.15e} "*6)+"\n").format(
                    self.genXXP[i,0],
                    self.genXXP[i,1],
                    self.genYYP[i,0],
                    self.genYYP[i,1],
                    self.genZ[i],
                    self.genDDP[i]
                ))
        
        timePassed = timeit.default_timer() - startTime
        
        logger.info("Wrote %d particle pairs to file in %.4f sec" % (nPairs,timePassed))
        
        return True
    
# End Class Dist
