# -*- coding: utf-8 -*
"""Test Script for Fort2 Class
  
  SixTrack Tools - Test Script for Fort2 Class
 ==============================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import filecmp as fcmp

from os      import path, unlink
from sttools import Concatenator

currPath = path.dirname(path.realpath(__file__))

fCC = Concatenator(path.join(currPath,"test.hdf5"))

def testFileInit():
    assert fCC.initFile()

