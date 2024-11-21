from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agent import Car


# Define the parking model
class ParkingLotModel(Model):
    def __init__(self, height, width, common_spots, electric_spots=0, premium_spots=0,
                 electric_chance=0, premium_chance=0, starting_cars=0):
        super().__init__()  # Explicitly initialize the base Model class
        self.datacollector = None
        self.num_agents = starting_cars
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)

        self.common_spots = common_spots
        self.electric_spots = electric_spots
        self.premium_spots = premium_spots

        self.number_electric = electric_chance
        self.number_premium = premium_chance
        if starting_cars != 0:
            self.create_normal_cars()
            if electric_chance != 0:
                self.create_electric_cars()

            if premium_chance != 0:
                self.create_premium_cars()

    def place_car_random_empty_spot(self, car):
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        self.grid.place_agent(car, (x, y))
        self.datacollector = DataCollector(
            {"Parked Cars": lambda m: self.count_parked_cars()}
        )

    def create_normal_cars(self):
        for i in range(int(self.num_agents * (1 - self.number_electric - self.number_premium))):
            car = Car(i, self, "Normal")
            self.schedule.add(car)
            self.place_car_random_empty_spot(car)

    def create_electric_cars(self):
        for i in range(int(self.num_agents * self.number_electric)):
            car = Car(i, self, "Electric")
            self.schedule.add(car)
            self.place_car_random_empty_spot(car)

    def create_premium_cars(self):
        for i in range(int(self.num_agents * self.number_premium)):
            car = Car(i, self, "Premium")
            self.schedule.add(car)
            self.place_car_random_empty_spot(car)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def count_parked_cars(self):
        return sum([1 for a in self.schedule.agents if isinstance(a, Car) and a.parked])
