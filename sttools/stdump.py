# -*- coding: utf-8 -*
"""Dump File Wrapper

  SixTrack Tools - Dump File Wrapper
 ====================================
  Parses dump files and converts them to Numpy arrays
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

  This class will parse the SixTrack dump.txt file and any file with a similar structure.
  The only requirement is that the first column is the particle ID and the second column is the turn number.

"""

import logging
import numpy   as np
import re

logger = logging.getLogger(__name__)


class STDump:

    fileName  = None
    metaData  = None

    colNames  = None
    colTypes  = None
    colLabels = None

    idxData   = None
    idxNames  = None
    hasIndex  = None

    Data      = None
    fData     = None

    nLines    = None
    isNumPy   = None

    def __init__(self, fileName):

        self.fileName = fileName
        self.metaData = {}

        self.colNames  = []
        self.colTypes  = []
        self.colLabels = []

        self.idxData   = {}
        self.idxNames  = []
        self.hasIndex  = {}

        self.nLines   = 0
        self.isNumPy  = False

        #  Read File
        # ===========
        #  Reads the first three lines:
        #  Line 1: File metadata. Must start with #
        #  Line 2: Column header. Must start with #
        #  Line 3: First dataline. Used to detect datatypes.
        with open(fileName,mode="rt") as tmpFile:

            # Line 1: Metadata
            tmpLine = tmpFile.readline().strip()
            if tmpLine[0] == "#":
                clLine   = tmpLine[1:].strip()
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
                logger.error("First line is not metadata")
                return

            # Line 2: Column Header
            tmpLine = tmpFile.readline().strip()
            if tmpLine[0] == "#":
                clLine  = tmpLine[1:].strip()
                colBits = clLine.split()
                for colBit in colBits:
                    colBit   = colBit.strip()
                    colParts = colBit.split("[")
                    colName  = colParts[0].strip().upper()
                    colName  = re.sub("[^0-9A-Z]+","",colName)
                    self.colNames.append(colName)
                    self.colTypes.append("str")
                    self.colLabels.append(colBit)
                self.Data = {dKey:[] for dKey in self.colNames}
            else:
                logger.error("Second line is not column labels")
                return

            # Line 3: First Data Line
            tmpLine = tmpFile.readline().strip()
            if tmpLine[0] == "#":
                logger.error("Third line is not data")
                return
            else:
                colBits = tmpLine.split()
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
                    colNum += 1

        return

    def loadAll(self):

        #     for tmpLine in tmpFile:
        # 
        #         tmpLine = tmpLine.strip()
        #         if tmpLine[0] == "#": continue # Skip all further comment lines
        # 
        #         spLines = tmpLine.split()
        #         for (spLine,cN) in zip(spLines,self.colNames):
        #             if len(spLines) == len(self.colNames):
        #                 self.Data[cN].append(spLine)
        #             else:
        #                 logger.warning("Line %d has an unexpected number of elements" % lineNo)
        # 
        #             # For first data line, try to determine data type
        #             if not gotType:
        #                 for e in range(len(spLines)):
        #                     if isinstance(spLines[e],int):
        #                         self.colTypes[e] = "int"
        #                     elif isinstance(spLines[e],float):
        #                         self.colTypes[e] = "float"
        #                     else:
        #                         self.colTypes[e] = "str"
        #                     # Create index for all columns
        #                 gotType = True
        # 
        #         dataID = len(self.Data["ID"]) -1
        #         self.turnIdx.setdefault(pTurn,[]).append(dataID)
        #         self.partIdx.setdefault(pPart,[]).append(dataID)
        # 
        #     self.nLines = len(self.Data["ID"])
        # 
        #     logger.info("%d lines of data read" % self.nLines)
        # 
        # for i in range(len(self.colNames)):
        #     cN = self.colNames[i]
        #     cT = self.colTypes[i]
        #     self.Data[cN] = np.asarray(self.Data[cN],dtype=cT)
        return

    def convertToNumpy(self):
        """
        Convert data to NumPy arrays
        """

        for i in range(len(self.colNames)):
            cN = self.colNames[i]
            cT = self.colTypes[i]
            self.Data[cN] = np.asarray(self.Data[cN],dtype=cT)

        self.isNumPy = True

        return True


    def filterPart(self, partID):
        """
        Select all particles with a given particle ID and copy them to a new dataset
        """

        if partID < 0:
            partID = len(self.partIdx.keys()) + partID + 1

        if not partID in self.partIdx.keys():
            logger.error("Particle ID %d does not exist in dataset" % partID)
            return False

        if not self.isNumPy:
            logger.error("Convert data to numpy arrays first")
            return False

        self.fData = None
        self.fData = {dKey:[] for dKey in self.colNames}

        for cN in self.colNames:
            self.fData[cN] = self.Data[cN][self.partIdx[partID]]

        logger.info("%d turns with particle ID %d were filtered into fData" % (len(self.fData["ID"]),partID))

        return True


    def filterTurn(self, turnID):
        """
        Select all particles with a given turn ID and copy them to a new dataset
        """

        if turnID < 0:
            turnID = len(self.turnIdx.keys()) + turnID + 1

        if not turnID in self.turnIdx.keys():
            logger.error("Turn ID %d does not exist in dataset" % turnID)
            return False

        if not self.isNumPy:
            logger.error("Convert data to numpy arrays first")
            return False

        self.fData = None
        self.fData = {dKey:[] for dKey in self.colNames}

        for cN in self.colNames:
            self.fData[cN] = self.Data[cN][self.turnIdx[turnID]]

        logger.info("%d particles with turn ID %d were filtered into fData" % (len(self.fData["ID"]),turnID))

        return True

    #
    #  Internal Functions
    #

    def stripQuotes(self, sVar):

        if (sVar[0] == sVar[-1]) and sVar.startswith(("'",'"')):
            return sVar[1:-1]

        return sVar

## End Class TableFS
