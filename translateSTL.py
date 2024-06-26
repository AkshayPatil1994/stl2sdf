#
# Python routines to translate stl
#
# Load the library
from functions import trasRot
import numpy as np
#
# File I/O
#
saveMesh = 1                                            # Save mesh flag
scale = 0.001                                           # Scale mesh 
translation = np.array([0.12,0.12,0.0])                 # Translation in x y and z input
rotAngle = 90                                           # Rotation angle magnitude [degrees]
rotAx = [1, 0, 0]                                       # Which rotation axis to rotate about?
inFile = 'assets/sphere.stl'                            # Input file + location
outFile = 'assets/newsphere.stl'                        # Output file + location
#
# Call functions
#
trasRot(saveMesh,inFile,outFile,translation,rotAngle,rotAx,scale)
#
# End of script
#
