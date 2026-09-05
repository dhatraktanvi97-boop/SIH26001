from datetime import datetime


def get_risk_level(score):
    if score >= 70:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    return "LOW"


def calculate_hazard_scores(
    rainfall,
    soil_moisture,
    ground_movement,
    water_level
):
    landslide_score = min(
        100,
        rainfall * 0.40
        + soil_moisture * 0.25
        + ground_movement * 2.5
    )

    flood_score = min(
        100,
        rainfall * 0.50
        + water_level * 0.50
    )

    ground_collapse_score = min(
        100,
        ground_movement * 3.0
        + soil_moisture * 0.40
    )

    return {
        "Landslide": round(landslide_score, 2),
        "Flood": round(flood_score, 2),
        "Ground Collapse": round(ground_collapse_score, 2)
    }


def generate_alert(site_id, scores):
    highest_hazard = max(scores, key=scores.get)
    highest_score = scores[highest_hazard]

    level = get_risk_level(highest_score)

    if level == "HIGH":
        message = (
            f"CRITICAL ALERT: {highest_hazard} risk is HIGH "
            f"at monitoring site {site_id}."
        )

    elif level == "MEDIUM":
        message = (
            f"WARNING: {highest_hazard} risk is MEDIUM "
            f"at monitoring site {site_id}."
        )

    else:
        message = (
            f"System monitoring normal at {site_id}. "
            f"No immediate hazard detected."
        )

    return {
        "site_id": site_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hazard": highest_hazard,
        "score": round(highest_score, 2),
        "level": level,
        "message": message
    }


def check_alert(
    site_id,
    rainfall,
    soil_moisture,
    ground_movement,
    water_level
):
    scores = calculate_hazard_scores(
        rainfall,
        soil_moisture,
        ground_movement,
        water_level
    )

    alert = generate_alert(site_id, scores)

    return scores, alert
  
