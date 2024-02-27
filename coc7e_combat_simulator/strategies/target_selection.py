import random
from typing import List

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..character import Character


class TargetSelectionStrategy:
    def select_target(
        self, character: "Character", characters: List["Character"]
    ) -> "Character":
        raise NotImplementedError()


class RandomTargetSelectionStrategy(TargetSelectionStrategy):
    def select_target(
        self, character: "Character", characters: List["Character"]
    ) -> "Character":
        target_candidates = [
            target
            for target in characters
            if target.side != character.side and target.hp > 0
        ]
        return random.choice(target_candidates)


class MinimumHpTargetSelectionStrategy(TargetSelectionStrategy):
    def select_target(
        self, character: "Character", characters: List["Character"]
    ) -> "Character":
        target_candidates = [
            target
            for target in characters
            if target.side != character.side and target.hp > 0
        ]
        return min(target_candidates, key=lambda target: target.hp)


class MaximumHpTargetSelectionStrategy(TargetSelectionStrategy):
    def select_target(
        self, character: "Character", characters: List["Character"]
    ) -> "Character":
        target_candidates = [
            target
            for target in characters
            if target.side != character.side and target.hp > 0
        ]
        return max(target_candidates, key=lambda target: target.hp)
