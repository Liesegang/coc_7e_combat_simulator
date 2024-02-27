import unittest
from unittest.mock import patch, call
from coc7e_combat_simulator.character import Character
from coc7e_combat_simulator.skill import Skill
from coc7e_combat_simulator.combat_simulator import CombatSimulator, LevelOfSuccess
from coc7e_combat_simulator import dice_parser


class TestCombatSimulatorCalculateDamage(unittest.TestCase):
    def setUp(self):
        self.skill_non_physical_non_impale = Skill(
            name="Test Skill",
            success_rate=75,
            damage="1D8",
            physical_attack=False,
            impale=False,
        )
        self.skill_physical_non_impale = Skill(
            name="Test Skill",
            success_rate=75,
            damage="1D8",
            physical_attack=True,
            impale=False,
        )
        self.skill_non_physical_impale = Skill(
            name="Test Skill",
            success_rate=75,
            damage="1D8",
            physical_attack=False,
            impale=True,
        )
        self.skill_physical_impale = Skill(
            name="Test Skill",
            success_rate=75,
            damage="1D8",
            physical_attack=True,
            impale=True,
        )
        self.character = Character.of(
            name="Test Character",
            attribute_params={
                "strength": 70,
                "constitution": 60,
                "size": 70,
                "dexterity": 40,
                "appearance": 50,
                "intelligence": 60,
                "power": 50,
                "education": 60,
                "luck": 50,
            },
            skills=[
                self.skill_non_physical_non_impale,
                self.skill_physical_non_impale,
                self.skill_non_physical_impale,
                self.skill_physical_impale,
            ],
        )

    def test_calculate_damage_failure(self):
        damage = CombatSimulator.calculate_damage(
            self.character, self.skill_non_physical_non_impale, LevelOfSuccess.FAILURE
        )
        self.assertEqual(damage, 0)

    @patch("coc7e_combat_simulator.dice_parser.DiceParser.parse")
    def test_calculate_damage_success_non_physical_non_impale(self, mock_parse):
        mock_parse.side_effect = [(6, [])]

        damage = CombatSimulator.calculate_damage(
            self.character, self.skill_non_physical_non_impale, LevelOfSuccess.SUCCESS
        )
        self.assertEqual(damage, 6)

        expected_parse_calls = [call("1D8")]
        self.assertEqual(mock_parse.call_args_list, expected_parse_calls)

    @patch("coc7e_combat_simulator.dice_parser.DiceParser.parse")
    def test_calculate_damage_success_physical_non_impale(self, mock_parse):
        mock_parse.side_effect = [(6, []), (2, [])]

        damage = CombatSimulator.calculate_damage(
            self.character, self.skill_physical_non_impale, LevelOfSuccess.SUCCESS
        )
        self.assertEqual(damage, 8)

        expected_parse_calls = [call("1D8"), call("1d4")]
        self.assertEqual(mock_parse.call_args_list, expected_parse_calls)

    @patch("coc7e_combat_simulator.dice_parser.DiceParser.parse")
    def test_calculate_damage_hard_non_physical_non_impale(self, mock_parse):
        mock_parse.side_effect = [(6, [])]

        damage = CombatSimulator.calculate_damage(
            self.character, self.skill_non_physical_non_impale, LevelOfSuccess.HARD
        )
        self.assertEqual(damage, 6)

        expected_parse_calls = [call("1D8")]
        self.assertEqual(mock_parse.call_args_list, expected_parse_calls)

    @patch("coc7e_combat_simulator.dice_parser.DiceParser.parse")
    def test_calculate_damage_hard_physical_non_impale(self, mock_parse):
        mock_parse.side_effect = [(6, []), (2, [])]

        damage = CombatSimulator.calculate_damage(
            self.character, self.skill_physical_non_impale, LevelOfSuccess.HARD
        )
        self.assertEqual(damage, 8)

        expected_parse_calls = [call("1D8"), call("1d4")]
        self.assertEqual(mock_parse.call_args_list, expected_parse_calls)

    @patch("coc7e_combat_simulator.dice_parser.DiceParser.parse")
    def test_calculate_damage_special_non_physical_non_impale(self, mock_parse):
        mock_parse.side_effect = [(4, []), (6, [])]

        damage = CombatSimulator.calculate_damage(
            self.character, self.skill_non_physical_non_impale, LevelOfSuccess.SPECIAL
        )
        self.assertEqual(damage, 10)

        expected_parse_calls = [call("1D8"), call("1D8")]
        self.assertEqual(mock_parse.call_args_list, expected_parse_calls)

    @patch("coc7e_combat_simulator.dice_parser.DiceParser.parse")
    def test_calculate_damage_special_physical_non_impale(self, mock_parse):
        mock_parse.side_effect = [(4, []), (6, []), (2, []), (1, [])]

        damage = CombatSimulator.calculate_damage(
            self.character, self.skill_physical_non_impale, LevelOfSuccess.SPECIAL
        )
        self.assertEqual(damage, 13)

        expected_parse_calls = [call("1D8"), call("1D8"), call("1d4"), call("1d4")]
        self.assertEqual(mock_parse.call_args_list, expected_parse_calls)

    @patch("coc7e_combat_simulator.dice_parser.DiceParser.parse")
    def test_calculate_damage_special_non_physical_impale(self, mock_parse):
        mock_parse.side_effect = [(7, [])]

        damage = CombatSimulator.calculate_damage(
            self.character, self.skill_non_physical_impale, LevelOfSuccess.SPECIAL
        )
        self.assertEqual(damage, 15)

        expected_parse_calls = [call("1D8")]
        self.assertEqual(mock_parse.call_args_list, expected_parse_calls)

    @patch("coc7e_combat_simulator.dice_parser.DiceParser.parse")
    def test_calculate_damage_special_physical_impale(self, mock_parse):
        mock_parse.side_effect = [(4, []), (2, [])]

        damage = CombatSimulator.calculate_damage(
            self.character, self.skill_physical_impale, LevelOfSuccess.SPECIAL
        )
        self.assertEqual(damage, 18)

        expected_parse_calls = [call("1D8"), call("1d4")]
        self.assertEqual(mock_parse.call_args_list, expected_parse_calls)

    @patch("coc7e_combat_simulator.dice_parser.DiceParser.parse")
    def test_calculate_damage_critical_non_physical_non_impale(self, mock_parse):
        mock_parse.side_effect = [(8, []), (6, [])]

        damage = CombatSimulator.calculate_damage(
            self.character, self.skill_non_physical_non_impale, LevelOfSuccess.CRITICAL
        )
        self.assertEqual(damage, 14)

        expected_parse_calls = [call("1D8"), call("1D8")]
        self.assertEqual(mock_parse.call_args_list, expected_parse_calls)

    @patch("coc7e_combat_simulator.dice_parser.DiceParser.parse")
    def test_calculate_damage_critical_physical_non_impale(self, mock_parse):
        mock_parse.side_effect = [(4, []), (6, []), (2, []), (1, [])]

        damage = CombatSimulator.calculate_damage(
            self.character, self.skill_physical_non_impale, LevelOfSuccess.CRITICAL
        )
        self.assertEqual(damage, 13)

        expected_parse_calls = [call("1D8"), call("1D8"), call("1d4"), call("1d4")]
        self.assertEqual(mock_parse.call_args_list, expected_parse_calls)

    @patch("coc7e_combat_simulator.dice_parser.DiceParser.parse")
    def test_calculate_damage_critical_non_physical_impale(self, mock_parse):
        mock_parse.side_effect = [(7, [])]

        damage = CombatSimulator.calculate_damage(
            self.character, self.skill_non_physical_impale, LevelOfSuccess.CRITICAL
        )
        self.assertEqual(damage, 15)

        expected_parse_calls = [call("1D8")]
        self.assertEqual(mock_parse.call_args_list, expected_parse_calls)

    @patch("coc7e_combat_simulator.dice_parser.DiceParser.parse")
    def test_calculate_damage_critical_physical_impale(self, mock_parse):
        mock_parse.side_effect = [(4, []), (2, [])]

        damage = CombatSimulator.calculate_damage(
            self.character, self.skill_physical_impale, LevelOfSuccess.CRITICAL
        )
        self.assertEqual(damage, 18)

        expected_parse_calls = [call("1D8"), call("1d4")]
        self.assertEqual(mock_parse.call_args_list, expected_parse_calls)


if __name__ == "__main__":
    unittest.main()
