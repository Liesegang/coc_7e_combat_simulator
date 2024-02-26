from combat_simulator import CombatSimulator

# group A has 4 members, group B has 3 members
# Status of all characters are generated randomly before every combat
simulator = CombatSimulator(4, 3)
results = simulator.simulate_multiple_combats(100000)
print(results)
