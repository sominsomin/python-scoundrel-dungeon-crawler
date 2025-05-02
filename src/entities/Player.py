from entities.Card import Card

class Player:
    def __init__(self):
        self.health = 20
        self.weapon = None

    def lose_health(self,  value: int) -> None:
        self.health = self.health - value

    def add_weapon(self, weapon: Card) -> None:
        self.weapon = weapon

    def add_health(self, health: Card) -> None:
        new_life = self.health + int(health.value)
        if new_life >= 20:
            self.health = 20
        else:
            self.health = new_life
