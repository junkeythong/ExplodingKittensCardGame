import random
from card import Card

class Deck:
    def __init__(self):
        self._cards = []
        self._init()
        self.shuffle()

    def _init(self):
        cards = [Card("Attack") for i in range(20)]
        cards += [Card("Skip") for i in range(80)]
        cards += [Card("Favor") for i in range(4)]
        cards += [Card("Shuffle") for i in range(4)]
        cards += [Card("See The Future") for i in range(5)]
        cards += [Card("Nope") for i in range(5)]
        # change the cat card to another name if we like
        cards += [Card("Cat 1") for i in range(4)]
        cards += [Card("Cat 2") for i in range(4)]
        cards += [Card("Cat 3") for i in range(4)]
        cards += [Card("Cat 4") for i in range(4)]
        cards += [Card("Cat 5") for i in range(4)]
        self._cards = cards

    def get_cards(self):
        return self._cards
    
    def add_card(self, card):
        self._cards.append(card)

    def draw_card(self):
        if len(self._cards) == 0:
            return None
        return self._cards.pop(0)
    
    def shuffle(self):
        random.shuffle(self._cards)

    def current_card_left(self):
        return len(self._cards)
    
    def get_top_3_cards(self):
        return [card.get_name() for card in self._cards[:3]]
