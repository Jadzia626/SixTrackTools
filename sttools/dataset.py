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

from sttools.functions  import parseKeyWordArgs, checkValue
from sttools.simulation import SixTrackSim

# Logging
logger = logging.getLogger(__name__)

class DataSet():

    simData = None # A SixTrackSim object
    dataSet = None # The dataset this wrapper is accessing
    iterIdx = 0

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
        self._checkValid()
        return len(self.simData)

    def __contains__(self, simSet):
        self._checkValid()
        if self.dataSet in stSim:
            return True
        else:
            return False

    def __getitem__(self, simSet):
        self._checkValid()
        stSim = self.simData[simSet]
        if self.dataSet in stSim:
            return stSim[self.dataSet]
        else:
            return None

    def __iter__(self):
        self._checkValid()
        self.iterIdx = 0
        return self

    def __next__(self):
        self._checkValid()
        self.iterIdx += 1
        if self.iterIdx > len(self.simData):
            self.iterIdx -= 1
            raise StopIteration
        else:
            return self.__getitem__(self.iterIdx-1)

    def __enter__(self):
        self._checkValid()
        return self

    def __exit__(self, *exArgs):
        self._checkValid()
        self.simData.close()

    def _checkValid(self):
        if self.simData is None:
            raise ValueError("No simulation loaded.")
        elif self.dataSet is None:
            raise ValueError("No dataset loaded.")

# END Class DataSet
