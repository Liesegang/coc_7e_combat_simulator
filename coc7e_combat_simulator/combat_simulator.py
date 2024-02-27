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
    CRITICAL = 0
    SPECIAL = 1
    HARD = 2
    SUCCESS = 3
    FAILURE = 4
    FUMBLE = 5


class CombatSimulator:
    def __init__(
        self,
        group_a_characters_init_strategy: Callable[[], List[Character]],
        group_b_characters_init_strategy: Callable[[], List[Character]],
    ):
        self.group_a_characters_init_strategy = group_a_characters_init_strategy
        self.group_b_characters_init_strategy = group_b_characters_init_strategy

    @staticmethod
    def calculate_damage(character: Character, skill: Skill) -> int:
        logger.info(f"{character.name} in side {character.side} used {skill.name}.")

        damage_result = dice_parser.parse(skill.damage)[0]

        if skill.physical_attack:
            damage_result += dice_parser.parse(character.db)[0]

        logger.info(
            f"{character.name} in side {character.side} dealt {damage_result} damage."
        )
        return damage_result

    @staticmethod
    def check_level_of_success(skill: Skill) -> LevelOfSuccess:
        roll = random.randint(1, 100)
        if roll == 1:
            return LevelOfSuccess.CRITICAL
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

    def someone_left_alive(self, characters: List[Character], side: str) -> bool:
        return any(
            character.hp > 0 for character in characters if character.side == side
        )

    def check_damage(
        self, character: Character, skill: Skill, target: Character
    ) -> None:
        reply = target.reply_strategy.reply(target, character)
        if skill.name != "Fighting (Brawl)" or reply == ReactionType.NOTHING:
            if self.check_level_of_success(skill) >= LevelOfSuccess.SUCCESS:
                damage = self.calculate_damage(character, skill)
                target.hp -= damage
                logger.info(
                    f"{character.name} in side {character.side} attacked {target.name} and dealt {damage} damage."
                )
                return
        elif reply == ReactionType.DODGE:
            attacker_level_of_success = self.check_level_of_success(skill)
            dodge_skill = (
                list(filter(lambda skill: skill.name == "Dodge", target.skills))[0]
                if list(filter(lambda skill: skill.name == "Dodge", target.skills))
                else Skill(
                    "Dodge",
                    target.attributes.dexterity // 5 * 3,
                    "0",
                    physical_attack=False,
                )
            )
            dodge_level_of_success = self.check_level_of_success(dodge_skill)
            if (
                attacker_level_of_success > dodge_level_of_success
                and attacker_level_of_success >= LevelOfSuccess.SUCCESS
            ):
                damage = self.calculate_damage(character, skill)
                target.hp -= damage
                logger.info(
                    f"{character.name} in side {character.side} attacked {target.name} and dealt {damage} damage."
                )
                return
            elif (
                attacker_level_of_success <= dodge_level_of_success
                and dodge_level_of_success >= LevelOfSuccess.SUCCESS
            ):
                logger.info(
                    f"{target.name} in side {target.side} dodged {character.name}'s attack."
                )
                return
            else:
                logger.info(
                    f"{character.name} in side {character.side} failed to attack {target.name}."
                )
                return
        elif reply == ReactionType.FIGHT_BACK:
            attacker_level_of_success = self.check_level_of_success(skill)
            fight_back_skill = (
                list(
                    filter(
                        lambda skill: skill.name == "Fighting (Brawl)", target.skills
                    )
                )[0]
                if list(
                    filter(
                        lambda skill: skill.name == "Fighting (Brawl)", target.skills
                    )
                )
                else FightingBrawl
            )
            fight_back_skill_level_of_success = self.check_level_of_success(
                fight_back_skill
            )
            if (
                attacker_level_of_success >= fight_back_skill_level_of_success
                and attacker_level_of_success >= LevelOfSuccess.SUCCESS
            ):
                damage = self.calculate_damage(character, skill)
                target.hp -= damage
                logger.info(
                    f"{character.name} in side {character.side} attacked {target.name} and dealt {damage} damage."
                )
                return
            elif (
                attacker_level_of_success < fight_back_skill_level_of_success
                and fight_back_skill_level_of_success >= LevelOfSuccess.SUCCESS
            ):
                damage = self.calculate_damage(target, fight_back_skill)
                character.hp -= damage
                logger.info(
                    f"{target.name} in side {target.side} fought back {character.name} and dealt {damage} damage."
                )
                return
            else:
                logger.info(
                    f"{character.name} in side {character.side} failed to attack {target.name}."
                )
                return

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

                        self.check_damage(character, skill, target)
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
