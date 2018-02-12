# -*- coding: utf-8 -*
"""Fort.3 File Wrapper

  SixTrack Tools - Fort.3 File Wrapper
 ====================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

  Parses and manipulates the SixTrack fort.3 file

"""

import logging
import numpy   as np

from os import path

logger = logging.getLogger(__name__)

class Fort3():
    
    filePath   = None
    fileName   = None
    fileExists = None
    
    blockOrder = None # Original order of blocks
    blockData  = None # Data of blocks
    isGeom     = None # Treue for GEOM, False for FREE
    
    def __init__(self, filePath, fileName="fort.3"):
        
        self.fileExists = False
        
        self.blockOrder = []
        self.blockData  = {}
        
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
        
        fort3File = path.join(self.filePath,self.fileName)
        whatLine  = 0
        inBlock   = False
        hasEnde   = False
        
        with open(fort3File,"r") as inFile:
            for theLine in inFile:
                whatLine += 1
                theLine   = theLine.strip()
                
                # Skipping comment lines
                if theLine[0] == "/":
                    continue
                
                toCheck = theLine[0:4].upper()
                if not inBlock:
                    inBlock = True
                    if toCheck == "GEOM":
                        logger.info("Found GEOM keyword")
                        self.isGeom = True
                        inBlock = False
                    elif toCheck == "FREE":
                        logger.info("Found FREE keyword")
                        self.isGeom = False
                        inBlock = False
                    elif toCheck == "ENDE":
                        logger.info("Found ENDE keyword")
                        inBlock = False
                        hasEnde = True
                        break
                    else:
                        logger.info("Found %s block (not parsed)" % toCheck)
                else:
                    if toCheck == "NEXT":
                        logger.info("End of block")
                        inBlock = False
        
       
        return True
    
    def saveFile(self, savePath=None, saveFile="fort.3"):
        
        if savePath is None:
            savePath = self.filePath
        
        if not path.isdir(savePath):
            logger.error("Path not found: %s" & savePath)
            return False
        
        with open(path.join(savePath,saveFile),"w") as outFile:
            
            pass
        
        return True
        
# END Fort3
