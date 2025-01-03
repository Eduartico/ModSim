import pandas as pd
import matplotlib.pyplot as plt
from agent import Car, Spot, Type


def collect_data(simulation_model, steps=1440):
    """
    Runs the simulation for a specified number of steps and collects data.
    """
    data = {
        "time": [],
        "parked_cars": [],
        "waiting_cars": [],
        "total_cars_parked": [],
        "available_electric_spots": [],
        "available_premium_spots": [],
        "available_common_spots": [],
        "total_electric_spots": [],
        "total_premium_spots": [],
        "total_common_spots": [],
    }

    for step in range(steps):
        simulation_model.step()

        # Filter only spots
        spots = [agent for agent in simulation_model.schedule.agents if isinstance(agent, Spot)]

        # Calculate metrics
        currently_parked = sum(
            isinstance(agent, Car) and agent.parked for agent in simulation_model.schedule.agents
        )
        total_cars_parked = currently_parked + len(simulation_model.graveyard)

        # Append data
        data["time"].append(step)
        data["parked_cars"].append(currently_parked)
        data["waiting_cars"].append(len(simulation_model.queue))
        data["total_cars_parked"].append(total_cars_parked)
        data["available_electric_spots"].append(
            sum(spot.available and spot.spot_type == Type.ELECTRIC for spot in spots)
        )
        data["available_premium_spots"].append(
            sum(spot.available and spot.spot_type == Type.PREMIUM for spot in spots)
        )
        data["available_common_spots"].append(
            sum(spot.available and spot.spot_type == Type.NORMAL for spot in spots)
        )
        data["total_electric_spots"].append(simulation_model.electric_spots)
        data["total_premium_spots"].append(simulation_model.premium_spots)
        data["total_common_spots"].append(simulation_model.common_spots)

    return pd.DataFrame(data)


def analyze_data(df):
    """
    Performs analysis on the simulation data.
    """
    summary = {
        "total_parked_cars": df["parked_cars"].iloc[-1],
        "max_waiting_cars": df["waiting_cars"].max(),
        "average_available_common_spots": df["available_common_spots"].mean(),
        "average_available_electric_spots": df["available_electric_spots"].mean(),
        "average_available_premium_spots": df["available_premium_spots"].mean(),
        "total_cars_parked": df["total_cars_parked"].iloc[-1],
    }
    return summary


def visualize_data(df, electric_chance, premium_chance, title):
    """
    Visualizes the simulation data with graphs in a single window.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.canvas.manager.set_window_title(title)
    plt.subplots_adjust(hspace=0.5, wspace=0.3)

    # Parked cars and waiting cars
    axes[0, 0].plot(df["time"], df["parked_cars"], label="Parked Cars")
    axes[0, 0].plot(df["time"], df["waiting_cars"], label="Waiting Cars")
    axes[0, 0].set_title("Cars Parked and Waiting Over Time")
    axes[0, 0].set_xlabel("Time")
    axes[0, 0].set_ylabel("Number of Cars")
    axes[0, 0].legend()
    axes[0, 0].grid(True)

    # Total cars parked
    axes[0, 1].plot(df["time"], df["total_cars_parked"], label="Total Cars Parked", color="green")
    axes[0, 1].set_title("Total Cars Parked Over Time")
    axes[0, 1].set_xlabel("Time")
    axes[0, 1].set_ylabel("Number of Cars")
    axes[0, 1].legend()
    axes[0, 1].grid(True)

    # Availability of parking spots
    axes[1, 0].plot(df["time"], df["available_common_spots"], label="Available Common Spots")
    if electric_chance > 0:
        axes[1, 0].plot(df["time"], df["available_electric_spots"], label="Available Electric Spots")
    if premium_chance > 0:
        axes[1, 0].plot(df["time"], df["available_premium_spots"], label="Available Premium Spots")
    axes[1, 0].set_title("Availability of Parking Spots Over Time")
    axes[1, 0].set_xlabel("Time")
    axes[1, 0].set_ylabel("Available Spots")
    axes[1, 0].legend()
    axes[1, 0].grid(True)

    # Total parking spots if common spots change
    if df["total_common_spots"].nunique() > 1:
        axes[1, 1].plot(df["time"], df["total_common_spots"], label="Total Common Spots")
        if electric_chance > 0:
            axes[1, 1].plot(df["time"], df["total_electric_spots"], label="Total Electric Spots")
        if premium_chance > 0:
            axes[1, 1].plot(df["time"], df["total_premium_spots"], label="Total Premium Spots")
        axes[1, 1].set_title("Total Parking Spots Over Time")
        axes[1, 1].set_xlabel("Time")
        axes[1, 1].set_ylabel("Total Spots")
        axes[1, 1].legend()
        axes[1, 1].grid(True)
    else:
        axes[1, 1].axis("off")

    plt.show()
