# -*- coding: utf-8 -*
"""Dump File Wrapper

  SixTrack Tools - Dump File Wrapper
 ====================================
  Parses dump files and converts them to Numpy arrays
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging
import numpy   as np

logger = logging.getLogger(__name__)


class STDump:
    
    fileName  = None
    metaData  = None
    colNames  = None
    colTypes  = None
    colLabels = None
    turnIdx   = None
    partIdx   = None
    Data      = None
    fData     = None

    nLines    = None

    def __init__(self, fileName):

        self.fileName = fileName
        self.metaData = {}
        self.turnIdx  = {}
        self.partIdx  = {}
        self.nLines   = 0

        # Read File
        with open(fileName,mode="rt") as tfsFile:

            # Metadata
            tfsLine = tfsFile.readline().strip()
            if tfsLine[0] == "#":
                clLine = tfsLine[1:].strip()
                if clLine[0:2] == "DU":
                    metaBits = clLine.split(",")
                    self.metaData["FORMAT"] = metaBits[0][-1]
                    for metaBit in metaBits:
                        metaBit   = metaBit.strip()
                        metaParts = metaBit.split("=")
                        if metaParts[0] == "bez":                 self.metaData["BEZ"]         = str(metaParts[1].strip())
                        if metaParts[0] == "number of particles": self.metaData["N_PART"]      = int(metaParts[1].strip())
                        if metaParts[0] == "dump period":         self.metaData["DUMP_PERIOD"] = int(metaParts[1].strip())
                        if metaParts[0] == "first turn":          self.metaData["FIRST_TURN"]  = int(metaParts[1].strip())
                        if metaParts[0] == "last turn":           self.metaData["LAST_TURN"]   = int(metaParts[1].strip())
                        if metaParts[0] == "HIGH":                self.metaData["HIGH"]        = str(metaParts[1].strip())
                        if metaParts[0] == "FRONT":               self.metaData["FRONT"]       = str(metaParts[1].strip())
            else:
                logger.error("First line is not metadata")
                return

            # Set Columns from Dump Format
            if self.metaData["FORMAT"] == "2":
                self.colNames  = ["ID", "TURN","S",    "X",    "XP",      "Y",    "YP",      "Z",    "E",      "KTRACK"]
                self.colTypes  = ["int","int", "float","float","float",   "float","float",   "float","float",  "int"]
                self.colLabels = ["ID", "Turn","s[m]", "x[mm]","xp[mrad]","y[mm]","yp[mrad]","z[mm]","dE/E[1]","ktrack"]
                self.Data      = {dKey:[] for dKey in self.colNames}
            else:
                logger.error("Unsupported data format")
                return

            # Read Data
            for tfsLine in tfsFile:

                tfsLine = tfsLine.strip()
                if tfsLine[0] == "#": continue

                spLines = tfsLine.split()
                for (spLine,cN) in zip(spLines,self.colNames):
                    if len(spLines) == 10:
                        pPart = int(spLines[0])
                        pTurn = int(spLines[1])
                        self.Data[cN].append(spLine)

                dataID = len(self.Data["ID"]) -1
                self.turnIdx.setdefault(pTurn,[]).append(dataID)
                self.partIdx.setdefault(pPart,[]).append(dataID)

            self.nLines = len(self.Data["ID"])

            logger.info("%d lines of data read" % self.nLines)

        return


    def convertToNumpy(self):
        """
        Convert data to NumPy arrays
        """

        for i in range(len(self.colNames)):
            cN = self.colNames[i]
            cT = self.colTypes[i]
            self.Data[cN] = np.asarray(self.Data[cN],dtype=cT)

        return True


    def filterPart(self, partID):
        """
        Select all particles with a given particle ID and copy them to a new dataset
        """

        if not partID in self.partIdx.keys():
            logger.error("Particle ID %d does not exist in dataset" % partID)
            return False

        self.fData = None
        self.fData = {dKey:[] for dKey in self.colNames}

        for cN in self.colNames:
            self.fData[cN] = self.Data[cN][self.partIdx[partID]]

        logger.info("%d lines were filtered into fData" % len(self.fData["ID"]))

        return True


    def filterTurn(self, turnID):
        """
        Select all particles with a given turn ID and copy them to a new dataset
        """

        if not turnID in self.turnIdx.keys():
            logger.error("Turn ID %d does not exist in dataset" % turnID)
            return False

        self.fData = None
        self.fData = {dKey:[] for dKey in self.colNames}

        for cN in self.colNames:
            self.fData[cN] = self.Data[cN][self.turnIdx[turnID]]

        logger.info("%d lines were filtered into fData" % len(self.fData["ID"]))

        return True

    #
    #  Internal Functions
    #

    def stripQuotes(self, sVar):

        if (sVar[0] == sVar[-1]) and sVar.startswith(("'",'"')):
            return sVar[1:-1]

        return sVar

## End Class TableFS
