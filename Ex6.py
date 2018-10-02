import numpy as np
import math as ma
import time
from matplotlib import animation
import matplotlib.pyplot as plot
from Rocket import Rocket
from Body import Body
from SolarSystem import SolarSystem

rocket = Rocket(0, 0, (0, 12756e3 / 2 + 10), (0, 0), None)
rocket.set_mass(rocket.rocket_mass(0))

dt = 24 * 1. / 60
ss = SolarSystem(dt / 10.0, 1e-10)
ss.add_body(Body(5.97e24, 12756e3 / 2, (0, 0),
                 (0, 0), (0.0, 0.0, 7.292115053925690e-05)))  # The Earth
ss.add_body(rocket)

# Visualization
fig = plot.figure()
axes = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                       xlim=(-16e8, 16e8), ylim=(-16e8, 16e8))

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
    rock = ss.bodies[1]
    for l in range(body_count):
        lines[l].set_data(*ss.bodies[l].coord)
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
