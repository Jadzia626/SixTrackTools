# -*- coding: utf-8 -*
"""Test Script for Fort3 Class
  
  SixTrack Tools - Test Script for Fort3 Class
 ==============================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import filecmp as fcmp

from os      import path, unlink
from sttools import Fort3

currPath = path.dirname(path.realpath(__file__))

fThree = Fort3(currPath,"fort.3.input")

def testFileLoad():
    assert fThree.loadFile()
    assert False
