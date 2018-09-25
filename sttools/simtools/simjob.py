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
import asyncio
import subprocess
import concurrent.futures

from os      import path, mkdir, listdir
from shutil  import rmtree, copy2
from zipfile import ZipFile
from time    import time
from math    import floor, log10

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
        self.doCleanup = True                    # Delete run folder(s) after execution
        self.stdJobLog = False                   # Print content of job log to stdout

        # Runtime Stuff
        self.timeStamp = ""
        self.seedLog   = None
        self.jobLog    = None
        self.valLog    = None
        self.allSeeds  = []
        self.numSeed   = 0
        self.numSim    = 0
        self.numThread = 0
        self.jobNames  = []
        self.runDir    = []
        self.outLog    = []
        self.errLog    = []
        self.simOut    = []
        self.textBuff  = {}
        self.runStart  = 0.0
        self.cpuTime   = []
        self.simExit   = []

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

    def setCleanup(self, doClean):
        if isinstance(doClean, bool):
            self.doCleanup = doClean
        else:
            raise ValueError("setCleanup takes a boolean argument.")
        return True

    def setEchoJobLog(self, stdJobLog):
        if isinstance(stdJobLog, bool):
            self.stdJobLog = stdJobLog
        else:
            raise ValueError("setEchoJobLog takes a boolean argument.")
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

    def addInputFile(self, fileList, replaceQueue=False):
        """Adds a file that will be copied to the simulation folder before execution. If the
        replaceQueue flag is True, it will also apply all simulation value entries to the file.
        """
        inFiles = []
        if isinstance(fileList, str):
            inFiles.append(fileList)
        else:
            inFiles = fileList
        for fileName in inFiles:
            fullPath = path.join(self.jobFolder, fileName)
            if path.isfile(fullPath):
                if fileName not in self.inFiles.keys():
                    self.inFiles[fileName] = replaceQueue
            else:
                raise FileNotFoundError("No file named '%s' in job folder." % fileName)
        return True

    def addOutputFile(self, fileList):
        if isinstance(fileList, str):
            self.outFiles.append(fileList)
        else:
            self.outFiles += fileList
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
            logger.warning("Requested %d simulation jobs. I don't know how to do that ..." % numSim)
            return False
        self.numSim    = numSim
        self.numThread = 1
        self._initRun()
        self._prepareFolders()
        for simID in range(numSim):
            logger.info("")
            logger.info("Starting Simulation: %5d/%d" % (simID+1,numSim))
            logger.info("="*80)
            self._logJobStart(simID)
            prTime = 0.0
            prTime        += self._prepareSimulation(simID)
            prTime        += self._processInputFile(simID)
            exTime,exCode  = self._runSimulation(simID)
            prTime        += self._finaliseSimulation(simID)
            self._logJobEnd(simID,exTime,exCode)
            logger.info("-"*80)
            logger.info("Execution Time: %12.3f seconds" % (exTime+prTime))
        self._endRun()
        return True

    def runParallel(self, numSim, numThreads):
        if numThreads <= 0:
            logger.warning("Requested %d simulation threads. I don't know how to do that ..." % numThreads)
            return False
        if numSim <= 0:
            logger.warning("Requested %d simulation jobs. I don't know how to do that ..." % numSim)
            return False
        self.numSim    = numSim
        self.numThread = numThreads
        self._initRun()
        self._prepareFolders()
        sExec = concurrent.futures.ThreadPoolExecutor(max_workers=numThreads)
        sLoop = asyncio.get_event_loop()
        try:
            sLoop.run_until_complete(self._jobThreader(sExec))
        finally:
            sLoop.close()
        self._endRun()
        return True

    #
    #  Internal Functions : Job (Threaded)
    #

    async def _jobThreader(self, sExec):
        sTasks = []
        sLoop  = asyncio.get_event_loop()
        for simID in range(self.numSim):
            sTasks.append(sLoop.run_in_executor(sExec, self._jobWorker, simID))
        await asyncio.wait(sTasks)
        return True

    def _jobWorker(self, simID):
        self._logJobStart(simID)
        logger.info("Starting Simulation: %5d/%d" % (simID+1,self.numSim))
        prTime         = 0.0
        prTime        += self._prepareSimulation(simID)
        prTime        += self._processInputFile(simID)
        exTime,exCode  = self._runSimulation(simID)
        prTime        += self._finaliseSimulation(simID)
        logger.info("Finished Simulation: %5d/%d in %12.3f seconds" % (simID+1,self.numSim,exTime+prTime))
        self._logJobEnd(simID,exTime,exCode)
        return True

    #
    #  Internal Functions : Job
    #

    def _initRun(self):
        self.runStart = time()

        # Generate the jobnames
        jobExt = ""
        if self.outFormat == self.OUT_ARCH: jobExt = ".zip"
        if self.outFormat == self.OUT_HDF5: jobExt = ".hdf5"
        for i in range(self.numSim):
            self.jobNames.append("%s.%05d%s" % (self.outName,i+1,jobExt))
            self.outLog.append("stdOut.%05d.log"   % (i+1))
            self.errLog.append("stdErr.%05d.log"   % (i+1))
            self.simOut.append("simFiles.%05d.zip" % (i+1))
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
        self.seedLog.flush()

        self.valLog = open(self.LOG_VALS,mode="w")
        self.valLog.write(" Input Values Log\n")
        self.valLog.write("==================\n")
        self.valLog.write(" TimeStamp:  %s\n" % self.timeStamp)
        self.valLog.write("\n")
        self.valLog.write(" {:<20} {:<16} {:<16} {:<16} {:<5} \n".format(
            "Job Name","File","Key","Value","Count"
        ))
        self.valLog.write("="*79+"\n")
        self.valLog.flush()
        self.textBuff["valLog"] = {}

        jobLog = []
        self.jobLog = open(self.LOG_JOB,mode="w")
        jobLog.append("")
        jobLog.append(" Running Simulations")
        jobLog.append("=====================")
        jobLog.append(" TimeStamp: %s" % self.timeStamp)
        jobLog.append(" Particles: %d" % self.numPart)
        jobLog.append(" Turns:     %d" % self.numTurn)
        jobLog.append("")
        for jobLine in jobLog:
            self.jobLog.write(jobLine+"\n")
            if self.stdJobLog: print(jobLine)

        return True

    def _endRun(self):
        nFailed   = sum(self.simExit)
        nSuccess  = self.numSim-nFailed
        totTime   = sum(self.cpuTime)
        runTime   = time()-self.runStart
        jobStatus = []
        jobStatus.append("")
        jobStatus.append(" Job Summary")
        jobStatus.append("=============")
        jobStatus.append(" Completed: %7d    simulation(s)" % nSuccess)
        jobStatus.append(" Failed:    %7d    simulation(s)" % nFailed)
        jobStatus.append(" Run Setup: %7d    thread(s)"     % self.numThread)
        jobStatus.append(" CPU Time:  %10.2f seconds"       % totTime)
        jobStatus.append(" Run Time:  %10.2f seconds"       % runTime)
        jobStatus.append("")
        for jobLine in jobStatus:
            self.jobLog.write(jobLine+"\n")
            if self.stdJobLog: print(jobLine)
        self.seedLog.close()
        self.valLog.close()
        self.jobLog.close()
        return True

    #
    #  Internal Functions : Simulation
    #

    def _prepareSimulation(self, simID):
        tStart = time()

        # Set up temp folder
        tmpDir = path.join(self.jobFolder, self.DIR_TEMP, "RunTmp.%d" % (simID+1))
        if path.isdir(tmpDir):
            rmtree(tmpDir)
        mkdir(tmpDir)
        self.runDir[simID] = tmpDir
        copy2(path.join(self.jobFolder,self.execName),self.runDir[simID])

        # Run particle generator
        if self.partGen == self.GEN_COLL:
            pGen = PartDist(self.genParams)
            pGen.setSeed(self.allSeeds[simID*self.numSeed])
            pGen.genNormDist(int(self.numPart/2))
            pGen.writeCollDist(self.runDir[simID], int(self.numPart/2))

        return time()-tStart

    def _runSimulation(self, simID):
        tStart  = time()
        execCmd = "./"+self.execName
        logger.info("Running: %s" % execCmd)
        stdOut, stdErr, exCode = self._runShellCommand(execCmd,self.runDir[simID])
        if exCode == 0:
            logger.info("Simulation completed without errors")
        else:
            logger.error("Simulation exited with error code %d" % exCode)
        with open(path.join(self.runDir[simID],self.outLog[simID]),mode="w") as outLog:
            outLog.write(stdOut)
        with open(path.join(self.runDir[simID],self.errLog[simID]),mode="w") as errLog:
            errLog.write(stdErr)
        return time()-tStart, exCode

    def _finaliseSimulation(self, simID):
        tStart = time()
        resDir = path.join(self.jobFolder, self.DIR_RESULT)
        if self.outFormat == self.OUT_HDF5:
            copy2(path.join(self.runDir[simID], self.jobNames[simID]),resDir)
        copy2(path.join(self.runDir[simID], self.outLog[simID]),resDir)
        copy2(path.join(self.runDir[simID], self.errLog[simID]),resDir)
        if len(self.outFiles) == 0:
            logger.info("Not keeping any text output files")
        else:
            if self.outFiles[0] == "*":
                keepThese = listdir(self.runDir[simID])
            else:
                keepThese = self.outFiles
            if self.outFormat != self.OUT_PLAIN:
                zOut = ZipFile(path.join(resDir, self.simOut[simID]),"w")
            else:
                simRes = path.join(resDir, self.jobNames[simID])
                mkdir(simRes)
            for outFile in keepThese:
                toKeep = path.join(self.runDir[simID], outFile)
                if path.isfile(toKeep):
                    if self.outFormat != self.OUT_PLAIN:
                        logger.info("Archiving file '%s' ..." % outFile)
                        zOut.write(toKeep,arcname=outFile)
                    else:
                        logger.info("Saving file '%s' ..." % outFile)
                        copy2(toKeep,simRes)
                elif path.isdir(toKeep):
                    logger.warning("Not a file '%s', skipping" % outFile)
                else:
                    logger.warning("Could not find file '%s' in run folder" % outFile)
            if self.outFormat != self.OUT_PLAIN:
                zOut.close()
        if self.doCleanup:
            rmtree(self.runDir[simID])
        return time()-tStart

    def _processInputFile(self, simID):
        tStart = time()
        toReplace = {
            "%SIMNO%"  : str(simID+1),
            "%NPART%"  : str(self.numPart),
            "%NPAIR%"  : str(int(self.numPart/2)),
            "%NTURN%"  : str(self.numTurn),
            "%H5FILE%" : self.jobNames[simID],
            "%H5ROOT%" : "/",
        }

        if self.partGen != self.GEN_NONE:
            seedOne = 1
        else:
            seedOne = 0
        for seedNo in range(seedOne,self.numSeed):
            toReplace[self.jobSeeds[seedNo-seedOne]] = str(self.allSeeds[simID*self.numSeed+seedNo])

        for keyName in self.inVars.keys():
            keySpec = self.inVars[keyName]
            if keySpec[2] == -1 or keySpec[2] == simID:
                toReplace[keyName] = keySpec[0]
            else:
                toReplace[keyName] = keySpec[1]

        for fileName in self.inFiles.keys():
            nReplace = 0
            if self.inFiles[fileName]:
                # Parse for search/replace
                inFile = open(path.join(self.jobFolder,fileName), mode="r")
                inBuff = inFile.read()
                inFile.close()
                for keyName in toReplace.keys():
                    nFound = inBuff.count(keyName)
                    if nFound == 0: continue
                    inBuff = inBuff.replace(keyName,toReplace[keyName])
                    self._logValues(simID, fileName, keyName, toReplace[keyName], nFound)
                    nReplace += 1
                outFile = open(path.join(self.runDir[simID],fileName), mode="w")
                outFile.write(inBuff)
                outFile.close()
                if nReplace == 0:
                    self._logValuesCopy(simID, fileName)
            else:
                copy2(path.join(self.jobFolder,fileName),self.runDir[simID])
                self._logValuesCopy(simID, fileName)

        self._logValuesNext(simID)
        return time()-tStart

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

    def _runShellCommand(self, callStr, callDir):
        sysP = subprocess.Popen([callStr], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=callDir)
        stdOut, stdErr = sysP.communicate()
        return stdOut.decode("utf-8"), stdErr.decode("utf-8"), sysP.returncode

    def _logValues(self, simID, fileName, keyName, keyValue, nFound):
        if not simID in self.textBuff["valLog"]:
            self.textBuff["valLog"][simID] = ""
        self.textBuff["valLog"][simID] += " {:<20} {:<16} {:<16} {:<16} {:5d} \n".format(
            self.jobNames[simID], fileName, keyName, keyValue, nFound
        )
        return True

    def _logValuesCopy(self, simID, fileName):
        if not simID in self.textBuff["valLog"]:
            self.textBuff["valLog"][simID] = ""
        self.textBuff["valLog"][simID] += " {:<20} {:<16} {:<4} \n".format(
            self.jobNames[simID], fileName, "NONE"
        )
        return True

    def _logValuesNext(self, simID):
        self.valLog.write(self.textBuff["valLog"][simID])
        self.valLog.write("-"*79+"\n")
        self.valLog.flush()
        return True

    def _logJobStart(self, simID):
        nDigit   = int(floor(log10(self.numSim)))+1
        fmtCount = "{:%dd}/{:<%dd}" % (nDigit,nDigit)
        logStr   = (" "+fmtCount+" Start"+(" "*nDigit)+" {:}").format(
            simID+1, self.numSim, self.jobNames[simID]
        )
        self.jobLog.write(logStr+"\n")
        self.jobLog.flush()
        if self.stdJobLog:
            print(logStr)
        return True

    def _logJobEnd(self, simID, simTime, exCode):
        if exCode == 0:
            exStatus = "Completed"
            self.simExit.append(0)
        else:
            exStatus = "Failed %d" % exCode
            self.simExit.append(1)
        nDigit   = int(floor(log10(self.numSim)))+1
        fmtCount = "{:<%dd}" % (nDigit)
        logStr   = ((" "*2*nDigit)+"   Sim #"+fmtCount+" {:.<40}  {:<10}  {:8.2f} sec").format(
            simID+1, self.jobNames[simID]+" ", exStatus, simTime
        )
        self.jobLog.write(logStr+"\n")
        self.jobLog.flush()
        self.cpuTime.append(simTime)
        if self.stdJobLog:
            print(logStr)
        return

# END Class SixTrackJob
