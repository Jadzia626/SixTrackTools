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

unlink(path.join(currPath,"test.hdf5"))
fCC = Concatenator(path.join(currPath,"test.hdf5"),True)

def testLoadDumpFile():
    assert fCC.appendParticles(path.join(currPath,"dump_ip5.txt"),Concatenator.FTYPE_PART_DUMP)

#unlink(path.join(currPath,"test.hdf5"))
