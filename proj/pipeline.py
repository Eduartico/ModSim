import pandas as pd
import matplotlib.pyplot as plt
from simulation import Simulation, Modes
from collections import defaultdict

configurations = [
    ("Config 1", Modes.PRIORITY, 0.95, 0.05, 0),
    ("Config 2", Modes.PRIORITY, 0.9, 0.1, 0),
    ("Config 3", Modes.PRIORITY, 0.85, 0.15, 0),
    ("Config 1", Modes.ON_DEMAND, 0.95, 0.05, 0),
    ("Config 2", Modes.ON_DEMAND, 0.9, 0.1, 0),
    ("Config 3", Modes.ON_DEMAND, 0.85, 0.15, 0),
    ("Config 1", Modes.TIME_BASED, 0.95, 0.05, 0),
    ("Config 2", Modes.TIME_BASED, 0.9, 0.1, 0),
    ("Config 3", Modes.TIME_BASED, 0.85, 0.15, 0),
    ("Config 1", Modes.MEMBERSHIP, 0.9, 0.05, 0.05),
    ("Config 2", Modes.MEMBERSHIP, 0.8, 0.1, 0.1),
    ("Config 3", Modes.MEMBERSHIP, 0.7, 0.15, 0.15),
]

def analyze_data(df):
    total_parked_cars = df["total_cars_parked"].iloc[-1]
    max_waiting_cars = df["waiting_cars"].max()
    max_wait_time = df["time"][df["waiting_cars"].idxmax()] if max_waiting_cars > 0 else 0

    available_common_spots = (df["available_common_spots"] > 0).mean()
    available_electric_spots = (df["available_electric_spots"] > 0).mean()
    available_premium_spots = (df["available_premium_spots"] > 0).mean()

    total_earnings = df["earnings"].iloc[-1]

    summary = {
        "total_parked_cars": round(total_parked_cars, 2),
        "max_waiting_cars": round(max_waiting_cars, 2),
        "max_wait_time": round(max_wait_time, 2),
        "average_available_common_spots": round(available_common_spots, 2),
        "average_available_electric_spots": round(available_electric_spots, 2),
        "average_available_premium_spots": round(available_premium_spots, 2),
        "total_earnings": round(total_earnings, 2),
    }
    return summary


def visualize_model_results(results, model_title, include_total_spots):
    n_cols = 3 + int(include_total_spots)
    n_configs = len(results)
    fig, axes = plt.subplots(n_configs, n_cols, figsize=(6 * n_cols, 6 * n_configs))  # Adjusted display size
    fig.suptitle(f"Results for {model_title}", fontsize=12)  # Smaller title font
    if n_configs == 1:
        axes = [axes]  # Ensure axes is iterable for a single configuration

    for idx, (summary, df, electric_chance, premium_chance, title) in enumerate(results):
        # Filter the DataFrame to include only time >= 60
        df_filtered = df[df["time"] >= 60]
        hours = df_filtered["time"] / 60
        summary_text = "\n".join([f"{key}: {value}" for key, value in summary.items()])

        # Summary Text
        axes[idx][0].axis("off")
        axes[idx][0].text(0.5, 0.5, summary_text, fontsize=8, ha="center", va="center")  # Smaller text
        axes[idx][0].set_title(f"Summary: {title}", fontsize=10)  # Smaller font size

        # Earnings Over Time
        axes[idx][1].plot(hours, df_filtered["earnings"], label="Earnings")
        if idx == 0:
            axes[idx][1].set_title("Earnings Over Time", fontsize=10)  # Smaller font size
        axes[idx][1].set_xlabel("Hour of the Day", fontsize=8)
        axes[idx][1].set_ylabel("Earnings (€)", fontsize=8)
        axes[idx][1].legend(fontsize=8)
        axes[idx][1].grid(True)

        # Cars Parked and Waiting Over Time
        axes[idx][2].plot(hours, df_filtered["parked_cars"], label="Parked Cars")
        axes[idx][2].plot(hours, df_filtered["waiting_cars"], label="Waiting Cars")
        axes[idx][2].plot(
            hours,
            df_filtered["parked_cars"].rolling(window=20).median(),
            label="Rolling Median (Parked Cars)",
            linestyle="--"
        )
        axes[idx][2].plot(
            hours,
            df_filtered["waiting_cars"].rolling(window=20).median(),
            label="Rolling Median (Waiting Cars)",
            linestyle="--"
        )
        if idx == 0:
            axes[idx][2].set_title("Cars Parked and Waiting Over Time", fontsize=10)  # Smaller font size
        axes[idx][2].set_xlabel("Hour of the Day", fontsize=8)
        axes[idx][2].set_ylabel("Number of Cars", fontsize=8)
        axes[idx][2].legend(fontsize=8)
        axes[idx][2].grid(True)

        # Total Parking Spots Over Time
        if include_total_spots and df_filtered["total_common_spots"].nunique() > 1:
            axes[idx][3].plot(hours, df_filtered["total_common_spots"], label="Total Common Spots")
            if electric_chance > 0:
                axes[idx][3].plot(hours, df_filtered["total_electric_spots"], label="Total Electric Spots")
            if premium_chance > 0:
                axes[idx][3].plot(hours, df_filtered["total_premium_spots"], label="Total Premium Spots")
            if idx == 0:
                axes[idx][3].set_title("Total Parking Spots Over Time", fontsize=10)  # Smaller font size
            axes[idx][3].set_xlabel("Hour of the Day", fontsize=8)
            axes[idx][3].set_ylabel("Total Spots", fontsize=8)
            axes[idx][3].legend(fontsize=8)
            axes[idx][3].grid(True)

    plt.subplots_adjust(wspace=0.4, hspace=0.6)
    plt.tight_layout(rect=(0, 0, 1, 0.96))
    plt.show()


