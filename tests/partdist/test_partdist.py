# -*- coding: utf-8 -*
"""Test Script for PartDist Class
  
  SixTrack Tools - Test Script for PartDist Class
 =================================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import filecmp as fcmp

from os      import path, unlink
from sttools import Const, PartDist

currPath = path.dirname(path.realpath(__file__))

distParamF13 = {
    "energy"   : 7e12,
    "mass"     : Const.ProtonMass,
    "nemit"    : [2.5e-6, 2.5e-6],
    "twbeta"   : [150e-3, 150e-3],
    "twalpha"  : [0.0, 0.0],
    "sigmaz"   : 0.0,
    "spreade"  : 0.0e-4,
}

distParamCol = {
    "sigmaxxp" : [1.0, 2.0],
    "sigmayyp" : [3.0, 4.0],
    "sigmaz"   : 5.0,
    "spreadp"  : 6.0,
}

pDistF13 = PartDist(distParamF13)
pDistCol = PartDist(distParamCol)

def testParam():
    assert not pDistF13.hasError
    assert not pDistCol.hasError

def testSeed():
    assert pDistF13.setSeed(42)
    assert pDistCol.setSeed(42)
    assert pDistF13.setSeed(45,path.join(currPath,"seed.dat"))
    assert pDistF13.setSeed(44,path.join(currPath,"seed.dat"))
    assert pDistF13.setSeed(43,path.join(currPath,"seed.dat"))
    assert pDistF13.setSeed(42,path.join(currPath,"seed.dat"))
    assert pDistCol.setSeed(45,path.join(currPath,"seed.dat"))
    assert pDistCol.setSeed(44,path.join(currPath,"seed.dat"))
    assert pDistCol.setSeed(43,path.join(currPath,"seed.dat"))
    assert pDistCol.setSeed(42,path.join(currPath,"seed.dat"))
    assert fcmp.cmp(
        path.join(currPath,"seed.dat.ref"),
        path.join(currPath,"seed.dat"),
        shallow=False
    )
    unlink(path.join(currPath,"seed.dat"))

def testGenDist():
    pDistF13.genDist(64)
    assert len(pDistF13.genXXP) == 128
    assert len(pDistF13.genYYP) == 128
    assert len(pDistF13.genZ)   == 128
    assert len(pDistF13.genP)   == 128
    assert len(pDistF13.genDDP) == 128
    assert len(pDistF13.genE)   == 128

def testGenNormDist():
    pDistCol.genNormDist(64)
    assert len(pDistCol.genXXP) == 128
    assert len(pDistCol.genYYP) == 128
    assert len(pDistCol.genZ)   == 128
    assert len(pDistCol.genP)   == 128
    assert len(pDistCol.genDDP) == 128
    assert len(pDistCol.genE)   == 128

def testWriteFort13():
    assert pDistF13.writeFort13(currPath,64)
    assert fcmp.cmp(
        path.join(currPath,"fort.13.ref"),
        path.join(currPath,"fort.13"),
        shallow=False
    )
    unlink(path.join(currPath,"fort.13"))

def testWriteCollDist():
    assert pDistCol.writeCollDist(currPath,64)
    assert fcmp.cmp(
        path.join(currPath,"partDist.dat.ref"),
        path.join(currPath,"partDist.dat"),
        shallow=False
    )
    unlink(path.join(currPath,"partDist.dat"))
