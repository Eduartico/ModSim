import pandas as pd
import matplotlib.pyplot as plt
from agent import Car, Spot, Type


def collect_data(simulation_model, steps=1440):
    """
    Runs the simulation for a specified number of steps and collects data.

    Parameters:
    - simulation_model: Instance of the simulation to run.
    - steps (int): Number of steps to run the simulation.

    Returns:
    - pd.DataFrame: DataFrame containing simulation results.
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

    Parameters:
    - df (pd.DataFrame): DataFrame with simulation data.

    Returns:
    - dict: Summary of analyzed results.
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


def visualize_data(df, electric_chance, premium_chance):
    """
    Visualizes the simulation data with graphs.

    Parameters:
    - df (pd.DataFrame): DataFrame with simulation data.
    - electric_chance (float): Chance for an electric car to arrive.
    - premium_chance (float): Chance for a premium car to arrive.
    """
    # Parked cars and waiting cars
    plt.figure(figsize=(10, 6))
    plt.plot(df["time"], df["parked_cars"], label="Parked Cars")
    plt.plot(df["time"], df["waiting_cars"], label="Waiting Cars")
    plt.xlabel("Time")
    plt.ylabel("Number of Cars")
    plt.title("Cars Parked and Waiting Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Total cars parked
    plt.figure(figsize=(10, 6))
    plt.plot(df["time"], df["total_cars_parked"], label="Total Cars Parked", color="green")
    plt.xlabel("Time")
    plt.ylabel("Number of Cars")
    plt.title("Total Cars Parked Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Availability of parking spots
    plt.figure(figsize=(10, 6))
    plt.plot(df["time"], df["available_common_spots"], label="Available Common Spots")
    if electric_chance > 0:
        plt.plot(df["time"], df["available_electric_spots"], label="Available Electric Spots")
    if premium_chance > 0:
        plt.plot(df["time"], df["available_premium_spots"], label="Available Premium Spots")
    plt.xlabel("Time")
    plt.ylabel("Available Spots")
    plt.title("Availability of Parking Spots Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Total parking spots if common spots change
    if df["total_common_spots"].nunique() > 1:
        plt.figure(figsize=(10, 6))
        plt.plot(df["time"], df["total_common_spots"], label="Total Common Spots")
        if electric_chance > 0:
            plt.plot(df["time"], df["total_electric_spots"], label="Total Electric Spots")
        if premium_chance > 0:
            plt.plot(df["time"], df["total_premium_spots"], label="Total Premium Spots")
        plt.xlabel("Time")
        plt.ylabel("Total Spots")
        plt.title("Total Parking Spots Over Time")
        plt.legend()
        plt.grid(True)
        plt.show()
