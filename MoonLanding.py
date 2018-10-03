import time

import numpy as np
from matplotlib import animation
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle

from Body import Body, G
from Rocket import Rocket
from SolarSystem import SolarSystem
import matplotlib.pyplot as plot

from Stage import Stage

dt = 24 * 60 * 1. / 60

ss = SolarSystem(dt / 10.0, 1e-10)

# Some calculations to keep barycenter roughly at center
m = 5.97e24  # Earth mass
n = 0.073e24  # Moon mass
d = 4.84e8  # Earth moon distance
re = d * n / (m + n)  # Earth barycenter distance
rm = d - re  # Moon barycenter distance
vm = np.sqrt(G * (m + n) / rm)  # Moon orbital velocity around barycenter
ve = vm * n / m  # Earth orbital velocity around barycenter

moon = Body(n, 3475e3 / 2, (rm, 0.0), (0.0, vm), (0.0, 0.0, 2.6617e-06))
earth = Body(m, 12756e3 / 2, (-re, 0.0), (0.0, -ve), (0.0, 0.0, 7.29212e-05))

burn_angle = 2 * np.pi * 223 / 360  # 223 for free return trajectory, 221 for closer flybly, 220 for crash into moon

rocket = Rocket(1.95, (earth.coord[0] + np.cos(burn_angle) * (earth.radius + 300e3),
                       earth.coord[1] + np.sin(burn_angle) * (earth.radius + 300e3)),
                (earth.velocity[0] + np.cos(burn_angle + np.pi/2) * 7.731e3,
                 earth.velocity[1] + np.sin(burn_angle + np.pi/2) * 7.731e3),
                0.0011577, (np.cos(burn_angle + np.pi/2), np.sin(burn_angle + np.pi/2)))
rocket.add_stage(Stage(11900, 28800, 100, 250000))

# Earth moon
ss.add_body(moon)  # The Moon
ss.add_body(earth)  # The Earth
ss.add_body(rocket)

# Visualization
fig = plot.figure()
axes = fig.add_subplot(111, aspect='equal', autoscale_on=True,
                       xlim=(-6e8, 6e8), ylim=(-6e8, 6e8))

body_count = len(ss.bodies)

moon_circle = Circle(moon.coord, moon.radius, color='tab:gray', transform=axes.transData)
earth_circle = Circle(earth.coord, earth.radius, color='b', transform=axes.transData)
rocket_plot = \
    axes.plot([], [], 'tab:gray', marker=(3, 0, np.rad2deg(np.math.atan2(rocket.facing[1], rocket.facing[0])) - 90),
              lw=2)[0]

time_text = axes.text(0.02, 0.95, '', transform=axes.transAxes)
height_text = axes.text(0.02, 0.90, '', transform=axes.transAxes)
velocity_text = axes.text(0.02, 0.85, '', transform=axes.transAxes)


def init():
    """initialize animation"""
    axes.add_patch(earth_circle)
    axes.add_patch(moon_circle)
    rocket_plot.set_data([], [])

    velocity_text.set_text('')
    height_text.set_text('')
    time_text.set_text('')

    return earth_circle, moon_circle, rocket_plot, velocity_text, height_text, time_text


def animate(i):
    """perform animation step"""
    for _ in range(10):
        ss.step(dt)
    earth_circle.center = earth.coord
    moon_circle.center = moon.coord
    rocket_plot.set_marker((3, 0, np.rad2deg(np.math.atan2(rocket.facing[1], rocket.facing[0])) - 90))
    rocket_plot.set_data(*rocket.coord)

    velocity_text.set_text('velocity = %.1f' % rocket.absolute_velocity())
    height_text.set_text('height = %.1f' % rocket.height(rocket.coord, earth))
    time_text.set_text('time = %.1f' % rocket.t)

    return earth_circle, moon_circle, rocket_plot, velocity_text, height_text, time_text


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
