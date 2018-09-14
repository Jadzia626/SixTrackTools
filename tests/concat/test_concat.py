# -*- coding: utf-8 -*
"""Test Script for Concatenator Class
  
  SixTrack Tools - Test Script for Concatenator Class
 =====================================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import filecmp as fcmp

from os      import path, unlink
from shutil  import copyfile

from sttools.h5tools import Concatenator

currPath = path.dirname(path.realpath(__file__))

copyfile(path.join(currPath,"data.hdf5"),path.join(currPath,"test.001.hdf5"))
copyfile(path.join(currPath,"data.hdf5"),path.join(currPath,"test.002.hdf5"))
copyfile(path.join(currPath,"data.hdf5"),path.join(currPath,"test.003.hdf5"))

fCC = Concatenator(currPath)

def testLoadFiles():
    assert fCC.loadAll()
    assert len(set(fCC.fileList).intersection(
        ["data.hdf5","test.001.hdf5","test.002.hdf5","test.003.hdf5"]
    )) == 4
    # assert False

# def testLoadDumpFile():
#     assert fCC.appendParticles(path.join(currPath,"dump_ip5.dat"),Concatenator.FTYPE_PART_DUMP)
#     assert fCC.appendParticles(path.join(currPath,"dump_ip5.dat"),Concatenator.FTYPE_PART_DUMP)

# def testCloseFile():
#     assert fCC.closeFile()

# Checksum does not work for comparing HDF5 files.
# def testFileChecksum():
#     md5Sum = "2cb5b90811acc27dcfa3de80c3e3800c"
#     assert md5(open(path.join(currPath,"test.hdf5"),mode="rb").read()).hexdigest() == md5Sum

# unlink(path.join(currPath,"test.001.hdf5"))
# unlink(path.join(currPath,"test.002.hdf5"))
# unlink(path.join(currPath,"test.003.hdf5"))
