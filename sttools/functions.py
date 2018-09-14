# -*- coding: utf-8 -*
"""SixTrack Tools - Functions

  SixTrack Tools - Functions
 ============================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

  A set of useful functions
"""

import logging
import sttools
import pprint

logger = logging.getLogger(__name__)

def formatNumberExp(floatVal, formatString="%7.2f", expSize=2, nullLimit=1e-18):

    expVal = 0
    if abs(floatVal) > nullLimit:
        while abs(floatVal) > 1.0e3:
            floatVal /= 1.0e3
            expVal += 3

        while abs(floatVal) < 1.0:
            floatVal *= 1.0e3
            expVal -= 3
    else:
        floatVal = 0.0

    if expVal >= 0:
        expSign = "+"
    else:
        expSign = "-"

    formatString += "e%s%%0%dd" % (expSign,expSize)

    return formatString % (floatVal,abs(expVal))

def pPrintDict(theDict):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(theDict)
