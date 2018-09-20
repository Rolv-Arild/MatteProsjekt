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


dt = 1. / 60

ss = SolarSystem(dt/100, 5e-15)

# Sun earth moon
# ss.add_body(Body(1988500e24, 695700e3, (0, 0), (0, 0)))  # The Sun
# ss.add_body(Body(5.97e24, 12756e3 / 2, (149.6e9, 0), (0, 29.8e3)))  # The Earth
# ss.add_body(Body(0.073e24, 3475e3 / 2, (149.6e9, 0.384e9), (0, 29.8e3, -1.0e3)))  # The Moon

# Figure 8
ss.add_body(Body(1, 1, (-0.970, 0.243), (-0.466, -0.433)))
ss.add_body(Body(1, 1, (0.970, -0.243), (-0.466, -0.433)))
ss.add_body(Body(1, 1, (0, 0), (2*0.466, 2*0.433)))

# Earth moon
# ss.add_body(Body(5.97e24, 12756e3 / 2, (0, 0), (0, 0)))  # The Earth
# ss.add_body(Body(0.073e24, 3475e3 / 2, (0.384e9, 0), (0, 1.0e3)))  # The Moon

# Visualization
fig = plot.figure()
axes = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                       xlim=(-3, 3), ylim=(-3, 3))

body_count = len(ss.bodies)
lines = [axes.plot([], [], 'o-b', lw=2)[0] for i in range(body_count)]


def init():
    """initialize animation"""
    for l in lines:
        l.set_data([], [])
    return lines


def animate(i):
    """perform animation step"""
    ss.step(dt)
    for l in range(body_count):
        lines[l].set_data(*ss.bodies[l].coord)

    return lines


# choose the interval based on dt and the time to animate one step
# Take the time for one call of the animate.
t0 = time.time()
animate(0)
t1 = time.time()

delay = 10 * dt - (t1 - t0)

anim = animation.FuncAnimation(fig,  # figure to plot in
                               animate,  # function that is called on each frame
                               frames=30000,  # total number of frames
                               interval=delay,  # time to wait between each frame.
                               repeat=False,
                               blit=True,
                               init_func=init  # initialization
                               )
plot.show()
