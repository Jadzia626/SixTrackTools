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
from sttools import STDump

currPath        = path.dirname(path.realpath(__file__))
dumpFile        = path.join(currPath,"dump_ip1.dat")
scatterLogFile  = path.join(currPath,"scatter_log.dat")
collSummaryFile = path.join(currPath,"coll_summary.dat")

def testDumpFile():
    stData = STDump(dumpFile)
    stData.readAll()
    assert stData.nLines == 192
    assert stData.colNames[0] == "ID"
    assert stData.colNames[1] == "TURN"
    assert stData.colNames[2] == "S"
    assert stData.colNames[3] == "X"
    assert stData.colNames[4] == "XP"
    assert stData.colNames[5] == "Y"
    assert stData.colNames[6] == "YP"
    assert stData.colNames[7] == "Z"
    assert stData.colNames[8] == "DEE"
    assert stData.colNames[9] == "KTRACK"
    stData.filterPart("TURN",2)
    assert len(stData.filData["TURN"]) == 64
    stData.filterPart("ID",11)
    assert len(stData.filData["TURN"]) == 3

def testScatterLog():
    stData = STDump(scatterLogFile)
    stData.readAll()
    assert stData.nLines == 128
    assert stData.colNames[0] == "ID"
    assert stData.colNames[1] == "TURN"
    assert stData.colNames[2] == "BEZ"
    assert stData.colNames[3] == "SCATTER_GENERATOR"
    assert stData.colNames[4] == "T"
    assert stData.colNames[5] == "XI"
    assert stData.colNames[6] == "THETA"
    assert stData.colNames[7] == "PHI"
    assert stData.colNames[8] == "PROB"
    stData.filterPart("TURN",11)
    assert len(stData.filData["TURN"]) == 128
    stData.filterPart("ID",11)
    assert len(stData.filData["TURN"]) == 1

def testCollSummary():
    stData = STDump(collSummaryFile)
    stData.readAll()
    assert stData.nLines == 54
    assert stData.colNames[0] == "ICOLL"
    assert stData.colNames[1] == "COLLNAME"
    assert stData.colNames[2] == "NIMP"
    assert stData.colNames[3] == "NABS"
    assert stData.colNames[4] == "IMP_AV"
    assert stData.colNames[5] == "IMP_SIG"
    assert stData.colNames[6] == "LENGTH"
