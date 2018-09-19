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

from sttools.functions import parseKeyWordArgs, checkValue

# Logging
logger = logging.getLogger(__name__)

class DataSet():

    TYPE_FILE = 0
    TYPE_HDF5 = 1

    def __init__(self, dataSet, simData):

        self.simData  = simData
        self.dataSet  = simData.checkDataSetKey(dataSet)
        self.dataType = simData.dataType
        self.iterIdx  = 0

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

# END Class DataSet
