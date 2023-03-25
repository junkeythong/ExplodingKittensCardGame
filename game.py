from deck import Deck
from player import Player
from card import Card


class Game:
    def __init__(self, num_players):
        self._num_players = num_players
        self._current_player = 0
        self._players = []
        self._died_players = []
        self.setup()

    def init_player(self):
        for i in range(self._num_players):
            name = input(f"Enter name for player {i + 1}: ")
            self._players.append(Player(i, name))

    def setup(self):
        # Init all players
        self.init_player()

        # Init the deck
        self.deck = Deck()

        for player in self._players:
            # Each player will draw 7 shuffled cards
            for i in range(7):
                player.add_card_to_hand(self.deck.draw_card())

            # Give each player a defuse card
            player.add_card_to_hand(Card("Defuse"))

        # Add back the remaining defuse and kitten cards to the deck
        # Make sure only one person can live
        for i in range(self._num_players - 1):
            self.deck.add_card(Card("Exploding Kitten"))
        for i in range(6 - self._num_players):
            self.deck.add_card(Card("Defuse"))

        # Show all cards in the player's hand
        print("\nHands of players after dealing defuse card:")
        for player in self._players:
            print(
                f"{player.get_name()}: {[card.get_name() for card in player.get_hand()]}")

        # Shuffling the deck again to shuffle the Defuse and Kitten cards.
        self.deck.shuffle()

    def play_turn(self):
        player = self.get_current_player()
        self.show_deck_card_number()
        print(f"{player.get_name()} is under attack and must take a turn ({player.get_num_attacks()} turn left)")

        if len(player.get_hand()) == 0:
            print(f"\n{player.get_name()}, it's your turn!")
            print("You have no card. You draw a card and moving to next players!")
            card_drew = self.deck.draw_card()
            print(f"You drew: {card_drew.get_name()}")
            player.add_card_to_hand(card_drew)
            # If we drew a Kitten card, continue to check if we have defuse or not
            if card_drew.get_name() == "Exploding Kitten":
                self.handle_drew_kitten_card()
            self.move_to_next_player()
            return

        print(f"\n{player.get_name()}, it's your turn!")

        while True:
            answer = input("Do you want to play? (yes/no): ")
            if answer == "yes":
                break
            elif answer == "no":
                print("End your turn by drawing a card!")
                card_drew = self.deck.draw_card()
                print(f"You drew: {card_drew.get_name()}")
                player.add_card_to_hand(card_drew)

                # If we drew a Kitten card, continue to check if we have defuse or not
                if card_drew.get_name() == "Exploding Kitten":
                    self.handle_drew_kitten_card()
                self.move_to_next_player()
                return
            else:
                print("Invalid input!")

        is_continue = True
        while is_continue:
            print(f"You have {len(player.get_hand())} cards in your hand.")
            print("Here are your cards:")
            for i, card in enumerate(player.get_hand()):
                print(f"{i + 1}. {card.get_name()}")

            card = None
            while True:
                try:
                    card_index = int(
                        input(f"{player.get_name()}, enter the index of the card you want to play: "))
                    if card_index < 1 or card_index > len(player.get_hand()):
                        print("Invalid card index. Try again.")
                        continue
                    for i, play_card in enumerate(player.get_hand()):
                        if card_index == i + 1:
                            card = play_card
                            player.play_card(play_card)
                            break
                    break
                except (ValueError, IndexError):
                    print("Invalid card index. Try again.")

            self.handle_card(card)

            # The attack and skip card will end our turn!
            if card.get_name() != "Attack" and card.get_name() != "Skip":
                while True:
                    answer = input(
                        f"{player.get_name()}, do you want to continue playing? (yes/no): ")
                    if answer == "yes":
                        is_continue = True
                        break
                    elif answer == "no":
                        is_continue = False
                        break
                    else:
                        print("Invalid input!")
                if not is_continue:
                    break
            else:
                is_continue = False

        if card.get_name() != "Skip" and card.get_name() != "Attack":
            card_drew = self.deck.draw_card()
            print(f"You drew: {card_drew.get_name()}")
            player.add_card_to_hand(card_drew)

            # If we drew a Kitten card, continue to check if we have defuse or not
            if card_drew.get_name() == "Exploding Kitten":
                self.handle_drew_kitten_card()
        self.move_to_next_player()

    def move_to_next_player(self):
        self._current_player = (self._current_player + 1) % self._num_players

    def handle_card(self, card):
        player = self.get_current_player()
        card_name = card.get_name()

        if player.has_pair_card(card_name):
            while True:
                choice = input(
                    f"You have a pair of {card_name} cards. How many cards would you like to play? (1 or 2 cards): ".format(card.get_name()))
                if choice == "1":
                    print(f"You played: {card_name}")
                    self.handle_single_card(card)
                    break
                elif choice == "2":
                    print(f"You played pair of cards: {card_name}")
                    self.handle_special_combos(card)
                    break
                else:
                    print("Invalid input")
        else:
            self.handle_single_card(card)

    def handle_single_card(self, card):
        if self.has_noped(card.get_name()):
            # Discard if someone played a nope card
            return
        if card.get_name() == "Defuse":
            self.handle_defuse_card()
        elif card.get_name() == "Attack":
            self.handle_attack_card()
        elif card.get_name() == "Shuffle":
            self.handle_shuffle_card()
        elif card.get_name() == "Skip":
            self.handle_skip_card()
        elif card.get_name() == "Favor":
            self.handle_favor_card()
        elif card.get_name() == "Nope":
            self.handle_nope_card()
        elif card.get_name() == "See The Future":
            self.handle_see_future_card()
        else:
            self.handle_cat_card()

    def handle_drew_kitten_card(self):
        player = self.get_current_player()
        if player.has_card("Defuse"):
            kitten_card = player.get_card_from_hand("Exploding Kitten")
            defuse_card = player.get_card_from_hand("Defuse")
            print(f"Player {player.get_name()} defused the Exploding Kitten!!")
            # Add card to deck at an position you want!
            position = int(input(
                f"Position you want to add to the draw pile 1 -> {self.deck.current_card_left()}: "))
            self.deck.get_cards().insert(position - 1, kitten_card)
            player.remove_card_from_hand(kitten_card)
            player.remove_card_from_hand(defuse_card)
        else:
            print(f"Player {player.get_name()} exploded!!")
            self._died_players.append(player)
            player.died(True)
            self.show_died_player()
            self._players.pop(self._current_player)
            self._num_players -= 1
            if self._num_players == 1:
                print(
                    f"Player {self._players[0].get_name()} has won the game!!")
                exit()

    def handle_defuse_card(self):
        print("There is nothing to defuse!")

    def handle_attack_card(self):
        player = self.get_current_player()
        next_player_index = (self._current_player + 1) % self._num_players
        next_player = self._players[next_player_index]
        if player.get_num_attacks() > 0:
            remain_attacks = player.get_num_attacks()
            player.set_num_attacks(0)
            next_player.set_num_attacks(remain_attacks + 2)
        else:
            next_player.set_num_attacks(2)

        current_player_bk = player
        while next_player.get_num_attacks() > 0 and not next_player.has_died():
            print(
                f"{next_player.get_name()} is under attack and must take a turn ({next_player.get_num_attacks()} turn left)")
            self.move_to_next_player()
            self.play_turn()
            next_player.set_num_attacks(-1)

            # come back with the real current player while in attack loop
            self._current_player = current_player_bk.get_id()

        # otherwise move to next player as normal
        if next_player.get_num_attacks() == 0:
            self._current_player = next_player.get_id()

    def handle_shuffle_card(self):
        self.deck.shuffle()
        print("Deck shuffled!")

    def handle_skip_card(self):
        print("Do not draw and skip your turn!")
        player = self.get_current_player()
        if player.get_num_attacks() > 0:
            print("Removed an attack round from previous player")
            # player.set_num_attacks(-1)

    def handle_favor_card(self):
        player = self.get_current_player()
        print("you will take a card given by a target player.")
        target_player = self.choose_target_player()

        print(f"{target_player.get_name()}, here are cards on your hand:")
        for i, card in enumerate(target_player.get_hand()):
            print(f"{i + 1}. {card.get_name()}")

        took_card = None
        while True:
            try:
                card_index = int(input(
                    f"{target_player.get_name()}, enter the index of the card you want give to {player.get_name()}: "))
                if card_index > len(target_player.get_hand()):
                    print("Invalid card index. Try again.")
                else:
                    # double check here
                    took_card = target_player.get_hand()[card_index - 1]
                    target_player.take_card_from_hand(took_card)
                    player.add_card_to_hand(took_card)
                    print(
                        f"{player.get_name()}, you received {took_card.get_name()} from {target_player.get_name()}!")
                    break
            except (ValueError, IndexError):
                print("Invalid card index. Try again.")

    def handle_nope_card(self):
        # there is no action here
        pass

    def has_noped(self, card_name):
        player = self.get_current_player()
        has_noped = False
        for nope_player in self._players:
            if nope_player != player and nope_player.has_card("Nope") and card_name != "Exploding Kitten" and card_name != "Defuse":
                while True:
                    answer = input(
                        f"{nope_player.get_name()}, you have a Nope card, do you want to play? (yes/no): ")
                    if answer == "yes":
                        if not has_noped:
                            print(
                                f"{nope_player.get_name()} played a Nope card, the {card_name} card has been discard!")
                            nope_player.play_card(
                                nope_player.get_card_from_hand("Nope"))
                            has_noped = True
                            break
                        else:
                            print(
                                f"{nope_player.get_name()}, you created an Yup, the {card_name} card of {player.get_name()} still take action!")
                            has_noped = False
                            nope_player.play_card(
                                nope_player.get_card_from_hand("Nope"))
                            break
                    elif answer == "no":
                        break
                    else:
                        print("Invalid input!")
        return has_noped

    def handle_see_future_card(self):
        if len(self.deck.get_cards()) < 3:
            print("Less than 3 cards in the draw pile!!")
        else:
            print(f"Top 3 cards in deck: {self.deck.get_top_3_cards()}")

    def handle_cat_card(self):
        # cat card will take no action.
        pass

    def handle_special_combos(self, card):
        if self.has_noped(card.get_name()):
            # Discard if someone played a nope card
            return
        player = self.get_current_player()
        # Take an remain card in hand.
        player.play_card(player.get_card_from_hand(card.get_name()))
        while True:
            print("You will take a random card from an target user!")
            target_player = self.choose_target_player()
            card = target_player.get_random_card()
            print(
                f"Got a random card from {target_player.get_name()}: {card.get_name()}")
            target_player.take_card_from_hand(card)
            player.add_card_to_hand(card)
            break

    def choose_target_player(self):
        player = self.get_current_player()
        while True:
            target_player_name = input("Enter the name of the target player: ")
            target_player = None
            for tg_player in self._players:
                if tg_player.get_name() == target_player_name and player.get_name() != target_player_name:
                    target_player = tg_player
                    break

            if target_player is None:
                print("Invalid player. Try again!")
                continue
            return target_player

    def get_current_player(self):
        return self._players[self._current_player]

    def show_died_player(self):
        if len(self._died_players) > 0:
            print(
                f"These players are dead: {[player.get_name() for player in self._died_players]}")

    def show_deck_card_number(self):
        print(
            f"Number of cards left on the draw pile: {self.deck.current_card_left()}")
