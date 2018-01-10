# -*- coding: utf-8 -*
"""Aperture Parser

  SixTrack Tools - Aperture Parser
 ==================================
  Parses MadX Aperture Data
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging
import numpy   as np
import re

from os import path

logger = logging.getLogger(__name__)

class Aperture:
    
    def __init__(self, fileName):
        
        self.fileName = fileName
        
        return
    
# END Class Aperture
