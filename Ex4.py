import numpy as np
import math as ma


class Rocket:

    def __init__(self):
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

    def mass(self, t):
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


rocket = Rocket()

for i in range(0, 168 + 360 + 165 + 335):
    if i % 10 == 0:
        print(i, ":", rocket.eksosfart(i))
