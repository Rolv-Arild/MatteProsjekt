import numpy as np
import math as ma
import time
from matplotlib import animation
import matplotlib.pyplot as plot
from matplotlib.patches import Circle
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredDrawingArea

from Rocket import Rocket
from Body import Body, G
from SolarSystem import SolarSystem
from Stage import Stage

rocket = Rocket.saturn_v(Stage(13500, 13500 + 36135, 0, 0))
rocket.theta = 2 * np.pi * 0.26538848876953125 / 360
rocket.velocity = np.array((-460.0, 0.0))

earth = Body(5.97e24, 12756e3 / 2, (0, 0), (0, 0), (0.0, 0.0, 7.292115053925690e-05))
# Some calculations to keep barycenter roughly at center
m = 5.97e24  # Earth mass
n = 0.073e24  # Moon mass
d = 4.84e8  # Earth moon distance
re = d * n / (m + n)  # Earth barycenter distance
rm = d - re  # Moon barycenter distance
vm = np.sqrt(G * (m + n) / rm)  # Moon orbital velocity around barycenter
ve = vm * n / m  # Earth orbital velocity around barycenter

moon = Body(n, 3475e3 / 2, (rm, 0.0), (0.0, vm), (0.0, 0.0, 2.6617e-06))

dt = 24 * 1. / 60
ss = SolarSystem(dt / 10.0, 1e-14)
ss.add_body(earth)
ss.add_body(rocket)
ss.add_body(moon)

# Visualization
fig = plot.figure()
axes = fig.add_subplot(111, aspect='equal', autoscale_on=True,
                       xlim=(-1e7, 1e7), ylim=(-1e7, 1e7))

time_text = axes.text(0.02, 0.95, '', transform=axes.transAxes)
height_text = axes.text(0.02, 0.90, '', transform=axes.transAxes)
velocity_text = axes.text(0.02, 0.85, '', transform=axes.transAxes)

body_count = len(ss.bodies)

earth_circle = Circle(earth.coord, earth.radius, color='b', transform=axes.transData)
moon_circle = Circle(moon.coord, moon.radius, color='tab:gray', transform=axes.transData)


rocket_plot = axes.plot([], [], 'tab:gray', marker=(3, 0, np.rad2deg(np.math.atan2(rocket.facing[1], rocket.facing[0])) - 90), lw=2)[0]
com = axes.plot([], [], 'o-r', lw=2)[0]


def init():
    """initialize animation"""
    axes.add_patch(earth_circle)
    axes.add_patch(moon_circle)

    rocket_plot.set_data([], [])
    com.set_data([], [])
    time_text.set_text('')
    height_text.set_text('')
    velocity_text.set_text('')
    return earth_circle, rocket_plot, time_text, height_text, velocity_text, moon_circle


def animate(i):
    """perform animation step"""
    ss.step(dt)
    earth_circle.center = earth.coord
    moon_circle.center = moon.coord

    rocket_plot.set_marker((3, 0, np.rad2deg(np.math.atan2(rocket.facing[1], rocket.facing[0])) - 90))
    rocket_plot.set_data(*rocket.coord)
    velocity_text.set_text('velocity = %.1f' % rocket.absolute_velocity())
    height_text.set_text('height = %.1f' % rocket.height(rocket.coord, earth))
    time_text.set_text('time = %.1f' % rocket.t)
    return earth_circle, rocket_plot, time_text, height_text, velocity_text, moon_circle


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
