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
from .tablefs import TableFS

logger = logging.getLogger(__name__)

class Aperture:
    
    fileName   = None
    fileLoaded = None
    
    aperData   = None
    aperS      = None # Position along the beam line
    aperX      = None # Horisontal aperture limits
    aperY      = None # Vertical aperture limits
    aperN      = None # Number of elements
    
    def __init__(self, fileName):
        
        self.fileLoaded = False
        self.filterOpts = {
            
        }
        
        if path.isfile(fileName):
            logger.info("Loading file %s" % path.basename(fileName))
        else:
            logger.error("File not found %s" % fileName)
            return
        
        self.fileName   = fileName
        self.aperData   = TableFS(self.fileName)
        self.fileLoaded = True
        
        return
    
    def parseApertures(self):
        
        # Pre-allocate arrays
        self.aperN = self.aperData.nLines
        self.aperS = np.zeros(self.aperN)
        self.aperX = np.zeros(self.aperN)
        self.aperY = np.zeros(self.aperN)
        
        for n in range(self.aperN):
            
            aperName = self.aperData.Data["NAME"][n]
            aperKeyw = self.aperData.Data["KEYWORD"][n]
            aperType = self.aperData.Data["APERTYPE"][n]
            
            self.aperS[n] = self.aperData.Data["S"][n]
            
            if   aperType == "CIRCLE":
                self.aperX[n] = self.aperData.Data["APER_1"][n]
                self.aperY[n] = self.aperData.Data["APER_1"][n]
            elif aperType == "RECTANGLE":
                self.aperX[n] = self.aperData.Data["APER_1"][n]
                self.aperY[n] = self.aperData.Data["APER_2"][n]
            elif aperType == "ELLIPSE":
                self.aperX[n] = self.aperData.Data["APER_1"][n]
                self.aperY[n] = self.aperData.Data["APER_2"][n]
            elif aperType == "RECTELLIPSE":
                self.aperX[n] = min(self.aperData.Data["APER_1"][n], self.aperData.Data["APER_3"][n])
                self.aperY[n] = min(self.aperData.Data["APER_2"][n], self.aperData.Data["APER_4"][n])
            elif aperType == "RACETRACK":
                self.aperX[n] = self.aperData.Data["APER_1"][n] + self.aperData.Data["APER_3"][n]
                self.aperY[n] = self.aperData.Data["APER_2"][n] + self.aperData.Data["APER_4"][n]
            elif aperType == "NONE":
                self.aperX[n] = 0.0
                self.aperY[n] = 0.0
            else:
                logger.warning("Unhandled APERTYPE '%s'" % aperType)
                self.aperX[n] = 9.999
                self.aperY[n] = 9.999
        
        return
    
# END Class Aperture
