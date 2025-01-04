import pandas as pd
import matplotlib.pyplot as plt
from simulation import Simulation, Modes
from collections import defaultdict

configurations = [
    (Modes.PRIORITY, 0.95, 0.05, 0),
    (Modes.PRIORITY, 0.9, 0.1, 0),
    (Modes.PRIORITY, 0.85, 0.15, 0),
    (Modes.ON_DEMAND, 0.95, 0.05, 0),
    (Modes.ON_DEMAND, 0.9, 0.1, 0),
    (Modes.ON_DEMAND, 0.85, 0.15, 0),
]

def analyze_data(df):
    summary = {
        "total_parked_cars": df["parked_cars"].iloc[-1],
        "max_waiting_cars": df["waiting_cars"].max(),
        "average_available_common_spots": df["available_common_spots"].mean(),
        "average_available_electric_spots": df["available_electric_spots"].mean(),
        "average_available_premium_spots": df["available_premium_spots"].mean(),
    }
    return summary

def visualize_model_results(results, model_title, include_total_spots):
    n_cols = 3 + int(include_total_spots)
    n_configs = len(results)
    fig, axes = plt.subplots(n_configs, n_cols, figsize=(5 * n_cols, 5 * n_configs))
    fig.suptitle(f"Results for {model_title}", fontsize=14)
    if n_configs == 1:
        axes = [axes]  # Ensure axes is iterable for a single configuration

    for idx, (summary, df, electric_chance, premium_chance, title) in enumerate(results):
        hours = df["time"] / 60
        summary_text = "\n".join([f"{key}: {value}" for key, value in summary.items()])
        axes[idx][0].axis("off")
        axes[idx][0].text(0.5, 0.5, summary_text, fontsize=8, ha="center", va="center")
        axes[idx][0].set_title(f"Summary: {title}", fontsize=10)

        axes[idx][1].plot(hours, df["parked_cars"], label="Parked Cars")
        axes[idx][1].plot(hours, df["waiting_cars"], label="Waiting Cars")
        axes[idx][1].set_title("Cars Parked and Waiting Over Time")
        axes[idx][1].set_xlabel("Hour of the Day")
        axes[idx][1].set_ylabel("Number of Cars")
        axes[idx][1].legend()
        axes[idx][1].grid(True)

        axes[idx][2].plot(hours, df["available_common_spots"], label="Available Common Spots")
        if electric_chance > 0:
            axes[idx][2].plot(hours, df["available_electric_spots"], label="Available Electric Spots")
        if premium_chance > 0:
            axes[idx][2].plot(hours, df["available_premium_spots"], label="Available Premium Spots")
        axes[idx][2].set_title("Availability of Parking Spots Over Time")
        axes[idx][2].set_xlabel("Hour of the Day")
        axes[idx][2].set_ylabel("Available Spots")
        axes[idx][2].legend()
        axes[idx][2].grid(True)

        if include_total_spots and df["total_common_spots"].nunique() > 1:
            axes[idx][3].plot(hours, df["total_common_spots"], label="Total Common Spots")
            if electric_chance > 0:
                axes[idx][3].plot(hours, df["total_electric_spots"], label="Total Electric Spots")
            if premium_chance > 0:
                axes[idx][3].plot(hours, df["total_premium_spots"], label="Total Premium Spots")
            axes[idx][3].set_title("Total Parking Spots Over Time")
            axes[idx][3].set_xlabel("Hour of the Day")
            axes[idx][3].set_ylabel("Total Spots")
            axes[idx][3].legend()
            axes[idx][3].grid(True)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

def visualize_combined_results(combined_data):
    n_configs = len(combined_data)
    fig, axes = plt.subplots(n_configs, 4, figsize=(20, 5 * n_configs))
    fig.suptitle("Combined Results for Shared Configurations", fontsize=14)

    if n_configs == 1:
        axes = [axes]

    for idx, (config, model_results) in enumerate(combined_data.items()):
        config_text = f"Configuration: Normal: {config[0]}, Electric: {config[1]}, Premium: {config[2]}"
        axes[idx][0].axis("off")
        axes[idx][0].text(0.5, 0.5, config_text, fontsize=8, ha="center", va="center")
        axes[idx][0].set_title("Configuration Details", fontsize=10)

        for df, model_title in [(result[1], result[2].split()[0]) for result in model_results]:
            hours = df["time"] / 60
            axes[idx][1].plot(hours, df["parked_cars"], label=model_title)
            axes[idx][2].plot(hours, df["available_common_spots"], label=model_title)
            if "available_electric_spots" in df:
                axes[idx][3].plot(hours, df["available_electric_spots"], label=model_title)

        axes[idx][1].set_title("Parked Cars")
        axes[idx][1].set_xlabel("Hour of the Day")
        axes[idx][1].set_ylabel("Waiting Cars")
        axes[idx][1].legend()
        axes[idx][1].grid(True)

        axes[idx][2].set_title("Availability of Common Spots Over Time")
        axes[idx][2].set_xlabel("Hour of the Day")
        axes[idx][2].set_ylabel("Available Spots")
        axes[idx][2].legend()
        axes[idx][2].grid(True)

        axes[idx][3].set_title("Availability of Electric Spots Over Time")
        axes[idx][3].set_xlabel("Hour of the Day")
        axes[idx][3].set_ylabel("Available Electric Spots")
        axes[idx][3].legend()
        axes[idx][3].grid(True)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

def run_pipeline():
    model_results = defaultdict(list)
    combined_data = defaultdict(list)

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
        model_results[mode].append((summary, df, electric_chance, premium_chance, title))

        combined_key = (normal_chance, electric_chance, premium_chance)
        combined_data[combined_key].append((summary, df, title))

    for mode, results in model_results.items():
        visualize_model_results(results, f"{mode.value} Model", include_total_spots=mode == Modes.ON_DEMAND)

    visualize_combined_results(combined_data)
