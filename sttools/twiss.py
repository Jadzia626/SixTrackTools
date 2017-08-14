# -*- coding: utf-8 -*
"""Twiss Class

  SixTrack Tools - Twiss Class
 ==============================
  Twiss (emittance) related calculations
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging
import numpy   as np

logger = logging.getLogger(__name__)


class Twiss:

    Data = None # STData object

    def __init__(self, inData):

        self.Data = inData

        if not self.Data.isNumPy:
            self.Data.convertToNumpy()

        return


## End Class Twiss    
