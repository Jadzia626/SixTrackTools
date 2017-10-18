# -*- coding: utf-8 -*
"""SixTrack Tools - Physics Functions

  SixTrack Tools - Physics Functions
 ====================================
  A set of basic calculation functions
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

from math import sqrt, pi

def calcLuminosity(bunchParticles, nBunches, revFrequency, beamGamma, normTEmittance, betaStar,
                   crossingAngle, sigmaZ, sigmaStar):
    """Luminosity Calculation
    bunchParticles : Number of particles per bunch
    nBunches       : Number of bunches in the beam
    revFrequency   : Revolution frequency
    beamGamma      : The beam relativistic gamma
    normTEmittance : Normalised transverse emittance
    betaStar       : Beta value at the interaction point
    crossingAngle  : Crossing angle in the interaction point
    sigmaZ         : Bunch longitudinal size
    sigmaStar      : Bunch transverse size in the interaction point
    """
    reductionFactor = 1 / sqrt(1 + ((crossingAngle*sigmaZ) / (2*sigmaStar)))
    machineLuminosity = (bunchParticles**2 * nBunches * revFrequency * beamGamma)
                      / (4*pi * normTEmittance * betaStar)
    
    return machineLuminosity * reductionFactor
