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

currPath         = path.dirname(path.realpath(__file__))
dumpFile         = path.join(currPath,"dump_ip1.dat")
scatterLogFile   = path.join(currPath,"scatter_log.dat")
collSummaryFile  = path.join(currPath,"coll_summary.dat")
collFirstImpFile = path.join(currPath,"first_impacts.dat")
collScatterFile  = path.join(currPath,"coll_scatter.dat")

def testDumpFile():
    stData = STDump(dumpFile)
    stData.readAll()
    assert stData.nLines == 192
    assert len(set(stData.colNames).intersection(
        ["ID","TURN","S","X","XP","Y","YP","Z","DEE","KTRACK"]
    )) == 10
    stData.filterPart("TURN",2)
    assert len(stData.filData["TURN"]) == 64
    stData.filterPart("ID",11)
    assert len(stData.filData["TURN"]) == 3

def testScatterLog():
    stData = STDump(scatterLogFile)
    stData.readAll()
    assert stData.nLines == 128
    assert len(set(stData.colNames).intersection(
        ["ID","TURN","BEZ","SCATTER_GENERATOR","T","XI","THETA","PHI","PROB"]
    )) == 9
    stData.filterPart("TURN",11)
    assert len(stData.filData["TURN"]) == 128
    stData.filterPart("ID",11)
    assert len(stData.filData["TURN"]) == 1

def testCollSummary():
    stData = STDump(collSummaryFile)
    stData.readAll()
    assert stData.nLines == 54
    assert len(set(stData.colNames).intersection(
        ["ICOLL","COLLNAME","NIMP","NABS","IMP_AV","IMP_SIG","LENGTH"]
    )) == 7

def testCollFirstImpacts():
    stData = STDump(collFirstImpFile)
    stData.readAll()
    assert stData.nLines == 15
    assert len(set(stData.colNames).intersection([
        "NAME", "ITURN",  "ICOLL","NABS","S_IMP","S_OUT",
        "X_IN", "XP_IN", "Y_IN", "YP_IN",
        "X_OUT","XP_OUT","Y_OUT","YP_OUT"
    ])) == 14

def testCollScatter():
    stData = STDump(collScatterFile)
    stData.readAll()
    assert stData.nLines == 15
    assert len(set(stData.colNames).intersection(
        ["ICOLL","ITURN","NP","NABS","DP","DX","DY"]
    )) == 7
