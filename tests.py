#
# Python routines to test basic operations
#
# Load the library
import trimesh                            # Trimesh library
import numpy as np                        # Numpy library
# File to load
inFile = 'assets/sphere.stl'
# Load the mesh
mesh =trimesh.load(inFile)
# Do simple checks
waterTight = mesh.is_watertight     # mesh watertight? [Important for generating SDF]
# Check volume
if waterTight:
    print("Vol: of mesh/ Vol: of convex hull = ",mesh.volume/mesh.convex_hull.volume,".")
else:
    print("Mesh is not watertight!")
# Bounding box
print("STL is bounded by (lowest x,y,z):",mesh.bounds[0])
print("STL is bounded by (largest x,y,z):",mesh.bounds[1])
