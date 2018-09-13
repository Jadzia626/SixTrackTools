# -*- coding: utf-8 -*
"""SixTrack HDF5 File Wrapper

  SixTrack Tools - HDF5 File Wrapper
 ====================================
  A wrapper for a folder of HDF5 files
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging
import numpy as np
import h5py

from os import path, listdir

from sttools.functions     import pPrintDict
from sttools.h5tools.utils import H5Utils

logger = logging.getLogger(__name__)

class H5Wrapper():

    ORDERBY_SIMNO = 0
    ORDERBY_NAME  = 1
    ORDERBY_TIME  = 2

    fileList = []   # The list of accepted files, in order
    fileMeta = {}   # The meta data of the files
    data     = None # Holding the currently loaded data
    currIdx  = 0    # The index of the currently loaded data
    nData    = 0    # Number of data files

    def __init__(self, dataFolder, orderBy=ORDERBY_SIMNO, forceAccept=False):

        if not path.isdir(dataFolder):
            logger.error("Path not found: %s" % inFolder)
            return

        self.dataFolder  = dataFolder
        self.forceAccept = forceAccept
        self.orderBy     = orderBy

        self.scanFolder()

        return

    def scanFolder(self):
        """Scans a folder for HDF5 files and builds a list of valid ones.
        A valid file contains a "CreatedBy" field that states the file was written by SixTrack.
        """

        self.fileList = []
        self.fileMeta = {}

        fileList = listdir(self.dataFolder)
        logger.info("Loading files from '%s'" % self.dataFolder)

        for fName in fileList:
            fBase, fExt = path.splitext(fName)
            fPath       = path.join(self.dataFolder,fName)
            fStatus     = "Checking file '%s'" % fName
            try:
                fH5 = h5py.File(fPath,"r")
            except:
                logger.info("%-56s [Not HDF5]" % fStatus)
                continue
            if not self.forceAccept and not H5Utils.getAttrString(fH5,"CreatedBy")[:8] == "SixTrack":
                logger.info("%-56s [Not SixTrack]" % fStatus)
                continue
            logger.info("%-56s [OK]" % fStatus)
            self.nData += 1
            self.fileMeta[fBase] = {
                "TimeStamp"  : H5Utils.getAttrString(fH5,"TimeStamp"),
                "CreatedBy"  : H5Utils.getAttrString(fH5,"CreatedBy"),
                "SimNumber"  : fH5.attrs["SimNumber"][0],
                "Particles"  : fH5.attrs["Particles"][0],
                "Turns"      : fH5.attrs["Turns"][0],
                "PreTime"    : fH5.attrs["PreTime"][0],
                "TrackTime"  : fH5.attrs["TrackTime"][0],
                "PostTime"   : fH5.attrs["PostTime"][0],
                "TotalTime"  : fH5.attrs["TotalTime"][0],
                "FileName"   : fName,
                "FilePath"   : fPath,
            }

        pPrintDict(self.fileMeta)

        # Create the sorted list



        return True

# END Class H5Wrapper
