# How to use stl2sdf

1. Make sure you create a folder where you store the obj/stl geometry file (by Default this folder will be titled `assets`)
2. Ensure that the bounding box of the geometry is smaller than the computational grid to avoid any artefacts in the computational step. This can be done using a simple obj/stl visualiser such as Paraview, MeshLab, or Blender.
3. Generate the computational grid and place it in the `assets` directory
4. Source the python environment that has `stl2sdf` libraries (Optional)
5. To run the code with 4 cores with the default settings
```
mpirun -np 4 python -m mpi4py generateSDFmpi.py 
```
6. Alternatively, you can use the user input parameters by specifying them as shown below
```
mpirun -np 4 python -m mpi4py generateSDFmpi.py  --infile 'data/test.stl'
```
A total of five input parameters can be specified as listed below
```
--infile INFILE       Input STL/OBJ file | argument type - string 
--filename FILENAME   Target mesh folder | argument type - string
--nsamples NSAMPLES   Number of sampling points used to compute the SDF | argument type - integer
--writeData WRITEDATA Flag to write SDF to files | argument type - Boolean
--clipSDF CLIPSDF     Flag to clip the SDF computation at zmax | argument type - Boolean
```
7. Finally, you can visualise the sdf arrays using a reference script titled `visualiseSDF.py`
8. To export the numpy arrays to CaNS readable format, use the `numpy2CaNSarray.py` script. The utility in using numpy arrays is to provide full support for exporting the SDF to other solvers using basic numpy operations. Consequently, stl2sdf + CaNS can be used as a sparse SDF generator which can be then ported to say a spectral solver that uses SDF-based Immersed Boundary Method after appropriate interpolation and grid transfer is defined.

Sample output from the program (Please note that depending on your input parameters, this output might be slightly different). It is also important to note that while the SDF is being computed, there is no progress bar as this is an operation delegated to the `mesh_to_sdf` library, which does not provide an ETA.  
So the program might seem "stuck" but you can check your RAM and CPU usage with tools like `htop` to see that the program is indeed working on the tasks assigned.
```
---------------------------------------------------------
███████╗████████╗██╗     ██████╗ ███████╗██████╗ ███████╗
██╔════╝╚══██╔══╝██║     ╚════██╗██╔════╝██╔══██╗██╔════╝
███████╗   ██║   ██║      █████╔╝███████╗██║  ██║█████╗  
╚════██║   ██║   ██║     ██╔═══╝ ╚════██║██║  ██║██╔══╝  
███████║   ██║   ███████╗███████╗███████║██████╔╝██║     
╚══════╝   ╚═╝   ╚══════╝╚══════╝╚══════╝╚═════╝ ╚═╝
---------------------------------------------------------
 - - - - - - - Starting the MPI job - - - - - - - 
    User requested  8  CPUs for this job  
---------------------------------------------------------
 User Input Summary 
Write Data to file:  None
Name of inputfile:  assets/multi_sphere.stl
Location of data write:  assets/
Number of sampling points:  2000000
Will the SDF be clipped?:  True
---------------------------------------------------------
xp grid -- starts at 0.031250 | ends at 31.968750 with 512 points
yp grid -- starts at 0.031250 | ends at 7.968750 with 128 points
zp grid -- starts at 0.031250 | ends at 7.968750 with 128 points
xf grid -- starts at 0.062500 | ends at 32.000000 with 512 points
yf grid -- starts at 0.062500 | ends at 8.000000 with 128 points
zf grid -- starts at 0.062500 | ends at 8.000000 with 128 points
---------------------------------------------------------
File assets/multi_sphere.stl is watertight
---------------------------------------------------------
** Bounding Box for the OBJ **
X_i minimum:  [9.50009433 3.50001962 3.5       ]
X_i maximum:  [20.5        4.4999946  4.5      ]
---------------------------------------------------------
Truncating the vertical extent at 4.71875 at zp index:  75
---------------------------------------------------------
Broadcasting all data to other CPUs
Starting to compute the SDF fields
Code took around  82.38 seconds to run the analysis...
- Total wall-clock time:  137.8856 seconds -

```
