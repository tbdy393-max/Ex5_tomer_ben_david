class Body:
    def __init__(self, mass, heat_capacity, temperature):
        if mass <= 0:
            print("Mass must be greater than 0, using 1 kg")
            mass = 1
        if heat_capacity <= 0:
            print("Heat capacity must be greater than 0, using 1 J/kg°C")
            heat_capacity = 1
        if temperature < 0:
            print("Temperature can't be below 0, using 0 °C")
            temperature = 0
        self.mass = mass
        self.heat_capacity = heat_capacity
        self.temperature = temperature

    def add_heat(self, heat):
        delta_temperature = heat / (self.mass * self.heat_capacity)
        self.temperature += delta_temperature
        return self.temperature


if __name__ == '__main__':
    body = Body(100, 0.15, 200)
    print(body.add_heat(20))
    print(body.add_heat(-40))
