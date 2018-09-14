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
from sttools.filetools import TableFS

logger = logging.getLogger(__name__)

class Aperture:
    
    filePath   = None # Folder where aperture file is saved
    fileName   = None # Name of aperture file
    fileLoaded = None # Set to True after file is successfully loaded
    
    typePath   = None # The path for custom apertypes
    
    aperData   = None # The aperture file data (TableFS object)
    aperS      = None # Position along the beam line
    aperX      = None # Horisontal aperture limits
    aperY      = None # Vertical aperture limits
    aperN      = None # Number of elements
    
    customAper = None # Storage for custom apertypes
    
    def __init__(self, filePath, fileName):
        
        # Defaults
        self.fileLoaded = False
        self.filterOpts = {}
        self.customAper = {}
        
        if path.isdir(filePath):
            self.filePath = filePath
            self.typePath = filePath
        else:
            logger.error("Path not found: %s", filePath)
        
        if path.isfile(path.join(filePath,fileName)):
            self.fileName = fileName
            logger.info("Loading file %s" % fileName)
        else:
            logger.error("Found no %s file in path", fileName)
        
        self.aperData   = TableFS(path.join(self.filePath,self.fileName))
        self.fileLoaded = True
        
        return
    
    def parseAperture(self):
        
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
                wasFound, aperData = self.customAperture(aperType)
                if wasFound:
                    # This assumes the shape is an octagon:
                    self.aperX[n] = aperData["MaxX"]
                    self.aperY[n] = aperData["MaxY"]
                else:
                    logger.warning("Unhandled APERTYPE '%s'" % aperType)
                    self.aperX[n] = 9.999
                    self.aperY[n] = 9.999
        
        return True
    
    def customAperture(self, aperType):
        
        if aperType in self.customAper.keys():
            return True, self.customAper[aperType]
        else:
            logger.info("Unknown apertype '%s', looking for definition file", aperType)
        
        fnOrig  = path.join(self.typePath,aperType)
        fnLower = path.join(self.typePath,aperType.lower())
        fnUpper = path.join(self.typePath,aperType.upper())
        
        if   path.isfile(fnOrig):
            toLoad = fnOrig
        elif path.isfile(fnLower):
            toLoad = fnLower
        elif path.isfile(fnUpper):
            toLoad = fnUpper
        else:
            logger.error("No file matching apertype '%s' found in folder: %s" % (aperType,self.typePath))
            logger.error("If files are stored elsewhere, set the correct path with method setTypePath()")
            return False, None
        
        logger.info("Found aperture file '%s'" % path.basename(toLoad))
        
        xCoords = []
        yCoords = []
        
        with open(toLoad,"r") as inFile:
            for theLine in inFile:
                xySplit = theLine.split()
                if len(xySplit) == 2:
                    xCoords.append(xySplit[0])
                    yCoords.append(xySplit[1])
        
        xCoords = np.asarray(xCoords,dtype="float")
        yCoords = np.asarray(yCoords,dtype="float")
        
        aperData = {
            "X"    : xCoords,
            "Y"    : yCoords,
            "MaxX" : max(abs(xCoords)),
            "MaxY" : max(abs(yCoords)),
        }
        self.customAper[aperType] = aperData
        
        return True, aperData
    
    #
    # Setters and Getters
    #
    
    def setTypePath(self, typePath):
        
        if not path.isdir(typePath):
            logger.error("Path not found: %s" % typePath)
            return False
            
        self.typePath = typePath
        logger.info("Custom apertype path is: %s" % typePath)
        
        return True
    
# END Class Aperture
