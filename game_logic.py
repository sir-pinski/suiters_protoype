from card_deck import Deck


class Game:
    def __init__(self, deck, hand_size=7):
        self.deck = deck
        self.hand = [self.deck.draw() for _ in range(hand_size)]
        self.scores = self.calculate_score()

    def discard_and_draw(self, discard_indices):
        for index in sorted(discard_indices, reverse=True):
            if index >= 0:
                del self.hand[index]
                self.hand.append(self.deck.draw())

    # Original algorithm, no longer used
    def calculate_score_sum_prods(self):
        score_dict = {suit: [] for suit in Deck.SUITS}

        for card in self.hand:
            for number, suit in [card.first_half, card.second_half]:
                score_dict[suit].append(number)

        total_score = 0
        suit_scores = {}
        for suit, numbers in score_dict.items():
            if numbers:
                product = 1
                for num in numbers:
                    product *= num
                numbers_sorted = sorted(numbers)
                product -= numbers_sorted[-1]
                total_score += product
                suit_scores[suit] = product

        max_suit_score = max(suit_scores.values(), default=0)
        return suit_scores, total_score - max_suit_score

    def calculate_score(self):
        """Calculate the score for the current hand."""
        suit_sums = {suit: 0 for suit in Deck.SUITS}

        # Sum the values within each suit.
        for card in self.hand:
            for half_card in [card.first_half, card.second_half]:
                suit_sums[half_card.suit] += half_card.value

        # Multiply the sums across all suits.
        total_score = 1
        for suit_sum in suit_sums.values():
            total_score *= suit_sum

        return suit_sums, total_score

    def ai_play(self, draws):
        """AI decision-making logic."""
        for _ in range(draws):  # two discard/draw rounds
            discard_indices = self.ai_decide_discard()
            self.discard_and_draw(discard_indices)
            self.scores = self.calculate_score()

    def ai_decide_discard(self):
        """Determine which cards to discard based on the AI logic."""
        discard_indices = []

        for index, card in enumerate(self.hand):
            card_sum = card.first_half.value + card.second_half.value
            if card_sum < 6:
                discard_indices.append(index)

        return discard_indices

def calculate_score_from_hand(hand):
    """Calculate the score for the current hand."""
    suit_sums = {suit: 0 for suit in Deck.SUITS}

    # Sum the values within each suit.
    for card in hand:
        for half_card in [card.first_half, card.second_half]:
            suit_sums[half_card.suit] += half_card.value

    # Multiply the sums across all suits.
    total_score = 1
    for suit_sum in suit_sums.values():
        total_score *= suit_sum

    return suit_sums, total_score

def display_hand(hand):
    for index, card in enumerate(hand):
        print(f"{index + 1}. {card}")


def display_scores(scores):
    suit_scores, total_score = scores

    for suit, score in suit_scores.items():
        print(f"Score for {suit}: {score}")
    print(f"Total Score: {format(total_score, ',')}")


def ask_for_discard():
    discard_indices = input(
        "Enter the card numbers (separated by commas) you want to discard, or 0 to keep all: ")
    return [int(index) - 1 for index in discard_indices.split(",")]


def play_game(min_val=1, max_val=10, m_sum=14, hand=7, draws=2):
    deck = Deck(min_value=min_val, max_value=max_val, max_sum=m_sum)
    game = Game(deck, hand_size=hand)
    draw_chances = draws

    for chance in range(draw_chances):
        print("\nYour hand:")
        display_hand(game.hand)
        print("\nYour scores:")
        display_scores(game.scores)

        discard_indices = ask_for_discard()
        game.discard_and_draw(discard_indices)
        game.scores = game.calculate_score()

    print("\nYour final hand:")
    display_hand(game.hand)
    print("\nYour final scores:")
    display_scores(game.scores)
