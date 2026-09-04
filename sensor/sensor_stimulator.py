import random
import time


def get_sensor_data():
    """Generate simulated sensor readings."""

    rainfall = round(random.uniform(0, 300), 2)
    soil_moisture = round(random.uniform(20, 100), 2)
    ground_movement = round(random.uniform(0, 20), 2)
    water_level = round(random.uniform(10, 100), 2)

    return {
        "rainfall": rainfall,
        "soil_moisture": soil_moisture,
        "ground_movement": ground_movement,
        "water_level": water_level
    }


if __name__ == "__main__":

    print("Sensor simulator started...")
    print("Generating automatic sensor readings...\n")

    while True:

        data = get_sensor_data()

        print(f"Rainfall:         {data['rainfall']} mm")
        print(f"Soil Moisture:    {data['soil_moisture']} %")
        print(f"Ground Movement:  {data['ground_movement']} mm")
        print(f"Water Level:      {data['water_level']} %")
        print("-" * 40)

        time.sleep(3)
        