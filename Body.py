import functools

import numpy as np
from numpy.core.multiarray import ndarray

from RungeKuttaFehlberg import RungeKuttaFehlberg54

G = 6.67408e-11  # m^3 / kg s^2


class Body:
    mass: float
    radius: float
    coord: ndarray
    velocity: ndarray
    angular_velocity: ndarray

    def __init__(self, mass: float, radius: float, coord: tuple, velocity: tuple, angular_velocity: tuple = None):
        """
        :param mass: mass in kilograms
        :param radius: radius in meters, all bodies are approximated as solid spheres
        :param coord: a tuple containing the x, y (and z) coordinates
        :param velocity: a tuple containing the x, y (and z) velocity components in m/s
        :param angular_velocity: a tuple containing the angular velocity in rad/sec.
                                 Is set to (0, 0, 0) if the planet does not rotate
        """
        self.t = 0
        self.mass = mass
        self.radius = radius
        self.coord = np.array(coord, dtype='float64')
        self.velocity = np.array(velocity, dtype='float64')
        if angular_velocity is None:
            self.angular_velocity = np.zeros([len(coord)], dtype='float64')
        else:
            self.angular_velocity = np.array(angular_velocity, dtype='float64')

    def set_mass(self, mass):
        self.mass = mass

    def absolute_velocity(self) -> float:
        return np.linalg.norm(self.velocity)

    def x(self) -> float:
        return self.coord[0]

    def y(self) -> float:
        return self.coord[1]

    def z(self) -> float:
        return self.coord[2]

    def dist(self, body) -> float:
        return np.linalg.norm(body.coord - self.coord)

    def acceleration(self, body, coord=None) -> ndarray:
        if coord is None:
            coord = self.coord
        dists = body.coord - coord
        a = G * body.mass / (np.linalg.norm(dists) ** 3)
        return a * dists

    def F(self, body) -> ndarray:
        return self.acceleration(body) * self.mass

    def circumference(self) -> float:
        return 2 * np.pi * self.radius

    def area(self) -> float:
        return 2 * self.circumference() * self.radius

    def volume(self) -> float:
        return self.area() * self.radius / 3

    def orbital_velocity(self, r: float):  # Speed required to orbit at certain radius from the center
        return np.sqrt(G * self.mass / r)

    def escape_velocity(self, r: float = None) -> float:
        # default value is escape velocity at surface
        if r is None:
            r = self.radius
        return np.sqrt(2 * G * self.mass / r)

    def speed_at_surface(self) -> float:
        return np.linalg.norm(self.angular_velocity)

    def step(self, t, h, tol, bodies: list) -> None:
        W = self.state()
        rkf54 = RungeKuttaFehlberg54(functools.partial(self.y_dot, bodies=bodies), len(W), h, tol)

        while W[0] < t + self.t:
            W, E = rkf54.safe_step(W)

        rkf54.set_step_length(t + self.t - W[0])
        W, E = rkf54.step(W)
        self.set_state(W)

    def state(self):
        list = [self.t]
        for i in range(len(self.coord)):
            list.append(self.coord[i])
            list.append(self.velocity[i])
        return np.array(list)

    def y_dot(self, x, bodies) -> ndarray:
        dim = len(self.coord)
        coord = np.array([x[2 * i + 1] for i in range(dim)])
        vel = np.array([x[2 * i + 2] for i in range(dim)])
        z = np.zeros(1 + dim * 2)
        z[0] = 1
        for i in range(dim):
            z[2 * i + 1] = vel[i]
            z[2 * i + 2] = sum([self.acceleration(b, coord)[i] for b in bodies])

        return z

    def set_state(self, W):
        self.t = W[0]
        for i in range(len(self.coord)):
            self.coord[i] = W[2 * i + 1]
            self.velocity[i] = W[2 * i + 2]
