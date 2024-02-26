class Skill:
    def __init__(self, name: str, success_rate: int, damage: str, physical_attack: bool):
        self.name = name
        self.success_rate = success_rate
        self.damage = damage
        self.physical_attack = physical_attack

    def __repr__(self) -> str:
        return f"{self.name}: Success Rate: {self.success_rate}%, Damage: {self.damage}"