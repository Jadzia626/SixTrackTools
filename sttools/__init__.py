#!/usr/bin/env python3
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
from .stdump import STDump
from .twiss  import Twiss

__all__ = ["STDump","Twiss"]

# Package Meta
__author__     = "Veronica Berglyd Olsen"
__copyright__  = "Copyright 2017, Veronica Berglyd Olsen"
__credits__    = ["Veronica Berglyd Olsen"]
__license__    = "GPLv3"
__version__    = "0.1.0"
__date__       = "2017"
__maintainer__ = "Veronica Berglyd Olsen"
__email__      = "v.k.b.olsen@cern.ch"
__status__     = "Development"

logging.basicConfig(
    format  = "[%(asctime)s] %(name)s:%(lineno)-4d %(levelname)s: %(message)s",
    level   = logging.DEBUG,
#   datefmt = "%Y-%m-%d %H:%M:%S",
    datefmt = "%H:%M:%S",
)

if __name__ == '__main__':
    print("SixTrack Tools")
