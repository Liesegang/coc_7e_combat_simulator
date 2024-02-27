from dataclasses import dataclass


@dataclass
class Skill:
    name: str
    success_rate: int
    damage: str
    physical_attack: bool = False
    impale: bool = False

    def __repr__(self) -> str:
        return f"{self.name}: Success Rate: {self.success_rate}%, Damage: {self.damage}, Physical Attack: {self.physical_attack}, Impale: {self.impale}"


FightingBrawl = Skill("Fighting (Brawl)", 25, "1D3", True)
FirearmHandgun = Skill("Firearm (Handgun)", 20, "1D10", False)
