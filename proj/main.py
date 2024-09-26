from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer


# Define the car agent
class CarAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.parked = False

    def step(self):
        if not self.parked:
            # Find an empty spot
            empty_parking_spots = [(x, y) for x in range(self.model.grid.width) for y in range(self.model.grid.height)
                                   if self.model.grid.is_cell_empty((x, y))]
            if empty_parking_spots:
                new_position = self.random.choice(empty_parking_spots)
                self.model.grid.move_agent(self, new_position)
                self.parked = True
        else:
            # Decide to leave after a certain time
            if self.random.random() < 0.1:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)


# Define the parking model
class ParkingLotModel(Model):
    def __init__(self, width, height, N):
        super().__init__()  # Explicitly initialize the base Model class
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
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

# Visualization helper function
def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "r": 0.8, "Filled": "true"}
    if agent.parked:
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 1
    else:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    return portrayal

# Setting up CanvasGrid and ChartModule for visualization
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
chart = ChartModule([{"Label": "Parked Cars", "Color": "Black"}])

# Launch the simulation in a browser window
server = ModularServer(
    ParkingLotModel,
    [grid, chart],
    "Parking Lot Model",
    {"width": 10, "height": 10, "N": 20}
)

if __name__ == "__main__":
    server.port = 8521
    server.launch()

# Run the simulation
if __name__ == "__main__":
    parking_lot = ParkingLotModel(10, 10, 20)

    for i in range(10):  # Run for 10 steps
        parking_lot.step()
        print(f"Step {i + 1}: {parking_lot.count_parked_cars()} cars parked.")
