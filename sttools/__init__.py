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
from sttools.constants  import Const
from sttools.physics    import Physics
from sttools.simulation import SixTrackSim
from sttools.dataset    import DataSet

__all__ = ["Const","Physics","SixTrackSim","DataSet"]

# Package Meta
__package__    = "SixTrackTools"
__author__     = "Veronica Berglyd Olsen"
__copyright__  = "Copyright 2017-2019, Veronica Berglyd Olsen, CERN (BE-ABP-HSS)"
__credits__    = ["Veronica Berglyd Olsen","Kyrre Ness Sjøbæk","Andrea Santamaria Garcia"]
__license__    = "GPLv3"
__version__    = "0.1.0"
__date__       = "2019"
__maintainer__ = "Veronica Berglyd Olsen"
__email__      = "v.k.b.olsen@cern.ch"
__status__     = "Perpetual Development"

# Logging
logger = logging.getLogger(__name__)

def loggingConfig(logLevel, toStd=True, logFile=None, showSource=False):

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
    logger.handlers = []

    if logFile is not None:
        fHandle = logging.FileHandler(logFile)
        fHandle.setFormatter(logFormat)
        fHandle.setLevel(logLevel)
        logger.addHandler(fHandle)

    if toStd:
        sHandle = logging.StreamHandler()
        sHandle.setFormatter(logFormat)
        sHandle.setLevel(logLevel)
        logger.addHandler(sHandle)

    logger.setLevel(logLevel)

    return True

# Set default logging level
loggingConfig(logging.INFO)
