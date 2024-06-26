import trimesh                            # Trimesh library
import skimage                            # Sci-kit library
import numpy as np                        # Numpy library
import functions as myf                   # CaNS related grid operations
import time                               # Timing library to time the process
import sys                                # Import system to exit script
from concurrent.futures import ProcessPoolExecutor  # Concurrent thread library
from rich.console import Console          # Fancy prompt and logs
from rich.padding import Padding          # Fancy prompt and logs
#
# ---------------------------------------------------------------------------------------
#
LOGO_STRING = """
---------------------------------------------------------
███████╗████████╗██╗     ██████╗ ███████╗██████╗ ███████╗
██╔════╝╚══██╔══╝██║     ╚════██╗██╔════╝██╔══██╗██╔════╝
███████╗   ██║   ██║      █████╔╝███████╗██║  ██║█████╗  
╚════██║   ██║   ██║     ██╔═══╝ ╚════██║██║  ██║██╔══╝  
███████║   ██║   ███████╗███████╗███████║██████╔╝██║     
╚══════╝   ╚═╝   ╚══════╝╚══════╝╚══════╝╚═════╝ ╚═╝     
---------------------------------------------------------
"""
#
# ---------------------------------------------------------------------------------------
#
def compute_sdf(mesh, grid, sample_count=100000):
    """
        Compute the Signed-Distance-Field (SDF) for 3 velocities and 1 scalar
    INPUT
        mesh:           [mesh object] The stl/obj object
        grid:           [numpy array] 6 numpy arrays for x, y, and z faces and cell centers
        sample_count:   [integer] Number of sampling points for generating the SDF
    OUTPUT
        sdf_u:          [numpy array] SDF for the U velocity faces
        sdf_v:          [numpy array] SDF for the V velocity faces
        sdf_w:          [numpy array] SDF for the W velocity faces
        sdf_p:          [numpy array] SDF for the P/scalar cell centers
    """
    [xp,yp,zp,xf,yf,zf] = grid

    sdf_u = myf.computeSDF(mesh,xf,yp,zp,sample_count) # for U faces
    sdf_v = myf.computeSDF(mesh,xp,yf,zp,sample_count) # for V faces
    sdf_w = myf.computeSDF(mesh,xp,yp,zf,sample_count) # for W faces
    sdf_p = myf.computeSDF(mesh,xp,yp,zp,sample_count) # for scalars at cell center

    sdf_u = sdf_u.astype(np.float64,casting='same_kind')
    sdf_v = sdf_v.astype(np.float64,casting='same_kind')
    sdf_w = sdf_w.astype(np.float64,casting='same_kind')
    sdf_p = sdf_p.astype(np.float64,casting='same_kind')

    return sdf_u, sdf_v, sdf_w, sdf_p
#
# ------------------------------------------------------------------------------------
#
if __name__ == '__main__':

    if(sys.argv[1] == ''):
        sys.exit("Please input `IN_FILE`, `FILENAME`, and `NUM_OF_CORES`")

    IN_FILE = sys.argv[1]
    FILENAME = sys.argv[2]
    NUM_OF_CORES = int(sys.argv[3])

    console = Console()

    console.print(LOGO_STRING)

    console.print(f"Using {IN_FILE} input file")

    console.print(f"The analysis will use {NUM_OF_CORES} cores.")

    start_time = time.time()

    mesh = trimesh.load(IN_FILE)
    console.log("Mesh loaded.")

    if mesh.is_watertight:
        console.print(Padding(f":white_check_mark: File {IN_FILE} is watertight.", 1))
    else:
        console.print(Padding(f":warning: File {IN_FILE} is not watertight! The SDF may not be accurate.", 1))

    global_grid = myf.readGrid(FILENAME,[1,1,1],[0.0,0.0,0.0],1)    # Loading the grid from CaNS
    [xp,yp,zp,xf,yf,zf] = global_grid
    console.log("Grid computed.")

    analysis_start_time = time.time()
    with console.status("Computing SDF chunks...") as status:
        with ProcessPoolExecutor(max_workers=NUM_OF_CORES) as pool:
            futures = []

            xp_chunks = np.array_split(xp, NUM_OF_CORES)
            xf_chunks = np.array_split(xf, NUM_OF_CORES)

            for i in range(NUM_OF_CORES):
                local_grid = [xp_chunks[i], yp, zp, xf_chunks[i], yf, zf]
                future = pool.submit(compute_sdf, mesh, local_grid)
                futures.append(future)
            
            u_results = []
            v_results = []
            w_results = []
            p_results = []
            for future in futures:
                local_u, local_v, local_w, local_p = future.result()
                u_results.append(local_u)
                v_results.append(local_v)
                w_results.append(local_w)
                p_results.append(local_p)
                console.log("Chunk finished.")

    u = np.concatenate(u_results, axis=0)
    v = np.concatenate(v_results, axis=0)
    w = np.concatenate(w_results, axis=0)
    p = np.concatenate(p_results, axis=0)

    analysis_end_time = time.time()

    of = FILENAME+'/sdfu'
    np.save(of, u)
    of = FILENAME+'/sdfv'
    np.save(of, v)
    of = FILENAME+'/sdfw'
    np.save(of, w)
    of = FILENAME+'/sdfp'
    np.save(of, p)

    end_time = time.time()
    process_time = end_time - start_time
    console.print(f"Code took around {np.round(analysis_end_time - analysis_start_time, 4)} seconds to run the analysis...")
    console.print(f"- Total wall-clock time: {np.round(process_time, 4)} seconds - ")
