from matplotlib import pyplot as plt
import generate_distribution

Z,DELTAE,H = generate_distribution.get_bucket("SPS_55")
x,xp,y,yp,zz,ddp,EE = generate_distribution.dist_generator(1000, 55e9, "SPS_55", "True",1,1,3.1e-6,2.8e-6,-2.25,0.52,101,21,0,0,0,0,1.23,1.36,0.15,1e-3,42)
plt.contour(Z,DELTAE,H,40)
plt.contour(Z,DELTAE,H,levels=[0.0], linewidths=5)
plt.scatter(zz,ddp)
plt.show()
