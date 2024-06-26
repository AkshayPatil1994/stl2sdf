#!/bin/zsh
#
# Input parameters
#
nprocs=4
echo "Be sure to change the name of the infile and the outfile if you wish to run the multi_sphere.stl case!"
#
echo "------------------------------------"
echo "This script will run the example workflow for the sphere.stl case..."
echo "This should take around 5 mins..."
echo "------------------------------------"
#
echo "Using $nprocs processors to generate the SDF"
echo "------------------------------------"
#
mpirun -np $nprocs python -m mpi4py generateSDFmpi.py
echo "------------------------------------"
#
echo "Press q to exit the plot window"
python visualiseSDF.py
echo "------------------------------------"
#
python numpy2CaNSarray.py
#
echo "------------------------------------"
echo "All tasks completed......"
echo "------------------------------------"
