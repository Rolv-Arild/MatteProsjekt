import numpy as np

from Body import Body
from Rocket import Rocket
from SolarSystem import SolarSystem

A = 0
B = 90
eps = 0.0001
dt = 24 * 1. / 60
tol = 1e-14


def test_system(theta: float) -> int:
    rocket = Rocket.saturn_v()
    rocket.theta = 2 * np.pi * theta / 360
    earth = Body(5.97e24, 12756e3 / 2, (0, 0), (0, 0), (0.0, 0.0, 7.292115053925690e-05))
    ss = SolarSystem(dt / 10.0, tol)
    ss.add_body(earth)
    ss.add_body(rocket)

    t = 0
    while rocket.dist(earth) < earth.radius * 5:
        try:
            ss.step(dt)
            t += dt
            if t >= 56540:
                return 0  # orbit
        except ZeroDivisionError:
            return -1  # crash into earth
    return 1  # escape from earth


assert test_system(A) > 0
assert test_system(B) < 0

cont = True
while cont:
    angle = (A + B) / 2
    res = test_system(angle)
    if res == 0:
        print(angle)
        cont = False
    elif res > 0:
        A = angle
        print("A:", A)
    elif res < 0:
        B = angle
        print("B:", B)
