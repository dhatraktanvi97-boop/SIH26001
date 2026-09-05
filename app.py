from datetime import datetime


def receive_sensor_data(
    site_id,
    rainfall,
    soil_moisture,
    ground_movement,
    water_level
):
    """
    Receive sensor readings from a monitoring site
    and convert them into a standard data packet.
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
    
