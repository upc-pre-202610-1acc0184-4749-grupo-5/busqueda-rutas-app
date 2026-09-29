import pandas as pd
import random

def apply_traffic_and_weight(hour_of_the_day):
    print(f"Calculating Barcelona's traffic for the {hour_of_the_day}:00 hours")

    streets = pd.read_csv("dataset/streets.csv")

    if hour_of_the_day in [7, 8, 9, 17, 18, 19]:
        print("Rush hour detected. Applying traffic factor of 3.0 to the streets.")
        base_factor = 3.0
    elif hour_of_the_day in [23, 0, 1, 2, 3, 4, 5]:
        print("Night time detected. Applying traffic factor of 1.0 to the streets.")
        base_factor = 1.0
    else:
        print("Normal traffic detected. Applying traffic factor of 1.5 to the streets.")
        base_factor = 1.5

    streets['traffic_factor'] = streets.apply(lambda row: base_factor * random.uniform(0.8, 1.2), axis=1)

    streets['final_weight'] = streets['length'] * streets['traffic_factor']

    streets.to_csv("dataset/streets_with_traffic.csv", index=False)
    print("Traffic factors and final weights have been applied and saved to 'dataset/streets_with_traffic.csv'.")

if __name__ == "__main__":
    simulate = 18
    apply_traffic_and_weight(simulate)