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
    
    DT_INT = "int32"
    DT_FLT = "float64"
    DT_STR = h5py.special_dtype(vlen=str)
    
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
    #  Import SixTrack DUMP File
    #
    def importDump(self, dataFile):
        """
        Import SixTrack DUMP File
        Currently only supports DUMP format #2
        """
        
        if not path.isfile(dataFile):
            logger.error("File not found %s" % dataFile)
            return False
        
        stData = STDump(dataFile)
        stData.readAll()
        
        if stData.metaData["FORMAT"] == "DUMP format #2":
            
            if stData.nLines == 0:
                logger.error("The dump file has no data")
                return False
            
            # Prepare Data
            bezName = stData.metaData["BEZ"]
            bezPos  = float(stData.allData["S"][0])
            kTrack  = int(stData.allData["KTRACK"][0])
            nPart   = int(stData.metaData["NUMBER_OF_PARTICLES"])
            
            # Save Data
            h5Data = np.core.records.fromarrays(
                [
                    stData.allData["ID"],
                    stData.allData["TURN"],
                    stData.allData["X"],
                    stData.allData["XP"],
                    stData.allData["Y"],
                    stData.allData["YP"],
                    stData.allData["Z"],
                    stData.allData["DEE"]
                ],
                dtype=[
                    ("ID",   self.DT_INT),
                    ("TURN", self.DT_INT),
                    ("X",    self.DT_FLT),
                    ("XP",   self.DT_FLT),
                    ("Y",    self.DT_FLT),
                    ("YP",   self.DT_FLT),
                    ("Z",    self.DT_FLT),
                    ("DEE",  self.DT_FLT)
                ]
            )
            h5Grp = self._createH5Group(self.h5File,"dump")
            h5Set = h5Grp.create_dataset(bezName,data=h5Data)
            h5Set.attrs.create("S",        bezPos, dtype=self.DT_FLT)
            h5Set.attrs.create("KTRACK",   kTrack, dtype=self.DT_INT)
            h5Set.attrs.create("NPART",    nPart,  dtype=self.DT_INT)
            h5Set.attrs.create("UNITS_S",  "m",    dtype=self.DT_STR)
            h5Set.attrs.create("UNITS_X",  "mm",   dtype=self.DT_STR)
            h5Set.attrs.create("UNITS_XP", "mrad", dtype=self.DT_STR)
            h5Set.attrs.create("UNITS_Y",  "mm",   dtype=self.DT_STR)
            h5Set.attrs.create("UNITS_YP", "mrad", dtype=self.DT_STR)
            h5Set.attrs.create("UNITS_Z",  "mm",   dtype=self.DT_STR)
        
        else:
            logger.error("Unhandled format: %s" % stData.metaData["FORMAT"])
            return False
        
        return True
    
    #
    #  Import SixTrack SCATTER Log File
    #
    def importScatterLog(self, dataFile):
        """
        Import SixTrack SCATTER Log File
        """
        
        if not path.isfile(dataFile):
            logger.error("File not found %s" % dataFile)
            return False
        
        stData = STDump(dataFile)
        stData.readAll()
        
        if stData.metaData["FORMAT"] == "scatter_log":
            
            if stData.nLines == 0:
                logger.error("The dump file has no data")
                return False
            
            # Prepare Data
            dataDict = {}
            for idx in range(stData.nLines):
                
                bezName  = stData.allData["BEZ"][idx]
                scatGen  = stData.allData["SCATTER_GENERATOR"][idx]
                scatProb = stData.allData["PROB"][idx]
                if not bezName in dataDict.keys():
                    dataDict[bezName] = {
                        "scatGen"  : scatGen,
                        "scatProb" : float(scatProb),
                        "scatData" : {
                            "ID"    : [],
                            "TURN"  : [],
                            "T"     : [],
                            "XI"    : [],
                            "THETA" : [],
                            "PHI"   : []
                        }
                    }
                for dtKey in dataDict[bezName]["scatData"].keys():
                    dataDict[bezName]["scatData"][dtKey].append(
                        stData.allData[dtKey][idx]
                    )
            
            # Save Data
            h5Grp = self.h5File.create_group("scatter")
            for bezName in dataDict.keys():
                h5Data = np.core.records.fromarrays(
                    [
                        dataDict[bezName]["scatData"]["ID"],
                        dataDict[bezName]["scatData"]["TURN"],
                        dataDict[bezName]["scatData"]["T"],
                        dataDict[bezName]["scatData"]["XI"],
                        dataDict[bezName]["scatData"]["THETA"],
                        dataDict[bezName]["scatData"]["PHI"]
                    ],
                    dtype=[
                        ("ID",    self.DT_INT),
                        ("TURN",  self.DT_INT),
                        ("T",     self.DT_FLT),
                        ("XI",    self.DT_FLT),
                        ("THETA", self.DT_FLT),
                        ("PHI",   self.DT_FLT)
                    ]
                )
                h5Set = h5Grp.create_dataset("%s_log" % bezName,data=h5Data)
                h5Set.attrs.create("GENERATOR",   dataDict[bezName]["scatGen"], dtype=self.DT_STR)
                h5Set.attrs.create("PROBABILITY", dataDict[bezName]["scatProb"],dtype=self.DT_FLT)
                h5Set.attrs.create("UNIT_T",      "MeV^2", dtype=self.DT_STR)
                h5Set.attrs.create("UNIT_XI",     "",      dtype=self.DT_STR)
                h5Set.attrs.create("UNIT_THETA",  "mrad",  dtype=self.DT_STR)
                h5Set.attrs.create("UNIT_PHI",    "rad",   dtype=self.DT_STR)
        
        else:
            logger.error("Unhandled format: %s" % stData.metaData["FORMAT"])
            return False
        
        return True
    
    #
    #  Import SixTrack COLLIMATION Summary File
    #
    def importCollSummary(self, dataFile):
        """
        Import SixTrack COLLIMATION Summary File
        """
        
        if not path.isfile(dataFile):
            logger.error("File not found %s" % dataFile)
            return False
        
        stData = STDump(dataFile)
        stData.readAll()
        
        validCols = ["ICOLL","COLLNAME","NIMP","NABS","IMP_AV","IMP_SIG","LENGTH"]
        
        if bool(set(stData.colNames).intersection(validCols)):
            
            if stData.nLines == 0:
                logger.error("The data file has no data")
                return False
            
            # Save Data
            h5Data = np.core.records.fromarrays(
                [
                    stData.allData["ICOLL"],
                    stData.allData["COLLNAME"],
                    stData.allData["NIMP"],
                    stData.allData["NABS"],
                    stData.allData["IMP_AV"],
                    stData.allData["IMP_SIG"],
                    stData.allData["LENGTH"]
                ],
                dtype=[
                    ("ICOLL"    , self.DT_INT),
                    ("COLLNAME" , self.DT_STR),
                    ("NIMP"     , self.DT_INT),
                    ("NABS"     , self.DT_INT),
                    ("IMP_AV"   , self.DT_FLT),
                    ("IMP_SIG"  , self.DT_FLT),
                    ("LENGTH"   , self.DT_FLT)
                ]
            )
            h5Grp = self.h5File.create_group("collimation")
            h5Set = h5Grp.create_dataset("summary",data=h5Data)
            
        else:
            logger.error("Unexpected header variables in %s" % path.basename(dataFile))
            return False
        
        return True
    
    #
    #  Internal Functions
    #
    
    def _createH5Group(self, h5Obj, groupName):
        if not groupName in h5Obj.keys():
            h5Obj.create_group(groupName)
        return h5Obj[groupName]
    
# End Class HDF5Import
