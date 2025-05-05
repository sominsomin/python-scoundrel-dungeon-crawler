import pytest

from src.entities.Player import Player
from src.entities.Card import Card, CardColor, CardValue


@pytest.fixture
def player():
    player = Player()
    yield player


def test_initial_health(player):
    assert player.health == 20
    assert player.weapon is None


def test_lose_health(player):
    player.lose_health(5)
    assert player.health == 15

    player.lose_health(10)
    assert player.health == 5

    player.lose_health(10)
    assert player.health == -5


def test_add_weapon(player):
    weapon = Card(color=CardColor.DIAMONDS.value, value=10)
    player.add_weapon(weapon)
    assert player.weapon == weapon


@pytest.mark.parametrize(
    "health_value, health_card_value, expected_health",
    [
        (5, 5, 10),
        (10, 10, 20),
        (1, 5, 6),
        (20, 0, 20),
    ],
)
def test_add_health(player, health_value, health_card_value, expected_health):
    health_card = Card(color=CardColor.HEARTS.value, value=health_card_value)
    player.health = health_value
    player.add_health(health_card)
    assert player.health == expected_health
