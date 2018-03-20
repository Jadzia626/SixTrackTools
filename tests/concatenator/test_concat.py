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
from hashlib import md5

from sttools import Concatenator

currPath = path.dirname(path.realpath(__file__))

unlink(path.join(currPath,"test.hdf5"))
fCC = Concatenator(path.join(currPath,"test.hdf5"),True)

def testOpenFile():
    assert fCC.openFile()

def testLoadDumpFile():
    assert fCC.appendParticles(path.join(currPath,"dump_ip5.txt"),Concatenator.FTYPE_PART_DUMP)
    assert fCC.appendParticles(path.join(currPath,"dump_ip5.txt"),Concatenator.FTYPE_PART_DUMP)

def testCloseFile():
    assert fCC.closeFile()

def testFileChecksum():
    md5Sum = "2cb5b90811acc27dcfa3de80c3e3800c"
    assert md5(open(path.join(currPath,"test.hdf5"),mode="rb").read()).hexdigest() == md5Sum

#unlink(path.join(currPath,"test.hdf5"))
