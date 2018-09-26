import numpy as np
import math as ma
import time
from matplotlib import animation
import matplotlib.pyplot as plot
from Ex4 import Rocket
from Body import Body

rocket = Rocket(0, 0, (12756e3/2, 0), (0, 0), None)
rocket.set_mass(rocket.rocket_mass(0))


class LiftOff:
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


dt = 24 * 60 * 60 * 1. / 60
lo = LiftOff(dt / 10.0, 1e-10)
lo.add_body(Body(5.97e24, 12756e3 / 2, (1.601622423200423E+06, 1.471196461264217E+08),
                 (-3.028433032337041E+01, 8.741108700584631E-02), (0.0, 0.0, 7.292115053925690e-05)))  # The Earth
lo.add_body(rocket)

# Visualization
fig = plot.figure()
axes = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                       xlim=(-16e8, 16e8), ylim=(-16e8, 16e8))

body_count = len(lo.bodies)
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
    lo.step(dt)
    for l in range(body_count):
        lines[l].set_data(*lo.bodies[l].coord)
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