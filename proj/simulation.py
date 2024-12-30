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
    def __init__(self, width, height, total_spots, electric_percentage=0.1, premium_percentage=0.1, electric_chance=0.1, premium_chance=0.1, mode=Modes.PRIORITY, gui=False):
        self.electric_spots = None
        self.common_spots = None
        self.premium_spots = 0
        self.total_spots = total_spots
        self.electric_percentage = electric_percentage
        self.premium_percentage = premium_percentage
        self.model = None
        self.width = width
        self.height = height
        self.electric_chance = electric_chance
        self.premium_chance = premium_chance
        self.mode = mode
        self.current_minutes = 0
        self.day_length = 1440 # 24 hours
        self.gui = gui

    def set_mode(self, mode):
        if mode in ["P", "Priority"]:
            self.mode = Modes.PRIORITY
        elif mode in ["O", "On-Demand"]:
            self.mode = Modes.ON_DEMAND
        elif mode in ["T", "Time-based"]:
            self.mode = Modes.TIME_BASED
        elif mode in ["M", "Membership"]:
            self.mode = Modes.MEMBERSHIP
        else:
            raise ValueError("Invalid mode. Please choose from 'P', 'O', 'T', 'M', or their full names.")

        print(f"Setting mode to {self.mode.value}")
        if self.mode == Modes.PRIORITY:
            self.common_spots = int(self.total_spots * (1 - self.electric_percentage))
            self.electric_spots = int(self.total_spots * self.electric_percentage)
            self.premium_chance = 0

        elif self.mode == Modes.ON_DEMAND:
            def adjust_ev_spaces_based_on_demand():
                empty_spots = self.model.get_empty_spots()
                demand = self.model.calculate_ev_demand(empty_spots)
                if demand:
                    self.electric_percentage = min(0.2, self.electric_percentage + 0.05)
                else:
                    self.electric_percentage = max(0.05, self.electric_percentage - 0.05)
                self.common_spots = int(self.total_spots * (1 - self.electric_percentage))
                self.electric_spots = int(self.total_spots * self.electric_percentage)

            adjust_ev_spaces_based_on_demand()

        elif self.mode == Modes.TIME_BASED:
            def set_time_based_parking():
                current_hour = (self.current_minutes // 60) % 24
                if 8 <= current_hour < 18:  # rush hour
                    self.common_spots = int(self.total_spots * (1 - (self.electric_percentage * 0.5)))
                    self.electric_spots = int(self.total_spots * (self.electric_percentage * 0.5))
                else:
                    self.common_spots = int(self.total_spots * (1 - (self.electric_percentage * 1.5)))
                    self.electric_spots = int(self.total_spots * (self.electric_percentage * 1.5))

            set_time_based_parking()

        elif self.mode == Modes.MEMBERSHIP:
            self.common_spots = int(self.total_spots * (1 - (self.electric_percentage + self.premium_percentage)))
            self.electric_spots = int(self.total_spots * self.electric_percentage)
            self.premium_spots = int(self.total_spots * self.premium_percentage)

        self.model = model.ParkingLotModel(self.height, self.width, self.common_spots, self.electric_spots,
                                           self.premium_spots, self.electric_chance, self.premium_chance, 10)

    def run_simulation(self):
        simulation_data = {
            "time": [],
            "parked_cars": [],
            "waiting_cars": [],
            "total_cars_parked": [],
        }

        while self.current_minutes < self.day_length:
            self.current_minutes += 1
            self.model.step()

            if self.gui:
                time.sleep(0.1)

            if self.current_minutes % 15 == 0:
                current_hour = (self.current_minutes // 60) % 24
                print(f"Current time: {current_hour}:{self.current_minutes % 60}")

            simulation_data["time"].append(self.current_minutes)
            simulation_data["parked_cars"].append(sum(isinstance(agent, model.Car) and agent.parked for agent in self.model.schedule.agents))
            simulation_data["waiting_cars"].append(len(self.model.queue))
            simulation_data["total_cars_parked"].append(len(self.model.graveyard))

        print("Simulation day complete.")
        return pd.DataFrame(simulation_data)
