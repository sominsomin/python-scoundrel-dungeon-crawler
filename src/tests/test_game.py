import pytest

from src.entities.Game import Game
from src.entities.Card import Card, CardColor, CardValue, Weapon, Health, Creature, CardInteractionTypes


@pytest.fixture
def game():
    game = Game()
    yield game


def test_add_weapon_first_weapon(game):
    weapon = Weapon(CardValue.EIGHT.value)

    game.add_weapon(weapon)

    assert game.player.weapon == weapon


@pytest.mark.parametrize(
    "original_weapon, new_weapon",
    [
        (20, 10),
        (20, 1),
        (10, 10),
        (10, 8),
    ],
)
def test_add_weapon_overwrite_weapon(game, original_weapon, new_weapon):
    old_weapon = Weapon(original_weapon)
    game.player.add_weapon(old_weapon)
    new_weapon = Weapon(new_weapon)

    assert game.player.weapon == old_weapon

    game.add_weapon(new_weapon)

    assert game.player.weapon == new_weapon


@pytest.mark.parametrize(
    "original_health, health, expected_health",
    [
        (20, 10, 20),
        (20, 1, 20),
        (10, 10, 20),
        (10, 1, 11),
        (10, 15, 20),
    ],
)
def test_add_health(game, original_health, health, expected_health):
    health_card = Health(health)

    game.player.health = original_health
    game.add_health(health_card)

    assert game.player.health == expected_health


@pytest.mark.parametrize(
    "original_health, creature_value, weapon_value, expected_health",
    [
        (20, 10, 11, 20),
        (20, 10, 1, 11),
        (5, 10, 1, -4),
    ],
)
def test_fight_creature(
    game, original_health, creature_value, weapon_value, expected_health
):
    creature = Creature(creature_value)
    weapon = Weapon(weapon_value)

    game.player.health = original_health
    game.add_weapon(weapon)
    game.fight_creature(creature, CardInteractionTypes.FIGHT_CREATURE_WITH_WEAPON)

    assert game.player.health == expected_health
    assert game.player.weapon.defeated_creatures[0] == creature


@pytest.mark.parametrize(
    "original_health, creature_value, previous_defeated_creature, weapon_value, expected_health",
    [
        (20, 10, [11], 11, 20),
        (20, 10, [], 1, 11),
        (5, 10, [11], 1, -4),
        (5, 10, [], 1, -4),
        (5, 10, [9, 8], 1, -5),
    ],
)
def test_fight_creature_with_stack(
    game,
    original_health,
    creature_value,
    previous_defeated_creature,
    weapon_value,
    expected_health,
):
    creature = Creature(creature_value)
    previous_creatures = [Creature(value) for value in previous_defeated_creature]
    weapon = Weapon(weapon_value)
    weapon.defeated_creatures = previous_creatures

    game.player.health = original_health
    game.add_weapon(weapon)

    game.fight_creature(creature, CardInteractionTypes.FIGHT_CREATURE_WITH_WEAPON)

    assert game.player.health == expected_health

    if len(previous_defeated_creature) != 0:
        if creature.value <= previous_defeated_creature[-1]:
            assert game.player.weapon.defeated_creatures[-1] == creature
    else:
        assert game.player.weapon.defeated_creatures[-1] == creature
