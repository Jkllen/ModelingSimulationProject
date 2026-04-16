from model.monte_carlo_model import run_monte_carlo_simulation, generate_simulation_report

result = run_monte_carlo_simulation("Rainy High-Traffic Commute", 1000)
report = generate_simulation_report(result)

print(report)