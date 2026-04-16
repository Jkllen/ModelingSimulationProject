import random
from collections import Counter
from model.fuzzy_model import evaluate_fuzzy


SCENARIOS = {

    "Typical Driving Condition (Baseline)": {
        "driver_age": ("randint", 25, 55),
        "driver_experience": ("randint", 5, 25),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.95), (0.1, 0.05)]),

        "traffic_density": ("weighted_choice", [(1, 0.42), (0, 0.29), (2, 0.29)]),

        "vehicle_age": ("randint", 1, 12),
        "failure_history": ("weighted_choice", [(0.0, 0.60), (1.0, 0.40)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.76), (0.0, 0.24)]),

        "brake_condition": ("weighted_choice", [("good", 0.50), ("poor", 0.30), ("fair", 0.20)]),

        "weather": ("weighted_choice", [("clear", 0.50), ("sunny", 0.30), ("rain", 0.10), ("windy", 0.10)]),

        "lighting": ("weighted_choice", [("daylight", 0.70), ("light lit", 0.20), ("unlit", 0.10)]),

        "road_condition": ("weighted_choice", [("dry", 0.42), ("normal", 0.40), ("wet", 0.10), ("slippery", 0.08)]),

        "time_of_day": ("weighted_choice", [("morning", 0.40), ("afternoon", 0.35), ("evening", 0.15), ("night", 0.10)]),

        "road_type": ("weighted_choice", [("city road", 0.40), ("highway", 0.30), ("rural road", 0.30)]),
    },


    "Moderate Urban Risk Scenario": {
        "driver_age": ("randint", 20, 60),
        "driver_experience": ("randint", 3, 15),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.90), (0.1, 0.10)]),

        "traffic_density": ("weighted_choice", [(1, 0.45), (2, 0.40), (0, 0.15)]),

        "vehicle_age": ("randint", 5, 15),
        "failure_history": ("weighted_choice", [(1.0, 0.50), (0.0, 0.50)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.80), (0.0, 0.20)]),

        "brake_condition": ("weighted_choice", [("good", 0.40), ("fair", 0.35), ("poor", 0.25)]),

        "weather": ("weighted_choice", [("clear", 0.40), ("rain", 0.30), ("windy", 0.30)]),

        "lighting": ("weighted_choice", [("daylight", 0.60), ("light lit", 0.25), ("unlit", 0.15)]),

        "road_condition": ("weighted_choice", [("dry", 0.40), ("wet", 0.30), ("slippery", 0.30)]),

        "time_of_day": ("weighted_choice", [("morning", 0.30), ("evening", 0.40), ("night", 0.30)]),

        "road_type": ("weighted_choice", [("city road", 0.60), ("highway", 0.25), ("roundabout", 0.15)]),
    },


    "Environmental Hazard Scenario": {
        "driver_age": ("randint", 25, 60),
        "driver_experience": ("randint", 5, 20),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.95), (0.1, 0.05)]),

        "traffic_density": ("weighted_choice", [(1, 0.40), (2, 0.40), (0, 0.20)]),

        "vehicle_age": ("randint", 5, 18),
        "failure_history": ("weighted_choice", [(0.0, 0.50), (1.0, 0.50)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.75), (0.0, 0.25)]),

        "brake_condition": ("weighted_choice", [("good", 0.35), ("fair", 0.40), ("poor", 0.25)]),

        "weather": ("weighted_choice", [("rain", 0.50), ("heavy rain", 0.25), ("storm", 0.25)]),

        "lighting": ("weighted_choice", [("daylight", 0.40), ("light lit", 0.20), ("unlit", 0.40)]),

        "road_condition": ("weighted_choice", [("wet", 0.50), ("slippery", 0.30), ("flood", 0.20)]),

        "time_of_day": ("weighted_choice", [("evening", 0.40), ("night", 0.40), ("morning", 0.20)]),

        "road_type": ("weighted_choice", [("city road", 0.40), ("highway", 0.30), ("rural road", 0.30)]),
    },


    "High Driver-Vehicle Risk Scenario": {
        "driver_age": ("randint", 18, 60),
        "driver_experience": ("randint", 0, 8),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.40), (0.2, 0.30), (0.5, 0.30)]),

        "traffic_density": ("weighted_choice", [(2, 0.60), (1, 0.40)]),

        "vehicle_age": ("randint", 10, 21),
        "failure_history": ("weighted_choice", [(1.0, 0.70), (0.0, 0.30)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.85), (0.0, 0.15)]),

        "brake_condition": ("weighted_choice", [("poor", 0.55), ("fair", 0.35), ("good", 0.10)]),

        "weather": ("weighted_choice", [("rain", 0.40), ("storm", 0.30), ("windy", 0.30)]),

        "lighting": ("weighted_choice", [("unlit", 0.50), ("darkness-light lit", 0.30), ("daylight", 0.20)]),

        "road_condition": ("weighted_choice", [("slippery", 0.40), ("wet", 0.30), ("flood", 0.30)]),

        "time_of_day": ("weighted_choice", [("evening", 0.40), ("night", 0.60)]),

        "road_type": ("weighted_choice", [("highway", 0.30), ("rural road", 0.30), ("mountain road", 0.40)]),
    },
}

