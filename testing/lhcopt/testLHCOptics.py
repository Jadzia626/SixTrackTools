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

from sttools.lhcopt import LHCOptics

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

lhcOpts = LHCOptics(LHCOptics.HLLHC1_0)
lhcOpts.setConfigIP(0,LHCOptics.IP_1)
lhcOpts.echoValues()
