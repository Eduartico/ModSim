from mesa import Agent
from enum import Enum

class Type(Enum):
    NORMAL = "Normal"
    ELECTRIC = "Electric"
    PREMIUM = "Premium"

# Define the car agent
class Car(Agent):
    def __init__(self, unique_id, model, car_type, created_minute):
        super().__init__(unique_id, model)
        self.car_type = car_type
        self.parked = False
        self.created_minute = created_minute
        self.parked_minute = 0
        self.leaved_minute = 0
        
    def park_car(self, parked_minute):
        self.parked = True
        self.parked_minute = parked_minute
            
    def step(self):
        # try to leave the park
        if self.parked:
            if self.model.current_minutes - self.parked_minute >= self.random.randint(30, 40):
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

    def get_type(self):
        return self.spot_type

    def is_available(self):
        return self.available
