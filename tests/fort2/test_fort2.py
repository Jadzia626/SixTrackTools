# -*- coding: utf-8 -*
"""Test Script for Fort2 Class
  
  SixTrack Tools - Test Script for Fort2 Class
 ==============================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import filecmp as fcmp

from os                import path, unlink
from sttools.filetools import Fort2

currPath = path.dirname(path.realpath(__file__))

fTwo = Fort2(currPath,"fort.2.input")

def testFileLoad():
    assert fTwo.loadFile()

def testElemSize():
    assert len(fTwo.elemData["Name"]) == 185
    assert len(fTwo.elemData["Type"]) == 185
    assert len(fTwo.elemData["Val1"]) == 185
    assert len(fTwo.elemData["Val2"]) == 185
    assert len(fTwo.elemData["Val3"]) == 185
    assert len(fTwo.elemData["Val4"]) == 185
    assert len(fTwo.elemData["Val5"]) == 185
    assert len(fTwo.elemData["Val6"]) == 185

def testBlockSize():
    assert len(fTwo.blockData["Block"]) == 113
    assert len(fTwo.blockData["Drift"]) == 113

def testStructSize():
    assert len(fTwo.structData) == 3340

def testInsertElementOK():
    assert fTwo.insertElement("ip3_num",0,[0,0,0,0,0,0],0,1)
    assert fTwo.insertElement("ip3_str",1,[2,3,4,5,6,7],"ip3",2)
    assert len(fTwo.elemData["Name"]) == 187
    assert len(fTwo.elemData["Type"]) == 187
    assert len(fTwo.elemData["Val1"]) == 187
    assert len(fTwo.elemData["Val2"]) == 187
    assert len(fTwo.elemData["Val3"]) == 187
    assert len(fTwo.elemData["Val4"]) == 187
    assert len(fTwo.elemData["Val5"]) == 187
    assert len(fTwo.elemData["Val6"]) == 187

def testInsertElementBreak():
    assert not fTwo.insertElement("idx-too-small",0,[0,0,0,0,0,0],-1,1)
    assert not fTwo.insertElement("idx-too-large",0,[0,0,0,0,0,0],187,1)
    assert not fTwo.insertElement("off-too-small",0,[0,0,0,0,0,0],0,-1)
    assert not fTwo.insertElement("off-too-large",0,[0,0,0,0,0,0],180,10)
    assert not fTwo.insertElement("values-wrong",0,[0,0,0,0,0],1,1)
    assert not fTwo.insertElement("duplicate",0,[0,0,0,0,0,0],"duplicate",1)
    assert not fTwo.insertElement("non-existent",0,[0,0,0,0,0,0],"what?",1)
    assert not fTwo.insertElement("silly-index",0,[0,0,0,0,0,0],None,1)
    assert not fTwo.insertElement("silly-index",0,[0,0,0,0,0,0],0.0,1)
    
def testInsertStructOK():
    assert fTwo.insertStruct("ip3_num",0,1)
    assert fTwo.insertStruct("ip3_str","ip3",2)
    assert len(fTwo.structData) == 3342

def testInsertStructBreak():
    assert not fTwo.insertStruct("idx-too-small",-1,1)
    assert not fTwo.insertStruct("idx-too-large",3342,1)
    assert not fTwo.insertStruct("off-too-small",0,-1)
    assert not fTwo.insertStruct("off-too-large",3335,10)
    assert not fTwo.insertStruct("duplicate","duplicate",1)
    assert not fTwo.insertStruct("non-existent","what?",1)
    assert not fTwo.insertStruct("silly-index",None,1)
    assert not fTwo.insertStruct("silly-index",0.0,1)

def testSaveFile():
    assert fTwo.saveFile()
    assert fcmp.cmp(
        path.join(currPath,"fort.2.ref"),
        path.join(currPath,"fort.2"),
        shallow=False
    )
    unlink(path.join(currPath,"fort.2"))
