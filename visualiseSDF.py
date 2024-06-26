# Import required libraries
import numpy as np
import functions as myf
import matplotlib.pyplot as plt
#
# Setup the gridsize
#
N = [512,128,128]
#
# Load the grid
#
[xp,yp,zp,xf,yf,zf] = myf.readGrid('assets/',[1,1,1],[0.0,0.0,0.0],1)
#
# Load the file
#
sdfu = np.load('assets/sdfu.npy')
sdfu = np.reshape(sdfu,N)
sdfv = np.load('assets/sdfv.npy')
sdfv = np.reshape(sdfv,N)
sdfw = np.load('assets/sdfw.npy')
sdfw = np.reshape(sdfw,N)
sdfp = np.load('assets/sdfp.npy')
sdfp = np.reshape(sdfp,N)
#
# Plotting for check
#
plt.figure(1)
plt.subplot(2,2,1)
plt.pcolor(xp,zp,np.squeeze(sdfu[:,64,:]).T,shading='nearest')
plt.title('U faces')
plt.colorbar()
plt.clim(-1,1)
plt.gca().set_aspect('equal', adjustable='box')
plt.subplot(2,2,2)
plt.pcolor(xp,yp,np.squeeze(sdfv[:,64,:]).T,shading='nearest')
plt.colorbar()
plt.title('V faces')
plt.clim(-1,1)
plt.gca().set_aspect('equal', adjustable='box')
plt.subplot(2,2,3)
plt.pcolor(xp,zf,np.squeeze(sdfw[:,64,:]).T,shading='nearest')
plt.colorbar()
plt.title('W faces')
plt.clim(-1,1)
plt.gca().set_aspect('equal', adjustable='box')
plt.subplot(2,2,4)
plt.pcolor(xp,zp,np.squeeze(sdfp[:,64,:]).T,shading='nearest')
plt.colorbar()
plt.title('P cell-centers [scalars]')
plt.clim(-1,1)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

