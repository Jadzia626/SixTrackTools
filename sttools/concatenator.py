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
import numpy   as np
import h5py

from os import path,listdir

logger = logging.getLogger(__name__)

class Concatenator:
    
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
    
    def extractAppend(self, dataSet, dataCol):
        
        for inFile in self.fileList:
            filePath = path.join(self.inFolder,inFile)
            h5File = h5py.File(filePath, mode="r")
            
        
        return True
    
# End Class Concatenator
