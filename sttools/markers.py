# -*- coding: utf-8 -*
"""Markers Parser

  SixTrack Tools - Markers Parser
 =================================
  Parses MadX to SixTrack fc.2 files and related
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging
import numpy   as np
import re

from os import path

logger = logging.getLogger(__name__)

class Markers:
    
    fileName   = None
    hasFile    = None
    
    elemData   = []
    blockData  = []
    structData = []
    
    def __init__(self, fileName):
        
        # Set constants and defaults
        self.nameElem   = "SINGLE ELEMENTS"
        self.nameBlock  = "BLOCK DEFINITIONS"
        self.nameStruct = "STRUCTURE INPUT"
        
        if path.isfile(fileName):
            self.fileName = fileName
            self.hasFile  = True
        else:
            logger.error("File not found: %s" % fileName)
            self.hasFile  = False
            return
        
        return
    
# END Class
    