#!/usr/bin/env python3

from os import getcwd
from sttools.simtools import PartDist

distParam = {
  "sigmaxxp" : [1.0, 1.0],
  "sigmayyp" : [1.0, 1.0],
  "sigmaz"   : 1.0,
  "spreadp"  : 1.0,
}
pDist = PartDist(distParam)
pDist.setSeed(42,"seeds.dat")
pDist.genNormDist(5000)
pDist.writeCollDist(getcwd(),5000)
