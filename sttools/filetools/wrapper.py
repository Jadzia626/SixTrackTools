# -*- coding: utf-8 -*
"""SixTrack Simulation Folder Wrapper

  SixTrack Tools - Simulation Folder Wrapper
 ============================================
  A wrapper for a folder of simulation subfolders
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging
import numpy as np
import h5py

from os       import path, listdir, stat
from datetime import datetime

from sttools.functions         import parseKeyWordArgs
from sttools.filetools.colmaps import STColMaps
from sttools.filetools.stdump  import STDump

logger = logging.getLogger(__name__)

class FileWrapper():

    ORDERBY_NAME  = 0
    ORDERBY_VALID = [0]

    simList = [] # The list of accepted files, in order
    simMeta = {} # The meta data of the files
    simSets = [] # A list of all datasets across simulations
    iterIdx = 0  # Used for the iterator

    def __init__(self, simFolder, **theArgs):

        if path.isdir(simFolder):
            self.simFolder = simFolder
            logger.debug("Simulation folder is %s" % simFolder)
        else:
            raise FileNotFoundError("The folder '%s' does not exist." % simFolder)

        valArgs = {
            "orderBy"     : self.ORDERBY_NAME,
            "forceAccept" : False,
            "loadOnly"    : None,
            "isSingular"  : False,
        }
        kwArgs = parseKeyWordArgs(valArgs, theArgs)

        self.forceAccept = kwArgs["forceAccept"]
        self.loadOnly    = kwArgs["loadOnly"]
        self.isSingular  = kwArgs["isSingular"]
        if kwArgs["orderBy"] in self.ORDERBY_VALID:
            self.orderBy = kwArgs["orderBy"]
        else:
            logger.error("OrderBy value %d is invalid" % kwArgs["orderBy"])
            return

        self._scanFolder()

        return

    def __len__(self):
        return len(self.simList)

    def __contains__(self, simSet):
        if simSet in self.simList:
            return True
        else:
            return False

    def __getitem__(self, simSet):
        if isinstance(simSet, int):
            if abs(simSet) < len(self.simList):
                # We allow negative indices for looking backwards in the array
                simKey = self.simList[simSet]
            else:
                raise IndexError("Index value is out of range.")
        elif isinstance(simSet, str):
            if simSet in self.simList:
                simKey = simSet
            else:
                raise KeyError("Simulation key does not exist in this set.")
        else:
            raise KeyError("Key value must be either a string or an integer.")
        logger.info("Loading dataset '%s'" % (simKey))
        return SimWrapper(simKey,self.simMeta[simKey])

    def __iter__(self):
        self.iterIdx = 0
        return self.__getitem__[self.iterIdx]

    def __next__(self):
        self.iterIdx += 1
        if self.iterIdx >= len(self.simList):
            raise StopIteration
        else:
            return self.__getitem__[self.iterIdx]

    def __str__(self):
        return "SixTrack Simulation Data"

    #
    #  Class Methods
    #

    def checkDataSetKey(self, reqSet):
        """Check if a dataset exists and if necessary translate the key.
        """
        if reqSet in self.simSets:
            return reqSet
        else:
            reqSet = reqSet.lower()
            # Aperture
            if reqSet == "aperture_losses": return "aperture_losses.dat"
            # Collimation
            if reqSet == "all_absorptions": return "all_absorptions.dat"
            if reqSet == "all_impacts":     return "all_impacts.dat"
            if reqSet == "coll_scatter":    return "Coll_Scatter.dat"
            if reqSet == "coll_summary":    return "coll_summary.dat"
            if reqSet == "dist0":           return "dist0.dat"
            if reqSet == "distn":           return "distn.dat"
            if reqSet == "efficiency":      return "efficiency.dat"
            if reqSet == "efficiency_2d":   return "efficiency_2d.dat"
            if reqSet == "efficiency_dpop": return "efficiency_dpop.dat"
            if reqSet == "first_impacts":   return "FirstImpacts.dat"
            if reqSet == "survival":        return "survival.dat"
            # Scatter
            if reqSet == "scatter_log":     return "scatter_log.dat"
            if reqSet == "scatter_summary": return "scatter_summary.dat"
            return None

    #
    #  Internal Functions
    #

    def _scanFolder(self):
        """Scans a folder for simulation subfolders and builds a list of valid ones.
        A valid folder contains at least a fort.2 and fort.3 file.
        """

        self.simList = []
        self.simMeta = {}

        elemList = listdir(self.simFolder)
        sortList = []
        readList = []
        logger.info("Loading simulations from '%s'" % self.simFolder)

        if self.loadOnly is None:
            self.loadOnly = elemList.copy()

        for fName in elemList:
            fPath   = path.join(self.simFolder,fName)
            fStatus = "Checking item '%s'" % fName
            if fName[0] == ".":
                continue
            if path.isfile(fPath):
                logger.info("%-56s [Not a Simulation]" % fStatus)
                continue
            if fName not in self.loadOnly:
                logger.info("%-56s [Ignored]" % fStatus)
                continue
            if self.forceAccept:
                logger.info("%-56s [OK]" % fStatus)
            else:
                if path.isfile(path.join(fPath,"fort.2")) or path.isfile(path.join(fPath,"fort.3")):
                    logger.info("%-56s [OK]" % fStatus)
                else:
                    logger.info("%-56s [Not SixTrack]" % fStatus)
                    continue
            readList.append(fName)
            self.simMeta[fName] = {
                "SimPath"   : fPath,
                "SimName"   : fName,
                "DataFiles" : self._scanFiles(fPath),
                "DataSets"  : self._scanSets(fPath),
            }
            if self.orderBy == self.ORDERBY_NAME:
                sortList.append(fName)

        self.simList = [x for _,x in sorted(zip(sortList,readList))]

        return True

    def _scanFiles(self, simPath):
        """List all the files in a simulation folder.
        """
        elemList = listdir(simPath)
        fileList = []
        for fName in elemList:
            fPath = path.join(simPath,fName)
            if not path.isfile(fPath):
                continue
            fileList.append(fName)
        return fileList

    def _scanSets(self, simPath):
        """ToDo: Scan the files to check what they contain.
        For now, just return all files that are not input files or empty.
        """
        elemList = listdir(simPath)
        setsList = []
        inFiles  = ["fort.2","fort.3","fort.8","fort.13","fort.16"]
        for fName in elemList:
            fPath = path.join(simPath,fName)
            fStat = stat(fPath)
            if not path.isfile(fPath): continue
            if fStat.st_size == 0:     continue
            setsList.append(fName)
            if fName not in self.simSets:
                self.simSets.append(fName)
        return setsList

# END Class FileWrapper

class SimWrapper():

    def __init__(self, simName, simMeta):

        self.simName = simName
        self.simMeta = simMeta

        return

    def __contains__(self, dataSet):
        if dataSet in self.simMeta["DataSets"]:
            return True
        else:
            return False

    def __getitem__(self, dataSet):
        if dataSet not in self.simMeta["DataSets"]:
            return None
        dsPath  = path.join(self.simMeta["SimPath"],dataSet)
        tmpData = STDump(dsPath)
        tmpData.readAll()
        retData = {}
        if dataSet in STColMaps.MAP_COLS.keys():
            logger.debug("Remapping columns of datset '%s'" % dataSet)
            for colName in tmpData.colNames:
                logger.debug(" * %-20s = %-20s" % (colName,STColMaps.MAP_COLS[dataSet][colName]))
                retData[STColMaps.MAP_COLS[dataSet][colName]] = tmpData.allData[colName]
        else:
            logger.debug("Not remapping columns of datset '%s'" % dataSet)
            for colName in tmpData.colNames:
                retData[colName] = tmpData.allData[colName]
        return retData

# END Class SimWrapper
