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
from sttools.functions import formatNumberExp

logger = logging.getLogger(__name__)

class LHCOptics():
    
    LHC2016  = "lhc2016.csv"
    LHC2017  = "lhc2017.csv"
    HLLHC1_0 = "hllhc1.0.csv"
    HLLHC1_1 = "hllhc1.1.csv"
    HLLHC1_2 = "hllhc1.2.csv"
    HLLHC1_3 = "hllhc1.3.csv"
    
    IP_1 = "ATLAS (IP1)"
    IP_2 = "ALICE (IP2)"
    IP_5 = "CMS (IP5)"
    IP_8 = "LHCb (IP8)"
    
    validVersions = [LHC2016, LHC2017, HLLHC1_0, HLLHC1_1, HLLHC1_2, HLLHC1_3]
    validIPs      = [IP_1, IP_2, IP_5, IP_8]
    
    # Fixed Parameters
    ringCircumf   = 26658.883
    revFrequency  = 11245.499
    
    # Variable Parameters
    beamEnergy    = [None, None]
    partPerBunch  = [None, None]
    nBunches      = [None, None]
    normEmittance = [None, None]
    betaStarX     = [None, None]
    betaStarY     = [None, None]
    posX          = [None, None]
    posY          = [None, None]
    crossingX     = [None, None]
    crossingY     = [None, None]
    tuneQX        = [None, None]
    tuneQY        = [None, None]
    tuneQPX       = [None, None]
    tuneQPY       = [None, None]
    
    def __init__(self, lhcVersion):
        
        self.lhcVersion = lhcVersion
        self.lhcFolder  = path.dirname(__file__)
        self.dataBuffer = {}
        self.lhcConfigs = []
        self.valuesSet  = False
        self.selConfig  = None
        self.selIP      = None
        
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
        
        with open(csvFile,"rt") as fileIn:
            
            lineNo     = 0
            currConfig = ""
            currBeam   = 0
            
            for fileLine in fileIn:
                
                lineNo += 1
                
                rawData = fileLine.rstrip().split("\t")
                if not len(rawData) == 35:
                    logger.warning("Unexpected line length %d on line %d, skipping" % (
                        len(rawData), lineNo
                    ))
                
                if currConfig == "":
                    currConfig = rawData[0]
                    self.dataBuffer[currConfig] = {}
                    self.lhcConfigs.append(currConfig)
                if currConfig == "":
                    logger.warning("Unknown configuration on line %d, skipping" % lineNo)
                    continue
                
                if not rawData[0] == "" and not rawData[0] == currConfig:
                    currConfig = rawData[0]
                    self.dataBuffer[currConfig] = {}
                    self.lhcConfigs.append(currConfig)
                
                try:
                    currBeam = int(rawData[1])
                except:
                    logger.warning("Could not read beam number '%s' on line %d, skipping" % (
                        rawData[1], lineNo
                    ))
                    continue
                
                logger.debug("Now reading configuration '%s', beam %d on line %d" % (
                    currConfig, currBeam, lineNo
                ))
                
                self.dataBuffer[currConfig][currBeam] = [0]*32
                for idx in range(32):
                    try:
                        self.dataBuffer[currConfig][currBeam][idx] = float(rawData[idx+3])
                    except:
                        logger.error("Unable to convert element %d on line %d to float" % (
                            idx+3, lineNo
                        ))
        
        self.valuesSet = True
        
        return
    
    def setConfigIP(self, machineConfig, interactionPoint):
        
        if isinstance(machineConfig,int):
            if machineConfig >= 0 and machineConfig < len(self.lhcConfigs):
                machineConfig = self.lhcConfigs[machineConfig]
            else:
                logger.error("Unknown machine configuration %d" % machineConfig)
                return
        else:
            if not machineConfig in self.lhcConfigs:
                logger.error("Unknown machine configuration '%s'" % str(machineConfig))
                return
        
        if not interactionPoint in self.validIPs:
            logger.error("Unknown interaction point '%s'" % str(interactionPoint))
        
        self.selConfig = machineConfig
        self.selIP     = interactionPoint
        
        beamOne = self.dataBuffer[machineConfig][1]
        beamTwo = self.dataBuffer[machineConfig][2]
        
        ip = None
        if interactionPoint == self.IP_1: ip = 4
        if interactionPoint == self.IP_2: ip = 10
        if interactionPoint == self.IP_5: ip = 16
        if interactionPoint == self.IP_8: ip = 22
        
        self.beamEnergy    = [1.0e9  * beamOne[0]   , 1.0e9  * beamTwo[0]    ]
        self.partPerBunch  = [1.0e11 * beamOne[1]   , 1.0e11 * beamTwo[1]    ]
        self.nBunches      = [         beamOne[2]   ,          beamTwo[2]    ]
        self.normEmittance = [1.0e-6 * beamOne[3]   , 1.0e-6 * beamTwo[3]    ]
        self.betaStarX     = [         beamOne[ip]  ,          beamTwo[ip]   ]
        self.betaStarY     = [         beamOne[ip+1],          beamTwo[ip+1] ]
        self.posX          = [1.0e-3 * beamOne[ip+2], 1.0e-3 * beamTwo[ip+2] ]
        self.posY          = [1.0e-3 * beamOne[ip+3], 1.0e-3 * beamTwo[ip+3] ]
        self.crossingX     = [1.0e-6 * beamOne[ip+4], 1.0e-6 * beamTwo[ip+4] ]
        self.crossingY     = [1.0e-6 * beamOne[ip+5], 1.0e-6 * beamTwo[ip+5] ]
        self.tuneQX        = [         beamOne[28]  ,          beamTwo[28]   ]
        self.tuneQY        = [         beamOne[29]  ,          beamTwo[29]   ]
        self.tuneQPX       = [         beamOne[30]  ,          beamTwo[30]   ]
        self.tuneQPY       = [         beamOne[31]  ,          beamTwo[31]   ]
        
        return
    
    def echoValues(self):
        
        if not self.valuesSet:
            logger.error("Please run setConfigIP() first")
            return
        
        print("")
        print("Values Selected for:")
        print(" - Configuration: %s" % str(self.selConfig))
        print(" - Point:         %s" % str(self.selIP))
        print("")
        print(" Variable          Beam 1       Beam 2    Unit")
        print("================================================")
        print(" ringCircumf                 %s  [m]" % (
            formatNumberExp(self.ringCircumf)
        ))
        print(" revFrequency                %s  [Hz]" % (
            formatNumberExp(self.revFrequency)
        ))
        print(" beamEnergy     %s  %s  [eV]" % (
            formatNumberExp(self.beamEnergy[0]), formatNumberExp(self.beamEnergy[1])
        ))
        print(" partPerBunch   %s  %s  [N]" % (
            formatNumberExp(self.partPerBunch[0]), formatNumberExp(self.partPerBunch[1])
        ))
        print(" nBunches       %-11s  %-11s  [N]" % (
            ("%4d"%self.nBunches[0]), ("%4d"%self.nBunches[1])
        ))
        print(" normEmittance  %s  %s  [m]" % (
            formatNumberExp(self.normEmittance[0]), formatNumberExp(self.normEmittance[1])
        ))
        print(" betaStarX      %s  %s  [m]" % (
            formatNumberExp(self.betaStarX[0]), formatNumberExp(self.betaStarX[1])
        ))
        print(" betaStarY      %s  %s  [m]" % (
            formatNumberExp(self.betaStarY[0]), formatNumberExp(self.betaStarY[1])
        ))
        print(" posX           %s  %s  [m]" % (
            formatNumberExp(self.posX[0]), formatNumberExp(self.posX[1])
        ))
        print(" posY           %s  %s  [m]" % (
            formatNumberExp(self.posY[0]), formatNumberExp(self.posY[1])
        ))
        print(" crossingX      %s  %s  [rad]" % (
            formatNumberExp(self.crossingX[0]), formatNumberExp(self.crossingX[1])
        ))
        print(" crossingY      %s  %s  [rad]" % (
            formatNumberExp(self.crossingY[0]), formatNumberExp(self.crossingY[1])
        ))
        print(" tuneQX         %s  %s" % (
            formatNumberExp(self.tuneQX[0]), formatNumberExp(self.tuneQX[1])
        ))
        print(" tuneQY         %s  %s" % (
            formatNumberExp(self.tuneQY[0]), formatNumberExp(self.tuneQY[1])
        ))
        print(" tuneQPX        %s  %s" % (
            formatNumberExp(self.tuneQPX[0]), formatNumberExp(self.tuneQPX[1])
        ))
        print(" tuneQPY        %s  %s" % (
            formatNumberExp(self.tuneQPY[0]), formatNumberExp(self.tuneQPY[1])
        ))
        print("")
        
        return
    
# End Class LHCOptics
