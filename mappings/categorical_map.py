def safe_get(mapping, key):
    key = str(key).strip().lower()
    return mapping.get(key, 0.5)

weather_map = {
    "clear": 0.1,
    "sunny": 0.1,
    "windy": 0.5,
    "fog": 0.6,
    "foggy": 0.6,
    "rain": 0.9,
    "heavy rain": 1.0,
    "storm": 1.0,
}

light_map = {
    "daylight": 0.1,
    "bright": 0.1,
    "darkness-light lit": 0.4,
    "light lit": 0.4,
    "darkness-lights unlit": 0.8,
    "unlit": 0.8,
    "no lighting": 0.9,
}

road_map = {
    "dry": 0.1,
    "normal": 0.1,
    "wet": 0.5,
    "slippery": 0.6,
    "muddy": 0.8,
    "sand": 0.8,
    "flood": 1.0,
}

vehicle_type_map = {
    "car": 0.2,
    "van": 0.2,
    "bus": 0.5,
    "truck": 0.6,
    "motorcycle": 0.9,
}

brake_map = {
    "good": 0.1,
    "fair": 0.5,
    "average": 0.5,
    "poor": 0.9,
    "bad": 0.95,
}

time_map = {
    "morning": 0.4,
    "afternoon": 0.2,
    "evening": 0.7,
    "night": 0.8,
}

road_type_map = {
    "city road": 0.3,
    "one way": 0.2,
    "roundabout": 0.5,
    "slip road": 0.5,
    "highway": 0.4,
    "rural road": 0.6,
    "mountain road": 0.9,
}

road_defect_map = {
    "none": 0.1,
    "minor": 0.4,
    "potholes": 0.7,
    "severe": 0.9,
}

intersection_map = {
    "none": 0.1,
    "t-staggered": 0.5,
    "crossroads": 0.8,
}


def alcohol_map(value):
    try:
        value = float(value)
    except Exception:
        value = 0.0
    if value == 0:
        return 0.0
    if value < 0.3:
        return 0.5
    return 1.0
def normalize_inputs(data):
    return {
        "weather": safe_get(weather_map, data["weather_conditions"]),
        "lighting": safe_get(light_map, data["road_light_condition"]),
        "road": safe_get(road_map, data["road_conditions"]),
        "vehicle_type": safe_get(vehicle_type_map, data["vehicle_type"]),
        "brake": safe_get(brake_map, data["brake_condition"]),
        "time": safe_get(time_map, data["time_of_day"]),
        "road_type": safe_get(road_type_map, data["road_type"]),
        "road_defect": safe_get(road_defect_map, data["road_defect"]),
        "intersection": safe_get(intersection_map, data["intersection_related"]),
        "alcohol": alcohol_map(data["driver_alcohol"]),
    }