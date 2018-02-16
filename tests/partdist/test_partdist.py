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

distParam = {
    "energy"  : 7e12,
    "mass"    : Const.ProtonMass,
    "nemit"   : [2.5e-6, 2.5e-6],
    "twbeta"  : [150e-3, 150e-3],
    "twalpha" : [0.0, 0.0],
    "sigmaz"  : 0.0,
    "spreade" : 0.0e-4,
}

pDist = PartDist(distParam)

def testParam():
    assert not pDist.hasError

def testSeed():
    assert pDist.setSeed(42)
    assert pDist.setSeed(45,path.join(currPath,"seed.dat"))
    assert pDist.setSeed(44,path.join(currPath,"seed.dat"))
    assert pDist.setSeed(43,path.join(currPath,"seed.dat"))
    assert pDist.setSeed(42,path.join(currPath,"seed.dat"))
    assert fcmp.cmp(
        path.join(currPath,"seed.dat.ref"),
        path.join(currPath,"seed.dat"),
        shallow=False
    )
    unlink(path.join(currPath,"seed.dat"))

def testGenDist():
    pDist.genDist(64)
    assert len(pDist.genXXP) == 128
    assert len(pDist.genYYP) == 128
    assert len(pDist.genZ)   == 128
    assert len(pDist.genP)   == 128
    assert len(pDist.genDDP) == 128
    assert len(pDist.genE)   == 128

def testWriteFort13():
    assert pDist.writeFort13(currPath,64)
    assert fcmp.cmp(
        path.join(currPath,"fort.13.ref"),
        path.join(currPath,"fort.13"),
        shallow=False
    )
    unlink(path.join(currPath,"fort.13"))

def testWriteCollDist():
    assert pDist.writeCollDist(currPath,64)
    assert fcmp.cmp(
        path.join(currPath,"partDist.dat.ref"),
        path.join(currPath,"partDist.dat"),
        shallow=False
    )
    unlink(path.join(currPath,"partDist.dat"))
