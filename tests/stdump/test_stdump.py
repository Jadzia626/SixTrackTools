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
from sttools import STDump

currPath = path.dirname(path.realpath(__file__))

stData = STDump(path.join(currPath,"scatter_log.txt"))

def testReadAll():
    stData.readAll()
    assert stData.nLines == 128

def testFilterPart():
    stData.filterPart("TURN",11)
    assert len(stData.filData["TURN"]) == 128
    stData.filterPart("ID",11)
    assert len(stData.filData["TURN"]) == 1

#print("".join("%s: %s\n" % item for item in vars(stData).items()))
