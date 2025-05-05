# About
This is a python terminal based implementation of the dungeon crawler card game [Scoundrel](http://www.stfj.net/art/2011/Scoundrel.pdf) by Zach Gage and Kurt Biek, based on a standard 54 card poker deck.

# Install
You have to first install the necessary packages:
```bash
pip install -r requirements.txt
```

## Dependencies
[blessed](https://github.com/chjj/blessed)

# Run
run the game in your terminal with:
```bash
python -m main.py
```

# Game Rules
Each round you can choose to interact with 3 objects from 4 objects.
Possible objects are
- Weapon:
    - you can pick up a weapon, but it will replace the current weapon you have
- Creature:
    - you can fight a creature either with a weapon (if you have one) or by fist
- Health Potions:
    - health potions restore your health, but only up to your maximum health of 20

Fighting rules:
- you can only fight a creature with the current weapon, if its power is less or equal to the last creature you defeated with that weapon
- excess damage (creature strenght - weapon) are dealt to your health
- fighting a creature with a fist deals damage equal to the creatures strength to your life

You can also skip a room, but not twice in a row, and only when you haven't interacted with any object in a room. Skipping a room will put the current object at the bottom of the current stack of cards. So you will have to interact with them again at a later point. So choose your resource wisely!

After interacting with 3 objects, you will enter the next room. The first object will be the last object from the last room.

You lose when you run out of life, you win, when you manage to clear all cards.