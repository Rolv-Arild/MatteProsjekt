import numpy as np
import math as ma
import Body


class Rocket(Body.Body):

    def __init__(self, mass: float, radius: float, coord: tuple, velocity: tuple, angular_velocity: tuple = None):
        super().__init__(mass, radius, coord, velocity, angular_velocity)
        self.stage1_duration = 168
        self.stage1_gross_mass = 2290000
        self.stage1_empty_mass = 130000
        self.stage1_thrust = 35100000

        self.stage2_duration = 360
        self.stage2_gross_mass = 496200
        self.stage2_empty_mass = 40100
        self.stage2_thrust = 5141000

        self.stage3_duration = 165 + 335
        self.stage3_gross_mass = 123000
        self.stage3_empty_mass = 13500
        self.stage3_thrust = 1000000

    def skyvekraft(self, t):
        stage1_duration = 168
        stage2_duration = 360
        stage3_duration = 165 + 335

        if t < stage1_duration:
            return self.stage1_thrust
        elif t < stage1_duration + stage2_duration:
            return self.stage2_thrust
        elif t < stage1_duration + stage2_duration + stage3_duration:
            return self.stage3_thrust
        else:
            return 0

    def deltamass(self, t):
        if t < self.stage1_duration:
            return (self.stage1_gross_mass - self.stage1_empty_mass) / self.stage1_duration
        elif t < self.stage1_duration + self.stage2_duration:
            return (self.stage2_gross_mass - self.stage2_empty_mass) / self.stage2_duration
        elif t < self.stage1_duration + self.stage2_duration + self.stage3_duration:
            return (self.stage3_gross_mass - self.stage3_empty_mass) / self.stage3_duration

    def eksosfart(self, t):
        return self.skyvekraft(t) / self.deltamass(t)

    def luft_motstand(self, h):
        jordradius = 12756e3 / 2
        fart = self.velocity
        areal = np.pi * 5.05 ** 2
        CD = 0.5
        ph, th = 0, 0

        if h >= jordradius and h < jordradius + 11000:
            th = 288.19 - 0.00649 * h
            ph = 101290 * (th/288.08)**5.256
        elif h > jordradius + 11000:
            th = 216.69
            ph = 127760 * np.e**(-0.000157*h)
        elif h > jordradius + 25000 :
            th = 141.94 + 0.00299 * h
            ph = 2488 * (th/216.6)**-11.388

        #print(th,ph)
        trykk = (ph / th) * 3.4855
        F = 0.5 * CD * trykk * areal * fart**2

        return F

    def acceleration(self, body, coord=None):
        body_acc = body.acceleration(self)
        t = body.t/1440
        rocket_acc = (self.skyvekraft(t)) / self.rocket_mass(t)
        #print(np.sqrt(self.coord[0]**2 + self.coord[1]**2))
        #print(self.luft_motstand(np.sqrt(self.coord[0]**2 + self.coord[1]**2)))

        return [0, rocket_acc] + body_acc

    def rocket_mass(self, t):
        if t < self.stage1_duration:
            return self.stage3_gross_mass + self.stage2_gross_mass + ((
                                                                                  self.stage1_gross_mass - self.stage1_empty_mass) / self.stage1_duration) * t + self.stage1_empty_mass
        elif t < self.stage1_duration + self.stage2_duration:
            return self.stage3_gross_mass + ((
                                                         self.stage2_gross_mass - self.stage2_empty_mass) / self.stage2_duration) * t + self.stage2_empty_mass
        elif t < self.stage1_duration + self.stage2_duration + self.stage3_duration:
            return ((
                                self.stage3_gross_mass - self.stage3_empty_mass) / self.stage3_duration) * t + self.stage3_empty_mass
        else:
            return self.stage3_empty_mass


if __name__ == "__main__":
    rocket = Rocket(0.0, 0.0, (0.0, 0.0), (0.0, 0.0))

    for i in range(0, 168 + 360 + 165 + 335):
        if i % 10 == 0:
            print(i, ":", rocket.eksosfart(i))
