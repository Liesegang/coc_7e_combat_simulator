from enum import Enum

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..character import Character


class ReactionType(Enum):
    NOTHING = 0
    DODGE = 1
    FIGHT_BACK = 2


class ReactionStrategy:
    def reaction(self, character: "Character", attacker: "Character") -> ReactionType:
        raise NotImplementedError()


class NothingReactionStrategy(ReactionStrategy):
    def reaction(self, character: "Character", attacker: "Character") -> ReactionType:
        return ReactionType.NOTHING


class DodgeReactionStrategy(ReactionStrategy):
    def reaction(self, character: "Character", attacker: "Character") -> ReactionType:
        return ReactionType.DODGE


class FightBackReactionStrategy(ReactionStrategy):
    def reaction(self, character: "Character", attacker: "Character") -> ReactionType:
        return ReactionType.FIGHT_BACK
