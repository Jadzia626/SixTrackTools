#!/usr/bin/env python
# ----------------------------------------------------------------------------------------------------------------------------
# Function to generate a particle distribution as input for the collimation routine in SixTrack (round beams at symmetry point)
# Example for SPS:
# generate_distribution.py 64 26e9 'SPS_inj' True 1 1 0.9e-6 3.0e-6 1.50895801 -1.392739114 51.8375213 46.54197726 0 0 0 0 0 0 0.3 10.7e-4
# Example for HL-LHC:
# generate_distribution.py 64 7e12 'HL_coll' True 1 1 2.5e-6 2.5e-6 0.003485 -0.000764 0.150739 0.150235 -7.5e-4 0 0 0.3e-3 0.003652 0.000517 0.0755 1.13e-4
# ----------------------------------------------------------------------------------------------------------------------------
import datetime
import sys
import random

import numpy as np

#from util import get_bucket
#from util import get_rel_params
#from util import get_sigmas

if __name__=="__main__":

    if len(sys.argv) != 24:
        print "Function to generate a particle distribution as input for the collimation routine in SixTrack (round beams at symmetry point)"
        print "Expected 21 arguments, got", len(sys.argv)-1
        print
        print "Example for SPS:"
        print " generate_distribution.py 64 26e9 'SPS_inj' True 1 1 0.9e-6 3.0e-6 1.50895801 -1.392739114 51.8375213 46.54197726 0 0 0 0 0 0 0.3 10.7e-4 42"
        print "Example for HL-LHC:"
        print " generate_distribution.py 64 7e12 'HL_coll' True 1 1 2.5e-6 2.5e-6 0.003485 -0.000764 0.150739 0.150235 -7.5e-4 0 0 0.3e-3 0.003652 0.000517 0.0755 1.13e-4 42"
        print "Arguments:"
        print " particles, energy, machine, fort13, jobs, factor, emittance_x, emittance_y, alpha_x, alpha_y, beta_x, beta_y, offset_x, offset_xp, offset_y, offset_yp, dispersion_x, dispersion_xp, dispersion_y, dispersion_yp, bunch, spread, seed"

        print
        print sys.argv
        exit(1)

    # Pass the Command Line Arguments
    # --------------------------------------------------------------------------------------------------------------
    particles    = int(sys.argv[1])
    energy       = float(sys.argv[2])
    machine      = str(sys.argv[3])
    fort13       = sys.argv[4]
    jobs         = int(sys.argv[5])
    factor       = float(sys.argv[6])
    emittance_x  = float(sys.argv[7])
    emittance_y  = float(sys.argv[8])
    alpha_x      = float(sys.argv[9])
    alpha_y      = float(sys.argv[10])
    beta_x       = float(sys.argv[11])
    beta_y       = float(sys.argv[12])
    offset_x     = float(sys.argv[13])
    offset_xp    = float(sys.argv[14])
    offset_y     = float(sys.argv[15])
    offset_yp    = float(sys.argv[16])
    dispersion_x = float(sys.argv[17])
    dispersion_xp= float(sys.argv[18])
    dispersion_y = float(sys.argv[19])
    dispersion_yp= float(sys.argv[20])
    bunch        = float(sys.argv[21])
    spread       = float(sys.argv[22])
    seed         = int(sys.argv[23])

    #print "offsets:", offset_x, offset_xp, offset_y, offset_yp

#Copy-pasted from util.py
def get_rel_params(energy, mass=0.938272046e9):
    """
    Returns the relativistic beta and gamma, the momenta and mass used.
    The energy has to be input in [eV] and the particle mass in [eV/c^2].
    If no mass is input, the proton mass will be taken by default.
    """
    c = 2.99792485e8  # m/s
    gamma_rel = energy / mass
    beta_rel = np.sqrt(gamma_rel**2 - 1) / gamma_rel
    p0 = np.sqrt((energy - mass) * (energy + mass))
    return gamma_rel, beta_rel, p0, mass

