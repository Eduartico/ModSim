from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random
from collections import deque

from agent import Car, Spot, Type

class ParkingLotModel(Model):
    def __init__(self, height, width, common_spots, electric_spots=0, premium_spots=0,
                 electric_chance=0, premium_chance=0, starting_cars=0, max_queue_size=10):
        super().__init__()  # Explicitly initialize the base Model class
        
        self.num_agents = starting_cars
        self.grid = MultiGrid(width, height, torus=False)
        self.queue = deque(maxlen=max_queue_size)
        self.schedule = RandomActivation(self)
        self.current_minutes = 0
        self.graveyard = []
        
        # Number of spots
        self.common_spots = common_spots
        self.electric_spots = electric_spots
        self.premium_spots = premium_spots
        self.spot_id = 0

        # Probabilities of each type of car
        self.electric_chance = electric_chance
        self.premium_chance = premium_chance
        self.normal_chance = 1 - electric_chance - premium_chance
        self.probabilities = [self.normal_chance, self.electric_chance, self.premium_chance]
        self.car_id = 0
        
        self.create_spots()
        
    def create_spots(self):
        x, y = 0, 2
        spot_types = [
            (self.premium_spots, Type.PREMIUM),
            (self.electric_spots, Type.ELECTRIC),
            (self.common_spots, Type.NORMAL),
        ]

        for count, spot_type in spot_types:
            for _ in range(count):
                spot = Spot(self.spot_id, self, spot_type) if spot_type else Spot(self.spot_id, self)
                self.grid.place_agent(spot, (x, y))
                spot.set_position(x, y)
                self.schedule.add(spot)
                x += 1
                self.spot_id += 1
                if x == self.grid.width:
                    x = 0
                    y += 1
                    
    def add_car_to_queue(self):
        if(len(self.queue) < self.queue.maxlen):    
            car_type = random.choices([Type.NORMAL, Type.ELECTRIC, Type.PREMIUM], self.probabilities)[0]
            new_car = Car(self.car_id, self, car_type, self.current_minutes)
            self.car_id += 1
            self.queue.append(new_car)
            
    def get_empty_spots(self):
        empty_spots = []
        for agent in self.schedule.agents:
            if isinstance(agent, Spot) and agent.available:
                empty_spots.append(agent)
        return empty_spots
            
    def update_grid(self):
        # Clean queue representation
        for cell in range(self.grid.width):
            for agent in self.grid.get_cell_list_contents((cell, 0)):
                if agent in self.queue:
                    self.grid.remove_agent(agent)

        # Insert cars on queue representation
        queue_list = list(self.queue)  # Convert deque to list for slicing
        for x, car in enumerate(queue_list[:self.grid.width]):  # Slice the list
            if self.grid.is_cell_empty((x, 0)):  # Check if the cell is empty
                self.grid.place_agent(car, (x, 0))
                
    def park_car(self, car, spot):
        self.grid.place_agent(car, (spot.x, spot.y))
        spot.park_car(car)
        car.park_car(self.current_minutes)
        self.schedule.add(car)
        
    def leave_park(self, car):
        for agent in self.schedule.agents:
            if isinstance(agent, Spot) and agent.current_car == car:
                agent.unpark_car()  # Free the spot
                break 
        self.grid.remove_agent(car)
        self.graveyard.append(car)
        self.schedule.remove(car)

    def step(self):
        self.current_minutes += 1
        self.add_car_to_queue()
        self.get_empty_spots()
        self.manage_parking(self.get_empty_spots())
        self.update_grid()
        self.schedule.step()
        
    def manage_parking(self):
        raise NotImplementedError("Subclasses must implement this method")


class PriorityModel(ParkingLotModel):
    def manage_parking(self, empty_spots):
        # Handle queue and parking logic for Priority
        first_car = self.queue[0]
        
        for spot in empty_spots:
            if first_car.get_type() == Type.NORMAL:
                if spot.spot_type == Type.NORMAL:
                    self.park_car(first_car, spot)
                    self.queue.popleft()    
                    break     
            elif first_car.get_type() == Type.ELECTRIC:
                if spot.spot_type == Type.ELECTRIC:
                    self.park_car(first_car, spot)
                    self.queue.popleft()
                    break
        
        self.schedule.step()
        
class OnDemandModel(ParkingLotModel):
    def manage_parking(self, empty_spots):
        # Handle queue and parking logic for OnDemand
        print("Approach 2: OnDemand logic here.")
        self.schedule.step()
        
        
class TimeBasedModel(ParkingLotModel):
    def manage_parking(self, empty_spots):
        # Handle queue and parking logic for TimeBased
        print("Approach 3: TimeBased logic here.")
        self.schedule.step()
        
class MembershipModel(ParkingLotModel):
    def manage_parking(self, empty_spots):
        # Handle queue and parking logic for Membership
        print("Approach 4: Membership logic here.")
        self.schedule.step()
        