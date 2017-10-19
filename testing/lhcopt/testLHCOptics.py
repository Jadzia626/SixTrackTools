# -*- coding: utf-8 -*
"""SixTrack Tools - LHCOptics Test
  
  SixTrack Tools - LHCOptics Test
 =================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
  
  Test script for the LHCOptics class
  
"""

import logging
import sttools

from math import sqrt
from sttools.lhcopt import LHCOptics
from sttools.physics import calcLuminosity

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

lhcOpts = LHCOptics(LHCOptics.HLLHC1_2)
lhcOpts.setConfigIP(5,LHCOptics.IP_1)
lhcOpts.echoValues()
