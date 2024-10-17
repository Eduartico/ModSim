# FUNCOES RELACIONADAS AO PARQUE
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from car import CarAgent

# Define the parking model
class ParkingLotModel(Model):
    def __init__(self, width, height, N):
        super().__init__()  # Explicitly initialize the base Model class
        self.num_agents = N
        self.grid = MultiGrid(width, height, torus = False)
        self.schedule = RandomActivation(self)
        
        # Create agents
        for i in range(self.num_agents):
            car = CarAgent(i, self)
            self.schedule.add(car)

            # Place the car in a random empty spot
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(car, (x, y))

            self.datacollector = DataCollector(
                {"Parked Cars": lambda m: self.count_parked_cars()}
            )

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def count_parked_cars(self):
        return sum([1 for a in self.schedule.agents if isinstance(a, CarAgent) and a.parked])
