from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import ParkingLotModel, PriorityModel, OnDemandModel
from portrayal import parking_lot_portrayal
from auxiliar import calculate_dimensions

common_spots = 40
electric_spots = 5
premium_spots = 0
width, height = calculate_dimensions(common_spots, electric_spots, premium_spots)
# Setting up CanvasGrid for visualization
grid = CanvasGrid(parking_lot_portrayal, width, height + 1, 1000, 550)  # (height + 2 para fila)
grid.local_includes = ["custom.css"]
grid.local_dir = "static"

# Launch the simulation in a browser window
server = ModularServer(
    OnDemandModel,
    [grid],
    "Parking Lot Model",
    {"height": height + 1, "width": width,
     "common_spots": common_spots, "electric_spots": electric_spots, "premium_spots": premium_spots,
     "electric_chance": 0.2, "premium_chance": 0, "max_queue_size": 10}
)


if __name__ == "__main__":
    server.port = 8521
    server.launch()

# Run the simulation
if __name__ == "__main__":
    #parking_lot = ParkingLotModel(width, height + 2, common_spots)
    priority_model = OnDemandModel(width, height + 1, common_spots, electric_spots, premium_spots, 0.2, 0)

    for i in range(10):  # Run for 10 steps
        print(f"Step {i}")
        priority_model.step()
