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
    def __init__(self, width, height, total_spots, electric_percentage=0.1, premium_percentage=0.1, electric_chance=0.1, premium_chance=0.1, mode=Modes.PRIORITY):
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

    def set_mode(self, mode):
        self.mode = mode
        print(f"Setting mode to {self.mode.value}")
        if self.mode == Modes.PRIORITY:
            self.common_spots = self.total_spots * (1 - self.electric_percentage)
            self.electric_spots = self.total_spots * self.electric_percentage
            self.premium_chance = 0

        elif self.mode == Modes.ON_DEMAND:
            def adjust_ev_spaces_based_on_demand():
                demand = self.model.calculate_ev_demand() #TODO
                self.electric_percentage = 0.15 if demand > 0.5 else 0.05 #NAO SEREM VALORES HARD CODED, FAZER ALGO COMO O DEVIO GERADO PELA FUNÇÃO DA DEMANDA
                self.model.update_parking_spots(self.model) # TODO ATUALIZAR PARAMETROS QUANDO HUGO FIZER ISTO

            adjust_ev_spaces_based_on_demand()

        elif self.mode == Modes.TIME_BASED:
            def set_time_based_parking():
                current_hour = (self.current_minutes // 60) % 24
                if 8 <= current_hour < 18: # rush hour
                    self.common_spots = self.total_spots * (1 - (self.electric_percentage * 0.5)) # diminuir as vagas eletricas pela metade
                    self.electric_spots = self.total_spots * (self.electric_percentage * 0.5)
                else:
                    self.common_spots = self.total_spots * (1 - (self.electric_percentage * 1.5)) # aumentar as vagas eletricas pela metade
                    self.electric_spots = self.total_spots * (self.electric_percentage * 1.5)

                self.model.update_parking_spots(self.model)  # TODO ATUALIZAR PARAMETROS QUANDO HUGO FIZER ISTO

            set_time_based_parking()

        elif self.mode == Modes.MEMBERSHIP:
            self.common_spots = self.total_spots * (1 - (self.electric_percentage + self.premium_percentage))
            self.electric_spots = self.total_spots * self.electric_percentage
            self.premium_spots = self.total_spots * self.premium_percentage


        else:
            print("Wrong mode selected.")

        self.model = model.ParkingLotModel(self.height, self.width, self.common_spots, self.electric_spots,
                                           self.premium_spots, self.electric_chance, self.premium_chance, 10)

    def run_simulation(self):

        while self.current_minutes < self.day_length:
            self.current_minutes += 1
            self.model.current_minutes += 1
            current_hour = (self.current_minutes // 60) % 24
            if self.current_minutes % 15 == 0:
                print(f"Current time: {current_hour}:{self.current_minutes}")

            if self.current_minutes % 2 == 0 and current_hour <= 21:
                self.model.add_car_to_queue(model)

            if (mode on demand and demand > demandmax):
                self.model.update_parking_spots(self.model)
                self.model.on_demand_step(self.model)

            print(f"Parked cars: {self.model.count_parked_cars()}")
            time.sleep(0.1)

        print("Simulation day complete.")
        #TODO: IR BUSCAR O GRAVEYARD, CRIAR PANDAS DF RELEVANTE
        #return simulation_df



