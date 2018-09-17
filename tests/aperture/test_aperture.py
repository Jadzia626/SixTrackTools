# -*- coding: utf-8 -*
"""Test Script for Aperture Class
  
  SixTrack Tools - Test Script for Aperture Class
 =================================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import filecmp as fcmp

from os                import path, unlink
from sttools.filetools import Aperture

currPath = path.dirname(path.realpath(__file__))

lhcAper = Aperture(currPath,"aperture.tfs.input")

def testFileParse():
    assert lhcAper.parseAperture()
    #assert False

