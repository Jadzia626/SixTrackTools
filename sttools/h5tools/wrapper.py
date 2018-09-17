# -*- coding: utf-8 -*
"""SixTrack HDF5 File Wrapper

  SixTrack Tools - HDF5 File Wrapper
 ====================================
  A wrapper for a folder of HDF5 files
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging
import numpy as np
import h5py

from os       import path, listdir
from datetime import datetime

from sttools.functions     import pPrintDict, parseKeyWordArgs
from sttools.h5tools.utils import H5Utils

logger = logging.getLogger(__name__)

class H5Wrapper():

    ORDERBY_SIMNO = 0
    ORDERBY_NAME  = 1
    ORDERBY_TIME  = 2

    ORDERBY_VALID = [0,1,2]

    fileList = []   # The list of accepted files, in order
    fileMeta = {}   # The meta data of the files
    data     = None # Holding the currently loaded data
    currIdx  = 0    # The index of the currently loaded data
    nData    = 0    # Number of data files

    def __init__(self, dataFolder, **theArgs):

        if not path.isdir(dataFolder):
            logger.error("Path not found: %s" % dataFolder)
            return

        valArgs = {
            "orderBy"     : self.ORDERBY_SIMNO,
            "forceAccept" : False,
            "loadOnly"    : None,
        }
        kwArgs = parseKeyWordArgs(valArgs, theArgs)

        self.dataFolder  = dataFolder
        self.forceAccept = kwArgs["forceAccept"]
        self.loadOnly    = kwArgs["loadOnly"]
        if kwArgs["orderBy"] in self.ORDERBY_VALID:
            self.orderBy = kwArgs["orderBy"]
        else:
            logger.error("OrderBy value %d is invalid" % kwArgs["orderBy"])
            return

        self.scanFolder()

        return

    def scanFolder(self):
        """Scans a folder for HDF5 files and builds a list of valid ones.
        A valid file contains a "CreatedBy" field that states the file was written by SixTrack.
        """

        self.fileList = []
        self.fileMeta = {}

        fileList = listdir(self.dataFolder)
        sortList = []
        readList = []
        logger.info("Loading files from '%s'" % self.dataFolder)

        if self.loadOnly is None:
            self.loadOnly = fileList.copy()

        for fName in fileList:
            fBase, fExt = path.splitext(fName)
            fPath       = path.join(self.dataFolder,fName)
            fStatus     = "Checking file '%s'" % fName
            if fName not in self.loadOnly:
                logger.info("%-56s [Ignored]" % fStatus)
                continue
            try:
                fH5 = h5py.File(fPath,"r")
            except:
                logger.info("%-56s [Not HDF5]" % fStatus)
                continue
            if not self.forceAccept and not H5Utils.getAttrString(fH5,"CreatedBy")[:8] == "SixTrack":
                logger.info("%-56s [Not SixTrack]" % fStatus)
                continue
            logger.info("%-56s [OK]" % fStatus)
            timeStamp = H5Utils.getAttrString(fH5,"TimeStamp")
            self.nData += 1
            self.fileMeta[fBase] = {
                "TimeStamp"  : timeStamp,
                "NumTime"    : datetime.strptime(timeStamp,"%Y-%m-%dT%H:%M:%S.%f").timestamp(),
                "CreatedBy"  : H5Utils.getAttrString(fH5,"CreatedBy"),
                "SimNumber"  : fH5.attrs["SimNumber"][0],
                "Particles"  : fH5.attrs["Particles"][0],
                "Turns"      : fH5.attrs["Turns"][0],
                "PreTime"    : fH5.attrs["PreTime"][0],
                "TrackTime"  : fH5.attrs["TrackTime"][0],
                "PostTime"   : fH5.attrs["PostTime"][0],
                "TotalTime"  : fH5.attrs["TotalTime"][0],
                "FileName"   : fName,
                "FilePath"   : fPath,
                "SimName"    : fBase,
            }
            readList.append(fBase)
            if   self.orderBy == self.ORDERBY_SIMNO:
                sortList.append(self.fileMeta[fBase]["SimNumber"])
            elif self.orderBy == self.ORDERBY_NAME:
                sortList.append(fBase)
            elif self.orderBy == self.ORDERBY_TIME:
                sortList.append(self.fileMeta[fBase]["NumTime"])

        self.fileList = [x for _,x in sorted(zip(sortList,readList))]

        fH5.close()

        return True

    #
    # Loading and Closing of DataSets
    #

    def loadDataSet(self, setIdx=0):
        if abs(setIdx) < self.nData:
            # We allow negative indices for looking backwards in the array
            fPath = self.fileMeta[self.fileList[setIdx]]["FilePath"]
            fName = self.fileMeta[self.fileList[setIdx]]["FileName"]
            self.data    = h5py.File(fPath,"r")
            self.currIdx = setIdx
            logger.info("Loading dataset %d: %s" % (setIdx,fName))
            return True
        else:
            logger.error("No dataset with index %d" % setIdx)
            return False
    
    def loadNext(self):
        self.currIdx += 1
        if self.currIdx >= self.nData:
            logger.debug("You have already reached the last dataset.")
            return False
        return self.loadDataSet(self.currIdx)

    def loadPrev(self):
        self.currIdx -= 1
        if self.currIdx < 0:
            logger.debug("You have already reached the first dataset.")
            return False
        return self.loadDataSet(self.currIdx)

    def loadFirst(self):
        return self.loadDataSet(0)

    def loadLast(self):
        return self.loadDataSet(-1)

    def closeDataSet(self):
        self.data.close()
        return True

    #
    # print Information
    #

    def printSummary(self):

        print(" Simulation Summary")
        print("====================")
        print("Path: %s" % self.dataFolder)
        print("")

        print("{:20} {:20} {:>9} {:>9}".format("Simulation","Software","Particles","Turns"))
        print("-"*61)
        for h5Set in self.fileList:
            print("{SimName:20} {CreatedBy:20} {Particles:9d} {Turns:9d}".format(**self.fileMeta[h5Set]))

        return

# END Class H5Wrapper
