import unittest
from coc7e_combat_simulator.strategies.skill_selection import ExpectedDamageMaximizationSkillSelectionStrategy
from coc7e_combat_simulator.character import Character
from coc7e_combat_simulator.skill import Skill

class TestSkillSelection(unittest.TestCase):
    def setUp(self):
        self.strategy = ExpectedDamageMaximizationSkillSelectionStrategy()

    def test_select_skill_damage(self):
        skill1 = Skill("Skill1", 50, "2d6+3", False)
        skill2 = Skill("Skill2", 50, "1d8+2", True)
        skill3 = Skill("Skill3", 50, "3d4+1", False)
        character = Character.of_random("Test", skills=[skill1, skill2, skill3])

        selected_skill = self.strategy.select_skill(character)
        self.assertEqual(selected_skill, skill1)

    def test_select_skill_chance(self):
        skill1 = Skill("Skill1", 10, "3D6", False)
        skill2 = Skill("Skill2", 20, "3D6", True)
        skill3 = Skill("Skill3", 30, "3D6", False)
        character = Character.of_random("Test", skills=[skill1, skill2, skill3])

        selected_skill = self.strategy.select_skill(character)
        self.assertEqual(selected_skill, skill3)

if __name__ == '__main__':
    unittest.main()
