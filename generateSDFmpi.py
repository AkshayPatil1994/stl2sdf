import trimesh                            # Trimesh library
import skimage                            # Sci-kit library
import numpy as np                        # Numpy library
import functions as myf                   # CaNS related grid operations
from mpi4py import MPI                    # MPI for python module for parallelisation
import time                               # Timing library to time the process
import sys                                # Import system to exit script
import argparse                           # Argument parser for command line arguments
from distutils.util import strtobool
# 
# Parse input arguments
#
parser = argparse.ArgumentParser(description='Compute the SDF fields using MPI.')
parser.add_argument('--infile', type=str, default='assets/sphere.stl', help='Input STL/OBJ file')
parser.add_argument('--filename', type=str, default='assets/', help='Target mesh folder')
parser.add_argument('--nsamples', type=int, default=1000000, help='Number of sampling points used to compute the SDF')
parser.add_argument('--writeData',dest='writeData',type=lambda x: bool(strtobool(x)), help='Flag to write SDF to files')
parser.add_argument('--clipSDF',dest='clipSDF',type=lambda x: bool(strtobool(x)),help='Flag to clip the SDF computation at zmax')
args = parser.parse_args()
#
# Initialise MPI and communications
#
comm = MPI.COMM_WORLD   # Initialise MPI comm-world        
rank = comm.Get_rank()  # Get rank of each proc
size = comm.Get_size()  # Get size of mpirun for each instance
#
# Rank 0 does all the I/O and initial setup
#
if rank == 0:
    start_time = time.time()        # Store start time
    print("---------------------------------------------------------")
    print("███████╗████████╗██╗     ██████╗ ███████╗██████╗ ███████╗")
    print("██╔════╝╚══██╔══╝██║     ╚════██╗██╔════╝██╔══██╗██╔════╝")
    print("███████╗   ██║   ██║      █████╔╝███████╗██║  ██║█████╗  ")
    print("╚════██║   ██║   ██║     ██╔═══╝ ╚════██║██║  ██║██╔══╝  ")
    print("███████║   ██║   ███████╗███████╗███████║██████╔╝██║     ")
    print("╚══════╝   ╚═╝   ╚══════╝╚══════╝╚══════╝╚═════╝ ╚═╝")
    print("---------------------------------------------------------")
    print(" - - - - - - - Starting the MPI job - - - - - - - ")
    print("    User requested ",size," CPUs for this job  ")
    print("---------------------------------------------------------")
    #
    # User flag to write SDF to files
    #
    writeData = args.writeData
    #
    # Name of the input-output file
    #
    inFile = args.infile
    #
    # Target mesh folder
    #
    filename = args.filename
    #
    # Number of sampling points used to compute the SDF
    # [large values are memory and compute time intensive .but. improve the SDF computation]
    #
    nsamples = args.nsamples
    #
    # Clipping SDF flag
    #
    clipMySDF = args.clipSDF
    #
    # Load the mesh
    #
    [xp,yp,zp,xf,yf,zf] = myf.readGrid(filename,[1,1,1],[0.0,0.0,0.0],1)    # Loading the grid [CaNS]
    # For dopamine generated grid
    # gridfile = 'assets/grid.out'
    # [xft,yft,zft,xpt,ypt,zpt] = myf.loaddopaminegrid(gridfile)
    # Dopamine grid requires some boundary slicing to match the workflow [not important for other grids!]
    # xp = xpt[1:]
    # yp = ypt
    # zp = zpt[1:]
    # xf = xft[2:]
    # yf = yft[1:]
    # zf = zft[2:]
    #
    # Print grid information to screen
    #
    print("xp grid -- starts at %f | ends at %f with %d points"%(xp[0],xp[-1],len(xp)))
    print("yp grid -- starts at %f | ends at %f with %d points"%(yp[0],yp[-1],len(yp)))
    print("zp grid -- starts at %f | ends at %f with %d points"%(zp[0],zp[-1],len(zp)))
    print("xf grid -- starts at %f | ends at %f with %d points"%(xf[0],xf[-1],len(xf)))
    print("yf grid -- starts at %f | ends at %f with %d points"%(yf[0],yf[-1],len(yf)))
    print("zf grid -- starts at %f | ends at %f with %d points"%(zf[0],zf[-1],len(zf)))
    #
    # Load stl/obj file as mesh object
    #
    mesh = trimesh.load(inFile)
    #
    # Do some consistency checks on the mesh
    #
    ismeshWT = mesh.is_watertight           # Check if the mesh is watertight
    if(ismeshWT):
        print("---------------------------------------------------------")
        print("File %s is watertight"%(inFile))
        print("---------------------------------------------------------")
    else:
        print("---------------------------------------------------------")
        print("File %s is *NOT* watertight, the resulting SDF may not be accurate!"%(inFile))
        print("---------------------------------------------------------")
    # Check the bounds of the mesh
    print("** Bounding Box for the OBJ **")
    print("X_i minimum: ",mesh.bounds[0])
    print("X_i maximum: ",mesh.bounds[1])
    print("---------------------------------------------------------")
    # Find where zp < mesh.bounds[1,2]
    if(clipMySDF):
        zpmax_loc = np.where(zp<1.05*mesh.bounds[1,2])[0][-1]
        zfmax_loc = np.where(zf<1.05*mesh.bounds[1,2])[0][-1]
        # Truncate location
        print("Truncating the vertical extent at",zp[zpmax_loc], "at zp index: ",zpmax_loc)
        print("---------------------------------------------------------")
    else:
        # Define zpmax_loc and zfmax_loc as dummy values to avoid bcast error
        zpmax_loc = 1
        zfmax_loc = 1
    # Only supply the z limited values to do a narrow search
    #
    # Define the size of the array for U, V, W, and P
    #
    Nu = np.array([len(xf),len(yp),len(zp)])
    Nv = np.array([len(xp),len(yf),len(zp)])
    Nw = np.array([len(xp),len(yp),len(zf)])
    Ns = np.array([len(xp),len(yp),len(zp)])
    #
    # Force check for number of processors
    #
    remMod = Nu[0]%size
    if remMod != 0:
        sys.exit("Please set nprocs such that Nx%nprocs == 0...")
