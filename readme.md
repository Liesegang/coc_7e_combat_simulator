# Call of Cthulhu 7th Edition Combat Simulator

This repository contains a Python-based combat simulator for the Call of Cthulhu 7th Edition table talk role-playing game. The simulator is designed to model the intricacies of combat scenarios in the CoC universe, taking into account character attributes, skills, and the random nature of dice rolls. It aims to provide a tool for game masters and players to quickly simulate combat outcomes between characters with defined attributes and skills.

## Features

- **Character Attributes**: Supports the full range of CoC 7th edition character attributes including Strength, Constitution, Size, Dexterity, Appearance, Intelligence, Power, Education, and Luck.
- **Damage Bonus Calculation**: Automatically calculates a character's damage bonus based on their Strength and Size attributes.
- **Skill System**: Allows characters to have skills that affect their performance in combat, including success rates and damage potential.
- **Combat Simulation**: Simulates turn-based combat between two characters, considering skill success rates, damage calculation, and character health points (HP).
- **Selection of Various Strategies**: This simulator allows for the customization of strategies in three different aspects. It is possible to select a different strategy for each character, and you can also customize your own strategies.
  - **Enemy Selection Strategy**: Three types have been implemented: random selection, priority to the enemy with the lowest HP, and priority to the enemy with the highest HP.
  - **Skill Selection Strategy**: Two types have been implemented: random selection, and selection of the skill with the maximum expected damage (expected damage x success rate of the skill).
  - **Fight Back or Dodge Strategy**: Three types have been implemented: always do nothing, always fight back, and always dodge.

## Usage

To use the combat simulator, you will need Python 3.6 or later. Clone this repository to your local machine, navigate to the repository's directory, and run the simulator script from the command line.

### Prerequisites

- Python 3.6+

### Running a Simulation

1. **Define Characters**: Create character instances by specifying their attributes and skills. Use the provided `Character` and `Skill` classes for this purpose.

2. **Simulate Combat**: Call the `combat_simulation` function with two characters as arguments to simulate a combat scenario between them.

Example:


```python
from coc7e_combat_simulator.combat_simulator import CombatSimulator
from coc7e_combat_simulator.character import Character
from coc7e_combat_simulator.strategies.skill_selection import ExpectedDamageMaximizationSkillSelectionStrategy
from coc7e_combat_simulator.strategies.target_selection import MaximumHpTargetSelectionStrategy, RandomTargetSelectionStrategy
from coc7e_combat_simulator.strategies.reaction import FightBackReactionStrategy
from coc7e_combat_simulator.skill import FightingBrawl, FirearmHandgun

# group A has 4 members, group B has 3 members
# Status of all characters are generated randomly before every combat
def group_a_character_init():
    characters = [Character.of_random(f"A_{i}", skills=[FightingBrawl, FirearmHandgun]) for i in range(4)]
    for character in characters:
        character.skill_selection_strategy = ExpectedDamageMaximizationSkillSelectionStrategy()
        character.target_selection_strategy = MaximumHpTargetSelectionStrategy()
        character.reply_strategy = FightBackReactionStrategy()
    return characters

def group_b_character_init():
    characters = [Character.of_random(f"B_{i}", skills=[FightingBrawl]) for i in range(3)]
    for character in characters:
        character.target_selection_strategy = RandomTargetSelectionStrategy()
        character.reply_strategy = FightBackReactionStrategy()
    return characters

simulator = CombatSimulator(group_a_character_init, group_b_character_init)
results = simulator.simulate_multiple_combats(10000)
print(results)

```

## Customization

- **Character Creation**: You can customize characters further by adding or modifying skills and attributes as needed.
- **Combat Strategy**: For each character, you can customize the strategy for choosing attack targets, selecting skills, and deciding whether to respond or evade.

## Contributing

Contributions to the combat simulator are welcome. Please feel free to fork the repository, make changes, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

### Copyright Notice

This project is a character simulator for Call of Cthulhu 7th Edition (CoC7e), a product of Chaosium Inc. and its Japanese version, "New Cthulhu Mythos TRPG". All rules, settings, translations, etc. are the property of Chaosium Inc. or "Arkwright Inc." and "KADOKAWA Co.

This simulator is an unofficial tool created by fans and is not directly related to Chaosium Inc.

This simulator is intended for personal and non-commercial use only.

The developer of this project would like to thank Chaosium Inc., Arkwright Inc. and KADOKAWA Inc. and expressly identifies itself as a fan of the CoC world. and KADOKAWA, Inc. and will make every effort not to infringe on their rights.

### Copyright

This work is a derivative work of the "New Cthulhu Mythos TRPG", the rights to which are owned by Arkwright, Inc. and KADOKAWA, Inc.

Call of Cthulhu is copyright ©1981, 2015, 2019 by Chaosium Inc. ;all rights reserved. Arranged by Arclight Inc.
Call of Cthulhu is a registered trademark of Chaosium Inc.
PUBLISHED BY KADOKAWA CORPORATION "新クトゥルフ神話TRPG ルールブック".

Simulator program: @liesegang