import random

from mesa import Agent
from enum import Enum

class Type(Enum):
    NORMAL = "Normal"
    ELECTRIC = "Electric"
    PREMIUM = "Premium"

# Define the car agent
def leave_probability(time_parked, min, med, max):
    if time_parked < min:
        return 0.0
    elif time_parked < med:
        return 0.5 * (time_parked - min) / (med - min)
    elif time_parked < max:
        return 0.5 + 0.5 * (time_parked - med) / (max - med)
    else:
        return 1.0


class Car(Agent):
    def __init__(self, unique_id, model, car_type, created_minute):
        super().__init__(unique_id, model)
        self.car_type = car_type
        self.parked = False
        self.created_minute = created_minute
        self.parked_minute = 0
        self.leaved_minute = 0
        self.waiting_time = 0  
        
    def park_car(self, parked_minute):
        self.parked = True
        self.parked_minute = parked_minute
        
    def increment_waiting_time(self):
        self.waiting_time += 1

    def step(self):
        if self.parked:
            time_parked = self.model.current_minutes - self.parked_minute
            # 2. Call it as an instance method, passing just time_parked
            p = leave_probability(time_parked, 25, 50, 75)
            if random.random() < p:
                self.parked = False
                self.leaved_minute = self.model.current_minutes
                self.model.leave_park(self)
       
    def get_type(self):
        return self.car_type
    
    def get_state(self):
        return self.parked

# Define the spot agent
class Spot(Agent):
    def __init__(self, unique_id, model, spot_type = Type.NORMAL):
        super().__init__(unique_id, model)
        self.spot_type = spot_type
        self.x = 0
        self.y = 0
        self.available = True
        self.current_car = None

    def park_car(self, car):
        self.available = False
        self.current_car = car

    def unpark_car(self):
        self.available = True
        self.current_car = None

    def set_type(self, spot_type):
        self.spot_type = spot_type
        
    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_type(self):
        return self.spot_type

    def get_position(self):
        return self.x, self.y

    def is_available(self):
        return self.available
