# -*- coding: utf-8 -*
"""Python Toolbox for SixTrack, Column Name Maps

  SixTrack Tools - Column Name Maps
 ===================================
  This class holds maps to map SixTrack ascii file column names to HDF5 names
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging

# Logging
logger = logging.getLogger(__name__)

class STColMaps():

    COLLIMAT_DIST = {
        "0" : "X",
        "1" : "XP",
        "2" : "Y",
        "3" : "YP",
        "4" : "S",
        "5" : "P",
    }

    MAP_COLS = {
        "dist0.dat" : COLLIMAT_DIST,
        "distn.dat" : COLLIMAT_DIST,
    }

# END Class STColMaps
