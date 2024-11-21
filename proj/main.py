from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
import math
from model import ParkingLotModel
from portrayal import car_portrayal
from auxiliar import calculate_dimensions

common_spots = 20
electric_spots = 0
premium_spots = 0
width, height = calculate_dimensions(common_spots, electric_spots, premium_spots)
# Setting up CanvasGrid and ChartModule for visualization
grid = CanvasGrid(car_portrayal, 5, 5, 500, 550)  # 20x11 (10 para estacionamento + 1 para fila)

# Launch the simulation in a browser window
server = ModularServer(
    ParkingLotModel,
    [grid],
    "Parking Lot Model",
    {"height": height, "width": width,
     "common_spots": common_spots, "electric_spots": electric_spots, "premium_spots": premium_spots,
     "electric_chance": 0.4, "premium_chance": 0.1, "starting_cars": 30}
)

if __name__ == "__main__":
    server.port = 8521
    server.launch()

# Run the simulation
if __name__ == "__main__":
    parking_lot = ParkingLotModel(20, 10, 20)

    for i in range(10):  # Run for 10 steps
        parking_lot.step()
        print(f"Step {i + 1}: {parking_lot.count_parked_cars()} cars parked.")
