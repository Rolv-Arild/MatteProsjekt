import math

import numpy as np

import Body
import Stage


class Rocket(Body.Body):
    stages: list
    printC = 0

    def __init__(self, radius: float, coord: tuple, velocity: tuple, theta: float, facing: tuple = (0.0, 1.0),
                 angular_velocity: tuple = None):
        super().__init__(0.0, radius, coord, velocity, angular_velocity)
        self.facing = np.array(facing)
        self.stages = []
        self.theta = theta

    def add_stage(self, stage: Stage):
        self.stages.append(stage)
        self.mass += stage.gross_mass

    def thrust(self, t):
        for stage in self.stages:
            if t < stage.duration:
                return stage.thrust
            t -= stage.duration
        return 0.0

    def delta_mass(self, t):
        for stage in self.stages:
            if t < stage.duration:
                return stage.fuel_mass() / stage.duration
            t -= stage.duration
        return 0.0

    def exhaust_velocity(self, t):
        return self.thrust(t) / self.delta_mass(t)

    @staticmethod
    def height(coord, body):
        return np.linalg.norm(coord - body.coord) - body.radius

    def air_resistance(self, body, coord, velocity):
        area = np.pi * self.radius ** 2
        c_d = 0.5  # drag coefficient
        ph, th = 0, 0
        h = self.height(coord, body)
        vel = np.linalg.norm(velocity - body.velocity)

        # print(h)

        if h < 11000:
            th = 288.19 - 0.00649 * h
            ph = 101.290 * (th / 288.08) ** 5.256
        elif 11000 <= h < 25000:
            th = 216.69
            ph = 127.760 * np.e ** (-0.000157 * h)
        elif 25000 <= h:
            th = 141.94 + 0.00299 * h
            ph = 2.488 * (th / 216.6) ** -11.388

        density = (ph / th) * 3.4855
        F = -0.5 * c_d * density * area * vel * (velocity - body.velocity)

        # if self.printC % 100 == 0:
        #     print("%s, air resistance: %s, height: %s, velocity: %s, absolute vel: %s" % (
        #         self.printC, F, h, (velocity - body.velocity), vel))

        return F

    def acceleration(self, body, coord=None, vel=None):
        if vel is None:
            vel = self.velocity
        mass = self.rocket_mass(self.t)
        grav_acc = super().acceleration(body, coord)
        thrust_acc = self.thrust(self.t) / mass
        air_resistance_acc = self.air_resistance(body, coord, vel) / mass

        # if self.printC % 100 == 0:
        #     print("%s, mass: %s, time: %s, thrust acc: %s, grav acc: %s, air res acc: %s" % (
        #         self.printC, mass, self.t, thrust_acc, grav_acc, air_resistance_acc))
        # self.printC += 1

        return self.facing * thrust_acc + grav_acc + air_resistance_acc

    def step(self, t, h, tol, bodies: list):
        super().step(t, h, tol, bodies)
        c, s = np.cos(self.theta*t), np.sin(self.theta*t)
        R = np.matrix([[c, -s], [s, c]])

        self.facing = np.array(np.dot(R, self.facing).tolist()[0])

    def rocket_mass(self, t):
        mass = 0.0
        for stage in self.stages:
            if t < stage.duration:
                mass += stage.mass(t)
            t -= stage.duration
        if mass == 0.0:
            return self.stages[-1].empty_mass
        return mass

    @classmethod
    def saturn_v(cls, stage3: Stage = Stage.Stage(13500, 123000, 165 + 335, 10000000)):
        rocket = Rocket(5.05, (0, 12756e3 / 2 + 10), (0, 0), 0)
        rocket.add_stage(Stage.Stage(130000, 2290000, 168, 35100000))
        rocket.add_stage(Stage.Stage(40100, 496200, 360, 5141000))
        rocket.add_stage(stage3)
        return rocket
