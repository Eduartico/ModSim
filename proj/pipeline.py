import pandas as pd
import matplotlib.pyplot as plt
from simulation import Simulation, Modes

configurations = [
    (Modes.PRIORITY, 0.95, 0.05, 0),
    (Modes.PRIORITY, 0.9, 0.1, 0),
    (Modes.PRIORITY, 0.85, 0.15, 0),
    (Modes.ON_DEMAND, 0.95, 0.05, 0),
    (Modes.ON_DEMAND, 0.9, 0.1, 0),
    (Modes.ON_DEMAND, 0.85, 0.15, 0),
    #(Modes.MEMBERSHIP, 0.9, 0.05, 0.05),
    #(Modes.MEMBERSHIP, 0.8, 0.1, 0.1),
    #(Modes.MEMBERSHIP, 0.7, 0.15, 0.15),
]

def analyze_data(df):
    summary = {
        "total_parked_cars": df["parked_cars"].iloc[-1],
        "max_waiting_cars": df["waiting_cars"].max(),
        "average_available_common_spots": df["available_common_spots"].mean(),
        "average_available_electric_spots": df["available_electric_spots"].mean(),
        "average_available_premium_spots": df["available_premium_spots"].mean(),
        "total_cars_parked": df["total_cars_parked"].iloc[-1],
    }
    return summary

def visualize_data(df, electric_chance, premium_chance, title, summary):
    fig, axes = plt.subplots(3, 2, figsize=(14, 12))  # Adding an extra row for the summary
    fig.canvas.manager.set_window_title(title)
    plt.subplots_adjust(hspace=0.5, wspace=0.3)

    summary_text = "\n".join([f"{key}: {value}" for key, value in summary.items()])
    axes[2, 0].axis("off")
    axes[2, 1].axis("off")
    axes[2, 0].text(0.5, 0.5, summary_text, fontsize=10, ha="center", va="center")
    axes[2, 0].set_title("Summary", fontsize=12)

    hours = df["time"] / 60  # Convert minutes to hours for x-axis labels

    axes[0, 0].plot(hours, df["parked_cars"], label="Parked Cars")
    axes[0, 0].plot(hours, df["waiting_cars"], label="Waiting Cars")
    axes[0, 0].set_title("Cars Parked and Waiting Over Time")
    axes[0, 0].set_xlabel("Hour of the Day")
    axes[0, 0].set_ylabel("Number of Cars")
    axes[0, 0].legend()
    axes[0, 0].grid(True)

    axes[0, 1].plot(hours, df["total_cars_parked"], label="Total Cars Parked", color="green")
    axes[0, 1].set_title("Total Cars Parked Over Time")
    axes[0, 1].set_xlabel("Hour of the Day")
    axes[0, 1].set_ylabel("Number of Cars")
    axes[0, 1].legend()
    axes[0, 1].grid(True)

    axes[1, 0].plot(hours, df["available_common_spots"], label="Available Common Spots")
    if electric_chance > 0:
        axes[1, 0].plot(hours, df["available_electric_spots"], label="Available Electric Spots")
    if premium_chance > 0:
        axes[1, 0].plot(hours, df["available_premium_spots"], label="Available Premium Spots")
    axes[1, 0].set_title("Availability of Parking Spots Over Time")
    axes[1, 0].set_xlabel("Hour of the Day")
    axes[1, 0].set_ylabel("Available Spots")
    axes[1, 0].legend()
    axes[1, 0].grid(True)

    if df["total_common_spots"].nunique() > 1:
        axes[1, 1].plot(hours, df["total_common_spots"], label="Total Common Spots")
        if electric_chance > 0:
            axes[1, 1].plot(hours, df["total_electric_spots"], label="Total Electric Spots")
        if premium_chance > 0:
            axes[1, 1].plot(hours, df["total_premium_spots"], label="Total Premium Spots")
        axes[1, 1].set_title("Total Parking Spots Over Time")
        axes[1, 1].set_xlabel("Hour of the Day")
        axes[1, 1].set_ylabel("Total Spots")
        axes[1, 1].legend()
        axes[1, 1].grid(True)
    else:
        axes[1, 1].axis("off")

    plt.show()

def run_pipeline():
    for mode, normal_chance, electric_chance, premium_chance in configurations:
        simulation = Simulation(
            width=20,
            height=20,
            total_spots=40,
            electric_percentage=electric_chance,
            premium_percentage=premium_chance,
            electric_chance=electric_chance,
            premium_chance=premium_chance,
            mode=mode
        )
        df = simulation.run_simulation()
        summary = analyze_data(df)
        title = f"{mode.value} - Normal: {normal_chance}, Electric: {electric_chance}, Premium: {premium_chance}"
        print(f"\nSummary for {title}")
        for key, value in summary.items():
            print(f"{key}: {value}")
        visualize_data(df, electric_chance, premium_chance, title, summary)
