import time
from enum import Enum
import model
import agent
class Modes(Enum):
    PRIORITY = "Priority"
    ON_DEMAND = "On-Demand"
    TIME_BASED = "Time-based"
    MEMBERSHIP = "Membership"

class Simulation:
    def __init__(self, width, height, num_agents, mode=Modes.PRIORITY):
        self.electric_spots = None
        self.common_spots = None
        self.model = None
        self.width = width
        self.height = height
        self.total_spots = 60
        self.premium_spots = 0
        self.electric_chance = 0.1
        self.premium_chance = 0.1
        self.num_agents = num_agents
        self.mode = mode
        self.current_minutes = 0
        self.day_length = 1440 # 24 hours

    def set_mode(self, mode):
        self.mode = mode
        print(f"Setting mode to {self.mode.value}")
        if self.mode == Modes.PRIORITY:
            self.common_spots = self.total_spots * (1 - 0.1)
            self.electric_spots = self.total_spots * 0.1

        elif self.mode == Modes.ON_DEMAND:
            def adjust_ev_spaces_based_on_demand():
                # COMO DEFINIR SPOTS ON DEMAND NO MODEL?
                demand = self.model.calculate_ev_demand()
                ev_percentage = 0.15 if demand > 0.5 else 0.05
                self.model.set_ev_spaces(int(total_spaces * ev_percentage))
                print(f"On-Demand Mode: Adjusted EV spaces to {int(self.total_spaces * ev_percentage)} based on demand.")

            adjust_ev_spaces_based_on_demand()

        elif self.mode == Modes.TIME_BASED:
            def set_time_based_parking():
                current_hour = (self.current_minutes // 60) % 24
                if 8 <= current_hour < 18: # rush hour
                    self.common_spots = self.total_spots * (1 - 0.05)
                    self.electric_spots = self.total_spots * 0.05
                else:
                    self.common_spots = self.total_spots * (1 - 0.15)
                    self.electric_spots = self.total_spots * 0.15

            set_time_based_parking()

        elif self.mode == Modes.MEMBERSHIP:
            self.common_spots = self.total_spots * (1 - 0.2)
            self.electric_spots = self.total_spots * 0.1
            self.premium_spots = self.total_spots * 0.1


        else:
            print("Wrong mode selected.")

        self.model = model.ParkingLotModel(self.height, self.width, self.common_spots, self.electric_spots,
                                           self.premium_spots, self.electric_chance, self.premium_chance, 0, mode)

    def run_simulation(self):

        while self.current_minutes < self.day_length:
            self.current_minutes += 1 # avaliar se é necessário ter estes minutos
            self.model.current_minutes += 1
            current_hour = (self.current_minutes // 60) % 24
            print(f"Time: {self.current_minutes} minutes")

            if self.current_minutes % 5 == 0 and current_hour <= 21: # working hours
                self.model.add_car_to_queue(model)

            if (mode on demand and demand > demandmax):
                self.model.update_parking_spots(self.model)
                self.model.on_demand_step(self.model)

            print(f"Parked cars: {self.model.count_parked_cars()}")
            time.sleep(0.1)

        print("Simulation day complete.")
        #TODO: IR BUSCAR O GRAVEYARD, CRIAR PANDAS DF RELEVANTE
        #return simulation_df



