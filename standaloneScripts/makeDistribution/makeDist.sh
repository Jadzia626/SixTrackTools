#! /usr/bin/env bash

## LHC, 7 TeV

PARTICLES=20000
#PARTICLES=100
ENERGY=7e12
MACHINE=HL_coll
FORT13=True
JOBS=1
FACTOR=1.0
#FACTOR=0.0
EMITTANCE_X=2.5e-6
EMITTANCE_Y=2.5e-6
ALPHA_X=0.0035001
ALPHA_Y=-0.0007714
BETA_X=0.150741
BETA_Y=0.150236
OFFSET_X=0.0000018e-3
OFFSET_XP=0.0000001e-3
OFFSET_Y=0.0000022e-3
OFFSET_YP=0.2949993e-3
DISPERSION_X=0.0034332
DISPERSION_XP=-0.0114644
DISPERSION_Y=0.0008100
DISPERSION_YP=-0.0143341
BUNCH=0.0755
SPREAD=1.13e-4
if [ $# -eq 1 ]; then
    SEED=$1
else
    SEED=42
fi


#Single distribution
./generate_distribution.py $PARTICLES $ENERGY $MACHINE $FORT13 $JOBS $FACTOR $EMITTANCE_X $EMITTANCE_Y $ALPHA_X $ALPHA_Y $BETA_X $BETA_Y $OFFSET_X $OFFSET_XP $OFFSET_Y $OFFSET_YP $DISPERSION_X $DISPERSION_XP $DISPERSION_Y $DISPERSION_YP $BUNCH $SPREAD $SEED
mv fort.13 fort13-single

## LHC, 7 TeV, HALO

PARTICLES=20000
#PARTICLES=100
ENERGY=7e12
MACHINE=HL_coll
FORT13=True
JOBS=1
FACTOR=1.8
#FACTOR=0.0
EMITTANCE_X=2.5e-6
EMITTANCE_Y=2.5e-6
ALPHA_X=0.0035001
ALPHA_Y=-0.0007714
BETA_X=0.150741
BETA_Y=0.150236
OFFSET_X=0.0000018e-3
OFFSET_XP=0.0000001e-3
OFFSET_Y=0.0000022e-3
OFFSET_YP=0.2949993e-3
DISPERSION_X=0.0034332
DISPERSION_XP=-0.0114644
DISPERSION_Y=0.0008100
DISPERSION_YP=-0.0143341
BUNCH=0.0755
SPREAD=1.13e-4
if [ $# -eq 1 ]; then
    SEED=$1
else
    SEED=42
fi


#Single distribution
./generate_distribution.py $PARTICLES $ENERGY $MACHINE $FORT13 $JOBS $FACTOR $EMITTANCE_X $EMITTANCE_Y $ALPHA_X $ALPHA_Y $BETA_X $BETA_Y $OFFSET_X $OFFSET_XP $OFFSET_Y $OFFSET_YP $DISPERSION_X $DISPERSION_XP $DISPERSION_Y $DISPERSION_YP $BUNCH $SPREAD $SEED
mv fort.13 fort13-single-HALO