from enum import Enum


class CardColor(Enum):
    SPADES = "Spades"
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    SKIPROOM = "SkipRoom"


class CardValue(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    J = 11
    Q = 12
    K = 13
    A = 14


class CardValuePlayer(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10


class CardInteractionTypes(Enum):
    TAKE_WEAPON = "take Weapon"
    TAKE_HEALTH_POTION = "take Health"
    FIGHT_CREATURE_WITH_WEAPON = "fight with weapon"
    FIGHT_CREATURE_BARE_HANDED = "fight with hands"


class Card:
    def __init__(self, color: CardColor, value: CardValue):
        self.color = color
        self.value = value
        self.used = False

    def __str__(self):
        if self.is_weapon():
            return f"Weapon {self.value}"
        if self.is_health():
            return f"Health {self.value}"
        if self.is_creature():
            return f"Creature {self.value}"
        return f"Card(Color: {self.color}, Value: {self.value})"

    def __repr__(self):
        if self.is_weapon():
            return f"Weapon {self.value}"
        if self.is_health():
            return f"Health {self.value}"
        if self.is_creature():
            return f"Creature {self.value}"
        return f"Card(Color: {self.color}, Value: {self.value})"

    def is_weapon(self) -> bool:
        if self.color == CardColor.DIAMONDS.value:
            return True
        return False

    def is_health(self) -> bool:
        if self.color == CardColor.HEARTS.value:
            return True
        return False

    def is_creature(self) -> bool:
        if self.color == CardColor.SPADES.value or self.color == CardColor.CLUBS.value:
            return True
        return False

    def is_skiproom(self) -> bool:
        if self.color == CardColor.SKIPROOM.value:
            return True
        return False

    def is_used(self) -> bool:
        return self.used

    def set_used(self) -> None:
        self.used = True


class Weapon(Card):
    def __init__(self, value: CardValue):
        super().__init__(CardColor.DIAMONDS, value)
        self.color = CardColor.DIAMONDS.value
        self.value = value
        self.defeated_creatures = []

    def __str__(self):
        return f"Weapon {self.value}"

    def __repr__(self):
        return f"Weapon {self.value}"

    def interactions(self):
        return [CardInteractionTypes.TAKE_WEAPON]

    def display_content(self):
        return [
            "       ",
            "        /\ ",
            "       /  \ ",
            "       \  / ",
            "        \/ ",
        ]


class Creature(Card):
    def __init__(self, value: CardValue):
        super().__init__(CardColor.SPADES, value)
        self.color = CardColor.SPADES.value
        self.value = value

    def __str__(self):
        return f"Creature {self.value}"

    def __repr__(self):
        return f"Creature {self.value}"

    def interactions(self, weapon: Weapon = None):
        if weapon is None:
            return [CardInteractionTypes.FIGHT_CREATURE_BARE_HANDED]

        if len(weapon.defeated_creatures) != 0:
            if weapon.defeated_creatures[-1].value >= self.value:
                return [
                    CardInteractionTypes.FIGHT_CREATURE_WITH_WEAPON,
                    CardInteractionTypes.FIGHT_CREATURE_BARE_HANDED,
                ]
            return [CardInteractionTypes.FIGHT_CREATURE_BARE_HANDED]
        return [
            CardInteractionTypes.FIGHT_CREATURE_WITH_WEAPON,
            CardInteractionTypes.FIGHT_CREATURE_BARE_HANDED,
        ]

    def display_content(self):
        return [
            "       ",
            "       ",
            "        00 ",
            "       0000 ",
            "        00 ",
            "         ",
        ]


class Health(Card):
    def __init__(self, value: CardValue):
        super().__init__(CardColor.HEARTS, value)
        self.color = CardColor.HEARTS.value
        self.value = value

    def __str__(self):
        return f"Health {self.value}"

    def __repr__(self):
        return f"Health {self.value}"

    def interactions(self):
        return [CardInteractionTypes.TAKE_HEALTH_POTION]

    def display_content(self):
        return [
            "     ",
            "       00 00",
            "      0000000",
            "       00000",
            "         0",
        ]


class SkipRoom(Card):
    def __init__(self, value: CardValue = CardValue.ONE.value):
        super().__init__(CardColor.SKIPROOM, value)
        self.color = CardColor.SKIPROOM.value
        self.value = value

    def __str__(self):
        return (
            "Skip current room. (if chosen, next room this option won't be available)"
        )

    def __repr__(self):
        return (
            "Skip current room. (if chosen, next room this option won't be available)"
        )
