N-body simulation of solar system including Earths moon and Halleys's Comet.

There are 6 files included

project.py contains the main body of the code and calls the two other files
integration.py contains a function to perform velocity verlet time integration
functions.py contains a set of functions used within the main body for various calculations and within
                      the integration file
particle3D.py contains the code creating the objects used within the main body
param contains the parameters for the simulation
initial contains the initial conditions for each of the 12 bodies to be included in the simulation


The program takes three command line arguments,
i.e.:
[user@cplab001  ~]$ python3  <ParticleManyBody.py>  <particle.input> <traj.xyz>
<param.input>

where particle.input is the file containing the particle details
      param.input contains the simulation parameters
  and traj.xyz is the output file, which contains the trajectory details in a format
      which can be used for visualisation in VMD
      This can be run using:
        [user@cplab001 ~]$ vmd <myTrajFile.xyz>

The particle details should be in the format:
<mass(particle1)>  <label(particle1)> <x1> <y1> <z1> <vx1> <vy1> <vz1>
<mass(particle2)>  <label(particle2)> <x2> <y2> <z2> <vx2> <vy2> <vz2>
...
...

The program assumes the first particle is the Sun followed by the remaining bodies
It also assumes that the Moon is the particle directly after the Earth

The mass is in kg
    the x,y,z positions are in astronomical units,AU
    vx,vy,vz are in AU per day

The parameter file should be in the format:
<number of bodies>  <time step (in days)> <simulation length>
a simulation length of 200000 is sufficient for a full orbit of each body
a length of 2 million was found to have an unreasonable run-time > 30 mins

Once the simulation has finished the a plot of energy (in joules) of the total system against
time (in days) will be displayed to show energy fluctuations of the system

2 files should also open
one contains the energy data and the other contains observables of the simulation
the observables given are the apo- and perhelia for the bodies (displayed as maximum and minimum distances and given in AU) excluding the Sun
and the orbital period of the body around the Sun (in days)
an additional set of observables is given for the Moon around the Earth
