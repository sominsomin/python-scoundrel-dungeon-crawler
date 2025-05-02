import random
from entities.Card import Card, CardValuePlayer, CardValue, Creature, Weapon, Health


class Deck:
    def __init__(self):
        creatures = [Creature(value.value) for value in CardValue]
        creatures_2 = [Creature(value.value) for value in CardValue]
        health = [Health(value.value) for value in CardValuePlayer]
        weapon = [Weapon(value.value) for value in CardValuePlayer]
        self.stack = [*creatures, *creatures_2, *weapon, *health]
        self.init_n_rooms = len(self.stack)

    def __len__(self) -> int:
        return len(self.stack)

    def shuffle(self) -> None:
        random.shuffle(self.stack)

    def draw(self, n_cards: int) -> None:
        """
        return n_cards first cards, removes those from the stack 
        """
        drawn_cards = self.stack[0:n_cards]
        self.stack = self.stack[n_cards:]

        return drawn_cards

    def add_below(self, cards: list[Card]) -> None:
        self.stack.extend(cards)
