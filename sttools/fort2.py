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
    
    elemData   = {
        "Name" : [],
        "Type" : [],
        "Val1" : [],
        "Val2" : [],
        "Val3" : [],
        "Val4" : [],
        "Val5" : [],
        "Val6" : [],
    }
    blockData  = {
        "Block" : [],
        "Drift" : [],
    }
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
        whatLine  = 0
        
        with open(fort2File,"r") as inFile:
            whatLine += 1
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
                
                # This is a temporary fix while waiting for MadX Pull Request #552 to be merged
                theLine   = theLine.replace("_AP   3   1.000000000e-08","_AP   0   0.000000000e+00")
                lineElems = theLine.split()
                if whatStage == 1:
                    if len(lineElems) == 8:
                        self.elemData["Name"].append(lineElems[0])
                        self.elemData["Type"].append(lineElems[1])
                        self.elemData["Val1"].append(lineElems[2])
                        self.elemData["Val2"].append(lineElems[3])
                        self.elemData["Val3"].append(lineElems[4])
                        self.elemData["Val4"].append(lineElems[5])
                        self.elemData["Val5"].append(lineElems[6])
                        self.elemData["Val6"].append(lineElems[7])
                    else:
                        logger.warning("Line %d has the wrong number of elements" % whatLine)
                elif whatStage == 2:
                    if len(lineElems) == 2:
                        self.blockData["Block"].append(lineElems[0])
                        self.blockData["Drift"].append(lineElems[1])
                    else:
                        logger.warning("Line %d has the wrong number of elements" % whatLine)
                elif whatStage == 3:
                    for e in range(len(lineElems)):
                        self.structData.append(lineElems[e])
        
        self.elemData["Name"]   = np.asarray(self.elemData["Name"],  dtype="str")
        self.elemData["Type"]   = np.asarray(self.elemData["Type"],  dtype="int")
        self.elemData["Val1"]   = np.asarray(self.elemData["Val1"],  dtype="float")
        self.elemData["Val2"]   = np.asarray(self.elemData["Val2"],  dtype="float")
        self.elemData["Val3"]   = np.asarray(self.elemData["Val3"],  dtype="float")
        self.elemData["Val4"]   = np.asarray(self.elemData["Val4"],  dtype="float")
        self.elemData["Val5"]   = np.asarray(self.elemData["Val5"],  dtype="float")
        self.elemData["Val6"]   = np.asarray(self.elemData["Val6"],  dtype="float")
        self.blockData["Block"] = np.asarray(self.blockData["Block"],dtype="str")
        self.blockData["Drift"] = np.asarray(self.blockData["Drift"],dtype="str")
        self.structData         = np.asarray(self.structData[:],     dtype="str")
        
        return True
        
    def insertElement(self, inName, inType, inValues, inRef, inOffset=0):
        """
        Inserts a new marker before the element inRef.
        If inRef is a string, the index of the marker matching the string is used.
        inOffset can be used to offset this, i.e. an inOffset of 1 will insert the
        marker immediately after the inRef point instead of before (inOffset = 0).
        """
        
        if isinstance(inRef,str):
            arrRef = np.where(self.elemData["Name"] == inRef)
            if len(arrRef) == 1:
                inRef = arrRef[0]
            elif len(arrRef) > 1:
                logger.error("More than one marker named '%s' found" % inName)
                return False
            else:
                logger.error("Marker named '%s' not found" % inName)
                return False
        
        if inRef < 0 or inRef >= len(self.elemData["Name"]):
            logger.error("Index out of bounds")
            return False
        
        inPos = inRef + inOffset
        if inPos < 0 or inPos >= len(self.elemData["Name"]):
            logger.error("Index + offset out of bounds")
            return False
        
        if not len(inValues) == 6:
            logger.error("Value inValues must be an array of six floats")
            return False
        
        self.elemData["Name"] = np.insert(self.elemData["Name"],inPos,inName)
        self.elemData["Type"] = np.insert(self.elemData["Type"],inPos,inType)
        self.elemData["Val1"] = np.insert(self.elemData["Val1"],inPos,inValues[0])
        self.elemData["Val2"] = np.insert(self.elemData["Val2"],inPos,inValues[1])
        self.elemData["Val3"] = np.insert(self.elemData["Val3"],inPos,inValues[2])
        self.elemData["Val4"] = np.insert(self.elemData["Val4"],inPos,inValues[3])
        self.elemData["Val5"] = np.insert(self.elemData["Val5"],inPos,inValues[4])
        self.elemData["Val6"] = np.insert(self.elemData["Val6"],inPos,inValues[5])
        
        return True
    
# END Fort2
