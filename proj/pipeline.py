import pandas as pd
import matplotlib.pyplot as plt
from simulation import Simulation, Modes

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

def run_pipeline():
    combined_results = []

    for config_title, mode, normal_chance, electric_chance, premium_chance in configurations:
        simulation = Simulation(
            width=55,
            height=14,
            total_spots=540,
            electric_percentage=electric_chance,
            premium_percentage=premium_chance,
            electric_chance=electric_chance,
            premium_chance=premium_chance,
            mode=mode,
            max_queue_len=54,
            cars_added_per_step=16,
            peak_hour_start=8,
            peak_hour_end=18
        )

        df, avg_wait_time = simulation.run_simulation()
        df = df.apply(pd.to_numeric, errors='ignore')  # Ensure numeric conversion where possible
        df["Configuration"] = config_title
        df["Mode"] = mode.value
        combined_results.append(df)

    # Combine all dataframes into one CSV
    full_data = pd.concat(combined_results, ignore_index=True)
    full_data.to_csv("full_simulation_results.csv", index=False)
    full_data = full_data[full_data["Configuration"] == "Config 3"]

    # Generate comparative graphs
    plt.figure(figsize=(10, 6))
    for mode in Modes:
        mode_data = full_data[full_data["Mode"] == mode.value]
        grouped = mode_data.groupby("time").mean(numeric_only=True)
        rolling_avg = grouped["total_common_cars_parked"].rolling(window=20).mean()
        plt.plot(grouped.index / 60, rolling_avg, label=f"{mode.value} - Common Cars (Rolling Avg)")
    plt.title("Common Cars Parked per Model")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Common Cars Parked")
    plt.legend()
    plt.grid(True)
    plt.savefig("common_cars_per_model.png")

    plt.figure(figsize=(10, 6))
    for mode in Modes:
        mode_data = full_data[(full_data["Mode"] == mode.value)]
        grouped = mode_data.groupby("time").mean(numeric_only=True)
        rolling_avg_electric = grouped["total_electric_cars_parked"].rolling(window=20).mean()
        plt.plot(grouped.index / 60, rolling_avg_electric, label=f"{mode.value} - Electric Cars")
        if mode.value == "Membership":
            rolling_avg_premium = grouped["total_premium_cars_parked"].rolling(window=20).mean()
            plt.plot(grouped.index / 60, rolling_avg_premium, linestyle="--", label=f"{mode.value} - Premium Cars")
    plt.title("Electric and Premium Cars Parked per Model (Rolling Average)")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Cars Parked")
    plt.legend()
    plt.grid(True)
    plt.savefig("electric_premium_cars_per_model.png")

    plt.figure(figsize=(10, 6))
    total_earnings = full_data.groupby("Mode").last()["earnings"]
    total_earnings.plot(kind="bar")
    plt.title("Total Earnings per Model")
    plt.xlabel("Model")
    plt.ylabel("Total Earnings (€)")
    plt.grid(True)
    plt.savefig("total_earnings_config3.png")

if __name__ == "__main__":
    run_pipeline()