DETAILED_SCENARIOS = {
    "Morning City Commute in Light Rain": {
        "driver_age": ("randint", 28, 45),
        "driver_experience": ("randint", 5, 15),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.98), (0.1, 0.02)]),
        "traffic_density": ("weighted_choice", [(1, 0.75), (2, 0.25)]),
        "vehicle_age": ("randint", 5, 10),
        "failure_history": ("weighted_choice", [(0.0, 0.70), (1.0, 0.30)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.60), (0.0, 0.40)]),
        "brake_condition": ("weighted_choice", [("fair", 0.70), ("good", 0.20), ("poor", 0.10)]),
        "weather": ("weighted_choice", [("rain", 0.80), ("heavy rain", 0.20)]),
        "lighting": ("weighted_choice", [("daylight", 0.85), ("light lit", 0.15)]),
        "road_condition": ("weighted_choice", [("wet", 0.75), ("slippery", 0.25)]),
        "time_of_day": ("weighted_choice", [("morning", 1.0)]),
        "road_type": ("weighted_choice", [("city road", 1.0)]),
    },

    "Morning School Drop-Off in Heavy Traffic": {
        "driver_age": ("randint", 30, 50),
        "driver_experience": ("randint", 7, 20),
        "driver_alcohol": ("weighted_choice", [(0.0, 1.0)]),
        "traffic_density": ("weighted_choice", [(2, 0.80), (1, 0.20)]),
        "vehicle_age": ("randint", 3, 12),
        "failure_history": ("weighted_choice", [(0.0, 0.75), (1.0, 0.25)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.55), (0.0, 0.45)]),
        "brake_condition": ("weighted_choice", [("good", 0.55), ("fair", 0.35), ("poor", 0.10)]),
        "weather": ("weighted_choice", [("clear", 0.50), ("sunny", 0.30), ("rain", 0.20)]),
        "lighting": ("weighted_choice", [("daylight", 1.0)]),
        "road_condition": ("weighted_choice", [("dry", 0.60), ("normal", 0.25), ("wet", 0.15)]),
        "time_of_day": ("weighted_choice", [("morning", 1.0)]),
        "road_type": ("weighted_choice", [("city road", 0.80), ("roundabout", 0.20)]),
    },

    "Afternoon City Drive under Clear Weather": {
        "driver_age": ("randint", 25, 50),
        "driver_experience": ("randint", 5, 18),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.97), (0.1, 0.03)]),
        "traffic_density": ("weighted_choice", [(1, 0.60), (0, 0.25), (2, 0.15)]),
        "vehicle_age": ("randint", 2, 10),
        "failure_history": ("weighted_choice", [(0.0, 0.80), (1.0, 0.20)]),
        "maintenance_required": ("weighted_choice", [(0.0, 0.50), (1.0, 0.50)]),
        "brake_condition": ("weighted_choice", [("good", 0.65), ("fair", 0.25), ("poor", 0.10)]),
        "weather": ("weighted_choice", [("clear", 0.70), ("sunny", 0.30)]),
        "lighting": ("weighted_choice", [("daylight", 1.0)]),
        "road_condition": ("weighted_choice", [("dry", 0.75), ("normal", 0.25)]),
        "time_of_day": ("weighted_choice", [("afternoon", 1.0)]),
        "road_type": ("weighted_choice", [("city road", 1.0)]),
    },

    "Evening Rush Hour on a Busy City Road": {
        "driver_age": ("randint", 24, 55),
        "driver_experience": ("randint", 3, 15),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.93), (0.1, 0.07)]),
        "traffic_density": ("weighted_choice", [(2, 0.70), (1, 0.30)]),
        "vehicle_age": ("randint", 4, 14),
        "failure_history": ("weighted_choice", [(0.0, 0.60), (1.0, 0.40)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.70), (0.0, 0.30)]),
        "brake_condition": ("weighted_choice", [("fair", 0.45), ("good", 0.35), ("poor", 0.20)]),
        "weather": ("weighted_choice", [("clear", 0.45), ("windy", 0.20), ("rain", 0.35)]),
        "lighting": ("weighted_choice", [("daylight", 0.20), ("light lit", 0.50), ("unlit", 0.30)]),
        "road_condition": ("weighted_choice", [("dry", 0.40), ("wet", 0.35), ("slippery", 0.25)]),
        "time_of_day": ("weighted_choice", [("evening", 1.0)]),
        "road_type": ("weighted_choice", [("city road", 1.0)]),
    },

    "Night Highway Drive with Poor Brakes": {
        "driver_age": ("randint", 22, 50),
        "driver_experience": ("randint", 2, 12),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.80), (0.2, 0.10), (0.5, 0.10)]),
        "traffic_density": ("weighted_choice", [(1, 0.45), (2, 0.55)]),
        "vehicle_age": ("randint", 8, 18),
        "failure_history": ("weighted_choice", [(1.0, 0.60), (0.0, 0.40)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.80), (0.0, 0.20)]),
        "brake_condition": ("weighted_choice", [("poor", 0.70), ("fair", 0.30)]),
        "weather": ("weighted_choice", [("clear", 0.30), ("rain", 0.35), ("fog", 0.20), ("windy", 0.15)]),
        "lighting": ("weighted_choice", [("unlit", 0.50), ("darkness-light lit", 0.30), ("light lit", 0.20)]),
        "road_condition": ("weighted_choice", [("dry", 0.35), ("wet", 0.35), ("slippery", 0.30)]),
        "time_of_day": ("weighted_choice", [("night", 1.0)]),
        "road_type": ("weighted_choice", [("highway", 1.0)]),
    },

    "Late Night Highway Travel in Fog": {
        "driver_age": ("randint", 25, 55),
        "driver_experience": ("randint", 4, 16),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.85), (0.1, 0.10), (0.4, 0.05)]),
        "traffic_density": ("weighted_choice", [(0, 0.20), (1, 0.50), (2, 0.30)]),
        "vehicle_age": ("randint", 5, 16),
        "failure_history": ("weighted_choice", [(0.0, 0.55), (1.0, 0.45)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.70), (0.0, 0.30)]),
        "brake_condition": ("weighted_choice", [("fair", 0.45), ("good", 0.30), ("poor", 0.25)]),
        "weather": ("weighted_choice", [("fog", 0.70), ("foggy", 0.30)]),
        "lighting": ("weighted_choice", [("unlit", 0.55), ("darkness-light lit", 0.30), ("light lit", 0.15)]),
        "road_condition": ("weighted_choice", [("wet", 0.45), ("slippery", 0.35), ("dry", 0.20)]),
        "time_of_day": ("weighted_choice", [("night", 1.0)]),
        "road_type": ("weighted_choice", [("highway", 1.0)]),
    },

    "Heavy Rain Trip during Peak Traffic": {
        "driver_age": ("randint", 25, 52),
        "driver_experience": ("randint", 3, 14),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.96), (0.1, 0.04)]),
        "traffic_density": ("weighted_choice", [(2, 0.75), (1, 0.25)]),
        "vehicle_age": ("randint", 5, 15),
        "failure_history": ("weighted_choice", [(0.0, 0.50), (1.0, 0.50)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.75), (0.0, 0.25)]),
        "brake_condition": ("weighted_choice", [("fair", 0.45), ("poor", 0.35), ("good", 0.20)]),
        "weather": ("weighted_choice", [("heavy rain", 0.70), ("storm", 0.30)]),
        "lighting": ("weighted_choice", [("light lit", 0.35), ("unlit", 0.35), ("daylight", 0.30)]),
        "road_condition": ("weighted_choice", [("wet", 0.45), ("slippery", 0.35), ("flood", 0.20)]),
        "time_of_day": ("weighted_choice", [("morning", 0.30), ("evening", 0.70)]),
        "road_type": ("weighted_choice", [("city road", 0.65), ("highway", 0.35)]),
    },

    "Stormy Evening Drive with Flooded Roads": {
        "driver_age": ("randint", 28, 58),
        "driver_experience": ("randint", 5, 20),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.95), (0.1, 0.05)]),
        "traffic_density": ("weighted_choice", [(1, 0.45), (2, 0.40), (0, 0.15)]),
        "vehicle_age": ("randint", 6, 18),
        "failure_history": ("weighted_choice", [(0.0, 0.45), (1.0, 0.55)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.80), (0.0, 0.20)]),
        "brake_condition": ("weighted_choice", [("poor", 0.35), ("fair", 0.45), ("good", 0.20)]),
        "weather": ("weighted_choice", [("storm", 0.65), ("heavy rain", 0.35)]),
        "lighting": ("weighted_choice", [("light lit", 0.30), ("unlit", 0.40), ("darkness-light lit", 0.30)]),
        "road_condition": ("weighted_choice", [("flood", 0.55), ("slippery", 0.25), ("wet", 0.20)]),
        "time_of_day": ("weighted_choice", [("evening", 1.0)]),
        "road_type": ("weighted_choice", [("city road", 0.50), ("highway", 0.20), ("rural road", 0.30)]),
    },

    "Rural Road Trip with an Old Vehicle": {
        "driver_age": ("randint", 30, 60),
        "driver_experience": ("randint", 6, 22),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.94), (0.1, 0.06)]),
        "traffic_density": ("weighted_choice", [(0, 0.45), (1, 0.40), (2, 0.15)]),
        "vehicle_age": ("randint", 12, 21),
        "failure_history": ("weighted_choice", [(1.0, 0.65), (0.0, 0.35)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.80), (0.0, 0.20)]),
        "brake_condition": ("weighted_choice", [("fair", 0.50), ("poor", 0.30), ("good", 0.20)]),
        "weather": ("weighted_choice", [("clear", 0.45), ("windy", 0.20), ("rain", 0.35)]),
        "lighting": ("weighted_choice", [("daylight", 0.50), ("unlit", 0.35), ("light lit", 0.15)]),
        "road_condition": ("weighted_choice", [("dry", 0.35), ("wet", 0.30), ("slippery", 0.20), ("muddy", 0.15)]),
        "time_of_day": ("weighted_choice", [("afternoon", 0.35), ("evening", 0.45), ("night", 0.20)]),
        "road_type": ("weighted_choice", [("rural road", 1.0)]),
    },

    "Evening Rural Drive with Low Visibility": {
        "driver_age": ("randint", 27, 58),
        "driver_experience": ("randint", 5, 18),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.90), (0.1, 0.08), (0.4, 0.02)]),
        "traffic_density": ("weighted_choice", [(0, 0.35), (1, 0.45), (2, 0.20)]),
        "vehicle_age": ("randint", 8, 18),
        "failure_history": ("weighted_choice", [(1.0, 0.55), (0.0, 0.45)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.75), (0.0, 0.25)]),
        "brake_condition": ("weighted_choice", [("fair", 0.50), ("poor", 0.30), ("good", 0.20)]),
        "weather": ("weighted_choice", [("fog", 0.35), ("rain", 0.35), ("windy", 0.30)]),
        "lighting": ("weighted_choice", [("unlit", 0.55), ("darkness-light lit", 0.30), ("light lit", 0.15)]),
        "road_condition": ("weighted_choice", [("wet", 0.35), ("slippery", 0.30), ("muddy", 0.20), ("dry", 0.15)]),
        "time_of_day": ("weighted_choice", [("evening", 1.0)]),
        "road_type": ("weighted_choice", [("rural road", 1.0)]),
    },

    "Mountain Road Travel under Hazardous Conditions": {
        "driver_age": ("randint", 25, 55),
        "driver_experience": ("randint", 2, 12),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.92), (0.1, 0.06), (0.5, 0.02)]),
        "traffic_density": ("weighted_choice", [(0, 0.40), (1, 0.45), (2, 0.15)]),
        "vehicle_age": ("randint", 7, 18),
        "failure_history": ("weighted_choice", [(1.0, 0.55), (0.0, 0.45)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.80), (0.0, 0.20)]),
        "brake_condition": ("weighted_choice", [("poor", 0.35), ("fair", 0.45), ("good", 0.20)]),
        "weather": ("weighted_choice", [("fog", 0.30), ("rain", 0.35), ("storm", 0.20), ("windy", 0.15)]),
        "lighting": ("weighted_choice", [("daylight", 0.30), ("unlit", 0.40), ("darkness-light lit", 0.30)]),
        "road_condition": ("weighted_choice", [("slippery", 0.40), ("wet", 0.25), ("muddy", 0.20), ("flood", 0.15)]),
        "time_of_day": ("weighted_choice", [("evening", 0.50), ("night", 0.30), ("morning", 0.20)]),
        "road_type": ("weighted_choice", [("mountain road", 1.0)]),
    },

    "Weekend Highway Trip with an Aging Vehicle": {
        "driver_age": ("randint", 28, 55),
        "driver_experience": ("randint", 5, 20),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.88), (0.1, 0.08), (0.4, 0.04)]),
        "traffic_density": ("weighted_choice", [(1, 0.55), (2, 0.30), (0, 0.15)]),
        "vehicle_age": ("randint", 10, 20),
        "failure_history": ("weighted_choice", [(1.0, 0.60), (0.0, 0.40)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.75), (0.0, 0.25)]),
        "brake_condition": ("weighted_choice", [("fair", 0.50), ("poor", 0.25), ("good", 0.25)]),
        "weather": ("weighted_choice", [("clear", 0.50), ("windy", 0.20), ("rain", 0.30)]),
        "lighting": ("weighted_choice", [("daylight", 0.60), ("light lit", 0.20), ("unlit", 0.20)]),
        "road_condition": ("weighted_choice", [("dry", 0.45), ("wet", 0.30), ("slippery", 0.25)]),
        "time_of_day": ("weighted_choice", [("morning", 0.35), ("afternoon", 0.35), ("evening", 0.30)]),
        "road_type": ("weighted_choice", [("highway", 1.0)]),
    },

    "Short City Errand with Low Traffic": {
        "driver_age": ("randint", 25, 50),
        "driver_experience": ("randint", 4, 20),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.99), (0.1, 0.01)]),
        "traffic_density": ("weighted_choice", [(0, 0.70), (1, 0.30)]),
        "vehicle_age": ("randint", 1, 10),
        "failure_history": ("weighted_choice", [(0.0, 0.85), (1.0, 0.15)]),
        "maintenance_required": ("weighted_choice", [(0.0, 0.60), (1.0, 0.40)]),
        "brake_condition": ("weighted_choice", [("good", 0.70), ("fair", 0.25), ("poor", 0.05)]),
        "weather": ("weighted_choice", [("clear", 0.60), ("sunny", 0.25), ("windy", 0.15)]),
        "lighting": ("weighted_choice", [("daylight", 0.85), ("light lit", 0.15)]),
        "road_condition": ("weighted_choice", [("dry", 0.80), ("normal", 0.20)]),
        "time_of_day": ("weighted_choice", [("morning", 0.35), ("afternoon", 0.65)]),
        "road_type": ("weighted_choice", [("city road", 1.0)]),
    },

    "After-Work Drive Home with Light Rain": {
        "driver_age": ("randint", 24, 52),
        "driver_experience": ("randint", 3, 16),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.94), (0.1, 0.06)]),
        "traffic_density": ("weighted_choice", [(2, 0.60), (1, 0.40)]),
        "vehicle_age": ("randint", 4, 14),
        "failure_history": ("weighted_choice", [(0.0, 0.60), (1.0, 0.40)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.65), (0.0, 0.35)]),
        "brake_condition": ("weighted_choice", [("fair", 0.45), ("good", 0.35), ("poor", 0.20)]),
        "weather": ("weighted_choice", [("rain", 0.75), ("heavy rain", 0.25)]),
        "lighting": ("weighted_choice", [("light lit", 0.45), ("darkness-light lit", 0.30), ("unlit", 0.25)]),
        "road_condition": ("weighted_choice", [("wet", 0.65), ("slippery", 0.35)]),
        "time_of_day": ("weighted_choice", [("evening", 1.0)]),
        "road_type": ("weighted_choice", [("city road", 0.85), ("one way", 0.15)]),
    },

    "Commuter Drive with Fair Brakes and Wet Roads": {
        "driver_age": ("randint", 26, 50),
        "driver_experience": ("randint", 4, 14),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.97), (0.1, 0.03)]),
        "traffic_density": ("weighted_choice", [(1, 0.60), (2, 0.40)]),
        "vehicle_age": ("randint", 6, 14),
        "failure_history": ("weighted_choice", [(0.0, 0.55), (1.0, 0.45)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.70), (0.0, 0.30)]),
        "brake_condition": ("weighted_choice", [("fair", 0.75), ("poor", 0.15), ("good", 0.10)]),
        "weather": ("weighted_choice", [("rain", 0.60), ("windy", 0.20), ("clear", 0.20)]),
        "lighting": ("weighted_choice", [("daylight", 0.50), ("light lit", 0.30), ("unlit", 0.20)]),
        "road_condition": ("weighted_choice", [("wet", 0.70), ("slippery", 0.30)]),
        "time_of_day": ("weighted_choice", [("morning", 0.45), ("evening", 0.55)]),
        "road_type": ("weighted_choice", [("city road", 0.70), ("highway", 0.30)]),
    },

    "Low-Experience Driver on a Night Trip": {
        "driver_age": ("randint", 18, 25),
        "driver_experience": ("randint", 0, 3),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.85), (0.2, 0.10), (0.5, 0.05)]),
        "traffic_density": ("weighted_choice", [(1, 0.50), (2, 0.35), (0, 0.15)]),
        "vehicle_age": ("randint", 3, 12),
        "failure_history": ("weighted_choice", [(0.0, 0.65), (1.0, 0.35)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.60), (0.0, 0.40)]),
        "brake_condition": ("weighted_choice", [("fair", 0.50), ("good", 0.30), ("poor", 0.20)]),
        "weather": ("weighted_choice", [("clear", 0.35), ("rain", 0.35), ("fog", 0.15), ("windy", 0.15)]),
        "lighting": ("weighted_choice", [("unlit", 0.50), ("darkness-light lit", 0.30), ("light lit", 0.20)]),
        "road_condition": ("weighted_choice", [("dry", 0.35), ("wet", 0.35), ("slippery", 0.30)]),
        "time_of_day": ("weighted_choice", [("night", 1.0)]),
        "road_type": ("weighted_choice", [("city road", 0.45), ("highway", 0.35), ("rural road", 0.20)]),
    },

    "Older Driver in High Traffic during Rain": {
        "driver_age": ("randint", 56, 70),
        "driver_experience": ("randint", 15, 35),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.98), (0.1, 0.02)]),
        "traffic_density": ("weighted_choice", [(2, 0.70), (1, 0.30)]),
        "vehicle_age": ("randint", 6, 16),
        "failure_history": ("weighted_choice", [(0.0, 0.55), (1.0, 0.45)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.70), (0.0, 0.30)]),
        "brake_condition": ("weighted_choice", [("fair", 0.45), ("good", 0.30), ("poor", 0.25)]),
        "weather": ("weighted_choice", [("rain", 0.75), ("heavy rain", 0.25)]),
        "lighting": ("weighted_choice", [("daylight", 0.45), ("light lit", 0.30), ("unlit", 0.25)]),
        "road_condition": ("weighted_choice", [("wet", 0.65), ("slippery", 0.35)]),
        "time_of_day": ("weighted_choice", [("morning", 0.30), ("evening", 0.70)]),
        "road_type": ("weighted_choice", [("city road", 0.60), ("highway", 0.40)]),
    },

    "Delivery Van in Moderate Traffic on Wet Roads": {
        "driver_age": ("randint", 25, 50),
        "driver_experience": ("randint", 3, 12),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.99), (0.1, 0.01)]),
        "traffic_density": ("weighted_choice", [(1, 0.65), (2, 0.25), (0, 0.10)]),
        "vehicle_age": ("randint", 5, 14),
        "failure_history": ("weighted_choice", [(1.0, 0.50), (0.0, 0.50)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.70), (0.0, 0.30)]),
        "brake_condition": ("weighted_choice", [("fair", 0.50), ("good", 0.30), ("poor", 0.20)]),
        "weather": ("weighted_choice", [("rain", 0.55), ("clear", 0.20), ("windy", 0.25)]),
        "lighting": ("weighted_choice", [("daylight", 0.55), ("light lit", 0.25), ("unlit", 0.20)]),
        "road_condition": ("weighted_choice", [("wet", 0.70), ("slippery", 0.20), ("dry", 0.10)]),
        "time_of_day": ("weighted_choice", [("morning", 0.40), ("afternoon", 0.40), ("evening", 0.20)]),
        "road_type": ("weighted_choice", [("city road", 0.70), ("one way", 0.10), ("highway", 0.20)]),
    },

    "Highway Drive after Light Drinking": {
        "driver_age": ("randint", 24, 45),
        "driver_experience": ("randint", 3, 12),
        "driver_alcohol": ("weighted_choice", [(0.2, 0.65), (0.5, 0.20), (0.0, 0.15)]),
        "traffic_density": ("weighted_choice", [(1, 0.50), (2, 0.35), (0, 0.15)]),
        "vehicle_age": ("randint", 4, 12),
        "failure_history": ("weighted_choice", [(0.0, 0.60), (1.0, 0.40)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.60), (0.0, 0.40)]),
        "brake_condition": ("weighted_choice", [("fair", 0.45), ("good", 0.35), ("poor", 0.20)]),
        "weather": ("weighted_choice", [("clear", 0.40), ("windy", 0.20), ("rain", 0.40)]),
        "lighting": ("weighted_choice", [("light lit", 0.30), ("unlit", 0.40), ("darkness-light lit", 0.30)]),
        "road_condition": ("weighted_choice", [("dry", 0.35), ("wet", 0.35), ("slippery", 0.30)]),
        "time_of_day": ("weighted_choice", [("evening", 0.40), ("night", 0.60)]),
        "road_type": ("weighted_choice", [("highway", 1.0)]),
    },

    "Bad Weather Night Drive with Maintenance Issues": {
        "driver_age": ("randint", 25, 55),
        "driver_experience": ("randint", 2, 10),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.85), (0.2, 0.10), (0.5, 0.05)]),
        "traffic_density": ("weighted_choice", [(1, 0.45), (2, 0.40), (0, 0.15)]),
        "vehicle_age": ("randint", 10, 21),
        "failure_history": ("weighted_choice", [(1.0, 0.70), (0.0, 0.30)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.90), (0.0, 0.10)]),
        "brake_condition": ("weighted_choice", [("poor", 0.45), ("fair", 0.40), ("good", 0.15)]),
        "weather": ("weighted_choice", [("rain", 0.40), ("storm", 0.35), ("fog", 0.25)]),
        "lighting": ("weighted_choice", [("unlit", 0.55), ("darkness-light lit", 0.30), ("light lit", 0.15)]),
        "road_condition": ("weighted_choice", [("wet", 0.35), ("slippery", 0.35), ("flood", 0.30)]),
        "time_of_day": ("weighted_choice", [("night", 1.0)]),
        "road_type": ("weighted_choice", [("highway", 0.35), ("rural road", 0.35), ("mountain road", 0.30)]),
    },

    "Clear-Day Highway Travel with Good Vehicle Condition": {
        "driver_age": ("randint", 28, 52),
        "driver_experience": ("randint", 8, 22),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.99), (0.1, 0.01)]),
        "traffic_density": ("weighted_choice", [(0, 0.25), (1, 0.55), (2, 0.20)]),
        "vehicle_age": ("randint", 1, 8),
        "failure_history": ("weighted_choice", [(0.0, 0.90), (1.0, 0.10)]),
        "maintenance_required": ("weighted_choice", [(0.0, 0.70), (1.0, 0.30)]),
        "brake_condition": ("weighted_choice", [("good", 0.80), ("fair", 0.18), ("poor", 0.02)]),
        "weather": ("weighted_choice", [("clear", 0.65), ("sunny", 0.35)]),
        "lighting": ("weighted_choice", [("daylight", 0.90), ("light lit", 0.10)]),
        "road_condition": ("weighted_choice", [("dry", 0.85), ("normal", 0.15)]),
        "time_of_day": ("weighted_choice", [("morning", 0.35), ("afternoon", 0.65)]),
        "road_type": ("weighted_choice", [("highway", 1.0)]),
    },

    "Old Vehicle in Nighttime Mountain Travel": {
        "driver_age": ("randint", 26, 56),
        "driver_experience": ("randint", 3, 12),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.90), (0.1, 0.07), (0.4, 0.03)]),
        "traffic_density": ("weighted_choice", [(0, 0.45), (1, 0.40), (2, 0.15)]),
        "vehicle_age": ("randint", 14, 21),
        "failure_history": ("weighted_choice", [(1.0, 0.70), (0.0, 0.30)]),
        "maintenance_required": ("weighted_choice", [(1.0, 0.85), (0.0, 0.15)]),
        "brake_condition": ("weighted_choice", [("poor", 0.40), ("fair", 0.40), ("good", 0.20)]),
        "weather": ("weighted_choice", [("fog", 0.30), ("rain", 0.30), ("storm", 0.20), ("windy", 0.20)]),
        "lighting": ("weighted_choice", [("unlit", 0.60), ("darkness-light lit", 0.25), ("light lit", 0.15)]),
        "road_condition": ("weighted_choice", [("slippery", 0.40), ("wet", 0.25), ("muddy", 0.20), ("flood", 0.15)]),
        "time_of_day": ("weighted_choice", [("night", 1.0)]),
        "road_type": ("weighted_choice", [("mountain road", 1.0)]),
    },
}


