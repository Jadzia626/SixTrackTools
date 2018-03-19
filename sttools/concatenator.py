# -*- coding: utf-8 -*
"""SixTrack Concatenat0r

  SixTrack Tools - Concatenat0r
 ===============================
  Collects Simulation Data into HDF5 File
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging
import numpy   as np
import h5py

from os import path

from .tablefs import TableFS

logger = logging.getLogger(__name__)

class Concatenator:
    
    h5File = None
    
    def __init__(self, outFile, doOverwrite=False):
        
        if path.isfile(outFile) and not doOverwrite:
            logger.error("File already exists and will not be overwritten.")
            return
        
        self.h5File     = outFile
        
        self.partOffset = 0
        
        if path.isfile(outFile):
            self.readMeta()
        
        return
    
    def initFile(self):
        
        with h5py.File(self.h5File, mode="w") as h5Out:
            h5Meta = h5Out.create_group("meta")
            h5Meta.create_dataset("partOffset",0)
        
        return True
    
    def readMeta(self):
        return True
    
    

# End Class Concatenator
