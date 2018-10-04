import numpy as np

from Body import Body
from Rocket import Rocket
from SolarSystem import SolarSystem
from Stage import Stage

A = 0
B = 90
eps = 0.0001
dt = 24 * 1. / 60
tol = 1e-14


def test_system(theta: float) -> int:
    earth = Body(5.97e24, 12756e3 / 2, (0, 0), (0, 0), (0.0, 0.0, 7.292115053925690e-05))

    rocket = Rocket.saturn_v(Stage(13500, 13500 + 36135, 0, 0))
    rocket.theta = 2 * np.pi * theta / 360
    rocket.velocity = np.array((-earth.speed_at_surface(), 0.0))

    ss = SolarSystem(dt / 10.0, 1e-14)
    ss.add_body(earth)
    ss.add_body(rocket)

    while True:
        try:
            ss.step(dt)
            if rocket.t >= 25000:
                return 0  # orbit
        except ValueError:  # crash into earth
            # probably not the best metric to use, but simple and it works pretty well
            if rocket.t < 3000:
                return -1
            else:
                return 1


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
