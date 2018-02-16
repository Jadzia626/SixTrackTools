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
from .aperture import Aperture
from .fort2    import Fort2
from .fort3    import Fort3
from .stdump   import STDump
from .tablefs  import TableFS
from .twiss    import Twiss

__all__ = ["Aperture","Fort2","Fort3","STDump","TableFS","Twiss"]

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
logger   = logging.getLogger(__name__)
logLevel = logging.INFO

if logLevel == logging.DEBUG:
    logging.basicConfig(
        format  = "[%(asctime)s] %(name)s:%(lineno)d %(levelname)s: %(message)s",
        level   = logging.DEBUG,
        datefmt = "%Y-%m-%d %H:%M:%S",
    )
else:
    logging.basicConfig(
        format  = "%(levelname)s: %(message)s",
        level   = logLevel,
        datefmt = "%H:%M:%S",
    )
