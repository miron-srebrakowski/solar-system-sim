import numpy as np
import math

class Particle3D(object) :

    def __init__(self, name, pos, vel, mass) :
        """
        Initialises a Particle3D instance

        :param name: label of particle as string
        :param pos: position as numpy array
        :param vel: velocity as numpy array
        :param mass: mass as float
        """

        self.label = name
        self.position = np.array([pos[0], pos[1], pos[2]], float)
        self.velocity = np.array([vel[0], vel[1], vel[2]], float)
        self.mass = mass

    def __str__(self) :
        """
        Define output format.
        For particle p(1,2,3) this will print as
        "<p><1><2><3>"
        """
        return  str(self.label) + " " + str(self.position[0]) + " " + str(self.position[1]) + " " + str(self.position[2])

    def kinetic_energy(self) :
        """
        Return kinetic energy as
        1/2*mass*mod.vel^2
        """
        return 0.5*self.mass*(np.linalg.norm(self.velocity))**2

    def leap_velocity(self, dt, force) :
        """
        First-order velocity update,
        v(t+dt) = v(t) + dt*F(t)

        :param dt: timestep as float
        :param force: force on particle as numpy array
        """
        self.velocity = self.velocity*dt*force/self.mass

    def leap_pos1st(self, dt) :
        """
        First-order position update,
        x(t+dt) = x(t) + dt*v(t)

        :param dt: timestep as float
        """
        self.position = self.position + dt*self.velocity

    def leap_pos2nd(self, dt, force) :
        """
        Second-order position update,
        x(t+dt) = x(t) + dt*v(t) + 1/2*dt^2*F(t)

        :param dt: timestep as float
        :param force: current force as float
        """
        self.position = self.position + dt*self.velocity + (dt**2)*force/(2*self.mass)

    @staticmethod
    def create_particle(file_handle) :
        line = file_handle.readline()
        linesplit = line.split(" ")

        mass = float(linesplit[0])
        name = str(linesplit[1])
        x = float(linesplit[2])
        y = float(linesplit[3])
        z = float(linesplit[4])
        vx = float(linesplit[5])
        vy = float(linesplit[6])
        vz = float(linesplit[7])

        position = np.array([x, y, z], float)
        velocity = np.array([vx, vy, vz], float)

        particle = Particle3D(name, position, velocity, mass)
        return particle

    @staticmethod
    def vector_separation(particle1, particle2) :
        return np.linalg.norm(particle1.position - particle2.position)
