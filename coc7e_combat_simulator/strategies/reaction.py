from enum import Enum

class ReactionType(Enum):
    NOTHING = 0
    DODGE = 1
    FIGHT_BACK = 2

class ReactionStrategy:
    def reply(self, character: "Character", attacker: "Character") -> ReactionType:
        raise NotImplementedError()

class NothingReactionStrategy(ReactionStrategy):
    def reply(self, character: "Character", attacker: "Character") -> ReactionType:
        return ReactionType.NOTHING

class DodgeReactionStrategy(ReactionStrategy):
    def reply(self, character: "Character", attacker: "Character") -> ReactionType:
        return ReactionType.DODGE

class FightBackReactionStrategy(ReactionStrategy):
    def reply(self, character: "Character", attacker: "Character") -> ReactionType:
        return ReactionType.FIGHT_BACK