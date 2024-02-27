import random

from ..skill import Skill
from ..dice_parser import DiceParser

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..character import Character


class SkillSelectionStrategy:
    def select_skill(self, character: "Character") -> Skill:
        raise NotImplementedError()


class RandomSkillSelectionStrategy(SkillSelectionStrategy):
    def select_skill(self, character: "Character") -> Skill:
        return random.choice(character.skills)


class ExpectedDamageMaximizationSkillSelectionStrategy(SkillSelectionStrategy):
    dice_parser = DiceParser()

    def select_skill(self, character: "Character") -> Skill:
        return max(
            character.skills,
            key=lambda skill: skill.success_rate
            / 100
            * ExpectedDamageMaximizationSkillSelectionStrategy.dice_parser.expected(
                skill.damage
            ),
        )
