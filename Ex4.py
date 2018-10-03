from Rocket import Rocket
from Stage import Stage

if __name__ == "__main__":
    rocket = Rocket.saturn_v(165 + 335, 1000000)

    for i in range(0, 168 + 360 + 165 + 335):
        if i % 100 == 0:
            print("t=", i, ", skyvekraft: ", rocket.thrust(i))
        if i == 0:
            print("Totalmasse før trinn 1: ", rocket.rocket_mass(i), " kg")
        if i == 1:
            print("Hasighet til eksosgassen i trinn 1: ", rocket.exhaust_velocity(i))
        if i == 168:
            print("Totalmasse før trinn 2: ", rocket.rocket_mass(i), " kg")
        if i == 169:
            print("Hasighet til eksosgassen i trinn 2: ", rocket.exhaust_velocity(i))
        if i == 168 + 360:
            print("Totalmasse før trinn 3: ", rocket.rocket_mass(i), " kg")
        if i == 168 + 360 + 12:
            print("Hasighet til eksosgassen i trinn 3: ", rocket.exhaust_velocity(i))


