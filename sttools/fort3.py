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
import shlex

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
    
    # Blocks that are just keywords (no NEXT)
    blockKeywords = {
        "GEOM" : "GEOMETRY",
        "FREE" : "FREE",
        "PRIN" : "PRINT",
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
        
        fort3File = path.join(self.filePath,self.fileName)
        lineNo    = 0
        inBlock   = False
        currBlock = ""
        
        with open(fort3File,"r") as inFile:
            for theLine in inFile:
                lineNo  += 1
                theLine  = theLine.strip()
                toCheck  = theLine[0:4].upper()
                
                # Skipping comment lines
                if theLine[0] == "/":
                    continue
                
                # If not currently in a block, add it.
                if not inBlock:
                    if toCheck in self.blockKeywords.keys():
                        self.blockOrder.append(toCheck)
                        self.blockData[toCheck] = {
                            "LongName" : self.blockKeywords[toCheck],
                            "Type"     : "KEYWORD",
                            "Data"     : [],
                            "MaxLen"   : [],
                        }
                        inBlock = False # No further parsing needed
                    elif toCheck in self.blockSettings.keys():
                        self.blockOrder.append(toCheck)
                        self.blockData[toCheck] = {
                            "LongName" : self.blockSettings[toCheck][0],
                            "Type"     : "PARSED",
                            "Data"     : [],
                            "MaxLen"   : [],
                        }
                        inBlock   = True
                        currBlock = toCheck
                    else: # Unparsed block type
                        self.blockOrder.append(toCheck)
                        self.blockData[toCheck] = {
                            "LongName" : theLine.replace("-"," ").strip(),
                            "Type"     : "UNPARSED",
                            "Data"     : [],
                            "MaxLen"   : [],
                        }
                        inBlock   = True
                        currBlock = toCheck
                    
                    # Skip the rest of this loop step
                    continue
                
                # Check if end of block or end of file
                if toCheck == "NEXT":
                    inBlock   = False
                    continue
                elif toCheck == "ENDE":
                    self.isEnded = True
                    break
                
                # If this point is reached, it is a data line.
                # Add it to the current block.
                if not self.addBlockLineFromString(currBlock,theLine):
                    logger.warning("Did not know what to do with line %d" % lineNo)
        
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
                
                if theBlock == "ENDE":
                    outFile.write("ENDE\n")
                    continue
                
                longName = self.blockData[theBlock]["LongName"]
                outFile.write(longName+"-"*(72-len(longName))+"\n")
                
                if self.blockData[theBlock]["Data"] == []:
                    continue
                
                if theBlock in serBlock.keys():
                    # A serialisation function already exists
                    # for output formatting
                    for theList in self.blockData[theBlock]["Data"]:
                        outFile.write(
                            serBlock[theBlock](theList)+"\n"
                        )
                else:
                    # No serialisation function is defined, so
                    # align strings by the longest in each column
                    for theList in self.blockData[theBlock]["Data"]:
                        fmtString = ""
                        for i in range(len(theList)):
                            fmtString += (
                                "{:<%ds} " % self.blockData[theBlock]["MaxLen"][i]
                            )
                        outFile.write(
                            fmtString.format(*theList).strip()+"\n"
                        )
                
                if theBlock not in self.blockKeywords.keys():
                    outFile.write("NEXT\n")
        
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
            "MaxLen"   : [],
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
                    self.updateMaxLen(blockName,theList)
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
        
        if blockName in self.blockSettings.keys():
            blockFmt = self.blockSettings[blockName][1]
            blockOpt = self.blockSettings[blockName][2]
        else:
            blockFmt = ""
            blockOpt = "S"*100
        
        theList = self.splitBlockLine(newLine,blockFmt,blockOpt)
        
        if theList is None:
            logger.error("Invalid %s line" % blockName)
            return False
        
        self.blockData[blockName]["Data"].append(theList)
        self.updateMaxLen(blockName,theList)
        
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
        self.updateMaxLen(blockName,newList)
        
        return True
    
    #
    # Block Serialisation
    #
    
    def serialiseLIMI(self, inData):
        try:
            serString  = "{:<%ds}" % self.blockData["LIMI"]["MaxLen"][0]
            serString += " {:<2s}"+" {: 17.9e}"*7
            return serString.format(*inData)
        except:
            logger.error("Invalid LIMI list")
            return None
    
    def serialiseDUMP(self, inData):
        try:
            nIn = len(inData)
            serString  = "{:<%ds}" % self.blockData["DUMP"]["MaxLen"][0]
            serString += " {:3d} {:4d} {:1d}"
            if nIn > 4:
                serString += " {:<%ds}" % self.blockData["DUMP"]["MaxLen"][4]
            if nIn > 5:
                serString += " {: 5d}"
            if nIn > 6:
                serString += " {: 5d}"
            return serString.format(*inData)
        except:
            logger.error("Invalid DUMP list")
            return None
    
    #
    # Internal Functions
    #
    
    def splitBlockLine(self, inString, fmtReq, fmtOpt):
        """
        Splits a string using shlex.split (preserves quotes strings), and
        the convert the content according to a datatype string consiting
        of required and optional values.
        """
        
        inList  = shlex.split(inString,posix=False)
        retList = []
        
        nIn  = len(inList)
        nReq = len(fmtReq)
        nOpt = len(fmtOpt)
        
        fmtAll = fmtReq+fmtOpt
        
        if nIn < nReq or nIn > nReq+nOpt:
            return None
        
        for i in range(nReq+nOpt):
            if i > nIn-1: break
            if fmtAll[i] == "S":
                retList.append(inList[i])
            elif fmtAll[i] == "I":
                retList.append(int(inList[i]))
            elif fmtAll[i] == "F":
                retList.append(float(inList[i]))
            elif fmtAll[i] == "B":
                retList.append(inList[i].strip().lower() == ".true.")
            else:
                logger.error("Invalid datatype '%s' encountered" % fmtAll[i])
        
        return retList
    
    def updateMaxLen(self, blockName, inList):
        
        for i in range(len(inList)):
            if isinstance(inList[i],str):
                nCh = len(inList[i])
            else:
                nCh = 0
            if i < len(self.blockData[blockName]["MaxLen"]):
                self.blockData[blockName]["MaxLen"][i] = max(
                    self.blockData[blockName]["MaxLen"][i], nCh
                )
            else:
                self.blockData[blockName]["MaxLen"].append(nCh)
        
        return True
    
# END Fort3
