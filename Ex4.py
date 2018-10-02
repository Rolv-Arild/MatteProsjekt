from Rocket import Rocket

if __name__ == "__main__":
    rocket = Rocket(0.0, 0.0, (0.0, 0.0), (0.0, 0.0))

    for i in range(0, 168 + 360 + 165 + 335):
        if i % 10 == 0:
            print(i, ":", rocket.eksosfart(i))
