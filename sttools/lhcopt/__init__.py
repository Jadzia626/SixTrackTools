# -*- coding: utf-8 -*
"""Python Toolbox for SixTrack, LHC Optics

  SixTrack Tools - LHC Optics
 =============================
  Python Toolbox for SixTrack, LHC Optics
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging

# Submodules
from .lhcopt    import LHCOptics
from .lhcparams import LHCParams

__all__ = ["LHCOptics","LHCParams"]

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