def weighted_choice(options):
    values = [value for value, _ in options]
    weights = [weight for _, weight in options]
    return random.choices(values, weights=weights, k=1)[0]


def generate_value(rule):
    rule_type = rule[0]

    if rule_type == "randint":
        _, minimum, maximum = rule
        return random.randint(minimum, maximum)

    if rule_type == "uniform":
        _, minimum, maximum = rule
        return round(random.uniform(minimum, maximum), 2)

    if rule_type == "weighted_choice":
        _, options = rule
        return weighted_choice(options)

    raise ValueError(f"Unsupported rule type: {rule_type}")


def generate_inputs_for_scenario(scenario_name: str) -> dict:
    clean_name = scenario_name.replace("[General] ", "").replace("[Detailed] ", "")

    if clean_name in SCENARIOS:
        rules = SCENARIOS[clean_name]
    elif clean_name in DETAILED_SCENARIOS:
        rules = DETAILED_SCENARIOS[clean_name]
    else:
        raise ValueError(f"Scenario '{scenario_name}' does not exist.")

    generated = {}

    for field_name, rule in rules.items():
        generated[field_name] = generate_value(rule)

    return generated


def run_monte_carlo_simulation(scenario_name: str, iterations: int = 1000) -> dict:
    if iterations <= 0:
        raise ValueError("Iterations must be greater than 0.")

    clean_name = scenario_name.replace("[General] ", "").replace("[Detailed] ", "")

    risk_counts = Counter()
    all_scores = []
    reason_counts = Counter()
    sample_inputs = []

    for i in range(iterations):
        inputs = generate_inputs_for_scenario(scenario_name)
        score, risk_level, reasons, recommendations = evaluate_fuzzy(inputs)

        risk_counts[risk_level] += 1
        all_scores.append(score)

        for reason in reasons:
            reason_counts[reason] += 1

        if i < 5:
            sample_inputs.append({
                "trial": i + 1,
                "inputs": inputs,
                "risk_level": risk_level,
                "score": round(score, 4),
            })

    average_score = sum(all_scores) / len(all_scores)
    min_score = min(all_scores)
    max_score = max(all_scores)

    low_count = risk_counts.get("Low Risk", 0)
    medium_count = risk_counts.get("Medium Risk", 0)
    high_count = risk_counts.get("High Risk", 0)

    top_reasons = reason_counts.most_common(5)

    return {
        "scenario": clean_name,
        "iterations": iterations,
        "average_score": average_score,
        "min_score": min_score,
        "max_score": max_score,
        "low_count": low_count,
        "medium_count": medium_count,
        "high_count": high_count,
        "low_probability": low_count / iterations,
        "medium_probability": medium_count / iterations,
        "high_probability": high_count / iterations,
        "top_reasons": top_reasons,
        "sample_trials": sample_inputs,
    }


