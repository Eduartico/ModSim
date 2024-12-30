from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import ParkingLotModel, PriorityModel, OnDemandModel
from portrayal import parking_lot_portrayal
from auxiliar import calculate_dimensions
from pipeline import collect_data, analyze_data, visualize_data

# Parameters
common_spots = 40
electric_spots = 5
premium_spots = 0
displayGUI = False
model_to_run = "ParkingLotModel"
steps = 100
max_queue_size = 10
premium_chance = 0
electric_chance = 0.2
width, height = calculate_dimensions(common_spots, electric_spots, premium_spots)

# Map model names to classes
model_mapping = {
    "ParkingLotModel": ParkingLotModel,
    "PriorityModel": PriorityModel,
    "OnDemandModel": OnDemandModel,
}

def run_analysis(model_class):
    simulation_model = model_class(
        height=height + 1,
        width=width,
        common_spots=common_spots,
        electric_spots=electric_spots,
        premium_spots=premium_spots,
        electric_chance=electric_chance,
        premium_chance=premium_chance,
        max_queue_size=max_queue_size,
    )
    df = collect_data(simulation_model, steps=steps)
    summary = analyze_data(df)
    print("Simulation Summary:")
    for key, value in summary.items():
        print(f"{key}: {value}")
    visualize_data(df, electric_chance, premium_chance)

if __name__ == "__main__":
    model_class = model_mapping.get(model_to_run)
    if not model_class:
        raise ValueError(
            f"Invalid model_to_run value: '{model_to_run}'. Must be one of {list(model_mapping.keys())}.")

    if displayGUI:
        grid = CanvasGrid(parking_lot_portrayal, width, height + 1, 1000, 550)
        server = ModularServer(
            model_class,
            [grid],
            f"{model_class.__name__} Simulation",
            {
                "height": height + 1,
                "width": width,
                "common_spots": common_spots,
                "electric_spots": electric_spots,
                "premium_spots": premium_spots,
                "electric_chance": electric_chance,
                "premium_chance": premium_chance,
                "max_queue_size": max_queue_size,
            },
        )
        server.port = 8521
        server.launch()
    else:
        run_analysis(model_class)
