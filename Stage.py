class Stage:
    empty_mass: float
    fuel_mass: float
    duration: float
    thrust: float

    def __init__(self, empty_mass, fuel_mass, duration, thrust):
        self.empty_mass = empty_mass
        self.fuel_mass = fuel_mass
        self.duration = duration
        self.thrust = thrust

    def gross_mass(self) -> float:
        return self.empty_mass + self.fuel_mass

    def mass(self, t):
        if t < 0:
            return self.gross_mass()
        if 0 <= t <= self.duration:
            return self.empty_mass + (self.duration - t) * self.fuel_mass / self.duration
        else:
            return self.empty_mass