#
# Force all processors to arrive at this barrier
#
comm.Barrier()
if rank == 0:
    print("Broadcasting all data to other CPUs")
#        
# Allocate memory on all procs for broadcasted data
#
if rank != 0:
    inFile = ""
    nsamples = None
    clipMySDF = None
    zpmax_loc = None
    zfmax_loc = None
    Nu = np.array([0,0,0])
    Nv = np.array([0,0,0])
    Nw = np.array([0,0,0])
    Ns = np.array([0,0,0])   
#
# Broadcast common data to all ranks
#
inFile = comm.bcast(inFile,root=0)
nsamples = comm.bcast(nsamples,root=0)
clipMySDF = comm.bcast(clipMySDF,root=0)
zpmax_loc = comm.bcast(zpmax_loc,root=0)
zfmax_loc = comm.bcast(zfmax_loc,root=0)
comm.Bcast([Nu, MPI.DOUBLE],root=0)
comm.Bcast([Nv, MPI.DOUBLE],root=0)
comm.Bcast([Nw, MPI.DOUBLE],root=0)
comm.Bcast([Ns, MPI.DOUBLE],root=0)
#
# Broadcast common data to all procs
#
if rank != 0:
    # Grid data    
    yp = np.empty(Ns[1],dtype=np.float64)
    zp = np.empty(Ns[2],dtype=np.float64)
    yf = np.empty(Nv[1],dtype=np.float64)
    zf = np.empty(Nw[2],dtype=np.float64)
    xf = np.empty(np.int64(Nu[0]/size),dtype=np.float64)
    xp = np.empty(np.int64(Ns[0]/size),dtype=np.float64)
#
# Create local arrays that are split to distribute the workload
#     
xpl = np.empty(np.int64(Ns[0]/size),dtype=np.float64)
xfl = np.empty(np.int64(Nu[0]/size),dtype=np.float64)  
#          
# Broadcast all arrays as is and then split the workload [easier but **in-efficient**]
# Since the grid arrays have small memory footprint, this does not lead to any efficiency downgrade
#
comm.Bcast([yp, MPI.DOUBLE],root=0)
comm.Bcast([zp, MPI.DOUBLE],root=0)
comm.Bcast([yf, MPI.DOUBLE],root=0)
comm.Bcast([zf, MPI.DOUBLE],root=0)
comm.Scatter(xf,xfl,root=0)
comm.Scatter(xp,xpl,root=0)
#
# All procs now load the obj file
#
mesh = trimesh.load(inFile)
#
# Check start time of analysis
#
if rank == 0:
    anaStartTime = time.time()
    print("Starting to compute the SDF fields")
#
# Compute the SDF on each proc for all components
#
if(clipMySDF):
    SDFUlocal = myf.computeSDF(mesh,xfl,yp,zp[0:zpmax_loc],nsamples)
    SDFVlocal = myf.computeSDF(mesh,xpl,yf,zp[0:zpmax_loc],nsamples)
    SDFWlocal = myf.computeSDF(mesh,xpl,yp,zf[0:zfmax_loc],nsamples)
    SDFPlocal = myf.computeSDF(mesh,xpl,yp,zp[0:zpmax_loc],nsamples)
