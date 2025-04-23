import random
from base_classes.Card import Card, CardColor, CardValue


class DiscardPile:
    def __init__(self):
        self.stack = []

    def add(self, cards: list[Card]) -> None:
        self.stack.append(cards)
