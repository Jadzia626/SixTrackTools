# -*- coding: utf-8 -*
"""Python Toolbox for SixTrack, Simulation Wrapper

  SixTrack Tools - Simulation Wrapper
 =====================================
  Class to wrap a set of related simulations in a single folder
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging
import numpy as np

from os import path, listdir

from sttools.functions         import parseKeyWordArgs, checkValue
from sttools.h5tools.wrapper   import H5Wrapper
from sttools.filetools.wrapper import FileWrapper

# Logging
logger = logging.getLogger(__name__)

class SixTrackSim():

    TYPE_FILE = 0
    TYPE_HDF5 = 1

    simData    = None  # Holds either a H5Wrapper or FileWrapper object
    dataType   = None  # Whether the simulation set is HDF5 or TEXT
    isSingular = False # Whether a TEXT set is only one simulation

    def __init__(self, simFolder, **theArgs):
        """Wraps a folder containing SixTrack simulations and scans the content looking for either
        HDF5 files or subfolders presumably containing SixTrack simulation files. dataType is auto-
        detected but can be overridden. loadOnly gives a list of sets to load, excluding all else.
        orderBy defines how to order the sets, which defaults to order by name. forceAccept disables
        any checks for whether the simulation set actually contains SixTrack data.
        """

        if path.isdir(simFolder):
            self.simFolder = simFolder
            logger.debug("Simulation folder is %s" % simFolder)
        else:
            raise FileNotFoundError("The folder '%s' does not exist." % simFolder)

        valArgs = {
            "dataType"    : None,  # HDF5 files or text files
            "loadOnly"    : None,  # Only load these files/folders
            "orderBy"     : 0,     # How to order simulation sets. 0 = by name.
            "forceAccept" : False, # Whether to ignore validity checks for simulation sets
            "isSingular"  : False, # Whether the folder contains files from a single simulation
        }
        kwArgs = parseKeyWordArgs(valArgs, theArgs)

        # Detecting dataType
        simList = listdir(simFolder)
        h5List  = [".h5",".hdf",".hdf5"]
        nDirs   = 0
        nFiles  = 0
        nHDF5   = 0
        for simElem in simList:
            sPath       = path.join(simFolder,simElem)
            fBase, fExt = path.splitext(simElem)
            if simElem[0] == ".":  continue
            if path.isdir(sPath):  nDirs  += 1
            if path.isfile(sPath): nFiles += 1
            if fExt in h5List:     nHDF5  += 1
        if nHDF5 > nDirs:
            logger.info("Found %d HDF5 file(s). Assuming dataType is HDF5." % nHDF5)
            self.dataType = self.TYPE_HDF5
        elif nDirs > nFiles:
            logger.info("Found %d folders. Assuming dataType is TEXT." % nDirs)
            self.dataType = self.TYPE_FILE
        elif nFiles > nDirs:
            logger.info("Found %d files. Assuming dataType is TEXT." % nFiles)
            self.dataType = self.TYPE_FILE
            self.isSingular = True
        elif nHDF5 > 0:
            logger.info("Found %d HDF5 file(s). Assuming dataType is HDF5." % nHDF5)
            self.dataType = self.TYPE_HDF5
        elif nDirs > 0:
            logger.info("Found %d folders. Assuming dataType is TEXT." % nDirs)
            self.dataType = self.TYPE_FILE
        else:
            logger.error("Unable to detect the content of %s" % simFolder)
            logger.error(" * Found %d subfolders" % nDirs)
            logger.error(" * Found %d files" % nFiles)
            logger.error(" * Found %d HDF5 files" % nHDF5)
            return

        if kwArgs["dataType"] is not None:
            if   checkValue(kwArgs["dataType"], ["text",self.TYPE_FILE], False):
                logger.info("Setting dataType to TEXT.")
                self.dataType = self.TYPE_FILE
            elif checkValue(kwArgs["dataType"], ["hdf5",self.TYPE_HDF5], False):
                logger.info("Setting dataType to HDF5.")
                self.dataType = self.TYPE_HDF5
            else:
                logger.error("Unknown fileType specified.")
                return

        if checkValue(kwArgs["isSingular"], [True,False]):
            self.isSingular = kwArgs["isSingular"]

        if self.dataType == self.TYPE_FILE:
            self.simData = FileWrapper(
                simFolder,
                loadOnly    = kwArgs["loadOnly"],
                orderBy     = kwArgs["orderBy"],
                forceAccept = kwArgs["forceAccept"],
                isSingular  = kwArgs["isSingular"]
            )
        else:
            self.simData = H5Wrapper(
                simFolder,
                loadOnly    = kwArgs["loadOnly"],
                orderBy     = kwArgs["orderBy"],
                forceAccept = kwArgs["forceAccept"]
            )

        return
    
    def __len__(self):
        if self.simData is None:
            return None
        else:
            return len(self.simData)
    
    def __getitem__(self, simSet):
        if self.simData is None:
            return None
        else:
            return self.simData[simSet]

    #
    #  Class Methods
    #

    def checkDataSetKey(self, reqSet):
        if self.simData is None:
            return None
        else:
            return self.simData.checkDataSetKey(reqSet)

# END Class SixTrackSim
