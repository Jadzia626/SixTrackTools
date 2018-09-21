# -*- coding: utf-8 -*
"""Test Script for Fort3 Class
  
  SixTrack Tools - Test Script for Fort3 Class
 ==============================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import filecmp as fcmp

from os               import path, unlink
from sttools.simtools import Fort3

currPath = path.dirname(path.realpath(__file__))

fThree = Fort3(currPath,"fort.3.input")

def testFileLoad():
    assert fThree.loadFile()

def testAddBlockOk():
    assert fThree.addBlockFromFile("LIMI",currPath,"fc.3.aper")
    assert fThree.addBlockLineFromString("LIMI","Something AA 0 0 0 0 0 0 0")
    assert fThree.addBlockLineFromList("LIMI",["Something","AA",0,0,0,0,0,0,0])
    assert fThree.addBlockLineFromString("DUMP","ip8  1 650 2 dump.txt 1 -1")
    assert fThree.addBlockLineFromString("DUMP","ip8  1 650 2 \"with space.txt\" 1 -1")

def testAddBlockBreak():
    assert not fThree.addBlockFromFile("LIMI",currPath,"fc.2.aper")
    assert not fThree.addBlockLineFromString("LIMI","Something AA 0 0 0 0")
    assert not fThree.addBlockLineFromString("NOEXIST","")
    assert not fThree.addBlockLineFromList("LIMI",["Something","AA",0,0,0,0,0])
    assert not fThree.addBlockLineFromList("NOEXIST",[])

def testFileSave():
    assert fThree.saveFile()
    assert fcmp.cmp(
        path.join(currPath,"fort.3.ref"),
        path.join(currPath,"fort.3"),
        shallow=False
    )
    unlink(path.join(currPath,"fort.3"))
