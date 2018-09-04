# -*- coding: utf-8 -*
"""SixTrack Tools - LHC Parameters

  SixTrack Tools - LHC Parameters
 =================================
  Module that holds LHC parameters
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging
import sttools

logger = logging.getLogger(__name__)

class LHCParams():

    LHC_IPS_B1 = [
        26658.883200, # LHC Length
            0.000000, # IP1
         3332.436584, # IP2
         6664.720800, # IP3
         9997.005016, # IP4
        13329.289233, # IP5
        16661.725816, # IP6
        19994.162400, # IP7
        23315.378984, # IP8
    ]

# END Class LHCParams
