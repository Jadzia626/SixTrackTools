# -*- coding: utf-8 -*
"""SixTrack Concatenat0r

  SixTrack Tools - Concatenat0r
 ===============================
  Collects Simulation Data from Multiple DataSets
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
    
    def __init__(self, inFolder, fileFilter=None):
        
        if not path.isdir(inFolder):
            logger.error("Path not found: %s" % inFolder)
            return
        
        
        
        return
    
# End Class Concatenator
