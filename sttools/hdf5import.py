# -*- coding: utf-8 -*
"""SixTrack HDF5 Import

  SixTrack Tools - HDF5 Import
 ==============================
  Imports Simulation Data into a Single HDF5 File
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

class HDF5Import:
    
    def __init__(self, inFolder, outFile, doTruncate=False):
        
        if not path.isdir(inFolder):
            logger.error("Input folder not found: %s" % inFolder)
            return
        
        self.outFile  = outFile
        self.inFolder = inFolder
        self.doTrunc  = doTruncate
        self.h5File   = None
        
        return
    
    #
    #  Open and Close the File
    #
    
    def openFile(self):
        try:
            if self.doTrunc:
                self.h5File = h5py.File(self.outFile, mode="w")
            else:
                self.h5File = h5py.File(self.outFile, mode="a")
            return True
        except:
            logger.error("Unable to open file %s" % self.outFile)
            return False
    
    def closeFile(self):
        try:
            self.h5File.close()
            return True
        except:
            logger.error("Unable to close file %s" % self.outFile)
            return False
    
    #
    #  Append Data
    #
    
    def importDump(self, dataFile):
        
        stData = STDump(dataFile)
        stData.readAll()
        
        if stData.metaData["FORMAT"] == "DUMP format #2":
            
            if stData.nLines == 0:
                logger.error("The dump file has no data")
                return False
            
            bezName = stData.metaData["BEZ"]
            logger.info("Reading particle data from bez = %s" % bezName)
            
            h5Part = self._getH5Group("/dump")
            h5BEZ  = self._getH5Group("/dump/%s" % bezName)
            bezPos = stData.allData["S"][0]
            kTrack = stData.allData["KTRACK"][0]
            self._writeH5Attr("/dump/%s" % bezName,"S",bezPos)
            self._writeH5Attr("/dump/%s" % bezName,"KTRACK",kTrack)
            
            iTurn    = 0
            turnList = []
            turnNum  = []
            for idx in range(stData.nLines):
                
                if not iTurn == stData.allData["TURN"][idx]:
                    iTurn = stData.allData["TURN"][idx]
                    turnList.append({"ID":[],"6D":[]})
                    turnNum.append(iTurn)
                
                bezPos = stData.allData["S"][idx]
                turnList[len(turnList)-1]["ID"].append(
                    stData.allData["ID"][idx]
                )
                turnList[len(turnList)-1]["6D"].append([
                    stData.allData["X"][idx], stData.allData["XP"][idx],
                    stData.allData["Y"][idx], stData.allData["YP"][idx],
                    stData.allData["Z"][idx], stData.allData["DEE"][idx]
                ])
            
            for turnData, iTurn in zip(turnList,turnNum):
                if len(turnData) == 0:
                    continue
                setPath = "/dump/%s/turn%08d" % (bezName,iTurn)
                colID = [["col0","ID"]]
                col6D = [
                    ["col0","X"],["col1","XP"],
                    ["col2","Y"],["col3","YP"],
                    ["col4","Z"],["col5","DEE"]
                ]
                h5Set = self._saveH5Data(setPath+"_ID",turnData["ID"],colID,"int32")
                h5Set = self._saveH5Data(setPath+"_6D",turnData["6D"],col6D,"float64")
            
            self._writeH5Attr("/dump","nPart",int(stData.metaData["NUMBER_OF_PARTICLES"]))
        
        else:
            logger.error("Unhandled %s" % stData.metaData["FORMAT"])
            return False
        
        return True
    
    #
    #  Internal Functions
    #
    
    def _readH5Attr(self, h5Path, attrName, defaultVal):
        if attrName in self.h5File[h5Path].attrs.keys():
            return self.h5File[h5Path].attrs[attrName]
        return defaultVal
    
    def _writeH5Attr(self, h5Path, attrName, attrValue):
        if attrName in self.h5File[h5Path].attrs.keys():
            self.h5File[h5Path].attrs[attrName] = attrValue
        else:
            self.h5File[h5Path].attrs.create(attrName, attrValue)
        return True
    
    def _getH5Group(self, h5Path):
        if not h5Path in self.h5File.keys():
            self.h5File.create_group(h5Path)
        return self.h5File[h5Path]
    
    def _saveH5Data(self, h5Path, h5Data, colNames=[], dataType="float64"):
        
        dLen = len(h5Data)
        if dLen > 0:
            dWidth = len(np.atleast_1d(h5Data[0]))
        else:
            dWidth = 1
        
        if dWidth == 1:
            if not h5Path in self.h5File.keys():
                dSet = self.h5File.create_dataset(
                    h5Path,data=np.array(h5Data,dtype=dataType),maxshape=(None,)
                )
            else:
                dSet = self.h5File[h5Path]
                pLen = dSet.shape[0]
                dSet.resize(pLen+dLen,0)
                dSet[pLen:] = np.array(h5Data,dtype=dataType)
        else:
            if not h5Path in self.h5File.keys():
                dSet = self.h5File.create_dataset(
                    h5Path,data=np.array(h5Data,dtype=dataType),maxshape=(None,dWidth)
                )
            else:
                dSet = self.h5File[h5Path]
                pLen = dSet.shape[0]
                dSet.resize(pLen+dLen,0)
                dSet[pLen:,:] = np.array(h5Data,dtype=dataType)
        
        for colName in colNames:
            if not len(colName) == 2: continue
            if colName[0] in dSet.attrs.keys(): continue
            dSet.attrs.create(colName[0],colName[1],dtype=("S%d" % len(colName[1])))
        
        return dSet
    
# End Class Concatenator
