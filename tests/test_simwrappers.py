# -*- coding: utf-8 -*
"""Test Script for Simulation and DataSet Wrappers
  
  SixTrack Tools - Test Script for Simulation and DataSet Wrappers
 ==================================================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

from os                import path, unlink, listdir
from sttools           import loggingConfig, SixTrackSim, DataSet
from sttools.h5tools   import H5Wrapper
from sttools.filetools import FileWrapper

currPath = path.dirname(path.realpath(__file__))
h5Path   = path.join(currPath,"simdata","hdf5")

loggingConfig("DEBUG")

def testHDF5Single():
    stSim = SixTrackSim(h5Path,loadOnly=["data.000001.hdf5"])
    dSet  = DataSet("dist0",stSim)
    assert len(dSet) == 1
    dist0 = dSet[0]
    assert dist0 is not None
    assert len(dist0["X"]) == 64
    assert round(sum(dist0["X"]),8) == round(-0.0015416089348123877,8)

def testFileSingle(fileTestData):
    stSim = SixTrackSim(fileTestData,loadOnly=["Run.000001"])
    dSet  = DataSet("dist0",stSim)
    assert len(dSet) == 1
    dist0 = dSet[0]
    assert dist0 is not None
    assert len(dist0["X"]) == 64
    assert round(sum(dist0["X"]),8) == round(0.004054001460961671,8)

def testHDF5Multiple():
    stSim = SixTrackSim(h5Path)
    with DataSet("dist0",stSim) as dSet:
        assert len(dSet) == 3
        retVal = [
           -0.0015416089348123877,
            0.0034743258913091444,
            0.0014059369106693034
        ]
        setNum = 0
        for dist0 in dSet:
            assert dist0 is not None
            assert len(dist0["X"]) == 64
            assert round(sum(dist0["X"]),8) == round(retVal[setNum],8)
            setNum += 1
        assert setNum == 3

def testFileMultiple(fileTestData):
    stSim = SixTrackSim(fileTestData)
    with DataSet("dist0",stSim) as dSet:
        assert len(dSet) == 3
        retVal = [
            0.0040540014609616710,
           -0.0007982082980987052,
            0.0002978634826388683
        ]
        setNum = 0
        for dist0 in dSet:
            assert dist0 is not None
            assert len(dist0["X"]) == 64
            assert round(sum(dist0["X"]),8) == round(retVal[setNum],8)
            setNum += 1
        assert setNum == 3

def testH5WrapperIter():
    with H5Wrapper(h5Path) as stSim:
        assert "data.000001" in stSim
        assert "data.000002" in stSim
        assert "data.000003" in stSim
        simNum = 0
        for aSim in stSim:
            assert aSim.attrs["CreatedBy"][0] == b"SixTrack 5.0.2"
            simNum += 1
        assert simNum == 3

def testFileWrapperIter(fileTestData):
    with FileWrapper(fileTestData) as stSim:
        assert "Run.000001" in stSim
        assert "Run.000002" in stSim
        assert "Run.000003" in stSim
        simNum = 0
        for aSim in stSim:
            assert aSim.simName is not None
            simNum += 1
        assert simNum == 3

def testSimWrapperIter():
    with H5Wrapper(h5Path) as stSim:
        assert "data.000001" in stSim
        assert "data.000002" in stSim
        assert "data.000003" in stSim
        simNum = 0
        for aSim in stSim:
            assert aSim.attrs["CreatedBy"][0] == b"SixTrack 5.0.2"
            simNum += 1
        assert simNum == 3
