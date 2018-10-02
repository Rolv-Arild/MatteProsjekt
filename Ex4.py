from Rocket import Rocket
from Stage import Stage

if __name__ == "__main__":
    rocket = Rocket.saturn_v()

    for i in range(0, 168 + 360 + 165 + 335):
        if i % 10 == 0:
            print(i, ":", rocket.exhaust_velocity(i))
