from Particle3D import Particle3D
import math
import numpy as np
import sys


def energy_potential(p1,p2):
    '''
    Method calculating the potential energy between 2 Particle3D objects.
    :param p1: Particle 3D object
    :param p2: Particle 3D object
    :return: potential energy (float)
    '''
    sep=Particle3D.vector_separation(p1,p2)
    pot=-1*p1.mass*p2.mass/sep

    return pot


def gravitational_force(p1,p2):
    '''
    Method calculating the gravitational force vector
    between 2 Particle3D objects.
    :param p1: Particle 3D object
    :param p2: Particle 3D object
    :return: force vector (Numpy array)
    '''
    sep=Particle3D.vector_separation(p1,p2)
    force=(-1*p1.mass*p2.mass)/sep**2

    force_vec=(force/sep)*(p1.position-p2.position)

    return force_vec



def update_velocity (objects, dt, force_old, force_new):
    '''
    Method updates velocity of all Particle3D objects in a list using
    the velocity Verlet method.
    :param objects: list of Particle3D objects
    :param dt: time step (float)
    :param force_old: list of previous force vectors (Numpy arrays)
    :param force_new: list of new force vectors (Numpy arrays)
    '''

    for i in range (0, len(objects)):
        objects[i].leap_velocity(dt, 0.5 * (force_old[i] + force_new[i]))


def update_position (objects, dt):
    #updates position of all objets in list

    for i in range (0, len(objects)):

        objects[i].leap_pos1st(dt)

def energy_total (objects):
    '''
    Method calculating the total energy of the system.
    Total = Potential + Kinetic
    :param objects:
    '''

    total = 0

    for i in range (0, len(objects)):
        e_kin = objects[i].kinetic_energy()

        for j in range (i+1, len(objects)):
            e_pot = energy_potential(objects[i], objects[j])


            e_tot = e_kin + e_pot
            total = total + e_tot

    return total

def com_corr (objects):

    mv = 0
    mass = 0

    for i in range (0, len(objects)):
        mv = mv + (objects[i].mass * objects[i].velocity)
        mass = mass + objects[i].mass

    v_com = mv/mass

    for i in range (0, len(objects)):
        objects[i].velocity = objects[i].velocity - v_com




def trajectory (objects, file, p_curr, p_tot):

    file.write(str(p_tot) + "\n")
    file.write("Point = " + str(p_curr) + "\n")

    for i in range (0, len(objects)):
        file.write(objects[i].__str__() + "\n")






def main():

    if len(sys.argv)!=3:
        print("Wrong number of arguments.")
        print("Usage: " + sys.argv[0] + "<input file>" + "<trajectory file>")
        quit()
    else:
        infile_name = sys.argv[1]
        outfile_name = sys.argv[2]

    infile = open(infile_name, "r")
    traj_file = open(outfile_name, "w")

    dt = 1

    list = []
    force = []

    force_sum = np.array([0, 0, 0], float)
    force_old = np.array([0, 0, 0], float)

    list.append(Particle3D.create_particle(infile))
    list.append(Particle3D.create_particle(infile))
    list.append(Particle3D.create_particle(infile))
    

    for j in range (0, len(list)):
        for k in range (0, len(list)):
            if k != j:
                force_old = force_old + gravitational_force(list[j], list[k])
        force.append(force_old)

    for i in range (0, 5):
        trajectory (list, traj_file, i+1, 5)

        update_position(list, dt)

        for j in range (0, len(list)):
            for k in range (0, len(list)):
                if k != j:
                    force_sum = force_sum + gravitational_force(list[j], list[k])

            force[j] = force_sum

        update_velocity(list, dt, force_old, force)


        force_old = force





"""
    print("G force" + str(gravitational_force(list[0], list[1])) + "\n")
    print("Position" + str(update_position(list, dt)) + "\n")
    print("energy" + str(energy_total(list)))
    print("traj" + str(trajectory(list)) + "\n")
"""
main()
