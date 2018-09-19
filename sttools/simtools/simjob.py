# -*- coding: utf-8 -*
"""Python Toolbox for SixTrack, Simulation Job Class

  SixTrack Tools - Simulation Job Class
 =======================================
  Class for setting up and running SixTrack simulations
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging

# Logging
logger = logging.getLogger(__name__)

class SixTrackJob():

    def __init__(self, jobFolder):
        self.jobFolder = jobFolder
        return

# END Class SixTrackJob
