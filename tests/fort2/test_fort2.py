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

def testElemSize():
    assert len(fTwo.elemData["Name"]) == 183
    assert len(fTwo.elemData["Type"]) == 183
    assert len(fTwo.elemData["Val1"]) == 183
    assert len(fTwo.elemData["Val2"]) == 183
    assert len(fTwo.elemData["Val3"]) == 183
    assert len(fTwo.elemData["Val4"]) == 183
    assert len(fTwo.elemData["Val5"]) == 183
    assert len(fTwo.elemData["Val6"]) == 183

def testBlockSize():
    assert len(fTwo.blockData["Block"]) == 113
    assert len(fTwo.blockData["Drift"]) == 113

def testStructSize():
    assert len(fTwo.structData) == 3337

def testInsertElementOK():
    assert fTwo.insertElement("ip3_num",0,[0,0,0,0,0,0],0,1)
    assert fTwo.insertElement("ip3_str",0,[0,0,0,0,0,0],"ip3",2)
    assert len(fTwo.elemData["Name"]) == 185
    assert len(fTwo.elemData["Type"]) == 185
    assert len(fTwo.elemData["Val1"]) == 185
    assert len(fTwo.elemData["Val2"]) == 185
    assert len(fTwo.elemData["Val3"]) == 185
    assert len(fTwo.elemData["Val4"]) == 185
    assert len(fTwo.elemData["Val5"]) == 185
    assert len(fTwo.elemData["Val6"]) == 185
