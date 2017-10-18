# -*- coding: utf-8 -*
"""SixTrack Tools - HiLumi Parameters 1.3

  SixTrack Tools - HiLumi Parameters 1.3
 ========================================
  HL-LHC 1.3 Parameters
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import sttools

logger = logging.getLogger(__name__)

#  Optics Version 1.3
# ====================
#  http://abpdata.web.cern.ch/abpdata/lhc_optics_web/www/hllhc13/

class HLLHCv13():
    
    # Configurations
    CONF_INJECTION         = 0
    CONF_PRE_SQUEEZE       = 1
    CONF_COLLISION_ROUND20 = 2
    CONF_COLLISION_ROUND15 = 3
    
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
                self.posX      = [    2.00e-3,   -2.00e-3]
                self.posY      = [    0.00e-3,    0.00e-3]
                self.crossingX = [    0.00e-6,    0.00e-6]
                self.crossingY = [  295.00e-6, -295.00e-6]
            elif interactionPoint == self.IP_2:
                self.betaStarX = [   10.00   ,   10.00   ]
                self.betaStarY = [   10.00   ,   10.00   ]
                self.posX      = [   -3.50e-3,    3.50e-3]
                self.posY      = [    0.00e-3,    0.00e-3]
                self.crossingX = [   44.54e-6,   35.46e-6]
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
                self.crossingX = [ 1930.00e-6,-1930.00e-6]
                self.crossingY = [  -11.85e-6,  -68.15e-6]
            else:
                logger.error("Unknown interaction point encountered")
        elif machineConfig == self.CONF_PRE_SQUEEZE:
            self.beamEnergy    = [ 7000.00e9 , 7000.00e9 ]
            self.partPerBunch  = [    2.20e11,    2.20e11]
            self.nBunches      = [ 2748      , 2748      ]
            self.normEmittance = [    2.50e-6,    2.50e-6]
            if interactionPoint == self.IP_1:
                self.betaStarX = [  500.00e-3,  500.00e-3]
                self.betaStarY = [  500.00e-3,  500.00e-3]
                self.posX      = [  750.00e-6, -750.00e-6]
                self.posY      = [    0.00e-3,    0.00e-3]
                self.crossingX = [    0.00e-6,    0.00e-6]
                self.crossingY = [  295.00e-6, -295.00e-6]
            elif interactionPoint == self.IP_2:
                self.betaStarX = [   10.00   ,   10.00   ]
                self.betaStarY = [   10.00   ,   10.00   ]
                self.posX      = [   -2.00e-3,    2.00e-3]
                self.posY      = [    0.00e-3,    0.00e-3]
                self.crossingX = [  290.00e-9, -290.00e-9]
                self.crossingY = [  270.00e-6, -270.00e-6]
            elif interactionPoint == self.IP_5:
                self.betaStarX = [  500.00e-3,  500.00e-3]
                self.betaStarY = [  500.00e-3,  500.00e-3]
                self.posX      = [    0.00e-3,    0.00e-3]
                self.posY      = [  750.00e-6, -750.00e-6]
                self.crossingX = [  295.00e-6, -295.00e-6]
                self.crossingY = [    0.00e-6,    0.00e-6]
            elif interactionPoint == self.IP_8:
                self.betaStarX = [    3.00   ,    3.00   ]
                self.betaStarY = [    3.00   ,    3.00   ]
                self.posX      = [    0.00e-3,    0.00e-3]
                self.posY      = [   -2.00e-3,    2.00e-3]
                self.crossingX = [ -115.00e-6,  115.00e-6]
                self.crossingY = [    1.81e-6,   -1.81e-6]
            else:
                logger.error("Unknown interaction point encountered")
        elif machineConfig == self.CONF_COLLISION_ROUND20:
            self.beamEnergy    = [ 7000.00e9 , 7000.00e9 ]
            self.partPerBunch  = [    2.20e11,    2.20e11]
            self.nBunches      = [ 2748      , 2748      ]
            self.normEmittance = [    2.50e-6,    2.50e-6]
            if interactionPoint == self.IP_1:
                self.betaStarX = [  200.00e-3,  200.00e-3]
                self.betaStarY = [  200.00e-3,  200.00e-3]
                self.posX      = [  750.00e-6, -750.00e-6]
                self.posY      = [    0.00e-3,    0.00e-3]
                self.crossingX = [    0.00e-6,    0.00e-6]
                self.crossingY = [  295.00e-6, -295.00e-6]
            elif interactionPoint == self.IP_2:
                self.betaStarX = [   10.00   ,   10.00   ]
                self.betaStarY = [   10.00   ,   10.00   ]
                self.posX      = [   -2.00e-3,    2.00e-3]
                self.posY      = [    0.00e-3,    0.00e-3]
                self.crossingX = [  290.00e-9, -290.00e-9]
                self.crossingY = [  270.00e-6, -270.00e-6]
            elif interactionPoint == self.IP_5:
                self.betaStarX = [  200.00e-3,  200.00e-3]
                self.betaStarY = [  200.00e-3,  200.00e-3]
                self.posX      = [    0.00e-3,    0.00e-3]
                self.posY      = [  750.00e-6, -750.00e-6]
                self.crossingX = [  295.00e-6, -295.00e-6]
                self.crossingY = [    0.00e-6,    0.00e-6]
            elif interactionPoint == self.IP_8:
                self.betaStarX = [    3.00   ,    3.00   ]
                self.betaStarY = [    3.00   ,    3.00   ]
                self.posX      = [    0.00e-3,    0.00e-3]
                self.posY      = [   -2.00e-3,    2.00e-3]
                self.crossingX = [ -115.00e-6,  115.00e-6]
                self.crossingY = [    1.81e-6,   -1.81e-6]
            else:
                logger.error("Unknown interaction point encountered")
        elif machineConfig == self.CONF_COLLISION_ROUND15:
            self.beamEnergy    = [ 7000.00e9 , 7000.00e9 ]
            self.partPerBunch  = [    2.20e11,    2.20e11]
            self.nBunches      = [ 2748      , 2748      ]
            self.normEmittance = [    2.50e-6,    2.50e-6]
            if interactionPoint == self.IP_1:
                self.betaStarX = [  150.00e-3,  150.00e-3]
                self.betaStarY = [  150.00e-3,  150.00e-3]
                self.posX      = [  750.00e-6, -750.00e-6]
                self.posY      = [    0.00e-3,    0.00e-3]
                self.crossingX = [    0.00e-6,    0.00e-6]
                self.crossingY = [  295.00e-6, -295.00e-6]
            elif interactionPoint == self.IP_2:
                self.betaStarX = [   10.00   ,   10.00   ]
                self.betaStarY = [   10.00   ,   10.00   ]
                self.posX      = [   -2.00e-3,    2.00e-3]
                self.posY      = [    0.00e-3,    0.00e-3]
                self.crossingX = [  290.00e-9, -290.00e-9]
                self.crossingY = [  270.00e-6, -270.00e-6]
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
                self.crossingX = [ -115.00e-6,  115.00e-6]
                self.crossingY = [    1.81e-6,   -1.81e-6]
            else:
                logger.error("Unknown interaction point encountered")
        else:
            logger.error("Unknown machine config encountered")
        
        return
    
# End Class HLLHCv12
