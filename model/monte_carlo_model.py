import random
from collections import Counter
from model.fuzzy_model import evaluate_fuzzy


SCENARIOS = {
    "Normal Urban Daytime Driving": {
        "driver_age": ("randint", 25, 50),
        "driver_experience": ("randint", 5, 20),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.90), (0.1, 0.10)]),
        "traffic_density": ("weighted_choice", [(0, 0.50), (1, 0.40), (2, 0.10)]),
        "vehicle_age": ("randint", 1, 10),
        "failure_history": ("weighted_choice", [(0.0, 0.80), (1.0, 0.20)]),
        "maintenance_required": ("weighted_choice", [(0.0, 0.80), (1.0, 0.20)]),
        "brake_condition": ("weighted_choice", [("good", 0.70), ("fair", 0.25), ("poor", 0.05)]),
        "weather": ("weighted_choice", [("clear", 0.45), ("sunny", 0.35), ("windy", 0.20)]),
        "lighting": ("weighted_choice", [("daylight", 0.80), ("bright", 0.20)]),
        "road_condition": ("weighted_choice", [("dry", 0.70), ("normal", 0.30)]),
        "time_of_day": ("weighted_choice", [("morning", 0.45), ("afternoon", 0.55)]),
        "road_type": ("weighted_choice", [("city road", 0.70), ("one way", 0.20), ("roundabout", 0.10)]),
    },

    "Nighttime Highway Travel": {
        "driver_age": ("randint", 25, 55),
        "driver_experience": ("randint", 3, 20),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.80), (0.1, 0.15), (0.4, 0.05)]),
        "traffic_density": ("weighted_choice", [(0, 0.15), (1, 0.45), (2, 0.40)]),
        "vehicle_age": ("randint", 2, 15),
        "failure_history": ("weighted_choice", [(0.0, 0.75), (1.0, 0.25)]),
        "maintenance_required": ("weighted_choice", [(0.0, 0.70), (1.0, 0.30)]),
        "brake_condition": ("weighted_choice", [("good", 0.55), ("fair", 0.35), ("poor", 0.10)]),
        "weather": ("weighted_choice", [("clear", 0.40), ("windy", 0.20), ("fog", 0.20), ("rain", 0.20)]),
        "lighting": ("weighted_choice", [("light lit", 0.40), ("darkness-lights unlit", 0.35), ("unlit", 0.25)]),
        "road_condition": ("weighted_choice", [("dry", 0.55), ("wet", 0.30), ("slippery", 0.15)]),
        "time_of_day": ("weighted_choice", [("evening", 0.45), ("night", 0.55)]),
        "road_type": ("weighted_choice", [("highway", 0.80), ("slip road", 0.20)]),
    },

    "Rainy High-Traffic Commute": {
        "driver_age": ("randint", 23, 55),
        "driver_experience": ("randint", 1, 18),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.92), (0.1, 0.08)]),
        "traffic_density": ("weighted_choice", [(1, 0.30), (2, 0.70)]),
        "vehicle_age": ("randint", 3, 16),
        "failure_history": ("weighted_choice", [(0.0, 0.70), (1.0, 0.30)]),
        "maintenance_required": ("weighted_choice", [(0.0, 0.60), (1.0, 0.40)]),
        "brake_condition": ("weighted_choice", [("good", 0.35), ("fair", 0.45), ("poor", 0.20)]),
        "weather": ("weighted_choice", [("rain", 0.60), ("heavy rain", 0.25), ("storm", 0.15)]),
        "lighting": ("weighted_choice", [("daylight", 0.35), ("light lit", 0.15), ("darkness-light lit", 0.25), ("unlit", 0.25)]),
        "road_condition": ("weighted_choice", [("wet", 0.50), ("slippery", 0.30), ("flood", 0.20)]),
        "time_of_day": ("weighted_choice", [("morning", 0.35), ("evening", 0.65)]),
        "road_type": ("weighted_choice", [("city road", 0.65), ("highway", 0.20), ("roundabout", 0.15)]),
    },

    "High-Risk Driver-Vehicle Condition": {
        "driver_age": ("randint", 18, 65),
        "driver_experience": ("randint", 0, 8),
        "driver_alcohol": ("weighted_choice", [(0.0, 0.40), (0.2, 0.25), (0.5, 0.35)]),
        "traffic_density": ("weighted_choice", [(1, 0.35), (2, 0.65)]),
        "vehicle_age": ("randint", 10, 21),
        "failure_history": ("weighted_choice", [(0.0, 0.25), (1.0, 0.75)]),
        "maintenance_required": ("weighted_choice", [(0.0, 0.20), (1.0, 0.80)]),
        "brake_condition": ("weighted_choice", [("fair", 0.45), ("poor", 0.55)]),
        "weather": ("weighted_choice", [("windy", 0.20), ("fog", 0.20), ("rain", 0.35), ("storm", 0.25)]),
        "lighting": ("weighted_choice", [("darkness-light lit", 0.25), ("darkness-lights unlit", 0.40), ("unlit", 0.35)]),
        "road_condition": ("weighted_choice", [("wet", 0.30), ("slippery", 0.35), ("muddy", 0.20), ("flood", 0.15)]),
        "time_of_day": ("weighted_choice", [("evening", 0.45), ("night", 0.55)]),
        "road_type": ("weighted_choice", [("highway", 0.30), ("rural road", 0.30), ("mountain road", 0.40)]),
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
    if scenario_name not in SCENARIOS:
        raise ValueError(f"Scenario '{scenario_name}' does not exist.")

    rules = SCENARIOS[scenario_name]
    generated = {}

    for field_name, rule in rules.items():
        generated[field_name] = generate_value(rule)

    return generated


def run_monte_carlo_simulation(scenario_name: str, iterations: int = 1000) -> dict:
    if iterations <= 0:
        raise ValueError("Iterations must be greater than 0.")

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
        "scenario": scenario_name,
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
    return list(SCENARIOS.keys())