else:
    SDFUlocal = myf.computeSDF(mesh,xfl,yp,zp,nsamples)
    SDFVlocal = myf.computeSDF(mesh,xpl,yf,zp,nsamples)
    SDFWlocal = myf.computeSDF(mesh,xpl,yp,zf,nsamples)
    SDFPlocal = myf.computeSDF(mesh,xpl,yp,zp,nsamples)
# Type conversion [Change precision of the output array below]
SDFUlocal = SDFUlocal.astype(np.float64,casting='same_kind')
SDFVlocal = SDFVlocal.astype(np.float64,casting='same_kind')
SDFWlocal = SDFWlocal.astype(np.float64,casting='same_kind')
SDFPlocal = SDFPlocal.astype(np.float64,casting='same_kind')
#
# Check end time of analysis
#
if rank == 0:
    anaEndTime = time.time()
# Define size of the SDF required
if(clipMySDF):
    sdfusize = Nu[0]*Nu[1]*zpmax_loc
    sdfvsize = Nv[0]*Nv[1]*zpmax_loc
    sdfwsize = Nw[0]*Nw[1]*zfmax_loc
    sdfpsize = Ns[0]*Ns[1]*zpmax_loc
else:
    sdfusize = Nu[0]*Nu[1]*Nu[2]
    sdfvsize = Nv[0]*Nv[1]*Nv[2]
    sdfwsize = Nw[0]*Nw[1]*Nw[2]
    sdfpsize = Ns[0]*Ns[1]*Ns[2]
#
# Gather the array from all processors to id = 0
#
sdfu_recv = None
sdfv_recv = None
sdfw_recv = None
sdfp_recv = None
if rank == 0:
    sdfu_recv = np.empty(sdfusize,dtype='d')
    sdfv_recv = np.empty(sdfvsize,dtype='d')
    sdfw_recv = np.empty(sdfwsize,dtype='d')
    sdfp_recv = np.empty(sdfpsize,dtype='d')
#
# Gather all data
#
# Life is great as long as array chunk < 2GB see https://github.com/mpi4py/mpi4py/issues/23
# MPI and mpi4py give SystemError: Negative size passed to PyBytes_FromStringAndSize for chunk > 2GB
# For array chunks < 2GB comm.gather() works. However, for chunks > 2GB one needs to use comm.Gatherv([sentbuf, MPI.double],root=0)
#sdfu_recv = comm.gather(SDFUlocal,root=0)
#sdfv_recv = comm.gather(SDFVlocal,root=0)
#sdfw_recv = comm.gather(SDFWlocal,root=0)
#sdfp_recv = comm.gather(SDFPlocal,root=0)
comm.Gatherv(SDFUlocal,sdfu_recv,root=0)
comm.Gatherv(SDFVlocal,sdfv_recv,root=0)
comm.Gatherv(SDFWlocal,sdfw_recv,root=0)
comm.Gatherv(SDFPlocal,sdfp_recv,root=0)
#
# Write SDF to file
#
if rank == 0 and writeData:
    # First correctly size the arrays
    sdfu_write = np.ones(Nu)
    sdfv_write = np.ones(Nv)
    sdfw_write = np.ones(Nw)
    sdfp_write = np.ones(Ns)
    # Typecast to arrays
    sdfu_recv = np.array(sdfu_recv) 
    sdfv_recv = np.array(sdfv_recv)  
    sdfw_recv = np.array(sdfu_recv)
    sdfp_recv = np.array(sdfp_recv) 
    # Select clipped arrays to write
    if(clipMySDF):
        sdfu_write[:,:,0:zpmax_loc] = np.reshape(sdfu_recv,(Nu[0],Nu[1],zpmax_loc))
        sdfv_write[:,:,0:zpmax_loc] = np.reshape(sdfv_recv,(Nv[0],Nv[1],zpmax_loc))
        sdfw_write[:,:,0:zpmax_loc] = np.reshape(sdfw_recv,(Nw[0],Nw[1],zpmax_loc))
        sdfp_write[:,:,0:zpmax_loc] = np.reshape(sdfp_recv,(Ns[0],Ns[1],zpmax_loc))
    else:
        sdfu_write = sdfu_recv
        sdfv_write = sdfv_recv 
        sdfw_write = sdfw_recv 
        sdfp_write = sdfp_recv
    # Write all arrays to numpy format
    np.save(str(filename)+'sdfu',sdfu_write)
    np.save(str(filename)+'sdfv',sdfv_write)
    np.save(str(filename)+'sdfw',sdfw_write)
    np.save(str(filename)+'sdfp',sdfp_write)
#
# Print exit information
#
if rank == 0:
    end_time = time.time()
    process_time = end_time - start_time
    print("Code took around ",np.round(anaEndTime-anaStartTime,4),"seconds to run the analysis...")
    print("- Total wall-clock time: ",np.round(process_time,4),"seconds - ")
