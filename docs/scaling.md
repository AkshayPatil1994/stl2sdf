# stl2sdf Scaling Data  

The scaling data consists of two cases tested on two different computing system i.e., AMD and Intel. Case 1 was tested on a local workstation laptop with 16 GB memory and an Intel Core i9-9880H with 8 CPUs and 2.3GHz on the Ubuntu 22.04 LTS operating system. Case 2 was tested on a local server workstation with 252 GB memory and an AMD EPYC 7302 16 x 2 CPUs and 1.5 GHz on the 20.04 LTS operating system. All tests were run when there were no other users active on the system and the baseline memory usage of the operating system was around 1.5 GB on average. 

## Case 1: Wind Around Buildings

This case is built using the tutorial `windAroundBuildings` provided through `OpenFOAM`. The geometry consists of a small part of an urban landscape. 

- File size [OBJ]: 71 MB
- Grid size [CaNS]: 512 x 256 x 128 = 16.8 Million
- nSamples: 1 Million

| Number of Processors | Analysis Time [s] | Total Time [s] | Peak Memory Usage [GB]|
|:--------------------:|:-----------------:|:--------------:|:---------------------:|
|           1          |       680.1       |      695.8     |         2.2           |
|           2          |       538.9       |      540.7     |         2.5           |
|           4          |       347.6       |      349.5     |         5.0           |
|           8          |       263.7       |      265.9     |         6.5           |

Analysis Time: Time taken to compute the Signed-Distance-Field 
Total Time: Total time taken to complete the job including MPI initialising and file I/O

<hr>

## Case 2: Coral Channel

This case is built using a stochastically generated coral bed using three distinct coral geometries obtained from the Smithsonian library.

- File size [OBJ]: 57 MB
- Grid size [CaNS]: 2048 x 1024 x 256 = 536.8 Million
- nSamples: 5 Million

| Number of Processors | Analysis Time [s] | Total Time [s] | Peak Memory Usage [GB]|
|:--------------------:|:-----------------:|:--------------:|:---------------------:|
|           1          |       22584.0     |      22611.8   |         20            |
|           2          |       11244.5     |      11338.2   |         22            |
|           4          |       5476.5      |      5811.7    |         26            |
|           8          |       2723.0      |      3014.5    |         32            |
|           16         |       1243.8      |      1552.9    |         43            |
|           32         |       627.7       |      846.9     |         52            |

Analysis Time: Time taken to compute the Signed-Distance-Field
Total Time: Total time taken to complete the job including MPI initialising and file I/O

<hr>

## Wind Around Buildings Results 
<img src="../assets/windAroundBuildings.png" height=500>

## Coral Channel
<img src="../assets/coralchannel.png" height=500>

## Strong Scaling Based on Data
<img src="../assets/scaling.png" height=500>
