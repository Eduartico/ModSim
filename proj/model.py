from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random
from collections import deque

from agent import Car, Spot, Type

class ParkingLotModel(Model):
    def __init__(self, height, width, common_spots, electric_spots=0, premium_spots=0,
                 electric_chance=0, premium_chance=0, max_queue_size=10, cars_added_per_step=1,
                 peak_hour_start=8, peak_hour_end=18):
        super().__init__()

        self.grid = MultiGrid(width, height, torus=False)
        self.queue = deque(maxlen=max_queue_size)
        self.schedule = RandomActivation(self)
        self.current_minutes = 0
        self.graveyard = []
        self.cars_added_per_step = cars_added_per_step
        self.earnings = 0

        self.peak_hour_start = peak_hour_start
        self.peak_hour_end = peak_hour_end

        self.common_spots = common_spots
        self.electric_spots = electric_spots
        self.premium_spots = premium_spots
        self.total_spots = common_spots + electric_spots + premium_spots
        self.spot_id = 0

        self.electric_chance = electric_chance
        self.premium_chance = premium_chance
        self.normal_chance = 1 - electric_chance - premium_chance
        self.probabilities = [self.normal_chance, self.electric_chance, self.premium_chance]
        self.car_id = 0

        self.create_spots()
        
    def create_spots(self):
        x, y = 0, 1
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
        current_hour = (self.current_minutes // 60) % 24

        if self.peak_hour_start <= current_hour < self.peak_hour_end:
            peak_mid = (self.peak_hour_start + self.peak_hour_end) / 2
            if current_hour <= peak_mid:
                multiplier = 1 + (current_hour - self.peak_hour_start) / (peak_mid - self.peak_hour_start) * 0.5
            else:
                multiplier = 1 + (self.peak_hour_end - current_hour) / (self.peak_hour_end - peak_mid) * 0.5
        else:
            multiplier = 1

        adjusted_cars = int(self.cars_added_per_step * multiplier)
        for _ in range(adjusted_cars):
            if len(self.queue) < self.queue.maxlen:
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
            
    def update_queue(self):
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
        self.grid.remove_agent(car)
        self.grid.place_agent(car, (spot.x, spot.y))
        spot.park_car(car)
        car.park_car(self.current_minutes)
        self.schedule.add(car)

    def leave_park(self, car):
        for agent in self.schedule.agents:
            if isinstance(agent, Spot) and agent.current_car == car:
                agent.unpark_car()
                break

        if car.get_type() == Type.NORMAL:
            self.earnings += 10
        elif car.get_type() == Type.ELECTRIC:
            self.earnings += 15
        elif car.get_type() == Type.PREMIUM:
            self.earnings += 20

        self.grid.remove_agent(car)
        self.graveyard.append(car)
        self.schedule.remove(car)

    def step(self):
        self.current_minutes += 1
        if len(self.queue) < self.queue.maxlen:
            self.add_car_to_queue()

        self.update_queue()
        self.get_empty_spots()

        for _ in range(self.cars_added_per_step * 2):
            queueSize = len(self.queue)
            self.manage_parking(self.get_empty_spots())
            if len(self.queue) == queueSize or len(self.queue) <= 0:
                break

        self.schedule.step()

    def manage_parking(self):
        raise NotImplementedError("Subclasses must implement this method")


class PriorityModel(ParkingLotModel):
    def manage_parking(self, empty_spots):
        for car in self.queue:
            car.increment_waiting_time()

        # Handle queue and parking logic for Priority
        if len(self.queue) > 0:
            first_car = self.queue[0]
            if first_car.waiting_time > 2:  # Ensure the car has waited at least two steps
                electric_spot_found = False
                backup_normal_spot = None
                for spot in empty_spots:
                    if first_car.get_type() == Type.NORMAL and spot.get_type() == Type.NORMAL:
                        self.park_car(first_car, spot)
                        self.queue.popleft()
                        break
                    elif first_car.get_type() == Type.ELECTRIC and spot.get_type() == Type.ELECTRIC:
                        self.park_car(first_car, spot)
                        self.queue.popleft()
                        electric_spot_found = True
                        break
                    
                    if backup_normal_spot is None:
                        if spot.get_type() == Type.NORMAL and spot.is_available():
                            backup_normal_spot = spot

                if first_car.get_type() == Type.ELECTRIC and not electric_spot_found:
                    if backup_normal_spot is not None:
                        self.park_car(first_car, backup_normal_spot)
                        self.queue.popleft()

        self.schedule.step()
        
class OnDemandModel(ParkingLotModel):
    def update_parking_spots(self):
        # Update the number of parking spots based on demand
        for agent in self.schedule.agents:
            if isinstance(agent, Spot) and agent.available and agent.spot_type == Type.NORMAL:
                agent.spot_type = Type.ELECTRIC
                self.electric_spots += 1
                self.common_spots -= 1
                break
        print("Updating parking spots.")
    
    def calculate_ev_demand(self, empty_spots):
        if not any(spot.spot_type == Type.ELECTRIC and spot.available for spot in empty_spots):
            return True
        return False

    def calculate_demand(self):
        total_spots = self.common_spots + self.electric_spots
        electric_demand = sum(1 for spot in self.get_empty_spots() if spot.spot_type == Type.ELECTRIC)
        return electric_demand / total_spots if total_spots > 0 else 0

    def change_spots(self, normal_percentage, electric_percentage):
        total_spots = self.common_spots + self.electric_spots
        new_common_spots = int(total_spots * normal_percentage)
        new_electric_spots = int(total_spots * electric_percentage)

        if new_common_spots > self.common_spots:
            self.common_spots = new_common_spots
        elif new_common_spots < self.common_spots:
            self.common_spots = new_common_spots

        if new_electric_spots > self.electric_spots:
            self.electric_spots = new_electric_spots
        elif new_electric_spots < self.electric_spots:
            self.electric_spots = new_electric_spots

    def manage_parking(self, empty_spots):
        # Handle queue and parking logic for OnDemand
        for car in self.queue:
            car.increment_waiting_time()
            
        if len(self.queue) > 0:
            first_car = self.queue[0]
            if first_car.waiting_time > 2:  # Ensure the car has waited at least two step
                electric_spot_found = False
                backup_normal_spot = None
                for spot in empty_spots:
                    if first_car.get_type() == Type.NORMAL and spot.get_type() == Type.NORMAL:
                        self.park_car(first_car, spot)
                        self.queue.popleft()
                        break
                    elif first_car.get_type() == Type.ELECTRIC and spot.get_type() == Type.ELECTRIC:
                        self.park_car(first_car, spot)
                        self.queue.popleft()
                        electric_spot_found = True
                        break
                    if backup_normal_spot is None:
                        if spot.get_type() == Type.NORMAL and spot.is_available():
                            backup_normal_spot = spot

                if first_car.get_type() == Type.ELECTRIC and not electric_spot_found:
                    if backup_normal_spot is not None:
                        self.park_car(first_car, backup_normal_spot)
                        self.queue.popleft()

        demand = self.calculate_demand()
        self.change_spots(normal_percentage=(1 - demand), electric_percentage=demand)

        self.schedule.step()
        
class TimeBasedModel(ParkingLotModel):
    def convert_spots(self, from_type, to_type, count):
        converted = 0
        for agent in self.schedule.agents:
            if isinstance(agent, Spot) and agent.spot_type == from_type:
                agent.spot_type = to_type
                converted += 1
                if converted == count:
                    break

    def change_spots(self, common_percentage, electric_percentage):
        total_spots = self.common_spots + self.electric_spots
        desired_common = int(total_spots * common_percentage)
        desired_electric = int(total_spots * electric_percentage)

        if self.common_spots < desired_common:
            self.convert_spots(Type.ELECTRIC, Type.NORMAL, desired_common - self.common_spots)
        elif self.common_spots > desired_common:
            self.convert_spots(Type.NORMAL, Type.ELECTRIC, self.common_spots - desired_common)

        self.common_spots = desired_common
        self.electric_spots = desired_electric

    def manage_parking(self, empty_spots):
        current_hour = (self.current_minutes // 60) % 24

        if self.peak_hour_start <= current_hour < self.peak_hour_end:
            self.change_spots(common_percentage=0.9, electric_percentage=0.1)
        else:
            self.change_spots(common_percentage=0.8, electric_percentage=0.2)

        # Handle queue and parking logic
        for car in self.queue:
            car.increment_waiting_time()

        if len(self.queue) > 0:
            first_car = self.queue[0]
            if first_car.waiting_time > 2:  # Ensure the car has waited at least two steps
                for spot in empty_spots:
                    if spot.get_type() == first_car.get_type() or spot.get_type() == Type.NORMAL:
                        self.park_car(first_car, spot)
                        self.queue.popleft()
                        break

        self.schedule.step()

        
class MembershipModel(ParkingLotModel):
    def manage_parking(self, empty_spots):
        for car in self.queue:
            car.increment_waiting_time()

        # Handle queue and parking logic for Priority
        if len(self.queue) > 0:
            first_car = self.queue[0]
            if first_car.waiting_time > 2:  # Ensure the car has waited at least two steps
                electric_spot_found = False
                premium_spot_found = False
                backup_normal_spot = None
                backup_electric_spot = None
                for spot in empty_spots:
                    if first_car.get_type() == Type.NORMAL and spot.get_type() == Type.NORMAL:
                        self.park_car(first_car, spot)
                        self.queue.popleft()
                        break
                    elif first_car.get_type() == Type.ELECTRIC and spot.get_type() == Type.ELECTRIC:
                        self.park_car(first_car, spot)
                        self.queue.popleft()
                        electric_spot_found = True
                        break
                    elif first_car.get_type() == Type.PREMIUM and spot.get_type() == Type.PREMIUM:
                        self.park_car(first_car, spot)
                        self.queue.popleft()
                        premium_spot_found = True
                        break
                    
                    if backup_normal_spot is None:
                        if spot.get_type() == Type.NORMAL and spot.is_available():
                            backup_normal_spot = spot
                    if backup_electric_spot is None:
                        if spot.get_type() == Type.ELECTRIC and spot.is_available():
                            backup_electric_spot = spot

                if first_car.get_type() == Type.ELECTRIC and not electric_spot_found and backup_normal_spot is not None:
                    self.park_car(first_car, backup_normal_spot)
                    self.queue.popleft()
                        
                elif first_car.get_type() == Type.PREMIUM and not premium_spot_found:
                    if backup_normal_spot is not None:
                        self.park_car(first_car, backup_normal_spot)
                        self.queue.popleft()
                    elif backup_electric_spot is not None:
                        self.park_car(first_car, backup_electric_spot)
                        self.queue.popleft()
                    
        self.schedule.step()
        