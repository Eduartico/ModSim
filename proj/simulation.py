import time
from enum import Enum
import model
import pandas as pd


class Modes(Enum):
    PRIORITY = "Priority"
    ON_DEMAND = "On-Demand"
    TIME_BASED = "Time-based"
    MEMBERSHIP = "Membership"


class Simulation:
    def __init__(self, width, height, total_spots, electric_percentage=0.1, premium_percentage=0.1, electric_chance=0.1,
                 premium_chance=0, mode=Modes.ON_DEMAND, gui=False, max_queue_len=10, cars_added_per_step=1,
                 peak_hour_start=8, peak_hour_end=18):
        self.common_spots = int(total_spots * (1 - electric_percentage))
        self.electric_spots = int(total_spots * electric_percentage)
        self.premium_spots = 0
        self.total_spots = total_spots
        self.electric_percentage = electric_percentage
        self.premium_percentage = premium_percentage
        self.model = None
        self.width = width
        self.height = height
        self.electric_chance = electric_chance
        self.premium_chance = premium_chance
        self.mode = None
        self.current_minutes = 0
        self.day_length = 1440  # 24 hours
        self.gui = gui
        self.max_queue_len = max_queue_len
        self.cars_added_per_step = cars_added_per_step
        self.peak_hour_start = peak_hour_start
        self.peak_hour_end = peak_hour_end
        self.set_mode(mode)


    def set_mode(self, mode):
        self.mode = mode

        print(f"Setting mode to {self.mode.value}")
        if self.mode == Modes.PRIORITY:
            self.model = model.PriorityModel(self.height, self.width, self.common_spots, self.electric_spots,
                                             self.premium_spots, self.electric_chance, self.premium_chance,
                                             self.max_queue_len, self.cars_added_per_step,
                                             self.peak_hour_start, self.peak_hour_end)

        elif self.mode == Modes.ON_DEMAND:
            self.model = model.OnDemandModel(self.height, self.width, self.common_spots, self.electric_spots,
                                             self.premium_spots, self.electric_chance, self.premium_chance,
                                             self.max_queue_len, self.cars_added_per_step,
                                             self.peak_hour_start, self.peak_hour_end)

            self.model.update_parking_spots()

        elif self.mode == Modes.TIME_BASED:
            self.model = model.TimeBasedModel(self.height, self.width, self.common_spots, self.electric_spots,
                                              self.premium_spots, self.electric_chance, self.premium_chance,
                                              self.max_queue_len, self.cars_added_per_step,
                                             self.peak_hour_start, self.peak_hour_end)


        elif self.mode == Modes.MEMBERSHIP:
            self.common_spots = int(self.total_spots * (1 - (self.electric_percentage + self.premium_percentage)))
            self.electric_spots = int(self.total_spots * self.electric_percentage)
            self.premium_spots = int(self.total_spots * self.premium_percentage)
            self.model = model.MembershipModel(self.height, self.width, self.common_spots, self.electric_spots,
                                               self.premium_spots, self.electric_chance, self.premium_chance,
                                               self.max_queue_len, self.cars_added_per_step,
                                             self.peak_hour_start, self.peak_hour_end)

    def run_simulation(self):
        simulation_data = {
            "time": [],
            "parked_cars": [],
            "waiting_cars": [],
            "available_common_spots": [],
            "available_electric_spots": [],
            "available_premium_spots": [],
            "earnings": [],
            "total_common_cars_parked": [],
            "total_electric_cars_parked": [],
            "total_premium_cars_parked": []
        }

        while self.current_minutes < self.day_length:
            self.current_minutes += 1
            self.model.step()

            parked_cars = sum(agent.parked for agent in self.model.schedule.agents if isinstance(agent, model.Car))

            simulation_data["time"].append(self.current_minutes)
            simulation_data["parked_cars"].append(parked_cars)
            simulation_data["waiting_cars"].append(len(self.model.queue))
            simulation_data["available_common_spots"].append(
                sum(spot.available and spot.spot_type == model.Type.NORMAL for spot in self.model.schedule.agents if
                    isinstance(spot, model.Spot)))
            simulation_data["available_electric_spots"].append(
                sum(spot.available and spot.spot_type == model.Type.ELECTRIC for spot in self.model.schedule.agents if
                    isinstance(spot, model.Spot)))
            simulation_data["available_premium_spots"].append(
                sum(spot.available and spot.spot_type == model.Type.PREMIUM for spot in self.model.schedule.agents if
                    isinstance(spot, model.Spot)))
            simulation_data["earnings"].append(self.model.earnings)
            simulation_data["total_common_cars_parked"].append(
                sum(car.parked and car.car_type == model.Type.NORMAL for car in self.model.schedule.agents if
                    isinstance(car, model.Car)))
            simulation_data["total_electric_cars_parked"].append(
                sum(car.parked and car.car_type == model.Type.ELECTRIC for car in self.model.schedule.agents if
                    isinstance(car, model.Car)))
            simulation_data["total_premium_cars_parked"].append(
                sum(car.parked and car.car_type == model.Type.PREMIUM for car in self.model.schedule.agents if
                    isinstance(car, model.Car)))

        min_length = min(len(values) for values in simulation_data.values())
        for key in simulation_data:
            simulation_data[key] = simulation_data[key][:min_length]

        total_waiting_time = sum(car.waiting_time for car in self.model.graveyard if isinstance(car, model.Car))
        total_cars = len([car for car in self.model.graveyard if isinstance(car, model.Car)])
        average_waiting_time = total_waiting_time / total_cars if total_cars > 0 else 0

        print("Simulation complete.")

        return pd.DataFrame(simulation_data), average_waiting_time





