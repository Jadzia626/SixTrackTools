# -*- coding: utf-8 -*
"""SixTrack Tools - HiLumi Parameters 1.2

  SixTrack Tools - HiLumi Parameters 1.2
 ========================================
  HL-LHC 1.2 Parameters
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import sttools

logger = logging.getLogger(__name__)

#  Optics Version 1.2
# ====================
#  http://abpdata.web.cern.ch/abpdata/lhc_optics_web/www/hllhc12/index.html

class HLLHCv12():
    
    # Configurations
    CONF_INJECTION       = 0
    CONF_PRE_SQUEEZE     = 1
    CONF_COLLISION_ROUND = 2
    CONF_COLLISION_FLAT  = 3
    CONF_VDM_30          = 4
    CONF_LOW_BETA        = 5
    
    # Interaction Points
    IP_1 = "ATLAS"
    IP_2 = "ALICE"
    IP_5 = "CMS"
    IP_8 = "LHCb"
    
    # Parameters
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
    
    def setConfigIP(self, machineConfig, interactionPoint):
        
        if machineConfig == self.CONF_INJECTION:
            self.beamEnergy    = [  450.00e9 ,  450.00e9 ]
            self.partPerBunch  = [    2.20e11,    2.20e11]
            self.nBunches      = [ 2748      , 2748      ]
            self.normEmittance = [    2.50e-6,    2.50e-6]
            if interactionPoint == self.IP_1:
                self.betaStarX = [    6.00   ,    6.00   ]
                self.betaStarY = [    6.00   ,    6.00   ]
                self.posX      = [   -2.00e-3,    2.00e-3]
                self.posY      = [    0.00e-3,    0.00e-3]
                self.crossingX = [    0.00e-6,    0.00e-6]
                self.crossingY = [  295.00e-6, -295.00e-6]
            elif interactionPoint == self.IP_2:
                self.betaStarX = [   10.00   ,   10.00   ]
                self.betaStarY = [   10.00   ,   10.00   ]
                self.posX      = [    2.00e-3,   -2.00e-3]
                self.posY      = [    0.00e-3,    0.00e-3]
                self.crossingX = [    4.54e-6,   -4.54e-6]
                self.crossingY = [ 1259.00e-6,-1259.00e-6]
            elif interactionPoint == self.IP_5:
                self.betaStarX = [    6.00   ,    6.00   ]
                self.betaStarY = [    6.00   ,    6.00   ]
                self.posX      = [    0.00e-3,    0.00e-3]
                self.posY      = [    2.00e-3,   -2.00e-3]
                self.crossingX = [  295.00e-6, -295.00e-6]
                self.crossingY = [    0.00e-6,    0.00e-6]
            elif interactionPoint == self.IP_8:
                self.betaStarX = [   10.00   ,   10.00   ]
                self.betaStarY = [   10.00   ,   10.00   ]
                self.posX      = [    0.00e-3,    0.00e-3]
                self.posY      = [   -3.50e-3,    3.50e-3]
                self.crossingX = [-2270.00e-6, 2270.00e-6]
                self.crossingY = [  -68.15e-6,  -11.85e-6]
            else:
                logger.error("Unknown interaction point encountered")
        elif machineConfig == self.CONF_PRE_SQUEEZE:
            self.beamEnergy    = [ 7000.00e9 , 7000.00e9 ]
            self.partPerBunch  = [    2.20e11,    2.20e11]
            self.nBunches      = [ 2748      , 2748      ]
            self.normEmittance = [    2.50e-6,    2.50e-6]
            if interactionPoint == self.IP_1:
                self.betaStarX = [  480.00e-3,  480.00e-3]
                self.betaStarY = [  480.00e-3,  480.00e-3]
                self.posX      = [   -2.00e-3,    2.00e-3]
                self.posY      = [    0.00e-3,    0.00e-3]
                self.crossingX = [    0.00e-6,    0.00e-6]
                self.crossingY = [  295.00e-6, -295.00e-6]
            elif interactionPoint == self.IP_2:
                self.betaStarX = [   10.00   ,   10.00   ]
                self.betaStarY = [   10.00   ,   10.00   ]
                self.posX      = [    2.00e-3,   -2.00e-3]
                self.posY      = [    0.00e-3,    0.00e-3]
                self.crossingX = [  290.00e-9, -290.00e-9]
                self.crossingY = [  240.00e-6, -240.00e-6]
            elif interactionPoint == self.IP_5:
                self.betaStarX = [  480.00e-3,  480.00e-3]
                self.betaStarY = [  480.00e-3,  480.00e-3]
                self.posX      = [    0.00e-3,    0.00e-3]
                self.posY      = [    2.00e-3,   -2.00e-3]
                self.crossingX = [  295.00e-6, -295.00e-6]
                self.crossingY = [    0.00e-6,    0.00e-6]
            elif interactionPoint == self.IP_8:
                self.betaStarX = [    3.00   ,    3.00   ]
                self.betaStarY = [    3.00   ,    3.00   ]
                self.posX      = [    0.00e-3,    0.00e-3]
                self.posY      = [   -2.00e-3,    2.00e-3]
                self.crossingX = [ -415.00e-6,  415.00e-6]
                self.crossingY = [   -1.81e-6,    1.81e-6]
            else:
                logger.error("Unknown interaction point encountered")
        elif machineConfig == self.CONF_COLLISION_ROUND:
            self.beamEnergy    = [ 7000.00e9 , 7000.00e9 ]
            self.partPerBunch  = [    2.20e11,    2.20e11]
            self.nBunches      = [ 2748      , 2748      ]
            self.normEmittance = [    2.50e-6,    2.50e-6]
            if interactionPoint == self.IP_1:
                self.betaStarX = [  150.00e-3,  150.00e-3]
                self.betaStarY = [  150.00e-3,  150.00e-3]
                self.posX      = [ -750.00e-6,  750.00e-6]
                self.posY      = [    0.00e-3,    0.00e-3]
                self.crossingX = [    0.00e-6,    0.00e-6]
                self.crossingY = [  295.00e-6, -295.00e-6]
            elif interactionPoint == self.IP_2:
                self.betaStarX = [   10.00   ,   10.00   ]
                self.betaStarY = [   10.00   ,   10.00   ]
                self.posX      = [    2.00e-3,   -2.00e-3]
                self.posY      = [    0.00e-3,    0.00e-3]
                self.crossingX = [  290.00e-9, -290.00e-9]
                self.crossingY = [  240.00e-6, -240.00e-6]
            elif interactionPoint == self.IP_5:
                self.betaStarX = [  150.00e-3,  150.00e-3]
                self.betaStarY = [  150.00e-3,  150.00e-3]
                self.posX      = [    0.00e-3,    0.00e-3]
                self.posY      = [  750.00e-6, -750.00e-6]
                self.crossingX = [  295.00e-6, -295.00e-6]
                self.crossingY = [    0.00e-6,    0.00e-6]
            elif interactionPoint == self.IP_8:
                self.betaStarX = [    3.00   ,    3.00   ]
                self.betaStarY = [    3.00   ,    3.00   ]
                self.posX      = [    0.00e-3,    0.00e-3]
                self.posY      = [   -2.00e-3,    2.00e-3]
                self.crossingX = [ -415.00e-6,  415.00e-6]
                self.crossingY = [   -1.81e-6,    1.81e-6]
            else:
                logger.error("Unknown interaction point encountered")
        elif machineConfig == self.CONF_COLLISION_FLAT:
            self.beamEnergy    = [ 7000.00e9 , 7000.00e9 ]
            self.partPerBunch  = [    2.20e11,    2.20e11]
            self.nBunches      = [ 2748      , 2748      ]
            self.normEmittance = [    2.50e-6,    2.50e-6]
            if interactionPoint == self.IP_1:
                self.betaStarX = [   75.00e-3,   75.00e-3]
                self.betaStarY = [  300.00e-3,  300.00e-3]
                self.posX      = [ -750.00e-6,  750.00e-6]
                self.posY      = [    0.00e-3,    0.00e-3]
                self.crossingX = [    0.00e-6,    0.00e-6]
                self.crossingY = [  275.00e-6, -275.00e-6]
            elif interactionPoint == self.IP_2:
                self.betaStarX = [   10.00   ,   10.00   ]
                self.betaStarY = [   10.00   ,   10.00   ]
                self.posX      = [    2.00e-3,   -2.00e-3]
                self.posY      = [    0.00e-3,    0.00e-3]
                self.crossingX = [  290.00e-9, -290.00e-9]
                self.crossingY = [  240.00e-6, -240.00e-6]
            elif interactionPoint == self.IP_5:
                self.betaStarX = [  300.00e-3,  300.00e-3]
                self.betaStarY = [   75.00e-3,   75.00e-3]
                self.posX      = [    0.00e-3,    0.00e-3]
                self.posY      = [  750.00e-6, -750.00e-6]
                self.crossingX = [  275.00e-6, -275.00e-6]
                self.crossingY = [    0.00e-6,    0.00e-6]
            elif interactionPoint == self.IP_8:
                self.betaStarX = [    3.00   ,    3.00   ]
                self.betaStarY = [    3.00   ,    3.00   ]
                self.posX      = [    0.00e-3,    0.00e-3]
                self.posY      = [   -2.00e-3,    2.00e-3]
                self.crossingX = [ -415.00e-6,  415.00e-6]
                self.crossingY = [   -1.81e-6,    1.81e-6]
            else:
                logger.error("Unknown interaction point encountered")
        elif machineConfig == self.CONF_VDM_30:
            self.beamEnergy    = [ 7000.00e9 , 7000.00e9 ]
            self.partPerBunch  = [    2.20e11,    2.20e11]
            self.nBunches      = [ 2748      , 2748      ]
            self.normEmittance = [    2.50e-6,    2.50e-6]
            if interactionPoint == self.IP_1:
                self.betaStarX = [   30.00   ,   30.00   ]
                self.betaStarY = [   30.00   ,   30.00   ]
                self.posX      = [ -750.00e-6,  750.00e-6]
                self.posY      = [    0.00e-3,    0.00e-3]
                self.crossingX = [    0.00e-6,    0.00e-6]
                self.crossingY = [  295.00e-6, -295.00e-6]
            elif interactionPoint == self.IP_2:
                self.betaStarX = [   30.00   ,   30.00   ]
                self.betaStarY = [   30.00   ,   30.00   ]
                self.posX      = [    2.00e-3,   -2.00e-3]
                self.posY      = [    0.00e-3,    0.00e-3]
                self.crossingX = [  300.00e-9, -290.00e-9]
                self.crossingY = [  240.00e-6, -240.00e-6]
            elif interactionPoint == self.IP_5:
                self.betaStarX = [   30.00   ,   30.00   ]
                self.betaStarY = [   30.00   ,   30.00   ]
                self.posX      = [ -750.00e-6,  750.00e-6]
                self.posY      = [  750.00e-6, -750.00e-6]
                self.crossingX = [  295.00e-6, -295.00e-6]
                self.crossingY = [  295.00e-6, -295.00e-6]
            elif interactionPoint == self.IP_8:
                self.betaStarX = [   30.00   ,   30.00   ]
                self.betaStarY = [   30.00   ,   30.00   ]
                self.posX      = [    0.00e-3,    0.00e-3]
                self.posY      = [   -2.00e-3,    2.00e-3]
                self.crossingX = [ -305.00e-6,  305.00e-6]
                self.crossingY = [   -1.80e-6,    1.80e-6]
            else:
                logger.error("Unknown interaction point encountered")
        elif machineConfig == self.CONF_LOW_BETA:
            self.beamEnergy    = [ 7000.00e9 , 7000.00e9 ]
            self.partPerBunch  = [    2.20e11,    2.20e11]
            self.nBunches      = [ 2748      , 2748      ]
            self.normEmittance = [    2.50e-6,    2.50e-6]
            if interactionPoint == self.IP_1:
                self.betaStarX = [  480.00e-3,  480.00e-3]
                self.betaStarY = [  480.00e-3,  480.00e-3]
                self.posX      = [   -2.00e-3,    2.00e-3]
                self.posY      = [    0.00e-3,    0.00e-3]
                self.crossingX = [    0.00e-6,    0.00e-6]
                self.crossingY = [  295.00e-6, -295.00e-6]
            elif interactionPoint == self.IP_2:
                self.betaStarX = [  500.00e-3,  500.00e-3]
                self.betaStarY = [  500.00e-3,  500.00e-3]
                self.posX      = [    2.00e-3,   -2.00e-3]
                self.posY      = [    0.00e-3,    0.00e-3]
                self.crossingX = [  290.00e-9, -290.00e-9]
                self.crossingY = [  240.00e-6, -240.00e-6]
            elif interactionPoint == self.IP_5:
                self.betaStarX = [  480.00e-3,  480.00e-3]
                self.betaStarY = [  480.00e-3,  480.00e-3]
                self.posX      = [    0.00e-3,    0.00e-3]
                self.posY      = [    2.00e-3,   -2.00e-3]
                self.crossingX = [  295.00e-6, -295.00e-6]
                self.crossingY = [    0.00e-6,    0.00e-6]
            elif interactionPoint == self.IP_8:
                self.betaStarX = [  500.00e-3,  500.00e-3]
                self.betaStarY = [  500.00e-3,  500.00e-3]
                self.posX      = [    0.00e-3,    0.00e-3]
                self.posY      = [   -2.00e-3,    2.00e-3]
                self.crossingX = [ -305.00e-6,  305.00e-6]
                self.crossingY = [   -1.81e-6,    1.81e-6]
            else:
                logger.error("Unknown interaction point encountered")
        else:
            logger.error("Unknown machine config encountered")
        
        return
    
# End Class HLLHCv12
