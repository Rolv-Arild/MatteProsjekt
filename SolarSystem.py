import time

import numpy as np
from matplotlib import animation

from Body import Body
import matplotlib.pyplot as plot

from RungeKuttaFehlberg import RungeKuttaFehlberg54


class SolarSystem:
    bodies: list

    def __init__(self, h, tol):
        self.h = h
        self.tol = tol
        self.bodies = []

    def add_body(self, body: Body) -> None:
        self.bodies.append(body)

    def step(self, t):
        for b in self.bodies:
            bodies = list(self.bodies)
            bodies.remove(b)
            b.step(t, self.h, self.tol, bodies)

    def barycenter(self):
        b = self.bodies[0]
        mass_coordinate = b.mass * b.coord
        total_mass = b.mass
        for i in range(1, len(self.bodies)):
            b = self.bodies[i]
            total_mass += b.mass
            mass_coordinate += b.mass * b.coord

        return mass_coordinate / total_mass


dt = 24 * 60 * 60 * 1. / 60

ss = SolarSystem(dt / 10.0, 1e-10)

# December 21 1968 (Apollo 8 launch):
# Sun:    X = 6.581238156405360E+05 Y =-4.158903482447704E+04 Z =-8.242031373132893E+03
#         VX= 2.495612123392373E-03 VY= 9.727975051467044E-03 VZ=-8.539948490230657E-05
# Earth:  X = 1.601622423200423E+06 Y = 1.471196461264217E+08 Z = 2.569208270668983E+03
#         VX=-3.028433032337041E+01 VY= 8.741108700584631E-02 VZ=-4.136855940269427E-04
# Moon:   X = 1.707846768008920E+06 Y = 1.467782024215504E+08 Z =-2.813669182258844E+04
#         VX=-2.922740436493338E+01 VY= 3.794473047545215E-01 VZ= 1.545660220090553E-02
# source: https://ssd.jpl.nasa.gov/horizons.cgi

ss.add_body(Body(1988500e24, 695700e3, (6.581238156405360E+05, -4.158903482447704E+04),
                 (2.495612123392373E-03, 9.727975051467044E-03), (0.0, 0.0, 2.865329607243705e-06)))  # The Sun
ss.add_body(Body(5.97e24, 12756e3 / 2, (1.601622423200423E+06, 1.471196461264217E+08),
                 (-3.028433032337041E+01, 8.741108700584631E-02), (0.0, 0.0, 7.292115053925690e-05)))  # The Earth
ss.add_body(Body(0.073e24, 3475e3 / 2, (1.707846768008920E+06, 1.467782024215504E+08),
                 (-2.922740436493338E+01, 3.794473047545215E-01), (0.0, 0.0, 2.661699538941653e-06)))  # The Moon

# Figure 8
# ss.add_body(Body(1, 1, (-0.970, 0.243), (-0.466, -0.433)))
# ss.add_body(Body(1, 1, (0.970, -0.243), (-0.466, -0.433)))
# ss.add_body(Body(1, 1, (0.0, 0.0), (2 * 0.466, 2 * 0.433)))

# Earth moon
# ss.add_body(Body(5.97e24, 12756e3 / 2, (0.0, 0.0), (0.0, 0.0), (0.0, 0.0, 7.292115053925690e-05)))  # The Earth
# ss.add_body(Body(0.073e24, 3475e3 / 2, (0.384e9, 0.0), (0.0, 1.0e3), (0.0, 0.0, 2.661699538941653e-06)))  # The Moon

# Visualization
fig = plot.figure()
axes = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                       xlim=(-160e9, 160e9), ylim=(-160e9, 160e9))

body_count = len(ss.bodies)
lines = [axes.plot([], [], 'o-b', lw=2)[0] for i in range(body_count)]
com = axes.plot([], [], 'o-r', lw=2)[0]


def init():
    """initialize animation"""
    for l in lines:
        l.set_data([], [])
    com.set_data([], [])
    return lines + [com]


def animate(i):
    """perform animation step"""
    ss.step(dt)
    for l in range(body_count):
        lines[l].set_data(*ss.bodies[l].coord)
    com.set_data(*ss.barycenter())
    return lines + [com]


# choose the interval based on dt and the time to animate one step
# Take the time for one call of the animate.
t0 = time.time()
animate(0.0)
t1 = time.time()

delay = 1000 / (24 * 60 * 60) * dt - (t1 - t0)

anim = animation.FuncAnimation(fig,  # figure to plot in
                               animate,  # function that is called on each frame
                               frames=30000,  # total number of frames
                               interval=delay,  # time to wait between each frame.
                               repeat=False,
                               blit=True,
                               init_func=init  # initialization
                               )
plot.show()
