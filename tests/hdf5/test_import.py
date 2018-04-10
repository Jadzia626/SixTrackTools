# -*- coding: utf-8 -*
"""Test Script for HDF5 Import Class
  
  SixTrack Tools - Test Script for HDF5 Import Class
 ====================================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import filecmp as fcmp

from os      import path, unlink
from hashlib import md5

from sttools import HDF5Import

currPath = path.dirname(path.realpath(__file__))
hdf5File = path.join(currPath,"test.hdf5")
dump1File = path.join(currPath,"dump_ip1.dat")
dump5File = path.join(currPath,"dump_ip5.dat")

if path.isfile(hdf5File):
    unlink(hdf5File)

h5Imp = HDF5Import(currPath,path.join(currPath,"test.hdf5"),True)

def testOpenFile():
    assert h5Imp.openFile()

def testLoadDumpFile():
    assert h5Imp.importDump(dump1File)
    assert h5Imp.importDump(dump5File)

def testCloseFile():
    assert h5Imp.closeFile()

# Checksum does not work for comparing HDF5 files.
# def testFileChecksum():
#     md5Sum = "2cb5b90811acc27dcfa3de80c3e3800c"
#     assert md5(open(path.join(currPath,"test.hdf5"),mode="rb").read()).hexdigest() == md5Sum

#unlink(path.join(currPath,"test.hdf5"))
