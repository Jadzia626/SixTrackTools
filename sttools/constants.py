# -*- coding: utf-8 -*
"""SixTrack Tools - Constants 

  SixTrack Tools - Constants
 ============================
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

  A set of physical constants
  
"""

import logging

from numpy import pi

logger = logging.getLogger(__name__)

class Const():
    
    # Atomic Units
    ElectronMass       = 510.9989461e3      # eV
    ProtonMass         = 938.2720813e6      # eV
    BohrRadius         =   5.2917721067e-11 # m
    ElectronRadius     =   2.8179403227e-15 # m
    FineStructure      =   7.2973525664e-3  #
    
    # Constants of Nature
    SpeedOfLight       =   2.99792458e8     # m/s
    ElementaryCharge   =   1.6021766208e-19 # C
    Gravity            =   6.67408e-11      # m³/kg·s²
    Planck             =   6.626070040e-34  # J·s
    Boltzmann          =   1.38064852e-23   # J/K
    
    # Calculated Values
    VacuumPermeability =   4.0e-7*pi                              # N/A²
    VacuumPermittivity =   1.0/VacuumPermeability/SpeedOfLight**2 # F/m
    ReducedPlanck      =   Planck/2.0/pi                          # J·s
    
# End Class Const
