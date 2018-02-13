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
    isEnded    = None # Whether ENDE keyword has been encountered
    
    def __init__(self, filePath, fileName="fort.3"):
        
        self.fileExists = False
        
        self.blockOrder = []
        self.blockData  = {}
        self.isEnded    = False
        
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
        
        fort3File  = path.join(self.filePath,self.fileName)
        whatLine   = 0
        inBlock    = False
        currBlock  = ""
        blockBuff  = []
        noNext     = ["GEOM","FREE","PRIN"]
        
        with open(fort3File,"r") as inFile:
            for theLine in inFile:
                whatLine += 1
                theLine   = theLine.strip()
                toCheck   = theLine[0:4].upper()
                
                # Skipping comment lines
                if theLine[0] == "/":
                    continue
                
                blockBuff.append(theLine)
                
                if not inBlock:
                    if toCheck in noNext:
                        self.blockOrder.append(toCheck)
                        self.blockData[toCheck] = {}
                        self.blockData[toCheck]["Lines"] = blockBuff
                        inBlock   = False
                        blockBuff = []
                    else:
                        self.blockOrder.append(toCheck)
                        self.blockData[toCheck] = {}
                        inBlock   = True
                        currBlock = toCheck
                else:
                    if toCheck == "NEXT":
                        self.blockData[currBlock]["Lines"] = blockBuff
                        inBlock   = False
                        blockBuff = []
                    elif toCheck == "ENDE":
                        self.isEnded = True
                        break
        
        return True
    
    def saveFile(self, savePath=None, saveFile="fort.3"):
        
        if savePath is None:
            savePath = self.filePath
        
        if not path.isdir(savePath):
            logger.error("Path not found: %s" & savePath)
            return False
        
        with open(path.join(savePath,saveFile),"w") as outFile:
            for theBlock in self.blockOrder:
                if "Lines" in self.blockData[theBlock].keys():
                    for theLine in self.blockData[theBlock]["Lines"]:
                        outFile.write(theLine+"\n")
                elif theBlock == "ENDE":
                    outFile.write("ENDE\n")
                else:
                    logger.error("Empty block encountered in buffer")
        
        return True
    
    def appendToBlock(self, whichBlock, whichLine, newData):
        
        if not whichBlock in self.blockOrder:
            logger.error("No block named %s found" % whichBlock)
            return False
        
        if not "Lines" in self.blockData[whichBlock].keys():
            logger.error("No block data for block %s" % whichBlock)
            return False
        
        nLines = len(self.blockData[whichBlock]["Lines"])
        if whichLine == -1:
            whichLine = nLines-1
        if whichLine <= 0 or whichLine > nLines-1:
            logger.error("Line number out of bounds")
            logger.error("Valid range is 1 to %d or -1 for end" % (nLines-1))
            return False
        
        self.blockData[whichBlock]["Lines"].insert(whichLine,newData)
        
        return True
    
# END Fort3
