#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import sys

ifile_name = "fort.13"
if len(sys.argv) == 2:
    ifile_name = sys.argv[1]

ifile = open(ifile_name, 'r')

x = []
xp = []
y = []
yp = []
z = []
dpp = []

lmod = 0
for l in ifile.readlines():
    if lmod == 0:
        x.append(float(l))
    elif lmod == 1:
        xp.append(float(l))
    elif lmod == 2:
        y.append(float(l))
    elif lmod == 3:
        yp.append(float(l))
    elif lmod == 4:
        z.append(float(l))
    elif lmod == 5:
        dpp.append(float(l))

    elif lmod == 6:
        x.append(float(l))
    elif lmod == 7:
        xp.append(float(l))
    elif lmod == 8:
        y.append(float(l))
    elif lmod == 9:
        yp.append(float(l))
    elif lmod == 10:
        z.append(float(l))
    elif lmod == 11:
        dpp.append(float(l))
        
    elif lmod == 12:
        pass
    elif lmod == 13:
        pass        
    elif lmod == 14:
        pass

    lmod += 1
    lmod  = lmod % 15

ifile.close()

plt.figure()
plt.scatter(x,xp)
plt.xlabel("x [mm]")
plt.xlabel("xp [mrad]")

plt.figure()
plt.scatter(y,yp)
plt.xlabel("y [mm]")
plt.ylabel("yp [mrad]")

plt.figure()
plt.scatter(z,dpp)
plt.xlabel("z [mm]")
plt.ylabel("dp/p")


plt.show()
