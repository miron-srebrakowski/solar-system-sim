from Particle3D import Particle3D
import math
import numpy as np
import sys
import matplotlib.pyplot as pyplot
import functions as f
import integration

"""
Program containing the main function of the solar system simulation.
"""

def main():

    #Takes 3 file handle arguments and opens them 

    if len(sys.argv)!=4:
        print("Wrong number of arguments.")
        print("Usage: " + sys.argv[0] + "<intial cond file>" + "<trajectory file>" + "<parameter file>" )
        quit()
    else:
        infile = open(sys.argv[1], "r") #file containing the initial conditions of the objects
        traj_file = open(sys.argv[2], "w") #output trajectory file
        param_file = open(sys.argv[3], "r") #file containing the simulation parameters (number of objects, timestep size and number of time steps)
        energy_file = open("energy.dat", "w") #output total system energy file
        observables_file = open("observables.dat", "w") #output file to contain physical observables of the system


    #Initialises the time step, number of steps and number of objects from
    #a parameter file.

    line = param_file.readline()
    linesplit = line.split(" ")
    object_number = int(linesplit[0])
    dt = float(linesplit[1])
    steps = int(linesplit[2])

    #Initialises lists used in the simulation.

    energy_list = [] #contains the system energies at each time step.
    time_list = [] #contains the time steps.
    object_list = [] #contains the objects.
    prev_pos_list = [] #contains previous object positions
    angle_list = [] #contains total angular distance travelled by each object
    period_list = [] #contains the orbital periods of each object


    force = [] #contains new forces. [nx3]
    force_prev=[] #contains previous forces. [nx3]
    force_sum = np.array([0, 0, 0], float) # used to sum forces for intividual objects [1x3]
    force_int = np.array([0, 0, 0], float) # initial force on a single object [1x3].

    for i in range (0, object_number):
        object_list.append(Particle3D.create_particle(infile))
        prev_pos_list.append(0)

    for i in range (0, object_number):
        angle_list.append(0)


# Calculates the initial Force vector on each object, by summing the gravitational forces
# between the object and all the other objets in the system, eg. Fsun = Fsv + Fsm.


    for j in range (0, len(object_list)):
        for k in range (0, len(object_list)):
            if k != j:
                force_int = force_int + f.gravitational_force(object_list[j], object_list[k])
            force_prev.append(force_int)
            force.append(0)

        min_list, max_list, out_list = f.initial_object_separation(object_list)

# Sets initial forces to force.

        for l in range(0,len(force)):
            force_prev[l]=force[l]

# Corrects for centre of mass.

    f.com_corr(object_list)

# Main time integration loop. Fills trajectory file, finds total angular distance travelled byeach body
# and calculates total energy of the system at each time step.

    integration.time_integration (steps, object_list, traj_file, object_number, prev_pos_list, dt, force, min_list, max_list, angle_list, force_sum, force_prev, energy_file, energy_list, time_list)

# Calculates the orbital period of each object and stores it in a list

    for i in range(len(angle_list)):
        period_list.append(steps / (np.rad2deg(angle_list[i]) / 360))


# Writes the values of the physical observables of each object into a file

    for i in range (0, len(out_list)):
        observables_file.write(str(out_list[i]) + "\n")
        observables_file.write("Minimum Distance: " + str(min_list[i]) + "\n")
        observables_file.write("Maximum Distance: " + str(max_list[i]) + "\n")
        observables_file.write("Orbital Period: " + str(period_list[i]) + "\n")
        observables_file.write("\n")

    # Plots system energy to screen

    pyplot.title('Solar system: total energy vs time')
    pyplot.xlabel('Time')
    pyplot.ylabel('Total Energy')
    pyplot.plot(time_list, energy_list)
    pyplot.show()

# Closes input/output files

    infile.close()
    traj_file.close()
    param_file.close()
    energy_file.close()
    observables_file.close()

# Runs main function

main()
