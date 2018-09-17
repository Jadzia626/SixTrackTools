# -*- coding: utf-8 -*
"""PyTest Init Script
  
  SixTrack Tools - PyTest Init Script
 =====================================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland
"""

import pytest
import tarfile

from os import path, mkdir, unlink, listdir, rmdir

currPath = path.dirname(path.realpath(__file__))

@pytest.fixture(scope="session")
def fileTestData(request):
    print("Extracting test files ...")
    dataPath = path.join(currPath,"simdata","tmpfiles")
    archPath = path.join(currPath,"simdata","files")
    tarFiles = ["Run.000001","Run.000002","Run.000003"]
    if not path.isdir(dataPath):
        mkdir(dataPath)
    for fName in tarFiles:
        print(" * %s" % (fName+".tar.gz"))
        fPath = path.join(archPath,fName+".tar.gz")
        tFile = tarfile.open(fPath,"r:gz")
        tFile.extractall(path=dataPath)
        tFile.close()
    print("Done!")
    yield dataPath
    print("Deleting test files ...")
    for fName in tarFiles:
        fPath = path.join(dataPath,fName)
        for fFile in listdir(fPath):
            fDelete = path.join(fPath,fFile)
            if path.isfile(fDelete):
                unlink(fDelete)
        rmdir(fPath)
    print("Done!")
