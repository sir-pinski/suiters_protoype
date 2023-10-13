from itertools import product


class HalfCard:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return f"{self.value} of {self.suit}"


class Card:
    def __init__(self, top_half, bottom_half):
        self.first_half = HalfCard(top_half[0], top_half[1])
        self.second_half = HalfCard(bottom_half[0], bottom_half[1])

    def __repr__(self):
        return f"{self.first_half} | {self.second_half}"


class Deck:
    SUITS = ['hearts', 'spades', 'diamonds', 'clubs']

    def __init__(self, min_value=1, max_value=10, max_sum=12, hand_size=7):
        self.NUMBERS = list(range(min_value, max_value + 1))

        self.cards = [Card(first, second)
                      for first, second in product(product(self.NUMBERS, self.SUITS), repeat=2)
                      if (first[0] + second[0] <= max_sum and first[1] != second[1])]
        self.shuffle()

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)
