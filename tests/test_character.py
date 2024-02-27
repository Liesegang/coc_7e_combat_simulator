import unittest
from coc7e_combat_simulator.character import Character, Attribute, Skill
from coc7e_combat_simulator.strategies.reaction import NothingReactionStrategy
from coc7e_combat_simulator.strategies.skill_selection import (
    RandomSkillSelectionStrategy,
)
from coc7e_combat_simulator.strategies.target_selection import (
    RandomTargetSelectionStrategy,
)


class TestCharacter(unittest.TestCase):
    def setUp(self):
        self.skills = [
            Skill("Skill 1", 50, "3D6", True),
            Skill("Skill 2", 70, "3D6", False),
            Skill("Skill 3", 30, "3D6", True),
        ]
        self.attributes = Attribute(
            strength=10,
            constitution=20,
            size=30,
            dexterity=40,
            appearance=50,
            intelligence=60,
            power=70,
            education=80,
            luck=90,
        )
        self.character = Character("Test Character", self.attributes, self.skills)

    def test_character_creation(self):
        self.assertEqual(self.character.name, "Test Character")
        self.assertEqual(self.character.attributes, self.attributes)
        self.assertEqual(self.character.skills, self.skills)
        self.assertEqual(self.character.hp, 5)  # (20 + 30) // 10 = 5
        self.assertEqual(self.character.mp, 14)  # 70 // 5 = 10
        self.assertEqual(self.character.db, "-2")  # calculate_db(10, 30) = "-2"
        self.assertIsNone(self.character.side)
        self.assertIsInstance(
            self.character.target_selection_strategy, RandomTargetSelectionStrategy
        )
        self.assertIsInstance(
            self.character.skill_selection_strategy, RandomSkillSelectionStrategy
        )
        self.assertIsInstance(self.character.reply_strategy, NothingReactionStrategy)

    def test_character_of_method(self):
        attribute_params = {
            "strength": 10,
            "constitution": 20,
            "size": 30,
            "dexterity": 40,
            "appearance": 50,
            "intelligence": 60,
            "power": 70,
            "education": 80,
            "luck": 90,
        }
        character = Character.of("Test Character", attribute_params, self.skills)
        self.assertEqual(character.name, "Test Character")
        self.assertEqual(character.attributes, self.attributes)
        self.assertEqual(character.skills, self.skills)

    def test_character_of_random_method(self):
        character = Character.of_random("Test Character", self.skills)
        self.assertEqual(character.name, "Test Character")
        self.assertIsInstance(character.attributes, Attribute)
        self.assertEqual(len(character.skills), 3)
        self.assertGreaterEqual(character.attributes.strength, 15)
        self.assertLessEqual(character.attributes.strength, 95)

    def test_roll_dice_method(self):
        result = Character.roll_dice(3, 6)
        self.assertGreaterEqual(result, 3)
        self.assertLessEqual(result, 18)

    def test_calculate_db_method(self):
        args = [
            [1, 1, "-2"],
            [32, 32, "-2"],
            [32, 33, "-1"],
            [42, 42, "-1"],
            [42, 43, "0"],
            [62, 62, "0"],
            [62, 63, "1d4"],
            [82, 82, "1d4"],
            [82, 83, "1d6"],
            [102, 102, "1d6"],
            [102, 103, "2d6"],
            [122, 122, "2d6"],
            [122, 123, "3d6"],
            [142, 142, "3d6"],
            [642, 643, "29d6"],
            [662, 662, "29d6"],
        ]
        for arg in args:
            result = Character.calculate_db(arg[0], arg[1])
            self.assertEqual(result, arg[2])

    def test_add_skill_method(self):
        new_skill = Skill("New Skill", 80, "3D6", True)
        self.character.add_skill(new_skill)
        self.assertIn(new_skill, self.character.skills)

    def test_add_skill_method_with_invalid_skill(self):
        with self.assertRaises(ValueError):
            self.character.add_skill("invalid")

    def test_repr_method(self):
        expected_repr = "Attributes: Attribute(strength=10, constitution=20, size=30, dexterity=40, " + \
            "appearance=50, intelligence=60, power=70, education=80, luck=90)\n" + \
            "HP: 5, MP: 14\n" + \
            "Skills: Skill 1: Success Rate: 50%, Damage: 3D6, " + \
            "Skill 2: Success Rate: 70%, Damage: 3D6, " + \
            "Skill 3: Success Rate: 30%, Damage: 3D6"
        self.assertEqual(repr(self.character), expected_repr)


if __name__ == "__main__":
    unittest.main()
