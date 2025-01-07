from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import PriorityModel, OnDemandModel, TimeBasedModel, MembershipModel
from portrayal import parking_lot_portrayal
from pipeline import run_pipeline

interactive_GUI = False

model_mapping = {
    "PriorityModel": PriorityModel,
    "OnDemandModel": OnDemandModel,
    "TimeBasedModel": TimeBasedModel,
    "MembershipModel": MembershipModel,
}

if __name__ == "__main__":
    if interactive_GUI:
        model_class = model_mapping["MembershipModel"]
        grid = CanvasGrid(parking_lot_portrayal, 20, 20 + 1, 1000, 550)
        server = ModularServer(
            model_class,
            [grid],
            f"{model_class.__name__} Simulation",
            {
                "height": 20 + 1,
                "width": 20,
                "common_spots": 40,
                "electric_spots": 2,
                "premium_spots": 2,
                "electric_chance": 0.1,
                "premium_chance": 0.1,
                "max_queue_size": 10,
            },
        )
        server.port = 8521
        server.launch()
    else:
        run_pipeline()
