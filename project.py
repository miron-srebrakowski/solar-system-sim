from Particle3D import Particle3D
import math
import numpy as np
import sys
import matplotlib.pyplot as pyplot
import functions as f
import integration


"""
For period calculation takes start point and calculate time each objects
travels 360 around the sun.
"""



def main():

    #Takes 3 file names from comand line and opens them for use. 1) File with initial conditions of objects (read);

    #2) Trajectory output file (write); 3) System energy output file (write).


    if len(sys.argv)!=6:
        print("Wrong number of arguments.")
        print("Usage: " + sys.argv[0] + "<intial cond file>" + "<trajectory file>" + "<parameter file>" + "<energy file>" + "<observables file>")
        quit()
    else:
        init_name = sys.argv[1]
        traj_name = sys.argv[2]
        param_name = sys.argv[3]
        energy_name = sys.argv[4]
        observables_name = sys.argv[5]


    infile = open(init_name, "r")
    traj_file = open(traj_name, "w")
    param_file = open(param_name, "r")
    energy_file = open(energy_name, "w")
    observables_file = open(observables_name, "w")


    #Time step in days.
    line = param_file.readline()
    linesplit = line.split(" ")
    object_number = int(linesplit[0])
    dt = float(linesplit[1])
    steps = int(linesplit[2])


    energy_list = [] #contains the system energies at each time step.
    time_list = [] #contains the time steps.
    object_list = [] #contains the objects.
    prev_pos_list = []
    angle_list = []
    period_list = []


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


# Main simulation loop:
#1) Prints pos & v to traj file
#2) Updates pos using force (for first time step force = initial force)
#3) Calculates the sum of forces on each object
#4) Stores each force sum in force.
#5) Updates v of each objects with force and previous force of each object
#6) Sets force to previous force

    integration.time_integration (steps, object_list, traj_file, object_number, prev_pos_list, dt, force, min_list, max_list, angle_list, force_sum, force_prev, energy_file, energy_list, time_list)

    print(angle_list[1])
    for i in range(len(angle_list)):
        period_list.append(steps / (np.rad2deg(angle_list[i]) / 360))



    for i in range (0, len(out_list)):
        observables_file.write(str(out_list[i]) + "\n")
        observables_file.write("Minimum Distance: " + str(min_list[i]) + "\n")
        observables_file.write("Maximum Distance: " + str(max_list[i]) + "\n")
        observables_file.write("Orbital Period: " + str(period_list[i]) + "\n")
        observables_file.write("\n")

    # Plot system energy to screen


    pyplot.title('Solar system: total energy vs time')
    pyplot.xlabel('Time')
    pyplot.ylabel('Total Energy')
    pyplot.plot(time_list, energy_list)
    pyplot.show()


main()