def get_bucket(machine, plot=True, z=0, DELTA=0):
    """ Returns the data needed to plot the RF bucket of LHC.
    Adapted from Kyrre Sjobak.
    Usage: plt.contour(PHIp * 0.1, DELTA_E, H, 40, linewidths=0.3, cmap='terrain_r')
    """
    mp = 0.938272046e9                     # proton mass, eV/c^2
    e  = 1.60217657e-19                    # C, electron charge
    c  = 2.99792485e8                      # m/s, speed of light

    if machine == 'HL_coll' or machine == 'HL_coll_tcp':
        h = 35640                          # RF harmonic number
        omegaRF = 400.8e6 * np.pi * 2      # Hz, omegaRF = h*omega0
        slip = 3.467e-4                    # Slip factor @ collission
        V = 16e6                           # V, RF voltage @ collissions
        phiS = 0.0                         # Radians, synchronous RF phase
        E0 = 7e12                          # Beam energy, eV
#        bunch = 0.0755
#        limit = 8e-4
    elif machine == 'HL_coll_200' or machine == 'HL_coll_tcp_200':
        h = 17820                          # RF harmonic number
        omegaRF = 200.8e6 * np.pi * 2      # Hz, omegaRF = h*omega0
        slip = 3.467e-4                    # Slip factor @ collission
        V = 16e6                           # V, RF voltage @ collissions
        phiS = 0.0                         # Radians, synchronous RF phase
        E0 = 7e12                          # Beam energy, eV
#        bunch = 2*0.0755
#        limit = 8e-4
    elif machine == 'SPS_inj':
        h = 4636                           # RF harmonic number
        omegaRF = 200.2644e6 * np.pi * 2   # Hz, omegaRF = h*omega0
        slip = 5.55e-4
        # slip =5.98e-4
        V = 2e6                            # V, RF voltage @ collissions
        phiS = 0.0                         # Radians, synchronous RF phase
        E0 = 26e9                          # Beam energy, eV
#        bunch = 0.3
#        limit = 6e-3
    elif machine == 'SPS_55':
        h = 4636                           # RF harmonic number
        omegaRF = 200.2644e6 * np.pi * 2   # Hz, omegaRF = h*omega0
        slip = 0.0016174303947121386       #slip=gammatr**-2-gamma**-2
        V = 3e6                            # V, RF voltage @ collissions
        phiS = 0.0                         # Radians, synchronous RF phase
        E0 = 55.00800264e9                 # Beam energy, eV
        bunch = 0.3                        # Bunch longitudinal spread [m]
        limit = 6e-3                       # Energy spread (fractional)
    elif machine == 'SPS_120':
        h = 4620                           # RF harmonic number
        omegaRF = 200.2644e6 * np.pi * 2   # Hz, omegaRF = h*omega0
        slip = 0.0016855233500965051       #slip=gammatr**-2-gamma**-2
        V = 3e6                            # V, RF voltage @ collissions
        phiS = 0.0                         # Radians, synchronous RF phase
        E0 = 120.0036681e9                 # Beam energy, eV
        bunch = 0.3                        # Bunch longitudinal spread [m]
        limit = 6e-3                       # Energy spread (fractional)

        
    else:
        print '>> Please input "HL_coll" or "SPS_inj" as first argument.'

    def get_hamiltonian(DELTA, PHI, omegaRF, E0, slip, p0, beta, h, V, phiS):
        p = p0 * (1.0 + DELTA)  # eV/c
        E = np.sqrt(p ** 2 + mp ** 2)
        DELTA_E = E / E0 - 1
        omega0 = omegaRF / h
        H1 = 0.5 * omegaRF * slip * DELTA ** 2
        H2 = omega0 * V / (2 * np.pi * beta ** 2 * E) * \
            (np.cos(PHI) - np.cos(phiS) + (PHI - phiS) * np.sin(phiS))
        H = H1 + H2  # Given in action-angle variables

        PHIp = np.pi - PHI  # Unstable fixed point (end of bucket)

        return H, PHIp, DELTA_E

    gamma_rel, beta, p0, mass = get_rel_params(E0)

    if plot == True:
        conversion = c / (omegaRF / (np.pi * 2))
        bucket = (np.pi * beta * c) / omegaRF
        print '>> Half bucket length = ', bucket
        print beta
        delta = np.linspace(-limit * conversion, limit * conversion, 300)  # delta p / p
        phi = np.linspace(-3 * np.pi, 3 *np.pi, 300)
        DELTA, PHI   = np.meshgrid(delta, phi)
        H, PHIp, DELTA_E = get_hamiltonian(DELTA, PHI, omegaRF, E0, slip, p0, beta, h, V, phiS)

        return PHIp * ((beta * c) / omegaRF), DELTA_E, H

    elif plot == False:
        PHI = omegaRF * z / (c * beta) - np.pi
        H, PHIp, DELTA_E = get_hamiltonian(DELTA, PHI, omegaRF, E0, slip, p0, beta, h, V, phiS)

        return H


