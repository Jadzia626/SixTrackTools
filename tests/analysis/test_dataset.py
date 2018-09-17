# -*- coding: utf-8 -*
"""Test Script for Aperture Class
  
  SixTrack Tools - Test Script for Aperture Class
 =================================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import filecmp as fcmp

from os               import path, unlink, listdir
from sttools          import setLoggingLevel
from sttools.h5tools  import H5Wrapper
from sttools.analysis import DataSet

currPath = path.dirname(path.realpath(__file__))
h5Path   = path.join(currPath,"..","simdata","hdf5")

setLoggingLevel("DEBUG")

def testHDF5Single():
    h5W  = H5Wrapper(h5Path,loadOnly=["data.000001.hdf5"])
    dSet = DataSet("collimation/dist0",fileType="hdf5",h5Set=h5W)
    assert dSet.initOK
    assert dSet.getNumSets() == 1
    dist0 = dSet.loadData()
    assert dist0 is not None
    assert len(dist0["X"]) == 64
    assert round(sum(dist0["X"]),8) == round(-0.0015416089348123877,8)
    # assert False

def testFileSingle(fileTestData):
    dSet = DataSet("dist0.dat",fileType="text",dataFolder=fileTestData,loadOnly=["Run.000001"])
    assert dSet.initOK
    assert dSet.getNumSets() == 1
    dist0 = dSet.loadData()
    assert dist0 is not None
    assert len(dist0["X"]) == 64
    assert round(sum(dist0["X"]),8) == round(0.004054001460961671,8)
    # assert False

def testHDF5Multiple():
    h5W  = H5Wrapper(h5Path)
    dSet = DataSet("collimation/dist0",fileType="hdf5",h5Set=h5W)
    assert dSet.initOK
    assert dSet.getNumSets() == 3
    retVal = [
       -0.0015416089348123877,
        0.0034743258913091444,
        0.0014059369106693034
    ]
    setNum = 0
    for dist0 in dSet.iterateData():
        assert dist0 is not None
        assert len(dist0["X"]) == 64
        assert round(sum(dist0["X"]),8) == round(retVal[setNum],8)
        setNum += 1
    assert setNum == 3
    # assert False

def testFileMultiple(fileTestData):
    dSet = DataSet("dist0.dat",fileType="text",dataFolder=fileTestData)
    assert dSet.initOK
    assert dSet.getNumSets() == 3
    retVal = [
        0.0040540014609616710,
       -0.0007982082980987052,
        0.0002978634826388683
    ]
    setNum = 0
    for dist0 in dSet.iterateData():
        assert dist0 is not None
        assert len(dist0["X"]) == 64
        assert round(sum(dist0["X"]),8) == round(retVal[setNum],8)
        setNum += 1
    assert setNum == 3
    # assert False
