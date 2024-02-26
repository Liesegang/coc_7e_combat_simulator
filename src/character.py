from typing import List, Tuple
from attribute import Attribute
from skill import Skill
import random

class Character:
    def __init__(self, attributes: Attribute, skills: List[Skill] = []):
        if not isinstance(attributes, Attribute):
            raise ValueError("attributes must be an instance of Attribute")
        self.attributes = attributes
        self.skills = skills
        self.hp = (self.attributes.constitution + self.attributes.size) // 10
        self.mp = self.attributes.power // 5
        self.db = self.calculate_db()

    @classmethod
    def of(cls, attribute_params: dict, skills: List[Skill] = []) -> "Character":
        attributes = Attribute(**attribute_params)
        return cls(attributes, skills)

    @classmethod
    def of_random(cls, skills: List[Skill] = []) -> "Character":
        attribute_params = {
            "strength": cls.roll_dice(3, 6) * 5,
            "constitution": cls.roll_dice(3, 6) * 5,
            "size": (cls.roll_dice(2, 6) + 6) * 5,
            "dexterity": cls.roll_dice(3, 6) * 5,
            "appearance": cls.roll_dice(3, 6) * 5,
            "intelligence": (cls.roll_dice(2, 6) + 6) * 5,
            "power": cls.roll_dice(3, 6) * 5,
            "education": (cls.roll_dice(2, 6) + 6) * 5,
            "luck": cls.roll_dice(3, 6) * 5,
        }
        attribute_params["damage_bonus"] = cls.calculate_damage_bonus(
            attribute_params["strength"], attribute_params["size"]
        )
        attributes = Attribute(**attribute_params)
        return cls(attributes, skills)

    @staticmethod
    def roll_dice(n: int, sides: int) -> int:
        return sum(random.randint(1, sides) for _ in range(n))

    @staticmethod
    def calculate_db(self) -> str:
        combined = self.attributes.strength + self.attributes.size

        if 2 <= combined <= 64:
            return "-2"
        elif 65 <= combined <= 84:
            return "-1"
        elif 85 <= combined <= 124:
            return "0"
        elif 125 <= combined <= 164:
            return "1d4"
        elif combined >= 165:
            return "1d6"
        else:
            return "0"

    def add_skill(self, skill: Skill) -> None:
        if not isinstance(skill, Skill):
            raise ValueError("skill must be an instance of Skill")
        self.skills.append(skill)

    def __repr__(self) -> str:
        skills_str = ", ".join([str(skill) for skill in self.skills])
        return f"Attributes: {self.attributes}\nHP: {self.hp}, MP: {self.mp}\nSkills: {skills_str}"