def dist_generator(particles, energy, machine, fort13, jobs, factor, emittance_x, emittance_y, alpha_x, alpha_y, beta_x, beta_y, offset_x, offset_xp, offset_y, offset_yp, dispersion_x, dispersion_xp, dispersion_y, dispersion_yp, bunch, spread, seed):

    job_str = '%s'%jobs
    # Getting the Transverse sigmas (amplitudes of phase space ellipse)
    # --------------------------------------------------------------------------------------------------------------
    gamma_rel, beta_rel, p0, mass = get_rel_params(energy)
    emittance_x_geom = emittance_x/(beta_rel*gamma_rel)
    emittance_y_geom = emittance_x/(beta_rel*gamma_rel)
    
    # Seeding
    # --------------------------------------------------------------------------------------------------------------
    if seed == 0:
        myseed = random.randint(0, 429496729)
    else:
        myseed = seed
    with open('seed.txt', 'a') as g:
        print >> g,  'job ', job_str ,'seed ', myseed
    np.random.seed(myseed)
    random.seed(myseed)
    
    # Generating the Transverse Distribution
    # --------------------------------------------------------------------------------------------------------------
    x_t  = np.asarray(np.random.normal(0, 1, particles))*factor
    xp_t = np.asarray(np.random.normal(0, 1, particles))*factor
    y_t  = np.asarray(np.random.normal(0, 1, particles))*factor
    yp_t = np.asarray(np.random.normal(0, 1, particles))*factor

    sigma_x = np.array([[beta_x,alpha_x],[-alpha_x,(1+alpha_x**2)/beta_x]])*emittance_x_geom
    sigma_y = np.array([[beta_y,alpha_y],[-alpha_y,(1+alpha_y**2)/beta_y]])*emittance_y_geom
    C_x = np.linalg.cholesky(sigma_x)
    C_y = np.linalg.cholesky(sigma_y)
    
    x  = C_x[0,0]*x_t + C_x[0,1]*xp_t
    xp = C_x[1,0]*x_t + C_x[1,1]*xp_t
    y  = C_y[0,0]*y_t + C_y[0,1]*yp_t
    yp = C_y[1,0]*y_t + C_y[1,1]*yp_t
    
    
    # # Rotating the Transverse Distribution
    # # --------------------------------------------------------------------------------------------------------------
    # angle_x = np.arctan(-alpha_x/beta_x)
    # x       = x_t*np.cos(angle_x) - xp_t*np.sin(angle_x)
    # xp      = x_t*np.sin(angle_x) + xp_t*np.cos(angle_x)

    # angle_y = np.arctan(-alpha_y/beta_y)
    # y       = y_t*np.cos(angle_y) - yp_t*np.sin(angle_y)
    # yp      = y_t*np.sin(angle_y) + yp_t*np.cos(angle_y)
    
    # Generating the Longitudinal Distribution
    # --------------------------------------------------------------------------------------------------------------
    z  = []
    E  = []
    dp = []
    
    while len(z) < particles:
        # Generate for as long time as is needed
        particle_z = random.gauss(0,1)
        particle_e = random.gauss(0,1)
        trial_z    = particle_z * bunch
        trial_e    = energy * (1 + particle_e*spread) #eV

        trial_p = np.sqrt((trial_e - mass) * (trial_e + mass))
        dPP     = (trial_p - p0) / p0
        h       = get_bucket(machine, plot=False, z=trial_z, DELTA=dPP)  # Longitudinal contour

        if machine=='HL_coll' or  machine=='HL_coll_200' or machine=='HL_coll_tcp'  or machine=='HL_coll_tcp_200':
            Hmargin = -0.01
        elif machine=='SPS_inj':
            Hmargin = -1
        else:
            Hmargin = -1

        if h <= Hmargin:
            z.append(float(trial_z))
            E.append(float(trial_e))
            dp.append(dPP)
        else:
            #print 'Outside margin, trying again,', h
            pass
  
    zz  = np.asarray(z)
    EE  = np.asarray(E)
    ddp = np.asarray(dp)

    #Adding the dispersion
    x += dispersion_x*ddp
    xp += dispersion_xp*ddp
    y += dispersion_y*ddp
    yp += dispersion_yp*ddp
    
    
    if fort13=='False':
        outfile = 'init_dist_' + job_str + '.txt'
        with open(outfile, 'w') as f:
            for e1, e2, e3, e4, e5, e6 in zip(x, xp, y, yp, zz*1e3, EE*1e-6):
                f.write('%8.6e %8.6e %8.6e %8.6e %8.6e %8.6e\n' % (e1, e2, e3, e4, e5, e6))
    elif fort13=='True':
        outfile = 'fort.13'
        with open(outfile, 'w') as f:
            for i in xrange(0, particles, 2):
                f.write(str((x[i] + offset_x)*1e3) + "\n") #mm
                f.write(str((xp[i] + offset_xp)*1e3) + "\n") #mrad
                f.write(str((y[i] + offset_y)*1e3) + "\n") #mm
                f.write(str((yp[i] + offset_yp)*1e3) + "\n") #mrad
                f.write(str(zz[i]*1e3) + "\n") #mm
                f.write(str(ddp[i]) + "\n") #-

                f.write(str((x[i+1] + offset_x)*1e3) + "\n") #mm
                f.write(str((xp[i+1] + offset_xp)*1e3) + "\n") #mrad
                f.write(str((y[i+1] + offset_y)*1e3) + "\n") #mm
                f.write(str((yp[i+1] + offset_yp)*1e3) + "\n") #mrad
                f.write(str(zz[i+1]*1e3) + "\n") #mm
                f.write(str(ddp[i+1]) + "\n") #-

                f.write(str(energy*1e-6) + "\n") #MeV
                f.write(str(EE[i]*1e-6) + "\n") #MeV
                f.write(str(EE[i+1]*1e-6) + "\n") #MeV
    else:
        print 'Please input True or False in the fourth argument'

    return (x,xp,y,yp,zz,ddp,EE)
if __name__=="__main__":
    # Call the function
    # --------------------------------------------------------------------------------------------------------------
    job_range = range(1, int(jobs) + 1)
    with open('seed.txt', 'a') as g:
        print >> g, datetime.datetime.now()
        print >> g, "# ARGUMENTS = ", sys.argv
        for n in job_range:
            print "job", n
            j = '%s'%n
            dist_generator(particles, energy, machine, fort13, n, factor, emittance_x, emittance_y, alpha_x, alpha_y, beta_x, beta_y, offset_x, offset_xp, offset_y, offset_yp, dispersion_x, dispersion_xp, dispersion_y, dispersion_yp, bunch, spread, seed)
    


