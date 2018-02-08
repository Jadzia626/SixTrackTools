# -*- coding: utf-8 -*
"""Fort.2 File Wrapper

  SixTrack Tools - Fort.2 File Wrapper
 ====================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

  Parses and manipulates the SixTrack fort.2 file

"""

import logging
import numpy   as np

from os import path

logger = logging.getLogger(__name__)

class Fort2():
    
    filePath   = None
    fileName   = None
    fileExists = None
    
    elemData   = []
    blockData  = []
    structData = []
    
    def __init__(self, filePath, fileName="fort.2"):
        
        # Set constants and defaults
        self.nameElem   = "SINGLE ELEMENTS"
        self.nameBlock  = "BLOCK DEFINITIONS"
        self.nameStruct = "STRUCTURE INPUT"
        
        self.fileExists = False
        
        if path.isdir(filePath):
            self.filePath = filePath
        else:
            logger.error("Path not found: %s", filePath)
        
        if path.isfile(path.join(filePath,fileName)):
            self.fileName   = fileName
            self.fileExists = True
        else:
            logger.error("Found no %s file in path", fileName)
        
        return
    
    def loadFile(self):
        
        if not self.fileExists:
            logger.error("No valid file specified")
            return False
        
        fort2File = path.join(self.filePath,self.fileName)
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
                    self.structData.append(lineElems[:])
        
        return True
    
# END Fort2
