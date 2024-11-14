from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer


from model import ParkingLotModel
from portrayal import car_portrayal


# Setting up CanvasGrid and ChartModule for visualization
grid = CanvasGrid(car_portrayal, 20, 10, 500, 500)
chart = ChartModule([{"Label": "Parked Cars", "Color": "Black"}])

# Launch the simulation in a browser window
server = ModularServer(
    ParkingLotModel,
    [grid, chart],
    "Parking Lot Model",
    {"width": 20, "height": 10, "N": 20}
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
