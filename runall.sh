#!/bin/zsh
#
# Input parameters
#
nprocs=4
infile='assets/sphere.stl'
outfileloc='assets/'
#
echo "------------------------------------"
echo "This script will run the example workflow for the sphere.stl case..."
echo "This should take around 5 mins..."
echo "------------------------------------"
#
echo "Using $nprocs processors to generate the SDF"
echo "------------------------------------"
#
python generateSDF.py $infile $outfileloc $nprocs
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
