from Particle3D import Particle3D
import math
import numpy as np
import sys


def energy_potential(p1,p2):
    #method to calculate the potenital energy
    sep=Particle3D.vector_separation(p1,p2)
    pot=-1*p1.mass*p2.mass/sep
    return pot

def gravitational_force(p1,p2):
    #method to calculate the force vector
    sep=Particle3D.vector_separation(p1,p2)
    force=(-1*p1.mass*p2.mass)/sep**2

    force_vec=(force/sep)*(p1.position-p2.position)
    return force_vec



def update_velocity (objects, dt, force_old, force_new):

    for i in range (0, len(objects)):
        objects[i].leap_velocity(dt, 0.5 * (force_old[i] + force_new[i]))


def update_position (objects, dt):

    for i in range (0, len(objects)):

        objects[i].leap_pos1st(dt)

def energy_total (objects):

    total = 0

    for i in range (0, len(objects)):
        e_kin = objects[i].kinetic_energy()

        for j in range (i+1, len(objects)):
            e_pot = energy_potential(objects[i], objects[j])


            e_tot = e_kin + e_pot
            total = total + e_tot

    return total


def main():

    if len(sys.argv)!=2:
        print("Wrong number of arguments.")
        print("Usage: " + sys.argv[0] + "<input file>")
        quit()
    else:
        infile_name = sys.argv[1]

    infile = open(infile_name, "r")

    dt = 1

    list = []

    list.append(Particle3D.create_particle(infile))
    list.append(Particle3D.create_particle(infile))
    list.append(Particle3D.create_particle(infile))

    print("G force" + str(gravitational_force(list[0], list[1])) + "\n")
    print("Position" + str(update_position(list, dt)) + "\n")
    print("energy" + str(energy_total(list)))

main()
