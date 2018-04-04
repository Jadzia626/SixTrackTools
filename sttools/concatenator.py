# -*- coding: utf-8 -*
"""SixTrack Concatenat0r

  SixTrack Tools - Concatenat0r
 ===============================
  Collects Simulation Data into HDF5 File
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging
import numpy   as np
import h5py

from os import path

from .tablefs import TableFS
from .stdump  import STDump

logger = logging.getLogger(__name__)

class Concatenator:
    
    FTYPE_PART_DUMP = 100
    
    def __init__(self, outFile, doTruncate=False):
        
        self.dataFile = outFile
        self.doTrunc  = doTruncate
        self.h5Object = None
        
        return
    
    #
    #  Open and Close the File
    #
    
    def openFile(self):
        try:
            if self.doTrunc:
                self.h5Object = h5py.File(self.dataFile, mode="w")
            else:
                self.h5Object = h5py.File(self.dataFile, mode="a")
            return True
        except:
            logger.error("Unable to open file %s" % self.dataFile)
            return False
    
    def closeFile(self):
        try:
            self.h5Object.close()
            return True
        except:
            logger.error("Unable to close file %s" % self.dataFile)
            return False
    
    #
    #  Append Data
    #
    
    def appendParticles(self, dataFile, fileType):
        
        stData = STDump(dataFile)
        stData.readAll()
        
        if fileType == self.FTYPE_PART_DUMP:
            
            logger.info("Reading particle data from bez = %s" % stData.metaData["BEZ"])
            
            h5Part     = self._getH5Group("/particles")
            dsRead     = self._readH5Attr("/particles","datasetsRead",0)
            partOffset = self._readH5Attr("/particles","particleOffset",0)
            
            iTurn      = 0
            turnList   = []
            turnNum    = []
            for idx in range(stData.nLines):
                if not iTurn == stData.allData["TURN"][idx]:
                    iTurn = stData.allData["TURN"][idx]
                    turnList.append([])
                    turnNum.append(iTurn)
                
                turnList[len(turnList)-1].append([
                    stData.allData["ID"][idx] + partOffset,
                    stData.allData["S"][idx],
                    stData.allData["X"][idx],
                    stData.allData["XP"][idx],
                    stData.allData["Y"][idx],
                    stData.allData["YP"][idx],
                    stData.allData["Z"][idx],
                    stData.allData["DEE"][idx]
                ])
            
            partOffset += int(stData.metaData["NUMBER_OF_PARTICLES"])
            dsRead     += 1
                
            for turnData, iTurn in zip(turnList,turnNum):
                if len(turnData) == 0:
                    continue
                setPath = "/particles/%s/turn%08d" % (
                    stData.metaData["BEZ"],
                    iTurn
                )
                dataCols = [
                    ["col0","ID"],["col1","S"], ["col2","X"],["col3","XP"],
                    ["col4","Y"], ["col5","YP"],["col6","Z"],["col7","DEE"]
                ]
                h5Set = self._saveH5Data(setPath,turnData,dataCols)
            
            self._writeH5Attr("/particles","datasetsRead",  dsRead)
            self._writeH5Attr("/particles","particleOffset",partOffset)
        
        else:
            logger.error("Unknown fileType specified")
            return False
        
        return True
    
    #
    #  Internal Functions
    #
    
    def _readH5Attr(self, h5Path, attrName, defaultVal):
        if attrName in self.h5Object[h5Path].attrs.keys():
            return self.h5Object[h5Path].attrs[attrName]
        return defaultVal
    
    def _writeH5Attr(self, h5Path, attrName, attrValue):
        if attrName in self.h5Object[h5Path].attrs.keys():
            self.h5Object[h5Path].attrs[attrName] = attrValue
        else:
            self.h5Object[h5Path].attrs.create(
                attrName, attrValue
            )
        return True
    
    def _getH5Group(self, h5Path):
        if not h5Path in self.h5Object.keys():
            self.h5Object.create_group(h5Path)
        return self.h5Object[h5Path]
    
    def _saveH5Data(self, h5Path, h5Data, colNames=[], dataType="float64"):
        
        dLen = len(h5Data)
        if dLen > 0:
            dWidth = len(h5Data[0])
        else:
            dWidth = 1
        
        if not h5Path in self.h5Object.keys():
            dSet = self.h5Object.create_dataset(
                h5Path,data=np.array(h5Data,dtype=dataType),maxshape=(None,dWidth)
            )
        else:
            dSet = self.h5Object[h5Path]
            pLen,pWidth = dSet.shape
            dSet.resize(pLen+dLen,0)
            dSet[pLen:,:] = np.array(h5Data,dtype=dataType)
        
        for colName in colNames:
            if not len(colName) == 2:
                continue
            if colName[0] in dSet.attrs.keys():
                continue
            dSet.attrs.create(colName[0],colName[1],dtype=("S%d" % len(colName[1])))
        
        return dSet
    
# End Class Concatenator
