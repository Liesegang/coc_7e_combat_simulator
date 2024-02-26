import random
import copy
import logging
from typing import List, Tuple
import tqdm

from character import Character
from skill import Skill
from dice_parser import DiceParser

logger = logging.getLogger(__name__)
dice_parser = DiceParser()

class CombatSimulator:
    def __init__(self, group_a_num: int, group_b_num: int) -> None:
        self.group_a_num = group_a_num
        self.group_b_num = group_b_num

    @staticmethod
    def calculate_damage(character: Character) -> int:
        skill = random.choice(character.skills)
        logger.info(f"{character.name} in side {character.side} used {skill.name}.")

        if random.randint(1, 100) > skill.success_rate:
            logger.info(f"{character.name} in side {character.side} missed.")
            return 0

        damage_result = dice_parser.parse(skill.damage)[0]

        if skill.physical_attack:
            damage_result += dice_parser.parse(character.db)[0]

        logger.info(f"{character.name} in side {character.side} dealt {damage_result} damage.")
        return damage_result

    def someone_left_alive(self, characters: List[Character], side: str) -> bool:
        return any(character.hp > 0 for character in characters if character.side == side)

    def combat_simulation_single(self) -> str:
        class CombatEnd(Exception):
            pass

        characters_a = [Character.of_random(f"A_{i}", skills=[Skill("Punch", 50, "1d3", True)]).set_side("A") for i in range(self.group_a_num)]
        characters_b = [Character.of_random(f"B_{i}", skills=[Skill("Punch", 50, "1d3", True)]).set_side("B") for i in range(self.group_b_num)]
        characters = characters_a + characters_b

        characters.sort(key=lambda character: (character.attributes.dexterity, random.random()), reverse=True)

        round = 1
        try:
            while self.someone_left_alive(characters, "A") and self.someone_left_alive(characters, "B"):
                self.print_character_status(round, characters)
                for character in characters:
                    if character.hp > 0:
                        target_candidates = [target for target in characters if target.side != character.side and target.hp > 0]
                        if not target_candidates:
                            raise CombatEnd()
                        target = random.choice(target_candidates)
                        damage = self.calculate_damage(character)
                        target.hp -= damage
                        logger.info(f"{character.name} in side {character.side} attacked {target.name} and dealt {damage} damage.")
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

    def simulate_multiple_combats(self, number_of_simulations: int) -> Tuple[float, float, float]:
        results = {"A": 0, "B": 0, "Draw": 0}
        for _ in tqdm.tqdm(range(number_of_simulations)):
            result = self.combat_simulation_single()
            results[result] += 1

        rate_a = results["A"] / number_of_simulations
        rate_b = results["B"] / number_of_simulations
        rate_draw = results["Draw"] / number_of_simulations

        return {"A": rate_a, "B": rate_b, "Draw": rate_draw}