import random

class Player:
    def __init__(self, id, name):
        self._id = id
        self._name = name
        self._hand = []

        # This is a mark to know if the player has been attacked
        self._num_attacks = 0
        self._is_dead = False
        
    def add_card_to_hand(self, card):
        self._hand.append(card)

    def get_card_from_hand(self, card_name):
        for card in self._hand:
            if card._name == card_name:
                return card
        return None
    
    def get_name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name

    def get_id(self):
        return self._id

    def get_hand(self):
        return self._hand

    def remove_card_from_hand(self, card):
        self._hand.remove(card)

    def play_card(self, card):
        self.remove_card_from_hand(card)

    def take_card_from_hand(self, card):
        self.remove_card_from_hand(card)

    def has_card(self, card_name):
        return any(card._name == card_name for card in self._hand)
    
    def get_random_card(self):
        return random.choice(self._hand)
    
    def has_died(self):
        return self._is_dead
    
    def died(self, is_die):
        self._is_dead = is_die

    def get_num_attacks(self):
        return self._num_attacks
    
    def set_num_attacks(self, num_attacks):
        self._num_attacks += num_attacks
        
    # If the player plays special combos
    def has_pair_card(self, card_name):
        count = 1
        for card in self._hand:
            if card._name == card_name:
                count += 1
            if count == 2:
                return True
        return False