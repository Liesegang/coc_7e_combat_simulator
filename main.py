from coc7e_combat_simulator.combat_simulator import CombatSimulator
from coc7e_combat_simulator.character import Character, FightBackReplyStrategy, MinimumHpTargetSelectionStrategy, RandomTargetSelectionStrategy, ExpectedDamageMaximizationSkillSelectionStrategy
from coc7e_combat_simulator.skill import FightingBrawl, FirearmHandgun

# group A has 4 members, group B has 3 members
# Status of all characters are generated randomly before every combat
def group_a_character_init():
    characters = [Character.of_random(f"A_{i}", skills=[FightingBrawl, FirearmHandgun]) for i in range(4)]
    for character in characters:
        character.skill_selection_strategy = ExpectedDamageMaximizationSkillSelectionStrategy()
        character.target_selection_strategy = MinimumHpTargetSelectionStrategy()
        character.reply_strategy = FightBackReplyStrategy()
    return characters

def group_b_character_init():
    characters = [Character.of_random(f"B_{i}", skills=[FightingBrawl]) for i in range(3)]
    for character in characters:
        character.target_selection_strategy = RandomTargetSelectionStrategy()
        character.reply_strategy = FightBackReplyStrategy()
    return characters

simulator = CombatSimulator(group_a_character_init, group_b_character_init)
results = simulator.simulate_multiple_combats(10000)
print(results)
