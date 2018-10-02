class Stage:
    empty_mass: float
    gross_mass: float
    duration: float
    thrust: float

    def __init__(self, empty_mass, gross_mass, duration, thrust):
        self.empty_mass = empty_mass
        self.gross_mass = gross_mass
        self.duration = duration
        self.thrust = thrust

    def fuel_mass(self) -> float:
        return self.gross_mass - self.empty_mass

    def mass(self, t):
        if t < 0:
            return self.gross_mass
        if 0 <= t <= self.duration:
            return self.empty_mass + (self.duration - t) * self.fuel_mass() / self.duration
        else:
            return self.empty_mass
