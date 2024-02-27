import unittest
from coc7e_combat_simulator.strategies.target_selection import (
    MaximumHpTargetSelectionStrategy,
    MinimumHpTargetSelectionStrategy,
)
from coc7e_combat_simulator.character import Character


class TestMinimumHpTargetSelectionStrategy(unittest.TestCase):
    def setUp(self):
        self.strategy = MinimumHpTargetSelectionStrategy()

    def test_select_target(self):
        # Create some test characters
        main_character = Character.of_random("main", [])
        main_character.side = "A"
        opponent1 = Character.of(
            "opponent_1",
            {
                "strength": 50,
                "constitution": 50,
                "size": 50,
                "dexterity": 50,
                "appearance": 50,
                "intelligence": 50,
                "power": 50,
                "education": 50,
                "luck": 50,
            },
            [],
        )
        opponent2 = Character.of(
            "opponent_2",
            {
                "strength": 50,
                "constitution": 50,
                "size": 60,
                "dexterity": 50,
                "appearance": 50,
                "intelligence": 50,
                "power": 50,
                "education": 50,
                "luck": 50,
            },
            [],
        )
        opponent3 = Character.of(
            "opponent_3",
            {
                "strength": 50,
                "constitution": 50,
                "size": 70,
                "dexterity": 50,
                "appearance": 50,
                "intelligence": 50,
                "power": 50,
                "education": 50,
                "luck": 50,
            },
            [],
        )
        opponents = [opponent1, opponent2, opponent3]
        for opponent in opponents:
            opponent.side = "B"

        selected_target = self.strategy.select_target(main_character, opponents)
        self.assertEqual(selected_target, opponent1)


class TestMaximumHpTargetSelectionStrategy(unittest.TestCase):
    def setUp(self):
        self.strategy = MaximumHpTargetSelectionStrategy()

    def test_select_target(self):
        # Create some test characters
        main_character = Character.of_random("main", [])
        main_character.side = "A"
        opponent1 = Character.of(
            "opponent_1",
            {
                "strength": 50,
                "constitution": 50,
                "size": 50,
                "dexterity": 50,
                "appearance": 50,
                "intelligence": 50,
                "power": 50,
                "education": 50,
                "luck": 50,
            },
            [],
        )
        opponent2 = Character.of(
            "opponent_2",
            {
                "strength": 50,
                "constitution": 50,
                "size": 60,
                "dexterity": 50,
                "appearance": 50,
                "intelligence": 50,
                "power": 50,
                "education": 50,
                "luck": 50,
            },
            [],
        )
        opponent3 = Character.of(
            "opponent_3",
            {
                "strength": 50,
                "constitution": 50,
                "size": 70,
                "dexterity": 50,
                "appearance": 50,
                "intelligence": 50,
                "power": 50,
                "education": 50,
                "luck": 50,
            },
            [],
        )
        opponents = [opponent1, opponent2, opponent3]
        for opponent in opponents:
            opponent.side = "B"

        selected_target = self.strategy.select_target(main_character, opponents)
        self.assertEqual(selected_target, opponent3)


if __name__ == "__main__":
    unittest.main()
