import unittest
from unittest.mock import patch
from coc7e_combat_simulator.combat_simulator import LevelOfSuccess
from coc7e_combat_simulator.skill import Skill
from coc7e_combat_simulator.combat_simulator import CombatSimulator


class TestCombatSimulatorCheckLevelOfSuccess(unittest.TestCase):
    def setUp(self) -> None:
        self.combat_simulator = CombatSimulator(lambda: 0, lambda: 0)

    @patch("random.randint")
    def test_critical_success(self, mock_randint):
        mock_randint.return_value = 1
        skill = Skill(name="Skill1", damage="1D6", success_rate=70)
        self.assertEqual(
            self.combat_simulator.check_level_of_success(skill), LevelOfSuccess.CRITICAL
        )

    @patch("random.randint")
    def test_special_success(self, mock_randint):
        mock_randint.return_value = 14
        skill = Skill(name="Skill1", damage="1D6", success_rate=70)
        self.assertEqual(
            self.combat_simulator.check_level_of_success(skill), LevelOfSuccess.SPECIAL
        )

    @patch("random.randint")
    def test_hard_success(self, mock_randint):
        mock_randint.return_value = 35
        skill = Skill(name="Skill1", damage="1D6", success_rate=70)
        self.assertEqual(
            self.combat_simulator.check_level_of_success(skill), LevelOfSuccess.HARD
        )

    @patch("random.randint")
    def test_normal_success(self, mock_randint):
        mock_randint.return_value = 70
        skill = Skill(name="Skill1", damage="1D6", success_rate=70)
        self.assertEqual(
            self.combat_simulator.check_level_of_success(skill), LevelOfSuccess.SUCCESS
        )

    @patch("random.randint")
    def test_failure(self, mock_randint):
        mock_randint.return_value = 96
        skill = Skill(name="Skill1", damage="1D6", success_rate=50)
        self.assertEqual(
            self.combat_simulator.check_level_of_success(skill), LevelOfSuccess.FAILURE
        )

    @patch("random.randint")
    def test_fumble0(self, mock_randint):
        mock_randint.return_value = 96
        skill = Skill(name="Skill1", damage="1D6", success_rate=49)
        self.assertEqual(
            self.combat_simulator.check_level_of_success(skill), LevelOfSuccess.FUMBLE
        )

    @patch("random.randint")
    def test_fumble1(self, mock_randint):
        mock_randint.return_value = 100
        skill = Skill(name="Skill1", damage="1D6", success_rate=50)
        self.assertEqual(
            self.combat_simulator.check_level_of_success(skill), LevelOfSuccess.FUMBLE
        )

    @patch("random.randint")
    def test_fumble2(self, mock_randint):
        mock_randint.return_value = 100
        skill = Skill(name="Skill1", damage="1D6", success_rate=49)
        self.assertEqual(
            self.combat_simulator.check_level_of_success(skill), LevelOfSuccess.FUMBLE
        )

    @patch("random.randint")
    def test_fumble3(self, mock_randint):
        mock_randint.return_value = 100
        skill = Skill(name="Skill1", damage="1D6", success_rate=100)
        self.assertEqual(
            self.combat_simulator.check_level_of_success(skill), LevelOfSuccess.FUMBLE
        )


if __name__ == "__main__":
    unittest.main()
