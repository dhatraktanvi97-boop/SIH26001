from datetime import datetime


def receive_sensor_data(
    site_id,
    rainfall,
    soil_moisture,
    ground_movement,
    water_level
):
    """
    Receives a sensor data packet from a monitoring site.

    In the physical system, this function will receive
    data sent by the field monitoring device.
    """

    packet = {
        "site_id": site_id,
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "rainfall": rainfall,
        "soil_moisture": soil_moisture,
        "ground_movement": ground_movement,
        "water_level": water_level
    }

    return packet