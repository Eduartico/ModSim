from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import ParkingLotModel, PriorityModel, OnDemandModel, TimeBasedModel, MembershipModel
from portrayal import parking_lot_portrayal
from auxiliar import calculate_dimensions
from pipeline import collect_data, analyze_data, visualize_data

# Parameters
common_spots = 40
electric_spots = 5
premium_spots = 0
displayGUI = False
steps = 100
max_queue_size = 10

# Modes and configurations
configurations = [
    ("PriorityModel", 0.95, 0.05, 0),
    ("PriorityModel", 0.9, 0.1, 0),
    ("PriorityModel", 0.85, 0.15, 0),
    ("OnDemandModel", 0.95, 0.05, 0),
    ("OnDemandModel", 0.9, 0.1, 0),
    ("OnDemandModel", 0.85, 0.15, 0),
    ("TimeBasedModel", 0.95, 0.05, 0),
    ("TimeBasedModel", 0.9, 0.1, 0),
    ("TimeBasedModel", 0.85, 0.15, 0),
    ("MembershipModel", 0.9, 0.05, 0.05),
    ("MembershipModel", 0.8, 0.1, 0.1),
    ("MembershipModel", 0.7, 0.15, 0.15),
]

# Map model names to classes
model_mapping = {
    "ParkingLotModel": ParkingLotModel,
    "PriorityModel": PriorityModel,
    "OnDemandModel": OnDemandModel,
    "TimeBasedModel": TimeBasedModel,
    "MembershipModel": MembershipModel,
}


def run_analysis_for_config(model_class, normal_chance, electric_chance, premium_chance):
    common_spots = 40
    electric_spots = int(40 * electric_chance)
    premium_spots = int(40 * premium_chance)

    simulation_model = model_class(
        height=20,
        width=20,
        common_spots=common_spots,
        electric_spots=electric_spots,
        premium_spots=premium_spots,
        electric_chance=electric_chance,
        premium_chance=premium_chance,
        max_queue_size=max_queue_size,
    )

    df = collect_data(simulation_model, steps=steps)
    summary = analyze_data(df)
    title = f"{model_class.__name__} - Normal: {normal_chance}, Electric: {electric_chance}, Premium: {premium_chance}"
    print(f"\nSummary for {title}")
    for key, value in summary.items():
        print(f"{key}: {value}")
    visualize_data(df, electric_chance, premium_chance, title)


if __name__ == "__main__":
    if displayGUI:
        model_class = model_mapping.get("OnDemandModel")
        grid = CanvasGrid(parking_lot_portrayal, 20, 20 + 1, 1000, 550)
        server = ModularServer(
            model_class,
            [grid],
            f"{model_class.__name__} Simulation",
            {
                "height": 20 + 1,
                "width": 20,
                "common_spots": common_spots,
                "electric_spots": electric_spots,
                "premium_spots": premium_spots,
                "electric_chance": 0.2,
                "premium_chance": 0,
                "max_queue_size": max_queue_size,
            },
        )
        server.port = 8521
        server.launch()
    else:
        for mode, normal, electric, premium in configurations:
            run_analysis_for_config(model_mapping[mode], normal, electric, premium)
