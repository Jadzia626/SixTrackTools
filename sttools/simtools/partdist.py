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

from os                import path, getcwd
from sttools.constants import Const
from sttools.physics   import Physics
from sttools.functions import parsePath

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

        self.hasError = False
        logger.info("Initialising particle distribution:")
        if "energy" in keyVals:
            self.beamEnergy = initData["energy"]
            logger.info(" * Reference Energy:       %16.9e" % self.beamEnergy)
        else:
            self.beamEnergy = 1.0

        if "mass" in keyVals:
            self.partMass = initData["mass"]
            logger.info(" * Reference Mass:         %16.9e" % self.partMass)
        else:
            self.partMass = 1.0

        if "nemit" in keyVals:
            self.normEmit = initData["nemit"]
            if len(self.normEmit) == 2:
                logger.info(" * Normalised Emittance:   %16.9e %16.9e" % (self.normEmit[0],self.normEmit[1]))
            else:
                logger.error("Value 'nemit' must be a vector of [x,y] values")
                self.hasError = True
        else:
            self.normEmit = [0.0, 0.0]

        if "gemit" in keyVals:
            self.geomEmit = initData["gemit"]
            if len(self.geomEmit) == 2:
                logger.info(" * Geometric Emittance:    %16.9e %16.9e" % (self.geomEmit[0],self.geomEmit[1]))
            else:
                logger.error("Value 'gemit' must be a vector of [x,y] values")
                self.hasError = True
        else:
            self.geomEmit = [0.0, 0.0]

        if "twalpha" in keyVals:
            self.twissAlpha = initData["twalpha"]
            if len(self.twissAlpha) == 2:
                logger.info(" * Twiss Alpha:            %16.9e %16.9e" % (self.twissAlpha[0],self.twissAlpha[1]))
            else:
                logger.error("Value 'twalpha' must be a vector of [x,y] values")
                self.hasError = True
        else:
            self.twissAlpha = [0.0, 0.0]

        if "twbeta" in keyVals:
            self.twissBeta = initData["twbeta"]
            if len(self.twissBeta) == 2:
                logger.info(" * Twiss Beta:             %16.9e %16.9e" % (self.twissBeta[0],self.twissBeta[1]))
            else:
                logger.error("Value 'twbeta' must be a vector of [x,y] values")
                self.hasError = True
        else:
            self.twissBeta = [1.0, 1.0]

        if "offset" in keyVals:
            self.beamOffset = initData["offset"]
            if len(self.beamOffset) == 4:
                logger.info(" * Beam Offset X,XP:       %16.9e %16.9e" % (self.beamOffset[0],self.beamOffset[1]))
                logger.info(" * Beam Offset Y,YP:       %16.9e %16.9e" % (self.beamOffset[2],self.beamOffset[3]))
            else:
                logger.error("Value 'offset' must be a vector of [x,xp,y,yp] values")
                self.hasError = True
        else:
            self.beamOffset = [0.0, 0.0, 0.0, 0.0]

        if "sigmaxxp" in keyVals:
            self.sigmaXXP = initData["sigmaxxp"]
            if len(self.twissBeta) == 2:
                logger.info(" * Beam Sigma X,XP:        %16.9e %16.9e" % (self.sigmaXXP[0],self.sigmaXXP[1]))
            else:
                logger.error("Value 'sigmaxxp' must be a vector of [x,xp] values")
                self.hasError = True
        else:
            self.sigmaXXP = [1.0, 1.0]

        if "sigmayyp" in keyVals:
            self.sigmaYYP = initData["sigmayyp"]
            if len(self.twissBeta) == 2:
                logger.info(" * Beam Sigma Y,YP:        %16.9e %16.9e" % (self.sigmaYYP[0],self.sigmaYYP[1]))
            else:
                logger.error("Value 'sigmayyp' must be a vector of [y,yp] values")
                self.hasError = True
        else:
            self.sigmaYYP = [1.0, 1.0]

        if "sigmaz" in keyVals:
            self.sigmaZ = initData["sigmaz"]
            logger.info(" * Beam Sigma Z:           %16.9e" % self.sigmaZ)
        else:
            self.sigmaZ = 0.0

        if "spreade" in keyVals:
            self.spreadE = initData["spreade"]
            logger.info(" * Beam Energy Spread:     %16.9e" % self.spreadE)
        else:
            self.spreadE = 0.0

        if "spreadp" in keyVals:
            self.spreadP = initData["spreadp"]
            logger.info(" * Beam Momentum Spread:   %16.9e" % self.spreadP)
        else:
            self.spreadP = 0.0

        if "format" in keyVals:
            self.colFormat = initData["format"]
            logger.info("Output Column Formats:")
            logger.info(", ".join(self.colFormat))
        else:
            self.colFormat = []

        bG, bB, bP0 = Physics.energyGammaBeta(self.beamEnergy,self.partMass)
        self.beamGamma = bG
        self.beamBeta  = bB
        self.beamMom   = bP0

        if not "gemit" in keyVals:
            if self.beamBeta > 0.0:
                gEmitX = self.normEmit[0]/(self.beamGamma*self.beamBeta)
                gEmitY = self.normEmit[1]/(self.beamGamma*self.beamBeta)
                self.geomEmit = [gEmitX,gEmitY]
            else:
                self.geomEmit = [1.0,1.0]

        return

    def setSeed(self, newSeed, seedFile=None):

        if seedFile is not None:
            seedFile = parsePath(seedFile, getcwd(), "seeds.txt")
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

    def genNormDist(self, nPairs):

        nPart = nPairs * 2

        startTime   = timeit.default_timer()
        self.genXXP = np.random.normal(0.0, 1.0, (nPart,2)) * self.sigmaXXP
        self.genYYP = np.random.normal(0.0, 1.0, (nPart,2)) * self.sigmaYYP
        self.genZ   = np.random.normal(0.0, 1.0, nPart)     * self.sigmaZ
        self.genDDP = np.random.normal(0.0, 1.0, nPart)     * self.spreadP
        self.genE   = np.zeros(nPart)
        self.genP   = np.zeros(nPart)
        timePassed  = timeit.default_timer() - startTime

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
        sigmaX = np.array([[betaX, -alphaX], [-alphaX, gammaX]])
        sigmaY = np.array([[betaX, -alphaY], [-alphaY, gammaY]])

        # Cholesky decomposition
        cholX  = np.linalg.cholesky(sigmaX*gEmitX)
        cholY  = np.linalg.cholesky(sigmaY*gEmitY)

        # Generate uncorrelated distributions
        distX  = np.random.normal(0.0, 1.0, (nPart,2))
        distY  = np.random.normal(0.0, 1.0, (nPart,2))
        distX  = np.dot(distX, cholX)
        distY  = np.dot(distY, cholY)

        # Apply the Cholesky decomposition
        self.genXXP = np.column_stack((distX[:,1], distX[:,0]))
        self.genYYP = np.column_stack((distY[:,1], distY[:,0]))

        return

    def genLongitudinalDist(self, nPairs):

        nPart = nPairs * 2

        self.genZ   = np.random.normal(0, 1, nPart) * self.sigmaZ
        self.genE   = self.beamEnergy * (1 + np.random.normal(0, 1, nPart)*self.spreadE)
        self.genP   = np.sqrt((self.genE - self.partMass) * (self.genE + self.partMass))
        self.genDDP = (self.genP - self.beamMom) / self.beamMom

        return

    #
    # Write Files
    #

    def writeFort13(self, outPath, nPairs):

        startTime = timeit.default_timer()

        if nPairs*2 > len(self.genXXP):
            logger.error("Cannot output more particle pairs than has been generated")
            return False

        beamEnergy = self.beamEnergy * 1e-6 # Unit MeV
        outFile    = parsePath(outPath, getcwd(), "fort.13")
        with open(outFile, "w") as fort13:
            for i in range(nPairs):
                p1 = i*2
                p2 = p1+1

                # Particle 1
                fort13.write("%22.15e\n" % (self.genXXP[p1,0]*1e3))
                fort13.write("%22.15e\n" % (self.genXXP[p1,1]*1e3))
                fort13.write("%22.15e\n" % (self.genYYP[p1,0]*1e3))
                fort13.write("%22.15e\n" % (self.genYYP[p1,1]*1e3))
                fort13.write("%22.15e\n" % (self.genZ[p1]*1e3))
                fort13.write("%22.15e\n" %  self.genDDP[p1])

                # Particle 2
                fort13.write("%22.15e\n" % (self.genXXP[p2,0]*1e3))
                fort13.write("%22.15e\n" % (self.genXXP[p2,1]*1e3))
                fort13.write("%22.15e\n" % (self.genYYP[p2,0]*1e3))
                fort13.write("%22.15e\n" % (self.genYYP[p2,1]*1e3))
                fort13.write("%22.15e\n" % (self.genZ[p2]*1e3))
                fort13.write("%22.15e\n" %  self.genDDP[p2])

                # Energy
                fort13.write("%22.15e\n" % beamEnergy)
                fort13.write("%22.15e\n" % (self.genE[p1]*1e-6))
                fort13.write("%22.15e\n" % (self.genE[p2]*1e-6))

        timePassed = timeit.default_timer() - startTime

        logger.info("Wrote %d particle pairs to file in %.4f sec" % (nPairs,timePassed))

        return True

    def writeCollDist(self, outPath, nPairs):

        startTime = timeit.default_timer()

        if nPairs*2 > len(self.genXXP):
            logger.error("Cannot output more particle pairs than has been generated")
            return False

        outFile = parsePath(outPath, getcwd(), "partDist.dat")
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

    def writeDistBlockFile(self, outPath, nPairs, fPrec="22.15e"):

        startTime = timeit.default_timer()

        if nPairs*2 > len(self.genXXP):
            logger.error("Cannot output more particle pairs than has been generated")
            return False

        iS = 0
        iE = 2*nPairs

        xP = np.sin(np.arctan(self.genXXP[iS:iE,1]))
        yP = np.sin(np.arctan(self.genYYP[iS:iE,1]))
        pX = xP * self.genP[iS:iE]
        pY = yP * self.genP[iS:iE]
        pZ = np.sqrt(self.genP[iS:iE]**2 - pX**2 - pY**2)

        nCol = len(self.colFormat)
        outData = np.zeros((2*nPairs,nCol))
        for i in range(nCol):
            if self.colFormat[i] == "X":
                outData[:,i] = self.genXXP[iS:iE,0]
            elif self.colFormat[i] == "Y":
                outData[:,i] = self.genYYP[iS:iE,0]
            elif self.colFormat[i] == "XP":
                outData[:,i] = xP
            elif self.colFormat[i] == "YP":
                outData[:,i] = yP
            elif self.colFormat[i] == "PX":
                outData[:,i] = pX
            elif self.colFormat[i] == "PY":
                outData[:,i] = pY
            elif self.colFormat[i] in ("PX/P0","PXP0"):
                outData[:,i] = pX/self.beamMom
            elif self.colFormat[i] in ("PY/P0","PYP0"):
                outData[:,i] = pY/self.beamMom
            elif self.colFormat[i] == "SIGMA":
                outData[:,i] = self.genZ[iS:iE]
            else:
                logger.error("Unknown column format '%s'" % self.colFormat[i])

        outFile = parsePath(outPath, getcwd(), "partDist.dat")
        with open(outFile, "w") as outFile:
            outFile.write("# %s\n" % ", ".join(self.colFormat))
            for i in range(2*nPairs):
                outFile.write(((("{: "+fPrec+"} ")*nCol)+"\n").format(
                    *outData[i,:]
                ))

        timePassed = timeit.default_timer() - startTime

        logger.info("Wrote %d particle pairs to file in %.4f sec" % (nPairs,timePassed))

        return True

# End Class Dist
