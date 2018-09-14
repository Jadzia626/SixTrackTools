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

from sttools.h5tools import H5Import

currPath         = path.dirname(path.realpath(__file__))
hdf5File         = path.join(currPath,"test.hdf5")
dump1File        = path.join(currPath,"dump_ip1.dat")
dump5File        = path.join(currPath,"dump_ip5.dat")
scatterLogFile   = path.join(currPath,"scatter_log.dat")
collSummaryFile  = path.join(currPath,"coll_summary.dat")
collFirstImpFile = path.join(currPath,"first_impacts.dat")
collScatterFile  = path.join(currPath,"coll_scatter.dat")

if path.isfile(hdf5File):
    unlink(hdf5File)

h5Imp = H5Import(currPath,path.join(currPath,"test.hdf5"),True)

def testOpenFile():
    assert h5Imp.openFile()

def testLoadDumpFile():
    assert     h5Imp.importDump(dump1File)
    assert     h5Imp.importDump(dump5File)
    assert not h5Imp.importDump("non/existent/file")

def testLoadScatterLogFile():
    assert     h5Imp.importScatterLog(scatterLogFile)
    assert not h5Imp.importScatterLog(dump1File)
    assert not h5Imp.importScatterLog("non/existent/file")

def testLoadCollSummaryFile():
    assert     h5Imp.importCollSummary(collSummaryFile)
    assert not h5Imp.importCollSummary(dump1File)
    assert not h5Imp.importCollSummary("non/existent/file")

def testLoadCollFirstImpacts():
    assert     h5Imp.importCollFirstImpacts(collFirstImpFile)
    assert not h5Imp.importCollFirstImpacts(dump1File)
    assert not h5Imp.importCollFirstImpacts("non/existent/file")

def testLoadCollScatter():
    assert     h5Imp.importCollScatter(collScatterFile)
    assert not h5Imp.importCollScatter(dump1File)
    assert not h5Imp.importCollScatter("non/existent/file")

def testCloseFile():
    assert h5Imp.closeFile()

#unlink(path.join(currPath,"test.hdf5"))
