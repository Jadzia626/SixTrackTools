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
import datetime

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
    """Pretty print a dictionary.
    """
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(theDict)

def parseKeyWordArgs(refDict, checkDict):
    """This function takes a dictionary and checks that the keys correspond to the list in
    refDict. The check is case insensitive, and the return is a copy of the refDict dictionary
    where the values found in checkDict has been set. Otherwise the default values from refDict
    remain.
    """
    valMap  = {}             # Map of lower case valid keys to actual key name
    retDict = refDict.copy() # Make a copy of the original dictionary for return
    for validKey in refDict.keys():
        valMap[validKey.lower()] = validKey
    for keyWord in checkDict.keys():
        if keyWord.lower() in valMap.keys():
            # Copy the value from checkDict to the correct corresponding key
            retDict[valMap[keyWord.lower()]] = checkDict[keyWord]
        else:
            # Invalid key. Return an empty result
            logger.error("Invalid key '%s' in keyword argument list." % keyWord)
            return None
    return retDict

def checkValue(theValue, theList, caseSensitive=True):
    """Checks a value against a list of values. Returns True if the value is in the list, False if
    it was not found. The comparison can be case insensitve.
    """
    if not caseSensitive and isinstance(theValue, str):
        theValue = theValue.lower()
    for theCheck in theList:
        if not caseSensitive and isinstance(theCheck, str):
            theCheck = theCheck.lower()
        if theCheck == theValue:
            return True
    return False

def symmetricRange(minVal, maxVal, meanVal):
    """Returns a tuple of a range symmetric around mean with the same extent.
    """
    maxVal -= meanVal
    minVal -= meanVal
    extVal  = max(abs(minVal),abs(maxVal))
    return meanVal-extVal, meanVal+extVal

def getTimeStamp(dateSep=" "):
    timeValue  = datetime.datetime.now()
    returnDate = "{:%Y-%m-%d}".format(timeValue)
    returnTime = "{:%H:%M:%S}".format(timeValue)
    return "%s%s%s" % (returnDate,dateSep,returnTime)
