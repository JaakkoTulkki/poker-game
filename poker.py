import random
SUITS = ['S', 'D', 'H', 'C']
VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
class Card(object):
    def __init__(self, card):
        card = card.split(" ")
        self.suit = card[0]
        self.value = card[1]

    def __str__(self):
        return str(self.suit) + " " + self.value

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

class BaseDeck(object):
    _shared_state = {}

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj.__dict__ = cls._shared_state
        return obj

class Deck(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.deck = self.create_deck()

    def create_deck(self):
        if hasattr(self, "deck"):
            return self.deck
        deck = []
        for suit in SUITS:
            for value in VALUES:
                deck.append(Card("{} {}".format(suit, value)))
        self.shuffle(deck)
        return deck

    def shuffle(self, deck):
        random.shuffle(deck)
        return deck

class Poker(object):
    def __init__(self):
        self.deck = Deck()

    def give_cards(self, num):
        five_cards = self.deck.deck[:num]
        self.deck.deck = self.deck.deck[num:]
        return five_cards

    def give_hand(self):
        self.hand = self.give_cards(5)
        self.values = [e.value for e in self.hand]

    def evaluate_hand(self):
        self.high_card = self.set_high_card()
        self.pairs = self.has_pairs()
        self.two_pairs = self.has_two_pairs()
        self.threes = self.has_threes()
        self.straight = self.has_straight()
        self.flush = self.has_flush()
        self.full_house = self.has_full_house()
        self.four_of_kind = self.has_four_of_kind()
        self.roayl_flush = self.has_roayl_flush()

    def set_high_card(self):
        return [max(self.hand, key=lambda x: VALUES.index(x.value))]

    def has_pairs(self):
        if len(set(self.values)) != 4:
            return None
        pair_value = None
        cards = []
        for card in self.hand:
            if self.values.count(card.value) == 2:
                pair_value = card.value
                break
        if pair_value:
            for card in self.hand:
                if card.value == pair_value:
                    cards.append(card)
        if cards: return cards
        return None

    def has_two_pairs(self):
        if len(set(self.values)) != 3 or self.has_threes():
            return None
        cards = []
        for card in self.hand:
            if self.values.count(card.value) == 2:
                cards.append(card)
        return card

    def has_threes(self):
        if len(set(self.values)) != 3:
            return None
        cards = []
        for card in self.hand:
            if self.values.count(card.value) == 3:
                cards.append(card)
        return cards

    def has_straight(self):
        values = [VALUES.index(e.value) for e in self.hand]
        if len(set(self.values)) != 5:
            return False
        if max(values) - min(values) == 4:
            return self.hand
        #if we don't have ACE in the hand
        elif 13 not in values:
            return False
        #if we have it
        else:
            values.remove(max)
            values.append(-1)
            if max(values) - min(values) == 4:
                return self.hand
            else:
                return False

    def has_flush(self):
        return True if len(set([e.suit for e in self.hand])) == 1 else False

    def has_full_house(self):
        if len(set(self.values)) != 2:
            return False
        lens = [2, 3]
        for e in set(self.values):
            try:
                i = lens.index(self.values.count(e))
                del lens[i]
            except ValueError:
                return None
        return self.hand

    def has_four_of_kind(self):
        if len(set(self.values)) != 2:
            return False
        cards = []
        for card in self.hand:
            if self.values.count(card.value) == 4:
                cards.append(card)
        return cards

    def has_royal_flush(self):
        return True if self.has_flush() and self.has_straight() else False

    def return_best(self):
        combos = [self.has_royal_flush, self.has_four_of_kind, self.has_full_house, self.has_straight,
                  self.has_threes, self.has_two_pairs, self.has_pairs, self.set_high_card]
        for e in enumerate(combos):
            res = combos[e[0]]()
            if res:
                return e[0], res

if __name__ == "__main__":
    import time
    start = time.time()
    results = {}
    for e in range(1000):
        p = Poker()
        p.give_hand()
        best, cards = p.return_best()
        if best not in results:
            results[best] = 1
        else:
            results[best] += 1
        del p.deck
    print(results)
    print(time.time() - start)

    #let's start playing
    results = {}
    start = time.time()
    for e in range(1000):
        player1 = Poker()
        player1.give_hand()
        player1_best, player1_cards = player1.return_best()

        player2 = Poker()
        player2.give_hand()
        player2_best, player2_cards = player2.return_best()

        assert (len(player1.deck.deck) == 42)

        result = "Player 1 wins" if player1_best < player2_best else "Player 2 wins" if player2_best < player1_best else "It's a tie"
        if result not in results:
            results[result] = 1
        else:
            results[result] += 1
        del player2.deck
    print(results)
    print("End time for two player games ", time.time() - start)



