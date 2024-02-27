class Attribute:
    def __init__(
        self,
        strength: int,
        constitution: int,
        size: int,
        dexterity: int,
        appearance: int,
        intelligence: int,
        power: int,
        education: int,
        luck: int,
    ):
        self.strength = strength
        self.constitution = constitution
        self.size = size
        self.dexterity = dexterity
        self.appearance = appearance
        self.intelligence = intelligence
        self.power = power
        self.education = education
        self.luck = luck

    def __repr__(self) -> str:
        return (
            f"Strength: {self.strength}, Constitution: {self.constitution}, Size: {self.size}, "
            f"Dexterity: {self.dexterity}, Appearance: {self.appearance}, Intelligence: {self.intelligence}, "
            f"Power: {self.power}, Education: {self.education}, Luck: {self.luck}"
        )
