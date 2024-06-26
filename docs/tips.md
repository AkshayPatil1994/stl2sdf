# Scalable workflow

## Handling large input geometries

NOTE: This workflow is time-intensive and might require a few iterations, however, ensures non-degenerate SDF. 

[User be warned!]

Since the memory requirements for the parallel code can be quite drastic, we recommend the following workflow:

- Downsample the input geometry using the `Alpha wrap` functionality from the `CGAL` library. You can use [wrapwrap](https://github.com/ipadjen/wrapwrap.git) for this step.
- Once the input geometry is wrapped, the file size should become relatively more manageable with the MPI version of the code.

#### Limitations

- The first step will chamfer the sharp geometric features, so eventually it leads "smoother" edges. However, the novelty is the fact that it ensures that the geometry is watertight!
- There is a fair bit of iterations needed to get the right resolution for the stl geometry. For sharper edges the input arguments to `wrapwrap` upwards of 2000 and 3000 for `relative_alpha` and `relative_offset`, respectively, lead to acceptable to good outputs.

#### Credits: [Ivan Paden ](https://github.com/ipadjen)

## Other tips

- The code sometimes produce degenerate SDF, especially for low values of `nsamples`.
- We recommend using `nsamples > 1e7` for moderately complex geometry. If the degeneracy persists, try using `nsamples ~ 1e9`. This has to do with the resolution requirements for accurate sampling of the entire stl/obj. 
