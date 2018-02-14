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
    
    # Block Settings: Long Name, Required Fields (format), Optional Fields (format)
    blockSettings = {
        "LIMI" : ["LIMITATIONS","SSFFFFFFF",""],
        "DUMP" : ["DUMP",       "SIII",     "SII"],
    }
    
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
                        self.blockData[toCheck] = {
                            "LongName" : theLine.replace("-"," ").strip(),
                            "Lines"    : [],
                            "Data"     : [],
                        }
                        self.blockData[toCheck]["Lines"] = blockBuff
                        inBlock   = False
                        blockBuff = []
                    else:
                        self.blockOrder.append(toCheck)
                        self.blockData[toCheck] = {
                            "LongName" : theLine.replace("-"," ").strip(),
                            "Lines"    : [],
                            "Data"     : [],
                        }
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
        
        # Functions for serialisation, where they exist
        serBlock = {
            "LIMI" : self.serialiseLIMI,
            "DUMP" : self.serialiseDUMP,
        }
        
        with open(path.join(savePath,saveFile),"w") as outFile:
            for theBlock in self.blockOrder:
                if theBlock in serBlock.keys():
                    longName = self.blockData[theBlock]["LongName"]
                    outFile.write(longName+"-"*(72-len(longName))+"\n")
                    for theList in self.blockData[theBlock]["Data"]:
                        outFile.write(serBlock[theBlock](theList)+"\n")
                    outFile.write("NEXT\n")
                if theBlock == "ENDE":
                    outFile.write("ENDE\n")
                elif "Lines" in self.blockData[theBlock].keys():
                    for theLine in self.blockData[theBlock]["Lines"]:
                        outFile.write(theLine+"\n")
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
    
    def newBlock(self, shortName, longName=None):
        
        if shortName in self.blockOrder:
            logger.error("Block %s already exists" & shortName)
            return False
        
        if longName is None:
            longName = shortName
        
        self.blockOrder.insert(len(self.blockOrder)-1,shortName)
        self.blockData[shortName] = {
            "LongName" : longName,
            "Lines"    : [],
            "Data"     : [],
        }
        
        logger.info("Added block %s" % shortName)
        
        return True
    
    #
    # Blocks
    #
    
    def addBlockFromFile(self, blockName, blockPath, blockFile):
        """
        Adds a new block, line by line, from a file.
        If the block does not exist, it's created.
        """
        
        filePath = path.join(blockPath,blockFile)
        
        if not path.isfile(filePath):
            logger.error("File not found %s" % filePath)
            return False
        
        longName = self.blockSettings[blockName][0]
        blockFmt = self.blockSettings[blockName][1]
        blockOpt = self.blockSettings[blockName][2]
        
        if not blockName in self.blockOrder:
            self.newBlock(blockName,longName)
            
        lineNo = 0
        with open(filePath,"r") as inFile:
            for theLine in inFile:
                lineNo += 1
                theLine = theLine.strip()
                if theLine[:4] in [blockName,"NEXT"]: continue
                if theLine[:1] == "/": continue
                theList = self.splitBlockLine(theLine,blockFmt,blockOpt)
                if theList is not None:
                    self.blockData[blockName]["Data"].append(theList)
                else:
                    logger.warning("Invalid entry on line %d" % lineNo)
        
        return True
    
    def addBlockLineFromString(self, blockName, newLine):
        """
        Adds a line to a block from a string.
        Only valid for blocks known to the Fort3 class.
        Block must already exist.
        """
        
        if blockName not in self.blockOrder:
            logger.error("Block %s does not exist" % blockName)
            return False
        
        blockFmt = self.blockSettings[blockName][1]
        blockOpt = self.blockSettings[blockName][2]
        
        theList = self.splitBlockLine(newLine,blockFmt,blockOpt)
        
        if theList is None:
            logger.error("Invalid %s line" % blockName)
            return False
        
        self.blockData[blockName]["Data"].append(theList)
        
        return True
    
    def addBlockLineFromList(self, blockName, newList):
        """
        Adds a line to a block from a list.
        The list entries must have the correct data types.
        Only valid for blocks known to the Fort3 class.
        Block must already exist.
        """
        
        if blockName not in self.blockOrder:
            logger.error("Block %s does not exist" % blockName)
            return False
        
        blockFmt = self.blockSettings[blockName][1]
        
        if not len(newList) >= len(blockFmt):
            logger.error("Invalid %s list" % blockName)
            return False
            
        self.blockData[blockName]["Data"].append(newList)
        
        return True
    
    #
    # Block Serialisation
    #
    
    def serialiseLIMI(self, inData):
        try:
            return ("{:<24s} {:<2s}"+" {: 17.9e}"*7).format(*inData)
        except:
            logger.error("Invalid LIMI list")
            return None
    
    def serialiseDUMP(self, inData):
        try:
            nIn = len(inData)
            serString = ("{:<24s}"+" {:4d}"*3).format(*inData[0:4])
            if nIn > 4: serString += " {:<24s}".format(inData[4])
            if nIn > 5: serString += " {:4d}".format(inData[5])
            if nIn > 5: serString += " {:4d}".format(inData[5])
            return serString
        except:
            logger.error("Invalid DUMP list")
            return None
    
    #
    # Internal Functions
    #
    
    def splitBlockLine(self, inString, fmtReq, fmtOpt):
        
        inList  = inString.split()
        retList = []
        
        nIn  = len(inList)
        nReq = len(fmtReq)
        nOpt = len(fmtOpt)
        
        fmtAll = fmtReq+fmtOpt
        
        if nIn < nReq or nIn > nReq+nOpt:
            return None
        
        for i in range(nReq+nOpt):
            if i > nIn+1: break
            if fmtAll[i] == "S":
                retList.append(inList[i])
            elif fmtAll[i] == "I":
                retList.append(int(inList[i]))
            elif fmtAll[i] == "F":
                retList.append(float(inList[i]))
            else:
                logger.error("Invalid datatype '%s' encountered" % listFormat[i])
        
        return retList
    
# END Fort3
