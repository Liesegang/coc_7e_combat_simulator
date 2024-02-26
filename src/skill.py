class Skill:
    def __init__(self, name: str, success_rate: int, damage: str):
        self.name = name
        self.success_rate = success_rate
        self.damage = damage

    def __repr__(self) -> str:
        return f"{self.name}: Success Rate: {self.success_rate}%, Damage: {self.damage}"