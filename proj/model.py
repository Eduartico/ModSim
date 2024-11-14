from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from agent import Car

# Define the parking model
class ParkingLotModel(Model):
    def __init__(self, width, height, N):
        super().__init__()  # Explicitly initialize the base Model class
        self.num_agents = N
        self.grid = MultiGrid(width, height, torus = False)
        self.schedule = RandomActivation(self)
        
        number_electric = 0.4
        number_premium = 0.1
        
        self.create_normal_cars(number_electric, number_premium)
        self.create_electric_cars(number_electric)
        
        if number_premium != 0:
            self.create_premium_cars(number_premium)
        
    def place_car_random_empty_spot(self, car):
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        self.grid.place_agent(car, (x, y))
        self.datacollector = DataCollector(
                {"Parked Cars": lambda m: self.count_parked_cars()}
            )
        
        
    def create_normal_cars(self, number_electric, number_premium):
        for i in range(int(self.num_agents * (1-number_electric-number_premium))):
            car = Car(i, self, "Normal")
            self.schedule.add(car)
            self.place_car_random_empty_spot(car)
        
    def create_electric_cars(self, number_electric):
        for i in range(int(self.num_agents * number_electric)):
            car = Car(i, self, "Electric")
            self.schedule.add(car)
            self.place_car_random_empty_spot(car)
        
        
    def create_premium_cars(self, number_premium):
        for i in range(int(self.num_agents * number_premium)):
            car = Car(i, self, "Premium")
            self.schedule.add(car)
            self.place_car_random_empty_spot(car)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def count_parked_cars(self):
        return sum([1 for a in self.schedule.agents if isinstance(a, Car) and a.parked])
