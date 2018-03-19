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
from .stdump  import STDump

logger = logging.getLogger(__name__)

class Concatenator:
    
    FTYPE_PART_DUMP = 100
    
    def __init__(self, outFile, doOverwrite=False):
        
        if path.isfile(outFile) and not doOverwrite:
            logger.error("File already exists and will not be overwritten.")
            return
        
        self.h5File = outFile
        
        if not path.isfile(outFile):
            with h5py.File(self.h5File, mode="w") as h5Out:
                h5Out.attrs.create("datasetsRead",0)
                h5Out.attrs.create("particleOffset",0)
        
        return
    
    def appendParticles(self, dataFile, fileType):
        
        stData = STDump(dataFile)
        stData.readAll()
        
        if fileType == self.FTYPE_PART_DUMP:
            bezVal = stData.metaData["BEZ"]
            nPart  = stData.metaData["NUMBER_OF_PARTICLES"]
            nLines = stData.nLines
            nTurns = int(nLines/nPart)
            logger.info("Reading particle data from bez = %s" % bezVal)
            partData = np.array()
                
            # with h5py.File(self.h5File, mode="r+") as h5Out:
                
        return False
    
# End Class Concatenator
