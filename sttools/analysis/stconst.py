# -*- coding: utf-8 -*
"""Python Toolbox for SixTrack, Data Analysis Constants

  SixTrack Tools - Data Analysis Constants
 ==========================================
  Tools for analysing beams
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging

# Logging
logger = logging.getLogger(__name__)

class STConst():

    BEAM_DATA = {}
    BEAM_DATA["dist0"] = {
        "NAME"  : ["X",   "XP",  "Y",   "YP",  "S",   "P"]
        "LABEL" : ["x",   "x'",  "y",   "y'",  "s",   "p"]
        "UNIT"  : ["mm",  "mrad","mm",  "mrad","mm",  "MeV"]
        "SCALE" : [1e-3,  1e-3,  1e-3,  1e-3,  1e-3,  1e6]
    }
    BEAM_DATA["distn"] = BEAM_DATA["dist0"]
        else:
            isDump    = True
            colNames  = ["X", "XP",  "Y", "YP",  "Z", "dE/E"]
            colLabels = ["x", "x'",  "y", "y'",  "z", "dE/E"]
            colUnits  = ["mm","mrad","mm","mrad","mm","MeV"]
            colScales = [-3,  -3,    -3,  -3,    -3,  6]

# END Class STConst
