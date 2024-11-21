from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import random

from agent import Car


# Define the parking model
class ParkingLotModel(Model):
    def __init__(self, height, width, common_spots, electric_spots=0, premium_spots=0,
                 electric_chance=0, premium_chance=0, starting_cars=0):
        super().__init__()  # Explicitly initialize the base Model class
        self.datacollector = None
        self.num_agents = starting_cars
        self.grid = MultiGrid(width, height + 1, torus=False)
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
                
        self.queue = []
        self.car_id = 0
        self.num_spots = 0
            

    def place_car_random_empty_spot(self, car):
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        self.grid.place_agent(car, (x, y))

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
            
    def count_parked_cars(self):
        return sum([1 for a in self.schedule.agents if isinstance(a, Car) and a.parked])           

    def step(self):
        self.add_car_to_queue()
        
        # Place cars in queue grid
        for x, car in enumerate(self.queue[:self.grid.width]):
            self.grid.place_agent(car, (x, self.grid.height - 1))  # Place car in queue grid cell
        self.schedule.step()
        
    def add_car_to_queue(self):
        car_type = random.choice(["Normal", "Electric", "Premium"])
        car = Car(self.car_id, self, car_type)
        self.queue.append(car)
        self.car_id += 1
        
    def find_spot(self):
        return
        