import numpy as np

import Body
import Stage


class Rocket(Body.Body):
    stages: list
    printC = 0

    def __init__(self, mass: float, radius: float, coord: tuple, velocity: tuple, angular_velocity: tuple = None):
        super().__init__(mass, radius, coord, velocity, angular_velocity)
        self.stages = []
        self.mass = 0.0

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
                return stage.fuel_mass / stage.duration
            t -= stage.duration
        return 0.0

    def exhaust_velocity(self, t):
        return self.thrust(t) / self.delta_mass(t)

    def air_resistance(self, body, coord, velocity):
        area = np.pi * 5.05 ** 2
        c_d = 0.5  # drag coefficient
        ph, th = 0, 0
        h = np.abs(np.linalg.norm(coord - body.coord) - body.radius)
        vel = np.linalg.norm(velocity - body.velocity)

        if 0 <= h < 11000:
            th = 288.19 - 0.00649 * h
            ph = 101290 * (th / 288.08) ** 5.256
        elif 11000 <= h < 25000:
            th = 216.69
            ph = 127760 * np.e ** (-0.000157 * h)
        elif 25000 <= h:
            th = 141.94 + 0.00299 * h
            ph = 2488 * (th / 216.6) ** -11.388

        density = (ph / th) * 3.4855
        F = -0.5 * c_d * density * area * vel * (velocity - body.velocity)

        if self.printC % 100 == 0:
            print("%s, air resistance: %s, height: %s, velocity: %s, absolute vel: %s" % (self.printC, F, h, (velocity - body.velocity), vel))
        return F

    def acceleration(self, body, coord=None, vel=None):
        if vel is None:
            vel = self.velocity
        mass = self.rocket_mass(self.t)
        grav_acc = super().acceleration(body, coord)
        thrust_acc = self.thrust(self.t) / mass
        air_resistance_acc = self.air_resistance(body, coord, vel) / mass

        if self.printC % 100 == 0:
            print("%s, mass: %s, time: %s, thrust acc: %s, grav acc: %s, air res acc: %s" % (self.printC, mass, self.t, thrust_acc, grav_acc, air_resistance_acc))
        self.printC += 1
        return np.array([0, thrust_acc]) + grav_acc + air_resistance_acc

    def rocket_mass(self, t):
        mass = 0.0
        for stage in self.stages:
            if t <= stage.duration:
                mass += stage.mass(t)
            t -= stage.duration
        if mass == 0.0:
            return self.stages[-1].empty_mass
        return mass

    @classmethod
    def saturn_v(cls):
        rocket = Rocket(0, 0, (0, 12756e3 / 2 + 10), (0, 0), None)
        rocket.add_stage(Stage.Stage(130000, 2290000, 168, 35100000))
        rocket.add_stage(Stage.Stage(40100, 496200, 360, 5141000))
        rocket.add_stage(Stage.Stage(13500, 123000, 165 + 335, 1000000))
        return rocket
