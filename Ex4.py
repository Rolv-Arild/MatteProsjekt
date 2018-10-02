from Rocket import Rocket
from Stage import Stage

if __name__ == "__main__":
    rocket = Rocket(0.0, 0.0, (0.0, 0.0), (0.0, 0.0))
    rocket.add_stage(Stage(130000, 99000, 168, 35100000))
    rocket.add_stage(Stage(40100, 456100, 360, 5141000))
    rocket.add_stage(Stage(13500, 109500, 165 + 335, 1000000))

    for i in range(0, 168 + 360 + 165 + 335):
        if i % 10 == 0:
            print(i, ":", rocket.eksosfart(i))
