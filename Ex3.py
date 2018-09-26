import time

import numpy as np
from matplotlib import animation
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle

from Body import Body, G
from SolarSystem import SolarSystem
import matplotlib.pyplot as plot

dt = 24 * 60 * 60 * 1. / 60

ss = SolarSystem(dt / 10.0, 1e-10)

# Some calculations to keep barycenter roughly at center
m = 5.97e24  # Earth mass
n = 0.073e24  # Moon mass
d = 4.84e8  # Earth moon distance
re = d * n / (m + n)  # Earth barycenter distance
rm = d - re  # Moon barycenter distance
vm = np.sqrt(G * (m + n) / rm)  # Moon orbital velocity around barycenter
ve = vm * n / m  # Earth orbital velocity around barycenter

# Earth moon
ss.add_body(
    Body(n, 3475e3 / 2, (rm, 0.0), (0.0, vm),
         (0.0, 0.0, 2.6617e-06)))  # The Moon
ss.add_body(
    Body(m, 12756e3 / 2, (-re, 0.0), (0.0, -ve),
         (0.0, 0.0, 7.29212e-05)))  # The Earth

# Visualization
fig = plot.figure()
axes = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                       xlim=(-1e9, 1e9), ylim=(-1e9, 1e9))

body_count = len(ss.bodies)
lines = [axes.plot([], [], 'o-b', lw=i + 1)[0] for i in range(body_count)]
com = axes.plot([], [], 'o-r', lw=1)[0]


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
    print(ss.barycenter())
    return lines + [com]


# choose the interval based on dt and the time to animate one step
# Take the time for one call of the animate.
t0 = time.time()
animate(0)
t1 = time.time()

delay = 1. / (24 * 60 * 60) * dt - (t1 - t0)

anim = animation.FuncAnimation(fig,  # figure to plot in
                               animate,  # function that is called on each frame
                               frames=30000,  # total number of frames
                               interval=delay,  # time to wait between each frame.
                               repeat=False,
                               blit=True,
                               init_func=init  # initialization
                               )
plot.show()
