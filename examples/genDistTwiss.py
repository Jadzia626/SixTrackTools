#!/usr/bin/env python3

from os import getcwd

from sttools.constants import Const
from sttools.simtools  import PartDist

nPair = 5

distParam = {
  "energy"   : 7e12,
  "mass"     : Const.ProtonMass,
  "nemit"    : [2.5e-6, 2.5e-6],
  "twbeta"   : [0.15,   0.15],
  "twalpha"  : [0.5,    0.5],
  "sigmaz"   : 7.55e-2,
  "spreadp"  : 1.13e-4,
  "format"   : ["X","Y","XP","YP","PX","PY","PXP0","PYP0"],
}
pDist = PartDist(distParam)
pDist.setSeed(42,"seeds.dat")
pDist.genTransverseDist(nPair)
pDist.genLongitudinalDist(nPair)
pDist.writeDistBlockFile(getcwd(),nPair,"13.6e")