def generate_simulation_report(result: dict) -> str:
    top_reasons_text = "\n".join(
        f"- {reason} ({count} occurrences)"
        for reason, count in result["top_reasons"]
    ) or "- No dominant reasons recorded."

    sample_trials_text = "\n\n".join(
        [
            f"Trial {trial['trial']}\n"
            f"Inputs: {trial['inputs']}\n"
            f"Risk Level: {trial['risk_level']}\n"
            f"Risk Score: {trial['score']:.2f}"
            for trial in result["sample_trials"]
        ]
    ) or "No sample trials available."

    return f"""
=== MONTE CARLO SCENARIO-BASED SIMULATION REPORT ===

Scenario: {result['scenario']}
Iterations: {result['iterations']}

--- RISK DISTRIBUTION ---
Low Risk: {result['low_count']} ({result['low_probability'] * 100:.2f}%)
Medium Risk: {result['medium_count']} ({result['medium_probability'] * 100:.2f}%)
High Risk: {result['high_count']} ({result['high_probability'] * 100:.2f}%)

--- SCORE SUMMARY ---
Average Risk Score: {result['average_score']:.4f}
Minimum Risk Score: {result['min_score']:.4f}
Maximum Risk Score: {result['max_score']:.4f}

--- MOST FREQUENT RISK REASONS ---
{top_reasons_text}

--- SAMPLE TRIALS ---
{sample_trials_text}

=====================================================
""".strip()


def get_available_scenarios() -> list[str]:
    general = [f"[General] {name}" for name in SCENARIOS.keys()]
    detailed = [f"[Detailed] {name}" for name in DETAILED_SCENARIOS.keys()]
    return general + detailed