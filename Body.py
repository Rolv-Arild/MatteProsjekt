import numpy as np
from numpy.core.multiarray import ndarray

G = 6.67e-11  # m^3 / kg s^2


class Body:
    mass: float
    radius: float
    coord: ndarray
    velocity: ndarray
    angular_velocity: ndarray

    def __init__(self, mass: float, radius: float, coord: tuple, velocity: tuple, angular_velocity: tuple = (0, 0, 0)):
        """
        :param mass: mass in kilograms
        :param radius: radius in meters, all bodies are approximated as solid spheres
        :param coord: a tuple containing the x, y (and z) coordinates
        :param velocity: a tuple containing the x, y (and z) velocity components in m/s
        :param angular_velocity: a tuple containing the angular velocity in rad/sec.
                                 Is set to (0, 0, 0) if the planet does not rotate
        """
        self.mass = mass
        self.radius = radius
        self.coord = np.array(coord)
        self.velocity = np.array(velocity)
        self.angular_velocity = np.ndarray(angular_velocity)

    def total_velocity(self) -> float:
        return np.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2 + self.velocity[2] ** 2)

    def x(self) -> float:
        return self.coord[0]

    def y(self) -> float:
        return self.coord[1]

    def z(self) -> float:
        return self.coord[2]

    def dist(self, body) -> float:
        return np.linalg.norm(body.coord - self.coord)

    def acceleration(self, body) -> ndarray:
        a = G * body.mass / self.dist(body) ** 3
        dists = self.coord - body.coord
        return a * dists

    def F(self, body) -> ndarray:
        return self.acceleration(body) * self.mass

    def circumference(self) -> float:
        return 2 * np.pi * self.radius

    def area(self) -> float:
        return 2 * self.circumference() * self.radius

    def volume(self) -> float:
        return self.area() * self.radius / 3

    def escape_velocity(self, r: float = radius) -> float:
        # default value is escape velocity at surface
        return np.sqrt(2 * G * self.mass / r)