def visualize_combined_results(combined_data):
    n_configs = len(combined_data)
    fig, axes = plt.subplots(2 * n_configs, 2, figsize=(14, 6 * n_configs))

    if n_configs == 1:
        axes = [axes]

    for idx, (config_title, model_results) in enumerate(combined_data.items()):
        axes[idx * 2][0].axis("off")
        axes[idx * 2][0].text(0.5, 0.5, config_title, fontsize=10, ha="center", va="center")

        for df, model_title in [(result[1], result[2].split()[0]) for result in model_results]:
            df = df[df["time"] >= 60]
            hours = df["time"] / 60
            rolling_common = df["total_common_cars_parked"].rolling(window=30).median()
            rolling_electric = df["total_electric_cars_parked"].rolling(window=20).median()

            axes[idx * 2 + 1][0].plot(hours, rolling_common, label=f"{model_title}")
            axes[idx * 2 + 1][0].set_title("Common Cars Parked Over Time (Rolling Median)", fontsize=10)
            axes[idx * 2 + 1][0].set_xlabel("Hour of the Day", fontsize=8)
            axes[idx * 2 + 1][0].set_ylabel("Common Cars Parked", fontsize=8)
            axes[idx * 2 + 1][0].legend(fontsize=8, loc='upper left', bbox_to_anchor=(1, 1))
            axes[idx * 2 + 1][0].grid(True)

            axes[idx * 2 + 1][1].plot(hours, rolling_electric, label=f"{model_title}")
            if model_title == "Membership":
                rolling_premium = df["total_premium_cars_parked"].rolling(window=20).median()
                axes[idx * 2 + 1][1].plot(hours, rolling_premium, label=f"Membership - Premium")
            axes[idx * 2 + 1][1].set_title("Electric Cars Parked Over Time (Rolling Median)", fontsize=10)
            axes[idx * 2 + 1][1].set_xlabel("Hour of the Day", fontsize=8)
            axes[idx * 2 + 1][1].set_ylabel("Cars Parked", fontsize=8)
            axes[idx * 2 + 1][1].legend(fontsize=8, loc='upper left', bbox_to_anchor=(1, 1))
            axes[idx * 2 + 1][1].grid(True)

            axes[idx * 2][1].plot(hours, df["earnings"], label=f"{model_title}")
            axes[idx * 2][1].set_title("Earnings Over Time", fontsize=10)
            axes[idx * 2][1].set_xlabel("Hour of the Day", fontsize=8)
            axes[idx * 2][1].set_ylabel("Earnings (€)", fontsize=8)
            axes[idx * 2][1].legend(fontsize=8, loc='upper left', bbox_to_anchor=(1, 1))
            axes[idx * 2][1].grid(True)
    plt.tight_layout(rect=(0, 0, 0.85, 0.95))
    plt.subplots_adjust(wspace=0.5, hspace=0.98, right=0.85)
    plt.show()


def run_pipeline():
    model_results = defaultdict(list)
    combined_data = defaultdict(list)

    for config_title, mode, normal_chance, electric_chance, premium_chance in configurations:
        simulation = Simulation(
            width=12,
            height=12,
            total_spots=100,
            electric_percentage=electric_chance,
            premium_percentage=premium_chance,
            electric_chance=electric_chance,
            premium_chance=premium_chance,
            mode=mode,
            max_queue_len=20,
            cars_added_per_step=4,
            peak_hour_start=8,
            peak_hour_end=18
        )
        df = simulation.run_simulation()
        summary = analyze_data(df)
        title = f"{mode.value} - Normal: {normal_chance}, Electric: {electric_chance}, Premium: {premium_chance}"
        print(f"\nSummary for {title}")
        for key, value in summary.items():
            print(f"{key}: {value}")
        model_results[mode].append((summary, df, electric_chance, premium_chance, title))
        combined_data[config_title].append((summary, df, title))

    for mode, results in model_results.items():
        visualize_model_results(results, f"{mode.value} Model", include_total_spots=mode == Modes.ON_DEMAND)

    visualize_combined_results(combined_data)

