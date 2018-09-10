# -*- coding: utf-8 -*
"""SixTrack Concatenat0r

  SixTrack Tools - Concatenat0r
 ===============================
  Collects Simulation Data from Multiple DataSets
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging
import numpy as np
import h5py

from os import path, listdir

logger = logging.getLogger(__name__)

class Concatenator:

    fileList = []
    metaFile = None

    def __init__(self, inFolder):

        if not path.isdir(inFolder):
            logger.error("Path not found: %s" % inFolder)
            return

        self.inFolder = inFolder
        self.fileList = []

        return

    def loadAll(self, theExt=None):

        fileList = listdir(self.inFolder)
        if theExt is None:
            extList = (".hdf5",".h5",".hdf")
        else:
            extList = (theExt)

        for elem in fileList:
            fName, fExt = path.splitext(elem)
            if fExt in extList:
                self.fileList.append(elem)

        return True

    def writeMetaFile(self, fileName="metafile.h5"):
        """This functions creates a dummy HDF5 file containing external links to all files in the
        concatenated set of files. The feature is described in the h5py documentation here:
        http://docs.h5py.org/en/latest/high/group.html?highlight=externallink
        """
        mFileName = path.join(self.inFolder,fileName)
        self.metaFile = h5py.File(mFileName,"w")
        for h5File in self.fileList:
            print("%-40s : %-40s" % (h5File,path.basename(h5File)))
            if path.samefile(mFileName,path.join(self.inFolder,h5File)):
                # Don't link to itself!
                continue
            self.metaFile[path.splitext(h5File)[0]] = h5py.ExternalLink(h5File, self.inFolder)
        return True

    # ToDo!
    # def writeFullFile(self, fileName="concatfile.h5"):
    #     mFileName = path.join(self.inFolder,fileName)
    #     self.metaFile = h5py.File(mFileName,"w")
    #     for h5File in self.fileList:
    #         print("%-40s : %-40s" % (h5File,path.basename(h5File)))
    #         if path.samefile(mFileName,path.join(self.inFolder,h5File)):
    #             # Don't link to itself!
    #             continue
    #         self.metaFile[path.splitext(h5File)[0]] = h5py.ExternalLink(h5File, self.inFolder)
    #     return True

    def extractAppend(self, dataSet, dataCol):

        for inFile in self.fileList:
            filePath = path.join(self.inFolder,inFile)
            h5File = h5py.File(filePath, mode="r")

        return True

# END Class Concatenator
