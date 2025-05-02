from blessed import Terminal
import time

from base_classes.Player import Player
from base_classes.Deck import Deck
from base_classes.Card import Card, CardInteractionTypes
from base_classes.DiscardPile import DiscardPile


class Game:
    defeated_creatures = []
    drawn_cards = []

    def __init__(self):
        self.player = Player()
        self.deck = Deck()
        self.discard_pile = DiscardPile()
        self.term = Terminal()
        self.deck.shuffle()
        self.skipped_room = False
        self.term.hide_cursor()

    def reset_game(self) -> None:
        self.player = Player()
        self.deck = []
        self.drawn_cards = []
        self.deck = Deck()
        self.discard_pile = DiscardPile()
        self.deck.shuffle()

    def draw_player_state(self) -> None:
        print(self.term.home)
        current_room_count = len(self.deck) + len(self.drawn_cards)
        print(self.term.bold(f'Cards: {current_room_count}/{self.deck.init_n_rooms}'))
        print(self.term.bold(f'Health: {self.player.health}'))

        if self.player.weapon is not None:
            print(self.term.bold((f'Weapon: {self.player.weapon.value} {[creature.value for creature in self.player.weapon.defeated_creatures]}')))
        if self.skipped_room is False and self.n_used_cards == 0:
            print(self.term.bold((f'[s]: skip current room')))

        print(self.term.move_down(2))

    def check_win_condition(self) -> None:
        if self.player.health <= 0:
            self.death_screen()
        if len(self.deck) <= 0:
            self.win_screen()
        
    def handle_card_interaction(self, selected_card: Card, selected_interaction: CardInteractionTypes) -> None:
        if selected_card.is_weapon():
            self.add_weapon(selected_card)
        
        if selected_card.is_health():
            self.add_health(selected_card)

        if selected_card.is_creature():
            self.fight_creature(selected_card, selected_interaction)

        self.discard_pile.add(selected_card)

    def death_screen(self):
        print(self.term.clear + self.term.move_y(self.term.height // 2))
        print(self.term.black_on_red(self.term.center('You died ..... ')))
        print((self.term.center('Press any key to try again! ')))
        time.sleep(1)
        with self.term.cbreak(), self.term.hidden_cursor():
            key = self.term.inkey()
            if key:
                print(self.term.clear)
                self.reset_game()
                self.first_room()
    
    def win_screen(self):
        print(self.term.clear + self.term.move_y(self.term.height // 2))
        print(self.term.black_on_green(self.term.center('Congratulations! You finished the dungeon!')))
        print((self.term.center('Press any key to try again! ')))
        time.sleep(1)
        with self.term.cbreak(), self.term.hidden_cursor():
            key = self.term.inkey()
            if key:
                print(self.term.clear)
                self.reset_game()
                self.first_room()

    def draw_state(self, cursor_position_horizontal, cursor_position_vertical=0) -> int:
        self.check_win_condition()

        n_used_cards = [card.is_used() for card in self.drawn_cards].count(True)
        self.n_used_cards = n_used_cards

        if self.n_used_cards == 3:
            self.new_room()

        print(self.term.home + self.term.move_y(self.term.height // 4))
        self.term.hide_cursor()
        self.draw_player_state()

        n_options = len(self.drawn_cards)

        self.display_cards(self.drawn_cards)

        margin = 5
        box_width = 20
        box_height = 10
        start_x = 5
        start_y = 5

        if self.drawn_cards[cursor_position_horizontal].is_used():
            for i in range(2 * n_options):
                index = (cursor_position_horizontal + 1 + i) % n_options
                if not self.drawn_cards[index].is_used():
                    break
            cursor_position_horizontal = index

        for i, card in enumerate(self.drawn_cards):
            if card.is_used():
                continue
            if card.is_creature():
                card_interactions = card.interactions(self.player.weapon)
            else:
                card_interactions = card.interactions()
            if i == cursor_position_horizontal and len(card_interactions) <= cursor_position_vertical:
                cursor_position_vertical = 0

            for j, interaction in enumerate(card_interactions):
                line = f'{" > " if i == cursor_position_horizontal and j == cursor_position_vertical else "   "}{str(interaction.value)}'
                centered_line = self.term.bold(line)
                x = start_x + (box_width + margin) * i
                y = box_height + 7 + j
                print(self.term.move_xy(x, y) + centered_line)

        print(self.term.home)
        
        with self.term.cbreak(), self.term.hidden_cursor():
            key = self.term.inkey()

        if key.code == self.term.KEY_LEFT:
            for i in range(2 * n_options):
                index = (cursor_position_horizontal - 1 - i) % n_options
                if not self.drawn_cards[index].is_used():
                    break

            cursor_position_horizontal = index

            # cursor_position_horizontal = (cursor_position_horizontal - 1) % n_options
            self.draw_state(cursor_position_horizontal, cursor_position_vertical)
        elif key.code == self.term.KEY_RIGHT:
            for i in range(2 * n_options):
                index = (cursor_position_horizontal + 1 + i) % n_options
                if not self.drawn_cards[index].is_used():
                    break

            cursor_position_horizontal = index

            # cursor_position_horizontal = (cursor_position_horizontal + 1) % n_options
            self.draw_state(cursor_position_horizontal, cursor_position_vertical)
        elif key.code == self.term.KEY_UP:
            cursor_position_vertical = (cursor_position_vertical - 1) % 2
            self.draw_state(cursor_position_horizontal, cursor_position_vertical)
        elif key.code == self.term.KEY_DOWN:
            cursor_position_vertical = (cursor_position_vertical + 1) % 2
            self.draw_state(cursor_position_horizontal, cursor_position_vertical)
        elif (key == 's' or key == 'S') and self.skipped_room == False and self.n_used_cards == 0:
            self.skip_room()
        elif key.code == self.term.KEY_ENTER or key == ' ':
            selected_card = self.drawn_cards[cursor_position_horizontal]

            if selected_card.is_used():
                self.draw_state(0, 0)

            card = self.drawn_cards[cursor_position_horizontal]
            if card.is_creature():
                card_interactions = card.interactions(self.player.weapon)
            else:
                card_interactions = card.interactions()

            selected_interaction = card_interactions[cursor_position_vertical]
            
            self.handle_card_interaction(selected_card, selected_interaction)
            # updated_cards = [card for card in cards if card != selected_card]
            # self.drawn_cards = updated_cards
            self.skipped_room = False
            self.drawn_cards[cursor_position_horizontal].set_used()
            
            print(self.term.clear)
            self.draw_state(0, 0)
        else:
            self.draw_state(cursor_position_horizontal, cursor_position_vertical)

        return cursor_position_horizontal, cursor_position_vertical
    
    def first_room(self) -> None:
        self.drawn_cards = self.deck.draw(4)
        cursor_position = 0
        print(self.term.clear)
        print(self.term.home)

        cursor_position = self.draw_state(cursor_position)     

    def new_room(self, skipped_room=False) -> None:
        print(self.term.clear)
        if self.drawn_cards is None or len(self.drawn_cards) == 0:
            drawn_cards = self.deck.draw(4)
            new_cards = drawn_cards
        else:
            unused_card = [card for card in self.drawn_cards if not card.is_used()]
            drawn_cards = self.deck.draw(3)
            new_cards = [*unused_card, *drawn_cards]
        
        self.drawn_cards = new_cards

        cursor_position_horizontal = 0

        if skipped_room == True:
            self.skipped_room = True
        else:
            self.skipped_room = False

        cursor_position_horizontal, cursor_position_vertical = self.draw_state(cursor_position_horizontal)

    def run(self) -> None:
        print(self.term.clear + self.term.home + self.term.move_y(self.term.height // 2))
        print(self.term.black_on_darkkhaki(self.term.center('You start into the dungeon! press any key to continue')))
        with self.term.cbreak(), self.term.hidden_cursor():
            inp = self.term.inkey()
        self.first_room()

    def add_weapon(self, card: Card) -> None:
        self.player.add_weapon(card)

    def add_health(self, card: Card) -> None:
        self.player.add_health(card)

    def fight_creature(self, creature: Card, selected_interaction: CardInteractionTypes) -> None:
        ignore_weapon = (selected_interaction == CardInteractionTypes.FIGHT_CREATURE_BARE_HANDED)

        if self.player.weapon is not None:
            defeated_creatures = self.player.weapon.defeated_creatures
        else:
            defeated_creatures = []

        if len(defeated_creatures) == 0:
            self.get_value_diff(creature, ignore_weapon)
        else:
            if defeated_creatures[-1].value >= creature.value:
                self.get_value_diff(creature, ignore_weapon)
            else:
                print(self.term.black_on_darkkhaki(self.term.center(f'you have to fight it without a weapon')))
                self.get_value_diff(creature, True)

    def get_value_diff(self, creature: Card, ignore_weapon=False) -> None:
        if self.player.weapon is None or ignore_weapon is True:
            value_diff = creature.value
        else:
            value_diff = creature.value - self.player.weapon.value
            self.player.weapon.defeated_creatures.append(creature)
        if value_diff > 0:
            self.player.lose_health(value_diff)

    def skip_room(self) -> None:
        self.deck.add_below(self.drawn_cards)
        self.drawn_cards = []
        self.new_room(skipped_room=True)

    def draw_box(self, x, y, width, height, card):
        if card.is_used():
            title = 'XXXXXXX'
            content_lines = ''
        else:
            title = str(card)
            content_lines = card.display_content()

        print(self.term.move_xy(x, y) + '┌' + '─' * (width - 2) + '┐')
        title_line = f'│{title.center(width - 2)}│'
        print(self.term.move_xy(x, y + 1) + title_line)
        
        for i in range(height - 3):
            if i < len(content_lines):
                content_line = f'│{str(content_lines[i]).ljust(width - 2)}│'
            else:
                content_line = '│' + ' ' * (width - 2) + '│'
            print(self.term.move_xy(x, y + 2 + i) + content_line)

        print(self.term.move_xy(x, y + height - 1) + '└' + '─' * (width - 2) + '┘')

    def display_cards(self, cards):
        margin = 5
        box_width = 20
        box_height = 10
        start_x = 5
        start_y = 6

        for i, card in enumerate(cards):
            x = start_x + i * (box_width + margin)
            y = start_y
            self.draw_box(x, y, box_width, box_height, card)
