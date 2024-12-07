from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
import math
from model import ParkingLotModel
from portrayal import car_portrayal
from auxiliar import calculate_dimensions

common_spots = 40
electric_spots = 15
premium_spots = 10
width, height = calculate_dimensions(common_spots, electric_spots, premium_spots)
# Setting up CanvasGrid and ChartModule for visualization
grid = CanvasGrid(car_portrayal, width, height + 2, 1000, 550)  # (height + 2 para fila)
grid.local_includes = ["custom.css"]
grid.local_dir = "static"

# Launch the simulation in a browser window
server = ModularServer(
    ParkingLotModel,
    [grid],
    "Parking Lot Model",
    {"height": height + 2, "width": width,
     "common_spots": common_spots, "electric_spots": electric_spots, "premium_spots": premium_spots,
     "electric_chance": 0.2, "premium_chance": 0.05, "starting_cars": 30}
)


if __name__ == "__main__":
    server.port = 8521
    server.launch()

# Run the simulation
if __name__ == "__main__":
    parking_lot = ParkingLotModel(width, height + 2, common_spots)

    for i in range(10):  # Run for 10 steps
        parking_lot.step()
        print(parking_lot.grid.width, parking_lot.grid.height)
        print(f"Step {i + 1}: {parking_lot.count_parked_cars()} cars parked.")
