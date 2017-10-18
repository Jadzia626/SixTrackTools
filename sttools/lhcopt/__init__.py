# -*- coding: utf-8 -*
"""SixTrack Tools - LHC Parameters Init

  SixTrack Tools - LHC Parameters Init
 ======================================
  Module that holds LHC parameters
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging
import sttools

from os import path

logger = logging.getLogger(__name__)

class LHCOptics():
    
    LHC2016  = "lhc2016.csv"
    LHC2017  = "lhc2017.csv"
    HLLHC1_2 = "hllhc1.2.csv"
    HLLHC1_3 = "hllhc1.3.csv"
    
    IP_1 = "ATLAS"
    IP_2 = "ALICE"
    IP_5 = "CMS"
    IP_8 = "LHCb"
    
    validVersions = [LHC2017, HLLHC1_2, HLLHC1_3]
    validIPs      = [IP_1, IP_2, IP_5, IP_8]
    
    def __init__(self, lhcVersion):
        
        self.lhcVersion = lhcVersion
        self.lhcFolder  = path.dirname(__file__)
        
        logger.debug("CSV folder is %s" % self.lhcFolder)
        
        self.loadData()
        
        return
    
    def loadData(self):
        
        csvFile = path.join(self.lhcFolder,"csv",self.lhcVersion)
        if path.isfile(csvFile):
            logger.info("Loading LHC Optics file: %s" % csvFile)
        else:
            logger.error("LHC Optics file missing: %s" % csvFile)
            return
        
        dataBuffer = {}
        lhcConfigs = []
        with open(csvFile,"rt") as fileIn:
            
            lineNo     = 1
            currConfig = ""
            currBeam   = 0
            
            for fileLine in fileIn:
                
                rawData = fileLine.split("\t")
                if not len(rawData) == 35:
                    logger.warning("Unexpected line length %d on line %d, skipping" % (
                        len(rawData), lineNo
                    ))
                    
                if currConfig == "":
                    currConfig = rawData[0]
                if currConfig == "":
                    logger.warning("Unknown configuration on line %d, skipping" % lineNo)
        
        return
    
# End Class LHCOptics
