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

from os       import path, listdir
from datetime import datetime

from sttools.functions     import pPrintDict, parseKeyWordArgs
from sttools.h5tools.utils import H5Utils

logger = logging.getLogger(__name__)

class H5Wrapper():

    ORDERBY_NAME  = 0
    ORDERBY_SIMNO = 1
    ORDERBY_TIME  = 2

    ORDERBY_VALID = [0,1,2]

    simList = [] # The list of accepted files, in order
    simMeta = {} # The meta data of the files
    simSets = [] # A list of all datasets across simulations
    iterIdx = 0  # Used for the iterator

    def __init__(self, simFolder, **theArgs):

        if not path.isdir(simFolder):
            logger.error("Path not found: %s" % simFolder)
            return

        valArgs = {
            "orderBy"     : self.ORDERBY_SIMNO,
            "forceAccept" : False,
            "loadOnly"    : None,
        }
        kwArgs = parseKeyWordArgs(valArgs, theArgs)

        self.simFolder   = simFolder
        self.forceAccept = kwArgs["forceAccept"]
        self.loadOnly    = kwArgs["loadOnly"]
        if kwArgs["orderBy"] in self.ORDERBY_VALID:
            self.orderBy = kwArgs["orderBy"]
        else:
            logger.error("OrderBy value %d is invalid" % kwArgs["orderBy"])
            return

        self._scanFolder()

        return

    def __len__(self):
        return len(self.simList)

    def __contains__(self, simSet):
        if simSet in self.simList:
            return True
        else:
            return False

    def __getitem__(self, simSet):
        if isinstance(simSet, int):
            if abs(simSet) < len(self.simList):
                # We allow negative indices for looking backwards in the array
                simKey = self.simList[simSet]
            else:
                raise IndexError("Index value is out of range.")
        elif isinstance(simSet, str):
            if simSet in self.simList:
                simKey = simSet
            else:
                raise KeyError("Simulation key does not exist in this set.")
        else:
            raise KeyError("Key value must be either a string or an integer.")
        fPath = self.simMeta[simKey]["SimPath"]
        logger.info("Loading dataset '%s'" % (simKey))
        return h5py.File(fPath,"r")

    def __iter__(self):
        self.iterIdx = 0
        return self.__getitem__[self.iterIdx]

    def __next__(self):
        self.iterIdx += 1
        if self.iterIdx >= len(self.simList):
            raise StopIteration
        else:
            return self.__getitem__[self.iterIdx]

    def __str__(self):
        sumStr  = " Simulation Summary\n"
        sumStr += "====================\n"
        sumStr += "Path: %s\n" % self.simFolder
        sumStr += "\n"
        sumStr += "{:20} {:20} {:>9} {:>9}\n".format("Simulation","Software","Particles","Turns")
        sumStr += "-"*61
        for h5Set in self.fileList:
            sumStr += "{SimName:20} {CreatedBy:20} {Particles:9d} {Turns:9d}\n".format(**self.fileMeta[h5Set])
        return sumStr

    #
    #  Class Methods
    #

    def checkDataSetKey(self, reqSet):
        """Check if a dataset exists and if necessary translate the key.
        """
        if reqSet in self.simSets:
            return reqSet
        else:
            reqSet = reqSet.lower()
            # Aperture
            if reqSet == "aperture_losses": return "aperture/losses"
            # Collimation
            if reqSet == "all_absorptions": return "collimation/all_absorptions"
            if reqSet == "all_impacts":     return "collimation/all_impacts"
            if reqSet == "coll_scatter":    return "collimation/coll_scatter"
            if reqSet == "coll_summary":    return "collimation/coll_summary"
            if reqSet == "dist0":           return "collimation/dist0"
            if reqSet == "distn":           return "collimation/distn"
            if reqSet == "efficiency":      return "collimation/efficiency"
            if reqSet == "efficiency_2d":   return "collimation/efficiency_2d"
            if reqSet == "efficiency_dpop": return "collimation/efficiency_dpop"
            if reqSet == "first_impacts":   return "collimation/first_impacts"
            if reqSet == "survival":        return "collimation/survival"
            # Scatter
            if reqSet == "scatter_log":     return "scatter/scatter_log"
            if reqSet == "scatter_summary": return "scatter/summary"
            return None
    
    #
    #  Internal Functions
    #

    def _scanFolder(self):
        """Scans a folder for HDF5 files and builds a list of valid ones.
        A valid file contains a "CreatedBy" field that states the file was written by SixTrack.
        """

        self.simList = []
        self.simMeta = {}

        fileList = listdir(self.simFolder)
        sortList = []
        readList = []
        logger.info("Loading files from '%s'" % self.simFolder)

        if self.loadOnly is None:
            self.loadOnly = fileList.copy()

        for fName in fileList:
            fBase, fExt = path.splitext(fName)
            fPath       = path.join(self.simFolder,fName)
            fStatus     = "Checking file '%s'" % fName
            if fName not in self.loadOnly:
                logger.info("%-56s [Ignored]" % fStatus)
                continue
            try:
                fH5 = h5py.File(fPath,"r")
            except:
                logger.info("%-56s [Not HDF5]" % fStatus)
                continue
            if not self.forceAccept and not H5Utils.getAttrString(fH5,"CreatedBy")[:8] == "SixTrack":
                logger.info("%-56s [Not SixTrack]" % fStatus)
                continue
            logger.info("%-56s [OK]" % fStatus)
            timeStamp = H5Utils.getAttrString(fH5,"TimeStamp")
            self.simMeta[fBase] = {
                "TimeStamp"  : timeStamp,
                "NumTime"    : datetime.strptime(timeStamp,"%Y-%m-%dT%H:%M:%S.%f").timestamp(),
                "CreatedBy"  : H5Utils.getAttrString(fH5,"CreatedBy"),
                "SimNumber"  : fH5.attrs["SimNumber"][0],
                "Particles"  : fH5.attrs["Particles"][0],
                "Turns"      : fH5.attrs["Turns"][0],
                "PreTime"    : fH5.attrs["PreTime"][0],
                "TrackTime"  : fH5.attrs["TrackTime"][0],
                "PostTime"   : fH5.attrs["PostTime"][0],
                "TotalTime"  : fH5.attrs["TotalTime"][0],
                "FileName"   : fName,
                "SimPath"    : fPath,
                "SimName"    : fBase,
                "DataSets"   : self._scanSets(fH5),
            }
            readList.append(fBase)
            if   self.orderBy == self.ORDERBY_SIMNO:
                sortList.append(self.simMeta[fBase]["SimNumber"])
            elif self.orderBy == self.ORDERBY_NAME:
                sortList.append(fBase)
            elif self.orderBy == self.ORDERBY_TIME:
                sortList.append(self.simMeta[fBase]["NumTime"])

        self.simList = [x for _,x in sorted(zip(sortList,readList))]

        fH5.close()

        return True

    def _scanSets(self, h5File):
        tmpKeys = list(h5File.keys())
        theSets = []
        # Scan root and one layer of groups
        for aKey in tmpKeys:
            if isinstance(h5File[aKey], h5py.Dataset):
                theSets.append(aKey)
            else:
                theSets += [aKey+"/"+x for x in list(h5File[aKey].keys())]
        # Write all unique sets to the simSets list
        for aSet in theSets:
            if aSet not in self.simSets:
                self.simSets.append(aSet)
        return theSets

# END Class H5Wrapper
