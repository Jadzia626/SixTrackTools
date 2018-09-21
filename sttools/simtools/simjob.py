# -*- coding: utf-8 -*
"""Python Toolbox for SixTrack, Simulation Job Class

  SixTrack Tools - Simulation Job Class
 =======================================
  Class for setting up and running SixTrack simulations
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging
import subprocess

from os     import path, mkdir, listdir
from shutil import rmtree

from sttools.functions         import getTimeStamp
from sttools.simtools.partdist import PartDist
from sttools.simtools.fort2    import Fort2

# Logging
logger = logging.getLogger(__name__)

class SixTrackJob():

    OUT_ARCH   = 0
    OUT_HDF5   = 1
    OUT_PLAIN  = 2
    VAL_OUT    = [0,1,2]

    GEN_NONE   = 0
    GEN_FORT13 = 1
    GEN_COLL   = 2
    GEN_DIST   = 3
    VAL_GEN    = [0,1,2,3]

    DIR_RESULT = "simResults"
    DIR_TEMP   = "runTemp"

    LOG_SEED   = "rndSeeds.log"
    LOG_VALS   = "inputValues.log"
    LOG_JOB    = "jobExec.log"

    def __init__(self, jobFolder):

        # Input Values
        self.jobFolder = path.abspath(jobFolder) # Root job folder
        self.execName  = "SixTrack.e"            # Name of the executable
        self.outName   = "Run"                   # Base name for the output
        self.outFormat = self.OUT_ARCH           # Format of the output
        self.jobSeeds  = []                      # List of seed variables
        self.firstSeed = 1                       # The first seed in the sequence of seeds
        self.seedStep  = 1                       # Value added to previous seed
        self.inFiles   = {"fort.3":True}         # List of input files to copy to run directory
        self.outFiles  = []                      # List of output files to keep afterwards
        self.inVars    = {}                      # Dictionary of values to replace in input files
        self.partGen   = self.GEN_NONE           # Which particle generator to use
        self.genParams = None                    # Particle distribution parameters (see partdist)
        self.numPart   = 2                       # Number of particles in simulation
        self.partLabel = "%NPART%"               # Keyword for search/replace
        self.numTurn   = 1                       # Number of turns in simulation
        self.turnLabel = "%NTURN%"               # Keyword for search/replace

        # Runtime Stuff
        self.timeStamp = ""
        self.seedLog   = None
        self.jobLog    = None
        self.valLog    = None
        self.allSeeds  = []
        self.numSeed   = 0
        self.numSim    = 0
        self.jobNames  = []
        self.runDir    = []

        return

    #
    #  Set and Get Methods
    #

    def initSeeds(self, firstSeed, seedStep=1):
        self.firstSeed = firstSeed
        self.seedStep  = seedStep
        return True

    def setExecutable(self, execName):
        fullPath = path.join(self.jobFolder, execName)
        if path.isfile(fullPath):
            self.execName = execName
        else:
            raise FileNotFoundError("No file named '%s' in job folder." % execName)
        return True

    def setNPart(self, numPart, partLabel=None):
        if numPart > 0:
            self.numPart = numPart
        else:
            raise ValueError("Number of particles must be > 0, got %d" % numPart)
        if numPart % 2 != 0:
            raise ValueError("Number of particles must be an even number, got %d" % numPart)
        if partLabel is not None:
            self.partLabel = partLabel
        return True

    def setPartGen(self, partGen, genParams=None):
        if partGen in self.VAL_GEN:
            self.partGen   = partGen
            self.genParams = genParams
        else:
            raise ValueError("Unknown particle generator format %d")
        return True

    def setNTurn(self, numTurn, turnLabel=None):
        if numTurn > 0:
            self.numTurn = numTurn
        else:
            raise ValueError("Number of turns must be > 0, got %d" % numTurn)
        if turnLabel is not None:
            self.turnLabel = turnLabel
        return True

    def setOutput(self, outName="Run", outFormat=0):
        """Set the base name for the output files or folders.
        """
        self.outName = outName
        if outFormat == self.OUT_ARCH:
            self.outFormat = self.OUT_ARCH
        elif outFormat == self.OUT_HDF5:
            self.outFormat = self.OUT_HDF5
        elif outFormat == self.OUT_PLAIN:
            self.outFormat = self.OUT_PLAIN
        else:
            raise ValueError("Unknown output format %d." % outFormat)
        return

    def addInputFile(self, fileName, replaceQueue=False):
        """Adds a file that will be copied to the
        """
        fullPath = path.join(self.jobFolder, fileName)
        if path.isfile(fullPath):
            if fileName not in self.inFiles.keys():
                self.inFiles[fileName] = replaceQueue
        else:
            raise FileNotFoundError("No file named '%s' in job folder." % fileName)
        return True

    def addOutputFile(self, fileName):
        return True

    def addSeed(self, seedName):
        if isinstance(seedName,str):
            self.jobSeeds.append(seedName)
        else:
            for aSeed in seedName:
                if isinstance(aSeed,str):
                    self.jobSeeds.append(aSeed)
                else:
                    raise TypeError("Seed names must be strings.")
        return True

    def addSimValue(self, keyName, keyValue, altValue="", simID=0):
        if isinstance(keyName, str):
            if keyName in self.inVars.keys():
                raise KeyError("Keyname '%s' defined more than once." % keyName)
            else:
                self.inVars[keyName] = [keyValue,altValue,simID-1]
        else:
            raise ValueError("Keyname must be string.")
        return True

    def insertLattice(self, elemName, elemType, elemVals, refElem, refOffset=0):
        return True

    #
    #  Class Methods
    #

    def runSerial(self, numSim):
        if numSim <= 0:
            return False
        self.numSim = numSim
        self._initRun()
        self._prepareFolders()
        for simID in range(numSim):
            self._prepareSimulation(simID)
            self._processInputFile(simID)
            self._runSimulation(simID)
            self._finaliseSimulation(simID)
        self._endRun()
        return True

    #
    #  Internal Functions : Job
    #

    def _initRun(self):

        # Generate the jobnames
        jobExt = ""
        if self.outFormat == self.OUT_ARCH: jobExt = "tar.gz"
        if self.outFormat == self.OUT_HDF5: jobExt = "hdf5"
        for i in range(self.numSim):
            self.jobNames.append("%s.%05d.%s" % (self.outName,i+1,jobExt))
            self.runDir.append(None)

        # Generate the seeds
        seedKeys     = list(self.jobSeeds)
        self.numSeed = len(seedKeys)
        if self.partGen != self.GEN_NONE:
            self.numSeed += 1

        currSeed = self.firstSeed
        for i in range(self.numSeed * self.numSim):
            self.allSeeds.append(currSeed)
            currSeed += self.seedStep

        # Set up logfiles
        self.timeStamp = getTimeStamp()

        self.seedLog = open(self.LOG_SEED,mode="w")
        self.seedLog.write(" Seed Log\n")
        self.seedLog.write("==========\n")
        self.seedLog.write(" TimeStamp:  %s\n" % self.timeStamp)
        self.seedLog.write(" First Seed: %d\n" % self.firstSeed)
        self.seedLog.write(" Seed Step:  %d\n" % self.seedStep)
        self.seedLog.write("\n")
        self.seedLog.write(" {:<20} {:<10} {:<10} {:6} \n".format(
            "Job Name","Target","Seed","Value"
        ))
        self.seedLog.write("="*51+"\n")
        for i in range(self.numSim):
            for j in range(self.numSeed):
                k = i*self.numSeed + j
                if self.partGen != self.GEN_NONE and j == 0:
                    seedName = "PartDist"
                    seedType = "PartDist"
                else:
                    seedName = seedKeys[j-self.numSeed]
                    seedType = "SixTrack"
                self.seedLog.write(" {:<20} {:<10} {:<10} {:6d} \n".format(
                    self.jobNames[i],seedType,seedName,self.allSeeds[k]
                ))
        self.seedLog.write("\n")

        self.valLog = open(self.LOG_VALS,mode="w")
        self.valLog.write(" Input Values Log\n")
        self.valLog.write("==================\n")
        self.valLog.write(" TimeStamp:  %s\n" % self.timeStamp)
        self.valLog.write("\n")
        self.valLog.write(" {:<20} {:<16} {:<16} {:<16} {:<5} \n".format(
            "Job Name","File","Key","Value","Count"
        ))
        self.valLog.write("="*79+"\n")

        self.jobLog = open(self.LOG_JOB,mode="w")
        self.jobLog.write(" Job Log\n")
        self.jobLog.write("=========\n")
        self.jobLog.write(" TimeStamp: %s\n" % self.timeStamp)
        self.jobLog.write(" Particles: %d\n" % self.numPart)
        self.jobLog.write(" Turns:     %d\n" % self.numTurn)
        self.jobLog.write("\n")

        return True

    def _endRun(self):
        self.seedLog.close()
        self.valLog.close()
        self.jobLog.close()
        return True

    #
    #  Internal Functions : Simulation
    #

    def _prepareSimulation(self, simID):

        # Set up temp folder
        tmpDir = path.join(self.jobFolder, self.DIR_TEMP, "RunTmp.%d" % simID)
        if path.isdir(tmpDir):
            rmtree(tmpDir)
        mkdir(tmpDir)
        self.runDir[simID] = tmpDir

        # Run particle generator
        if self.partGen == self.GEN_COLL:
            pGen = PartDist(self.genParams)
            pGen.setSeed(self.allSeeds[simID*self.numSeed])
            pGen.genNormDist(int(self.numPart/2))
            pGen.writeCollDist(self.runDir[simID], int(self.numPart/2))

        return True

    def _runSimulation(self, simID):
        return True

    def _finaliseSimulation(self, simID):
        return True

    def _processInputFile(self, simID):

        toReplace = [
            ("%SIMNO%", str(simID+1)),
            ("%NPART%", str(self.numPart)),
            ("%NTURN%", str(self.numTurn)),
        ]

        if self.partGen != self.GEN_NONE:
            seedOne = 1
        else:
            seedOne = 0
        for seedNo in range(seedOne,self.numSeed):
            toReplace.append((
                self.jobSeeds[seedNo-seedOne],
                str(self.allSeeds[simID*self.numSeed+seedNo])
            ))

        for keyName in self.inVars.keys():
            keySpec = self.inVars[keyName]
            if keySpec[2] == -1 or keySpec[2] == simID:
                toReplace.append((keyName,keySpec[0]))
            else:
                toReplace.append((keyName,keySpec[1]))

        for fileName in self.inFiles.keys():
            if self.inFiles[fileName]:
                # Parse for search/replace
                inFile = open(path.join(self.jobFolder,fileName), mode="r")
                inBuff = inFile.read()
                inFile.close()
                for keyName, keyValue in toReplace:
                    nFound = inBuff.count(keyName)
                    if nFound == 0: continue
                    inBuff = inBuff.replace(keyName,keyValue)
                    self._logValues(simID, fileName, keyName, keyValue, nFound)
                outFile = open(path.join(self.runDir[simID],fileName), mode="w")
                outFile.write(inBuff)
                outFile.close()
            else:
                # Just copy them. No replace
                pass

        return True

    #
    #  Internal Functions : Utils and Wrappers
    #

    def _prepareFolders(self):
        tmpDir = path.join(self.jobFolder, self.DIR_TEMP)
        resDir = path.join(self.jobFolder, self.DIR_RESULT)
        if path.isdir(tmpDir):
            rmtree(tmpDir)
        if path.isdir(resDir):
            if len(listdir(resDir)) == 0:
                rmtree(resDir)
            else:
                raise FileExistsError("Results folder already exists and is not empty.")
        mkdir(tmpDir)
        mkdir(resDir)
        return True

    def _runShellCommand(self, callStr):
        sysP = subprocess.Popen([callStr], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdOut, stdErr = sysP.communicate()
        return stdOut.decode("utf-8"), stdErr.decode("utf-8"), sysP.returncode

    def _logValues(self, simID, fileName, keyName, keyValue, nFound):
        self.valLog.write(" {:<20} {:<16} {:<16} {:<16} {:5d} \n".format(
            self.jobNames[simID], fileName, keyName, keyValue, nFound
        ))
        return True

# END Class SixTrackJob
