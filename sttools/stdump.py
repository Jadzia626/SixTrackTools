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
    varNames  = None
    varTypes  = None
    Data      = None

    nLines    = None

    def __init__(self, fileName):

        self.fileName = fileName
        self.metaData = {}
        self.varNames = []
        self.varTypes = []
        self.Data     = {}
        
        self.nLines   = 0

        # Read File
        with open(fileName,mode="rt") as tfsFile:

            for tfsLine in tfsFile:

                tfsLine = tfsLine.strip()

                # Metadata
                if tfsLine[0] == "#":
                    clLine = tfsLine[1:].strip()
                    logger.debug("Metadata %s" % clLine)

                    #~ spLines = tfsLine.split(",")[1:]
                    
                    #~ if   spLines[1][-1] == "d":
                        #~ self.metaData[spLines[0]] = int(spLines[2])
                    #~ elif spLines[1][-1] == "e":
                        #~ self.metaData[spLines[0]] = float(spLines[2])
                    #~ elif spLines[1][-1] == "s":
                        #~ self.metaData[spLines[0]] = self.stripQuotes(spLines[2])
                    #~ else:
                        #~ logger.error("Unknown type '%s' for metadata variable '%s'" % (spLines[1], spLines[2]))
                        #~ return False

                #~ # Header/Variable Names
                #~ elif tfsLine[0] == "*":
                    #~ spLines = tfsLine.split()[1:]
                    #~ for spLine in spLines:
                        #~ self.varNames.append(spLine)
                        #~ self.Data[spLine] = []

                #~ # Header/Variable Type
                #~ elif tfsLine[0] == "$":
                    #~ spLines = tfsLine.split()[1:]
                    #~ for spLine in spLines:
                        #~ self.varTypes.append(spLine)

                #~ # Data
                #~ else:
                    #~ spLines = tfsLine.split()
                    #~ for (spLine,vN,vT) in zip(spLines,self.varNames,self.varTypes):
                        #~ self.Data[vN].append(spLine)
                        #~ if vT == "%s":
                            #~ self.Data[vN][-1] = self.stripQuotes(self.Data[vN][-1])
                    #~ self.nLines += 1

            logger.info("%d lines of data read" % self.nLines)

        return


    def convertToNumpy(self):
        """
        Convert data to NumPy arrays
        """

        for i in range(len(self.varNames)):

            vN = self.varNames[i]
            vT = self.varTypes[i]
            
            if   vT[-1] == "d":
                self.Data[vN] = np.asarray(self.Data[vN],dtype="int")
            elif vT[-1] == "e":
                self.Data[vN] = np.asarray(self.Data[vN],dtype="float")
            elif vT[-1] == "s":
                self.Data[vN] = np.asarray(self.Data[vN],dtype="str")
            else:
                logger.error("Unknown type '%s' for variable '%s'" % (vT, vN))
                return False

        return True

    def stripQuotes(self, sVar):

        if (sVar[0] == sVar[-1]) and sVar.startswith(("'", '"')):
            return sVar[1:-1]

        return sVar
    

## End Class TableFS

