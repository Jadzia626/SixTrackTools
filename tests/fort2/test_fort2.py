#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""Test Script for Fort2 Class
  
  SixTrack Tools - Test Script for Fort2 Class
 ==============================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import filecmp as fcmp

from os      import path
from sttools import Fort2

currPath = path.dirname(path.realpath(__file__))

fTwo = Fort2(currPath,"fort.2.ref")

def testFileLoad():
    assert fTwo.loadFile()

