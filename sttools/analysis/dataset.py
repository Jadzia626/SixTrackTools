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

from os import path

from sttools.functions       import parseKeyWordArgs, checkValue
from sttools.h5tools.wrapper import H5Wrapper

# Logging
logger = logging.getLogger(__name__)

class DataSet():

    TYPE_FILE = 0
    TYPE_HDF5 = 1

    # Holds the loaded data as a numpy dict
    data = None

    def __init__(self, dataSet, **theArgs):

        self.dataSet  = dataSet
        self.fileList = []

        valArgs = {
            "fileType"    : self.TYPE_FILE,
            "h5Set"       : None,
            "dataFolders" : [],
        }
        kwArgs = parseKeyWordArgs(valArgs, theArgs)

        if   checkValue(kwArgs["fileType"], ["text",self.TYPE_FILE], False):
            self.fileType = self.TYPE_FILE
        elif checkValue(kwArgs["fileType"], ["hdf5",self.TYPE_HDF5], False):
            self.fileType = self.TYPE_HDF5
        else:
            logger.error("Unknown fileType specified.")
            exit(1)

        if self.fileType == self.TYPE_FILE:
            if isinstance(kwArgs["dataFolders"], str):
                self.dataFolders = [kwArgs["dataFolders"]]
            else:
                self.dataFolders = kwArgs["dataFolders"]
            for dataFolder in self.dataFolders:
                fPath = path.join(dataFolder,dataSet)
                if path.isfile(fPath):
                    self.fileList.append(fPath)
                else:
                    logger.error("Cannot find the file: %s" % fPath)
                    exit(1)

        if self.fileType == self.TYPE_HDF5:
            if isinstance(kwArgs["h5Set"],H5Wrapper):
                self.h5Set = kwArgs["h5Set"]
            else:
                logger.error("Not a valid H5Wrapper object.")
                exit(1)

        return

    def loadData(self, startIdx=0, endIdx=0):
        nSets = endIdx-startIdx+1
        if nSets <= 0:
            logger.error("Your range of datasets to load makes no sense. Is endIdx >= startIdx?")
            return False
        if self.fileType == self.TYPE_HDF5:
            self.__loadDataHDF5(startIdx, endIdx)

    def __loadDataHDF5(self, startIdx, endIdx):

        self.h5Set.loadDataSet(startIdx)
        self.data = self.h5Set.data[self.dataSet]

        if endIdx == startIdx:
            return

        for s in range(startIdx+1,endIdx):
            self.h5Set.loadDataSet(startIdx)
            tmpData = self.h5Set.data[self.dataSet]
            print(list(tmpData.keys()))


# END Class Beams
