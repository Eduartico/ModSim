from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import random

from agent import Car, Spot


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

        self.queue = []
        self.unique_id = 0
        self.num_spots = 0
        self.aux = 3

        self.create_spots()

    def create_spots(self):
        x, y = 0, 2
        spot_types = [
            (self.premium_spots, "Premium"),
            (self.electric_spots, "Electric"),
            (self.common_spots, "Normal"),
        ]

        for count, spot_type in spot_types:
            for _ in range(count):
                spot = Spot(self.unique_id, self, spot_type) if spot_type else Spot(self.unique_id, self)
                self.grid.place_agent(spot, (x, y))
                x += 1
                self.unique_id += 1
                if x == self.grid.width:
                    x = 0
                    y += 1

    def count_parked_cars(self):
        return sum([1 for a in self.schedule.agents if isinstance(a, Car) and a.parked])

    def step(self):
        self.add_car_to_queue()
        self.update_grid()

        empty_spots = self.check_empty_spots()

        if self.aux < 0:
            if len(empty_spots) != 0:
                self.place_car_empty_spot(self.queue[0], empty_spots)

        self.aux -= 1
        self.schedule.step()

    def add_car_to_queue(self):
        car_type = random.choice(["Normal", "Electric", "Premium"])
        car = Car(self.unique_id, self, car_type)
        self.queue.append(car)
        self.unique_id += 1

    def update_grid(self):
        # Clean queue representation
        for cell in range(self.grid.width):
            for agent in self.grid.get_cell_list_contents((cell, 0)):
                if agent in self.queue:
                    self.grid.remove_agent(agent)

        # Insert cars on queue representation
        for x, car in enumerate(self.queue[:self.grid.width]):
            if self.grid.is_cell_empty((x, 0)):  # Verificar se a célula está vazia
                self.grid.place_agent(car, (x, 0))

    def check_empty_spots(self):
        empty_spots = [(x, y) for x in range(self.grid.width) for y in range(2, self.grid.height)
                       if self.is_cell_empty(x, y)]
        return empty_spots

    def is_cell_empty(self, x, y) -> bool:
        """Returns a bool of the contents of a cell."""
        return len(self.grid[x][y]) == 1

    def place_car_empty_spot(self, car, empty_spots):
        spot = empty_spots[0]
        self.grid.place_agent(car, spot)
        self.queue.pop(0)  # Remover o carro da fila
        car.parked = True

    def find_spot(self):
        return

    """
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
    """
