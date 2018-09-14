# -*- coding: utf-8 -*
"""Dump File Wrapper

  SixTrack Tools - Dump File Wrapper
 ====================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

  Parses dump files and converts them to Numpy arrays
  
  This class will parse the SixTrack dump.txt file and any file with a similar structure.
  The only requirement is that the first column is the particle ID and the second column is the turn number.

"""

import logging
import numpy   as np
import re

from os import path

logger = logging.getLogger(__name__)

class STDump:
    
    HEADER_CHAR = ("#","%","!")
    
    def __init__(self, fileName):
        
        if path.isfile(fileName):
            self.validFile = True
        else:
            logger.error("File not found: %s" % fileName)
            self.validFile = False
            return
        
        self.fileName  = fileName
        self.metaData  = {}
        
        self.colNames  = []
        self.colTypes  = []
        self.colLabels = []
        
        self.idxData   = {}
        self.idxNames  = []
        self.hasIndex  = {}
        
        self.allData   = None
        self.filData   = None
        self.nLines    = 0
        self.isNumPy   = False
        
        #
        # Scan the first lines of the file
        #
        
        headerLines = []
        firstData   = ""
        with open(self.fileName,mode="rt") as tmpFile:
            for tmpLine in tmpFile:
                tmpLine = tmpLine.lstrip()
                if len(tmpLine) == 0: continue
                if tmpLine[0] in self.HEADER_CHAR:
                    headerLines.append(tmpLine)
                else:
                    firstData = tmpLine
                    break
        
        if not firstData == "":
            logger.info("Found %d header lines and at least one data line" % len(headerLines))
        else:
            logger.error("Could not parse file %s" % path.basename(fileName))
            return
        
        # Treat first header line as metadata
        if len(headerLines) >= 2:
            clLine   = headerLines[0][1:].strip()
            metaBits = clLine.split(",")
            self.metaData["FORMAT"] = metaBits[0]
            for b in range(1,len(metaBits)):
                metaBit   = metaBits[b].strip()
                metaParts = metaBit.split("=")
                metaLabel = metaParts[0].strip().upper().replace(" ","_")
                metaValue = metaParts[1].strip()
                if isinstance(metaValue,int):
                    self.metaData[metaLabel] = int(metaValue)
                elif isinstance(metaValue,float):
                    self.metaData[metaLabel] = float(metaValue)
                else:
                    self.metaData[metaLabel] = metaValue
        else:
            logger.warning("Found no recognised metadata in header")
            self.metaData["FORMAT"] = "Unknown"
            
        # Treat last header line as column header
        if len(headerLines) >= 1:
            clLine = headerLines[-1][1:].strip()
            clLine = re.sub("\(.*?\)","",clLine)
            clLine = re.sub("\[.*?\]","",clLine)
            if "," in clLine:
                colBits = clLine.split(",")
            else:
                colBits = clLine.split()
            
            for colBit in colBits:
                colName = re.sub("^.*?=","",colBit)
                colName = colName.strip().upper()
                colName = re.sub("[^0-9A-Z_]+","",colName)
                self.colNames.append(colName)
                self.colTypes.append("str")
                self.colLabels.append(colBit)
            
        else:
            logger.warning("Found no recognised column header")
        
        # Extract data types from first data line
        colBits = firstData.split()
        colNum  = 0
        for colBit in colBits:
            colBit  = colBit.strip()
            makeIdx = False
            try:
                tmpVal = int(colBit)
            except ValueError:
                try:
                    tmpVal = float(colBit)
                except ValueError:
                    self.colTypes[colNum] = "str"
                else:
                    self.colTypes[colNum] = "float"
            else:
                self.colTypes[colNum] = "int"
                makeIdx = True
            
            self.hasIndex[self.colNames[colNum]] = makeIdx
            if makeIdx:
                self.idxData[self.colNames[colNum]] = {}
            
            colNum += 1
        
        return
    
    def addIndex(self, colName):
        """
        Adds an index for the sepcified column. Must be run before readAll.
        This function does not check whether it makes sense to index that column.
        For instance, if it's float values, it may generate one index entry per value.
        """
        
        if colName in self.colNames:
            self.hasIndex[colName] = True
        
        return
    
    def readAll(self):
        """
        Reads all lines that do not start with #
        Generates an index for all columns with hasIndex = True
        """
        
        self.allData = {dKey:[] for dKey in self.colNames}
        with open(self.fileName,mode="rt") as tmpFile:
            
            lineNo = 0
            
            for tmpLine in tmpFile:
                
                tmpLine = tmpLine.strip()
                lineNo += 1
                if tmpLine[0] in self.HEADER_CHAR: continue
                
                spLines = tmpLine.split()
                for (spLine,cN) in zip(spLines,self.colNames):
                    
                    if len(spLines) == len(self.colNames):
                        self.allData[cN].append(spLine)
                    else:
                        logger.warning("Line %d has an unexpected number of elements" % lineNo)
                    
                    if self.hasIndex[cN]:
                        dataID = len(self.allData[self.colNames[0]]) -1
                        self.idxData[cN].setdefault(spLine,[]).append(dataID)
            
            self.nLines = len(self.allData[self.colNames[0]])
            logger.info("%d lines of data read from %s" % (self.nLines,self.fileName))
        
        # Convert columns to numpy arrays
        for i in range(len(self.colNames)):
            cN = self.colNames[i]
            cT = self.colTypes[i]
            self.allData[cN] = np.asarray(self.allData[cN],dtype=cT)
        
        return
    
    def filterPart(self, colName, colValue):
        """
        Selects all particles with a given column value for a given column name.
        Entries are copied into filData
        """
        
        colName  = str(colName)
        colValue = str(colValue)
        if not colName in self.colNames:
            logger.error("Unknown column name '%s'" % colName)
            return False
        
        if not colValue in self.idxData[colName].keys():
            logger.error("Particles with %s = %s do not exist in dataset" % (colName,colValue))
            return False
        
        self.filData = None
        self.filData = {dKey:[] for dKey in self.colNames}
        
        for cN in self.colNames:
            self.filData[cN] = self.allData[cN][self.idxData[colName][colValue]]
        
        logger.info("%d particle with %s = %s were filtered into filData" % (len(self.filData["ID"]),colName,colValue))
        
        return True
    
    #
    #  Internal Functions
    #
    
    def stripQuotes(self, sVar):
        if (sVar[0] == sVar[-1]) and sVar.startswith(("'",'"')):
            return sVar[1:-1]
        return sVar
    
## End Class TableFS
