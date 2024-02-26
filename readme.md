# Call of Cthulhu 7th Edition Combat Simulator

This repository contains a Python-based combat simulator for the Call of Cthulhu 7th Edition table talk role-playing game. The simulator is designed to model the intricacies of combat scenarios in the CoC universe, taking into account character attributes, skills, and the random nature of dice rolls. It aims to provide a tool for game masters and players to quickly simulate combat outcomes between characters with defined attributes and skills.

## Features

- **Character Attributes**: Supports the full range of CoC 7th edition character attributes including Strength, Constitution, Size, Dexterity, Appearance, Intelligence, Power, Education, and Luck.
- **Damage Bonus and Build Calculation**: Automatically calculates a character's damage bonus and build based on their Strength and Size attributes.
- **Skill System**: Allows characters to have skills that affect their performance in combat, including success rates and damage potential.
- **Combat Simulation**: Simulates turn-based combat between two characters, considering skill success rates, damage calculation, and character health points (HP).

## Usage

To use the combat simulator, you will need Python 3.6 or later. Clone this repository to your local machine, navigate to the repository's directory, and run the simulator script from the command line.

### Prerequisites

- Python 3.6+

### Running a Simulation

1. **Define Characters**: Create character instances by specifying their attributes and skills. Use the provided `Character` and `Skill` classes for this purpose.

2. **Simulate Combat**: Call the `combat_simulation` function with two characters as arguments to simulate a combat scenario between them.

Example:

```python
from character import Character, Skill
from combat_simulation import combat_simulation

# Define character attributes and skills
attributes_char1 = {"strength": 50, "constitution": 60, "size": 55, "dexterity": 70, "appearance": 65, "intelligence": 80, "power": 45, "education": 70, "luck": 60}
skill_char1 = Skill(name="Punch", success_rate=50, damage="1d3")
char1 = Character.of(attributes_char1, [skill_char1])

attributes_char2 = {"strength": 65, "constitution": 70, "size": 60, "dexterity": 65, "appearance": 50, "intelligence": 75, "power": 55, "education": 65, "luck": 55}
skill_char2 = Skill(name="Knife Attack", success_rate=65, damage="1d4+2")
char2 = Character.of(attributes_char2, [skill_char2])

# Simulate combat
result = combat_simulation(char1, char2)
print(result)
```

## Customization

- **Character Creation**: You can customize characters further by adding or modifying skills and attributes as needed.
- **Combat Logic**: The combat simulation logic can be adjusted to incorporate additional factors like environmental effects, special abilities, or more complex skill interactions.

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