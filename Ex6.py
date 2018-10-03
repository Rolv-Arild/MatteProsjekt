import numpy as np
import math as ma
import time
from matplotlib import animation
import matplotlib.pyplot as plot
from matplotlib.patches import Circle
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredDrawingArea

from Rocket import Rocket
from Body import Body
from SolarSystem import SolarSystem
from Stage import Stage

rocket = Rocket.saturn_v()
rocket.theta = 2 * np.pi * 0.1 / 360

earth = Body(5.97e24, 12756e3 / 2, (0, 0),
             (0, 0), (0.0, 0.0, 7.292115053925690e-05))

dt = 24 * 1. / 60
ss = SolarSystem(dt / 10.0, 1e-14)
ss.add_body(earth)
ss.add_body(rocket)

# Visualization
fig = plot.figure()
axes = fig.add_subplot(111, aspect='equal', autoscale_on=True,
                       xlim=(-1e7, 1e7), ylim=(-1e7, 1e7))

body_count = len(ss.bodies)

earth_circle = Circle(earth.coord, earth.radius, color='b', transform=axes.transData)

rocket_plot = axes.plot([], [], 'tab:gray', marker=(3, 0, np.rad2deg(np.math.atan2(rocket.facing[1], rocket.facing[0])) - 90), lw=2)[0]
com = axes.plot([], [], 'o-r', lw=2)[0]


def init():
    """initialize animation"""
    axes.add_patch(earth_circle)

    rocket_plot.set_data([], [])
    com.set_data([], [])
    return earth_circle, rocket_plot


def animate(i):
    """perform animation step"""
    ss.step(dt)
    earth_circle.center = earth.coord

    rocket_plot.set_marker((3, 0, np.rad2deg(np.math.atan2(rocket.facing[1], rocket.facing[0])) - 90))
    rocket_plot.set_data(*rocket.coord)
    return earth_circle, rocket_plot


# choose the interval based on dt and the time to animate one step
# Take the time for one call of the animate.
t0 = time.time()
animate(0.0)
t1 = time.time()

delay = 1000 / (24 * 60 * 60) * dt - (t1 - t0)

anim = animation.FuncAnimation(fig,  # figure to plot in
                               animate,  # function that is called on each frame
                               frames=300000,  # total number of frames
                               interval=delay,  # time to wait between each frame.
                               repeat=False,
                               blit=True,
                               init_func=init  # initialization
                               )

plot.show()
