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
        self.predictors = []
        self.bodies = []

    def add_body(self, body: Body) -> None:
        self.bodies.append(body)
        self.predictors.append(None)
        for i in range(len(self.bodies)):
            bo = self.bodies[i]
            a = np.array((0, 0, 0))
            for b in self.bodies:
                if b != bo:
                    a += bo.acceleration(b)

            def F(Y):
                res = np.zeros([7])
                res[0] = 1
                res[1] = Y[1]
                res[2] = a[0]
                res[3] = Y[3]
                res[4] = a[1]
                res[5] = Y[5]
                res[6] = a[2]
                return res
            self.predictors[i] = RungeKuttaFehlberg54(F, 7, self.h, self.tol)

    def step(self, h):
        for i in range(len(self.bodies)):
            body = self.bodies[i]
            w = np.array([1, ])



ss = SolarSystem(0.01, 5e-14)
# ss.add_body(Body(1988500e24, 695700e3, (0, 0, 0), (0, 0, 0)))  # The Sun
# ss.add_body(Body(5.97e24, 12756e3 / 2, (149.6e9, 0, 0), (0, 29.8e3, 0)))  # The Earth
# ss.add_body(Body(0.073e24, 3475e3 / 2, (149.6e9 + 0.384e9, 0, 0), (0, 29.8e3 + 1.0e3, 0)))  # The Moon

ss.add_body(Body(5.97e24, 12756e3 / 2, (0, 0, 0), (0, 0, 0)))  # The Earth
ss.add_body(Body(0.073e24, 3475e3 / 2, (0.384e9, 0, 0), (0, 1.0e3, 0)))  # The Moon

# Visualization
fig = plot.figure()
axes = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                       xlim=(-3, 3), ylim=(-3, 3))

line1, = axes.plot([], [], 'o-g', lw=2)  # A green planet
line2, = axes.plot([], [], 'o-y', lw=2)  # A yellow sun
line3, = axes.plot([], [], 'o-b', lw=2)  # A blue moon
time_text = axes.text(0.02, 0.95, '', transform=axes.transAxes)
energy_text = axes.text(0.02, 0.90, '', transform=axes.transAxes)


def init():
    """initialize animation"""
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    time_text.set_text('')
    energy_text.set_text('')
    return line1, line2, line3, time_text, energy_text


def animate(i):
    """perform animation step"""
    global b1, b2, b3, dt
    b1.step(dt)
    b2.step(dt)
    b3.step(dt)
    line1.set_data(*b1.position())
    line2.set_data(*b2.position())
    line3.set_data(*b3.position())
    time_text.set_text('time = %.1f' % b1.time_elapsed())
    return line1, line2, line3, time_text, energy_text


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
