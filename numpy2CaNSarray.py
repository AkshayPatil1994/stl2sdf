#
# Convert the numpy array to CaNS compatible binary array
#
from functions import n2carray
#
# Convert all arrays here
#
# Define the grid size
N = [512,128,128]
# Write arrays to file
n2carray('assets/sdfu.npy',N,'assets/sdfu.bin')
n2carray('assets/sdfv.npy',N,'assets/sdfv.bin')
n2carray('assets/sdfw.npy',N,'assets/sdfw.bin')
n2carray('assets/sdfp.npy',N,'assets/sdfp.bin')
print("Done converting numpy array to CaNS compatible binary .....")
