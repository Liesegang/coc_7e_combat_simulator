from coc7e_combat_simulator.combat_simulator import CombatSimulator
import unittest
from coc7e_combat_simulator.character import Character
from coc7e_combat_simulator.skill import FightingBrawl, FirearmHandgun


class TestSomeoneLeftAliveMoreComprehensive(unittest.TestCase):
    def setUp(self):
        self.combat_simulator = CombatSimulator(lambda: 0, lambda: 0)
        self.character_a_alive = Character.of(
            "Character A Alive",
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
            [FightingBrawl],
        )
        self.character_a_dead = Character.of(
            "Character A Dead",
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
            [FirearmHandgun],
        )
        self.character_b_alive = Character.of(
            "Character B Alive",
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
            [FirearmHandgun],
        )
        self.character_b_dead = Character.of(
            "Character B Dead",
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
            [FightingBrawl],
        )

        self.character_a_alive.side = "A"
        self.character_a_dead.side = "A"
        self.character_b_alive.side = "B"
        self.character_b_dead.side = "B"

        self.character_a_alive.hp = 10
        self.character_a_dead.hp = 0
        self.character_b_alive.hp = 10
        self.character_b_dead.hp = 0

    def test_someone_left_alive_side_a(self):
        characters = [
            self.character_a_alive,
            self.character_a_dead,
            self.character_b_alive,
            self.character_b_dead,
        ]
        self.assertTrue(
            self.combat_simulator.someone_left_alive(characters, "A"),
            "Should return True if at least one character from side A is alive.",
        )

    def test_no_one_left_alive_side_a(self):
        characters = [
            self.character_a_dead,
            self.character_b_alive,
            self.character_b_dead,
        ]
        self.assertFalse(
            self.combat_simulator.someone_left_alive(characters, "A"),
            "Should return False if no characters from side A are alive.",
        )


if __name__ == "__main__":
    unittest.main()
