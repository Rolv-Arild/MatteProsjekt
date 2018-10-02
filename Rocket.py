import numpy as np

import Body
import Stage


class Rocket(Body.Body):
    stages: list

    def __init__(self, mass: float, radius: float, coord: tuple, velocity: tuple, angular_velocity: tuple = None):
        super().__init__(mass, radius, coord, velocity, angular_velocity)
        self.stages = []
        self.mass = 0.0

    def add_stage(self, stage: Stage):
        self.stages.append(stage)
        self.mass += stage.gross_mass()

    def skyvekraft(self, t):
        for stage in self.stages:
            if t < stage.duration:
                return stage.thrust
            t -= stage.duration
        return 0.0

    def deltamass(self, t):
        for stage in self.stages:
            if t < stage.duration:
                return stage.fuel_mass / stage.duration
            t -= stage.duration
        return 0.0

    def eksosfart(self, t):
        return self.skyvekraft(t) / self.deltamass(t)

    def air_resistance(self, body, velocity):
        areal = np.pi * 5.05 ** 2
        CD = 0.5
        ph, th = 0, 0
        h = np.abs(self.dist(body) - body.radius)
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

        trykk = (ph / th) * 3.4855
        F = -0.5 * CD * trykk * areal * vel * self.velocity

        # print("Air resistance: %s, height: %s, velocity: %s, absolute vel: %s" % (F, h, self.velocity, vel))
        print("Height:", h)
        return F

    def acceleration(self, body, coord=None, vel=None):
        if vel is None:
            vel = self.velocity
        mass = self.rocket_mass(self.t)
        body_acc = super().acceleration(body, coord)
        rocket_acc = (self.skyvekraft(self.t)) / mass
        air_resistance_acc = self.air_resistance(body, vel) / mass

        print("Mass:", mass, " Time:", self.t)

        # print("Time: %s, Rocket acc: %s, body acc: %s, air res acc: %s" % (self.t, rocket_acc, body_acc, air_resistance_acc))
        return np.array([0, rocket_acc]) + body_acc + air_resistance_acc

    def rocket_mass(self, t):
        mass = 0
        for stage in self.stages:
            if t < stage.duration:
                mass += stage.mass(t)
            t -= stage.duration
        if mass == 0:
            return self.stages[-1].empty_mass
        return mass
