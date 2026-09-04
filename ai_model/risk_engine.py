def calculate_risk(rainfall, soil_moisture, ground_movement, water_level):

    landslide = (
        rainfall * 0.4 +
        soil_moisture * 0.3 +
        ground_movement * 5 * 0.3
    )

    flood = (
        rainfall * 0.5 +
        water_level * 0.5
    )

    mine_collapse = (
        ground_movement * 5 * 0.6 +
        soil_moisture * 0.4
    )

    return {
        "Landslide": round(landslide, 2),
        "Flood": round(flood, 2),
        "Mine Collapse": round(mine_collapse, 2)
    }


def risk_level(score):

    if score >= 70:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    else:
        return "LOW"



        