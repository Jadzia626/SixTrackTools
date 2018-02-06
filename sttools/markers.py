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
    
    inPath     = None
    
    elemData   = []
    blockData  = []
    structData = []
    
    def __init__(self, inPath):
        
        # Set constants and defaults
        self.nameElem   = "SINGLE ELEMENTS"
        self.nameBlock  = "BLOCK DEFINITIONS"
        self.nameStruct = "STRUCTURE INPUT"
        
        if path.isdir(inPath):
            self.inPath = inPath
        else:
            logger.error("Path not found or not a folder: %s" % inPath)
            return
        
        return
    
    def readFort2(self):
        
        if self.inPath is None:
            logger.error("No path specified.")
            return False
        
        fort2File = path.join(self.inPath,"fort.2")
        
        if not path.isfile(fort2File):
            logger.error("No fort.2 file found in %s" % self.inPath)
            return False
        
        whatStage = 0
        with open(fort2File,"r") as inFile:
            for theLine in inFile:
                if   theLine[0:15] == self.nameElem:
                    whatStage = 1
                    logger.info("Parsing single elements ...")
                    continue
                elif theLine[0:17] == self.nameBlock:
                    whatStage = 2
                    logger.info("Parsing block definitions ...")
                    continue
                elif theLine[0:15] == self.nameStruct:
                    whatStage = 3
                    logger.info("Parsing structure inputs ...")
                    continue
                elif theLine[0:4]  == "NEXT":
                    whatStage = 0
                    
                if   whatStage == 1:
                    continue
                elif whatStage == 2:
                    continue
                elif whatStage == 3:
                    lineElems = theLine.split()
                    arrStruct.append(lineElems[e])
            
        
        return True
    
# END Class
    