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
from sttools.filetools.wrapper import FileWrapper, SimWrapper

from sttools.filetools.stdump  import STDump
from sttools.filetools.colmaps import STColMaps

# Logging
logger = logging.getLogger(__name__)

class DataSet():

    TYPE_FILE = 0
    TYPE_HDF5 = 1

    def __init__(self, dataSet, simData):

        self.simData  = simData
        self.dataSet  = simData.checkDataSetKey(dataSet)
        self.dataType = simData.dataType
    
        if self.dataType is None:
            raise TypeError("The simulation set is of an unknown type.")
        
        if self.dataSet is None:
            raise KeyError("The requested dataset '%s' does not exist." % dataSet)

        return

    def __len__(self):
        return len(self.simData)

    def __getitem__(self, simSet):
        stSim = self.simData[simSet]
        if self.dataSet in stSim:
            return stSim[self.dataSet]
        else:
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
            return self.simSet[oadIdx]
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
