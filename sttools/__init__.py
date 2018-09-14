# -*- coding: utf-8 -*
"""Python Toolbox for SixTrack

  SixTrack Tools
 ================
  Python Toolbox for SixTrack
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging

# Submodules
from .aperture     import Aperture
from .constants    import Const
from .fort2        import Fort2
from .fort3        import Fort3
from .hdf5import   import HDF5Import
from .partdist     import PartDist
from .stdump       import STDump
from .tablefs      import TableFS
from .twiss        import Twiss

__all__ = ["Aperture","Const","Fort2","Fort3","HDF5Import","PartDist","STDump","TableFS","Twiss"]

# Package Meta
__author__     = "Veronica Berglyd Olsen"
__copyright__  = "Copyright 2017-2018, Veronica Berglyd Olsen, CERN (BE-ABP-HSS)"
__credits__    = ["Veronica Berglyd Olsen","Kyrre Ness Sjøbæk","Andrea Santamaria Garcia"]
__license__    = "GPLv3"
__version__    = "0.1.0"
__date__       = "2018"
__maintainer__ = "Veronica Berglyd Olsen"
__email__      = "v.k.b.olsen@cern.ch"
__status__     = "Perpetual Development"

# Logging
logger = logging.getLogger(__name__)

def setLoggingLevel(logLevel, showSource=False):

    if isinstance(logLevel, str):
        logLevel = logLevel.upper()

    lvlMap = {
        "CRITICAL" : logging.CRITICAL, # 50
        "ERROR"    : logging.ERROR,    # 40
        "WARNING"  : logging.WARNING,  # 30
        "INFO"     : logging.INFO,     # 20
        "DEBUG"    : logging.DEBUG,    # 10
        "NOTSET"   : logging.NOTSET,   # 0
    }
    invMap = dict(zip(lvlMap.values(), lvlMap.keys()))
    if logLevel in lvlMap.keys():
        logLevel = lvlMap[logLevel]

    if showSource:
        logFormat = logging.Formatter(fmt = "{levelname:8} {name:>28}:{lineno:<4d}  {message}", style="{")
    else:
        logFormat = logging.Formatter(fmt = "{levelname:8}  {message}", style="{")
    logger = logging.getLogger("sttools")
    sHandle = logging.StreamHandler()
    sHandle.setFormatter(logFormat)
    logger.handlers = []
    logger.setLevel(logLevel)
    logger.addHandler(sHandle)

    return True

# Set default logging level
setLoggingLevel(logging.INFO)
