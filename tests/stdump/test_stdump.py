# -*- coding: utf-8 -*
"""Test Script for STDump Class
  
  SixTrack Tools - Test Script for STDump Class
 ===============================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

from os      import path, unlink
from sttools import STDump

currPath        = path.dirname(path.realpath(__file__))
dumpFile        = path.join(currPath,"dump_ip1.dat")
scatterLogFile  = path.join(currPath,"scatter_log.dat")
collSummaryFile = path.join(currPath,"coll_summary.dat")

def testDumpFile():
    stData = STDump(dumpFile)
    stData.readAll()
    assert stData.nLines == 192
    assert bool(set(stData.colNames).intersection(
        ["ID","TURN","S","X","XP","Y","YP","Z","DEE","KTRACK"]
    ))
    stData.filterPart("TURN",2)
    assert len(stData.filData["TURN"]) == 64
    stData.filterPart("ID",11)
    assert len(stData.filData["TURN"]) == 3

def testScatterLog():
    stData = STDump(scatterLogFile)
    stData.readAll()
    assert stData.nLines == 128
    assert bool(set(stData.colNames).intersection(
        ["ID","TURN","BEZ","SCATTER_GENERATOR","T","XI","THETA","PHI","PROB"]
    ))
    stData.filterPart("TURN",11)
    assert len(stData.filData["TURN"]) == 128
    stData.filterPart("ID",11)
    assert len(stData.filData["TURN"]) == 1

def testCollSummary():
    stData = STDump(collSummaryFile)
    stData.readAll()
    assert stData.nLines == 54
    assert bool(set(stData.colNames).intersection(
        ["ICOLL","COLLNAME","NIMP","NABS","IMP_AV","IMP_SIG","LENGTH"]
    ))
