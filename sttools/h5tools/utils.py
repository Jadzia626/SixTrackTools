# -*- coding: utf-8 -*
"""SixTrack HDF5 Utils

  SixTrack Tools - HDF5 Utils
 =============================
  A few HDF5 utilities
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging
import numpy as np
import h5py

logger = logging.getLogger(__name__)

class H5Utils:

    @staticmethod
    def getAttrString(h5Obj,valName,valIdx=0,defaultVal=""):
        if valName in h5Obj.attrs.keys():
            return h5Obj.attrs[valName][valIdx].decode("utf-8")
        else:
            return defaultVal

# END Class H%Utils
