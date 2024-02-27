from enum import IntEnum
import random
import logging
from typing import List, Callable
import tqdm

from .strategies.reaction import ReactionType
from .character import Character
from .skill import Skill, FightingBrawl
from .dice_parser import DiceParser

logger = logging.getLogger(__name__)
dice_parser = DiceParser()


class LevelOfSuccess(IntEnum):
    CRITICAL = 5
    SPECIAL = 4
    HARD = 3
    SUCCESS = 2
    FAILURE = 1
    FUMBLE = 0


class CombatSimulator:
    def __init__(
        self,
        group_a_characters_init_strategy: Callable[[], List[Character]],
        group_b_characters_init_strategy: Callable[[], List[Character]],
    ):
        self.group_a_characters_init_strategy = group_a_characters_init_strategy
        self.group_b_characters_init_strategy = group_b_characters_init_strategy

    @staticmethod
    def calculate_damage(
        character: Character, skill: Skill, success_level: LevelOfSuccess
    ) -> int:
        logger.info(f"{character.name} in side {character.side} used {skill.name}.")
        if success_level <= LevelOfSuccess.FAILURE:
            logger.info(f"{character.name} in side {character.side} failed.")
            return 0

        if success_level <= LevelOfSuccess.HARD:
            logger.info(f"{character.name} in side {character.side} succeeded with hard.")
            damage_result = dice_parser.parse(skill.damage)[0]
            if skill.physical_attack:
                damage_result += dice_parser.parse(character.db)[0]
            return damage_result

        if success_level <= LevelOfSuccess.CRITICAL:
            logger.info(f"{character.name} in side {character.side} succeeded with critical.")
            if skill.impale:
                damage_result = dice_parser.maximum(skill.damage) + dice_parser.parse(skill.damage)[0]
                if skill.physical_attack:
                    damage_result += dice_parser.maximum(character.db) + dice_parser.parse(character.db)[0]
                return damage_result
            else:
                damage_result = dice_parser.parse(skill.damage)[0] + dice_parser.parse(skill.damage)[0]
                if skill.physical_attack:
                    damage_result += dice_parser.parse(character.db)[0] + dice_parser.parse(character.db)[0]
                return damage_result

    @staticmethod
    def check_level_of_success(skill: Skill) -> LevelOfSuccess:
        roll = random.randint(1, 100)
        if roll == 1:
            return LevelOfSuccess.CRITICAL
        elif roll == 100:
            return LevelOfSuccess.FUMBLE
        elif roll <= skill.success_rate // 5:
            return LevelOfSuccess.SPECIAL
        elif roll <= skill.success_rate // 2:
            return LevelOfSuccess.HARD
        elif roll <= skill.success_rate:
            return LevelOfSuccess.SUCCESS
        elif roll <= 95 or (roll <= 99 and skill.success_rate >= 50):
            return LevelOfSuccess.FAILURE
        else:
            return LevelOfSuccess.FUMBLE

    @staticmethod
    def someone_left_alive(characters: List[Character], side: str) -> bool:
        return any(
            character.hp > 0 for character in characters if character.side == side
        )

    def process_attack(
        self, attacker: Character, skill: Skill, defender: Character
    ) -> None:
        if not skill.can_take_reaction:
            self.apply_attack_if_successful(attacker, skill, defender)
            return

        reaction = defender.reaction_strategy.reaction(defender, attacker)
        if reaction == ReactionType.NOTHING:
            self.apply_attack_if_successful(attacker, skill, defender)
        elif reaction == ReactionType.DODGE:
            self.handle_dodge_reaction(attacker, skill, defender)
        elif reaction == ReactionType.FIGHT_BACK:
            self.handle_fight_back_reaction(attacker, skill, defender)

    def apply_attack_if_successful(
        self, attacker: Character, skill: Skill, defender: Character
    ):
        success_level = self.check_level_of_success(skill)
        if success_level >= LevelOfSuccess.SUCCESS:
            self.apply_damage(attacker, skill, defender, success_level)

    def handle_dodge_reaction(
        self, attacker: Character, skill: Skill, defender: Character
    ):
        dodge_skill = defender.get_skill("Dodge")

        attacker_success_level = self.check_level_of_success(skill)
        dodge_success_level = self.check_level_of_success(dodge_skill)

        if (
            attacker_success_level > dodge_success_level
            and attacker_success_level >= LevelOfSuccess.SUCCESS
        ):
            self.apply_damage(attacker, skill, defender, attacker_success_level)

    def handle_fight_back_reaction(
        self, attacker: Character, skill: Skill, defender: Character
    ):
        fight_back_skill = defender.get_skill("Fighting (Brawl)")

        attacker_success_level = self.check_level_of_success(skill)
        fight_back_success_level = self.check_level_of_success(fight_back_skill)

        if (
            attacker_success_level >= fight_back_success_level
            and attacker_success_level >= LevelOfSuccess.SUCCESS
        ):
            self.apply_damage(attacker, skill, defender, attacker_success_level)
        elif (
            attacker_success_level < fight_back_success_level
            and fight_back_success_level >= LevelOfSuccess.SUCCESS
        ):
            self.apply_damage(
                defender, fight_back_skill, attacker, fight_back_success_level
            )

    def apply_damage(
        self,
        attacker: Character,
        skill: Skill,
        target: Character,
        success_level: LevelOfSuccess,
    ):
        damage = self.calculate_damage(attacker, skill, success_level)
        target.hp -= damage
        logger.info(
            f"{attacker.name} in side {attacker.side} attacked {target.name} and dealt {damage} damage."
        )

    def combat_simulation_single(self) -> str:
        class CombatEnd(Exception):
            pass

        characters_a = self.group_a_characters_init_strategy()
        for character in characters_a:
            character.side = "A"
        characters_b = self.group_b_characters_init_strategy()
        for character in characters_b:
            character.side = "B"

        characters = characters_a + characters_b

        characters.sort(
            key=lambda character: (character.attributes.dexterity, random.random()),
            reverse=True,
        )

        round = 1
        try:
            while self.someone_left_alive(characters, "A") and self.someone_left_alive(
                characters, "B"
            ):
                self.print_character_status(round, characters)
                for character in characters:
                    if character.hp > 0:
                        target_candidates = [
                            target
                            for target in characters
                            if target.side != character.side and target.hp > 0
                        ]
                        if not target_candidates:
                            raise CombatEnd()

                        target = character.target_selection_strategy.select_target(
                            character, characters
                        )
                        skill = character.skill_selection_strategy.select_skill(
                            character
                        )

                        self.process_attack(character, skill, target)
                round += 1
        except CombatEnd:
            pass

        if self.someone_left_alive(characters, "A"):
            return "A"
        elif self.someone_left_alive(characters, "B"):
            return "B"
        else:
            return "Draw"

    @staticmethod
    def print_character_status(round: int, characters: List[Character]) -> None:
        logger.info(f"Round {round}")
        for character in characters:
            logger.info(f"{character.name}: {character.hp}HP")

    def simulate_multiple_combats(self, number_of_simulations: int) -> dict:
        results = {"A": 0, "B": 0, "Draw": 0}
        for _ in tqdm.tqdm(range(number_of_simulations)):
            result = self.combat_simulation_single()
            results[result] += 1

        rate_a = results["A"] / number_of_simulations
        rate_b = results["B"] / number_of_simulations
        rate_draw = results["Draw"] / number_of_simulations

        return {"A": rate_a, "B": rate_b, "Draw": rate_draw}
