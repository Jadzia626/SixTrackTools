# -*- coding: utf-8 -*
"""Python Toolbox for SixTrack, DataSet Wrapper

  SixTrack Tools - DataSet Wrapper
 ==================================
  Class to wrap both HDF5 and and file datasets
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging
import numpy as np

from os import path, listdir

from sttools.functions         import parseKeyWordArgs, checkValue
from sttools.h5tools.wrapper   import H5Wrapper
from sttools.filetools.stdump  import STDump
from sttools.filetools.colmaps import STColMaps

# Logging
logger = logging.getLogger(__name__)

class DataSet():

    TYPE_FILE = 0
    TYPE_HDF5 = 1

    def __init__(self, dataSet, **theArgs):

        self.initOK   = False
        self.dataSet  = dataSet
        self.fileList = []
        self.h5Set    = None

        valArgs = {
            "fileType"   : self.TYPE_FILE,
            "h5Set"      : None,
            "dataFolder" : None,
            "loadOnly"   : None,
        }
        kwArgs = parseKeyWordArgs(valArgs, theArgs)

        if   checkValue(kwArgs["fileType"], ["text",self.TYPE_FILE], False):
            self.fileType = self.TYPE_FILE
        elif checkValue(kwArgs["fileType"], ["hdf5",self.TYPE_HDF5], False):
            self.fileType = self.TYPE_HDF5
        else:
            logger.error("Unknown fileType specified.")
            return

        if self.fileType == self.TYPE_FILE:
            if isinstance(kwArgs["loadOnly"], str):
                loadOnly = kwArgs["loadOnly"].split(",")
            else:
                loadOnly = kwArgs["loadOnly"]
            dataFolder = kwArgs["dataFolder"]
            if not path.isdir(kwArgs["dataFolder"]):
                logger.error("Path not found: %s" % dataFolder)
                return
            dirList = listdir(dataFolder)
            if loadOnly is None:
                loadOnly = dirList.copy()
            for dirElem in dirList:
                setPath = path.join(dataFolder,dirElem)
                if path.isdir(setPath) and dirElem in loadOnly:
                    fPath = path.join(setPath,dataSet)
                    if path.isfile(fPath):
                        self.fileList.append(fPath)
                        logger.debug("Found %s" % fPath)
                    else:
                        logger.error("Cannot find the file: %s" % fPath)
                        return

        if self.fileType == self.TYPE_HDF5:
            if isinstance(kwArgs["h5Set"],H5Wrapper):
                self.h5Set = kwArgs["h5Set"]
            else:
                logger.error("Not a valid H5Wrapper object.")
                return

        self.initOK = True

        return

    def getNumSets(self):
        if self.fileType == self.TYPE_FILE:
            return len(self.fileList)
        if self.fileType == self.TYPE_HDF5 and self.h5Set is not None:
            return self.h5Set.nData
        return None

    def loadData(self, loadIdx=0):
        if self.fileType == self.TYPE_FILE:
            tmpData = STDump(self.fileList[loadIdx])
            tmpData.readAll()
            retData = {}
            if self.dataSet in STColMaps.MAP_COLS.keys():
                logger.debug("Remapping columns of datset '%s'" % self.dataSet)
                for colName in tmpData.colNames:
                    logger.debug(" * %-20s = %-20s" % (colName,STColMaps.MAP_COLS[self.dataSet][colName]))
                    retData[STColMaps.MAP_COLS[self.dataSet][colName]] = tmpData.allData[colName]
            else:
                logger.debug("Not remapping columns of datset '%s'" % self.dataSet)
                for colName in tmpData.colNames:
                    retData[colName] = tmpData.allData[colName]
            return retData
        if self.fileType == self.TYPE_HDF5:
            self.h5Set.loadDataSet(loadIdx)
            return self.h5Set.data[self.dataSet]
        return None

    def iterateData(self):
        if self.fileType == self.TYPE_FILE:
            for n in range(len(self.fileList)):
                yield self.loadData(n)
        if self.fileType == self.TYPE_HDF5 and self.h5Set is not None:
            for n in range(self.h5Set.nData):
                yield self.loadData(n)
        return None

# END Class DataSet
