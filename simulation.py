from card_deck import Deck
from game_logic import Game, display_hand, play_game, calculate_score_from_hand, display_scores


def simulate_game_draws(n=500, min_val=1, max_val=10, m_sum=14, hand=7, draws=2):
    score_hand_pairs = []

    for _ in range(n):
        deck = Deck(min_value=min_val, max_value=max_val, max_sum=m_sum)
        game = Game(deck, hand_size=hand)
        game.ai_play(draws)
        _, total_score = game.calculate_score()
        score_hand_pairs.append((total_score, game.hand))

    return score_hand_pairs


def compute_statistics(score_hand_pairs):
    import numpy as np

    scores = [score for score, _ in score_hand_pairs]

    min_score = min(scores)
    max_score = max(scores)
    avg_score = np.mean(scores)
    median_score = np.median(scores)
    first_quartile = np.percentile(scores, 25)
    third_quartile = np.percentile(scores, 75)

    max_hand = [hand for score, hand in score_hand_pairs if score == max_score][0]
    min_hand = [hand for score, hand in score_hand_pairs if score == min_score][0]

    # Sort the score-hand pairs by score in descending order and extract the top 10
    top_10_score_hand_pairs = sorted(score_hand_pairs, key=lambda x: x[0], reverse=True)[:10]
    top_10_scores = [score for score, _ in top_10_score_hand_pairs]
    top_10_hands = [hand for _, hand in top_10_score_hand_pairs]

    return {
        'Hands': len(scores),
        'Minimum': min_score,
        'Maximum': max_score,
        'Average': avg_score,
        'Median': median_score,
        '1st Quartile': first_quartile,
        '3rd Quartile': third_quartile,
        'Hand with Max Score': max_hand,
        # 'Hand with Min Score': min_hand,
        'Top 10 Scores': top_10_scores,
        # 'Hands with Top 10 Scores': top_10_hands
    }


def main_simulation(n, min_val, max_val, m_sum, hand, draws):
    score_hand_pairs = simulate_game_draws(n, min_val, max_val, m_sum, hand, draws)
    stats = compute_statistics(score_hand_pairs)

    for key, value in stats.items():
        if key == 'Hand with Max Score' or key == 'Hand with Min Score':
            print(f"{key}:")
            display_hand(value)
            display_scores(calculate_score_from_hand(value))
        elif key == 'Top 10 Scores':
            formatted_scores = [format(score, ',') for score in value]
            print(f"{key}: {', '.join(formatted_scores)}")
        elif key == 'Hands with Top 10 Scores':
            print(f"{key}:")
            for hand in value:
                display_hand(hand)
                print("---")
        else:
            print(f"{key}: {format(value, ',.2f')}")


def user_choice():
    print("Choose an option:")
    print("1. Play the game manually")
    print("2. Run the AI simulation")
    return int(input("Enter your choice (1/2): "))


def main():
    choice = user_choice()

    n = 50
    min_val = 0
    max_val = 10
    m_sum = 12
    hand = 7
    draws = 2

    if choice == 1:
        # Play the game
        play_game(min_val, max_val, m_sum, hand, draws)
    elif choice == 2:
        # Run the simulation
        main_simulation(n, min_val, max_val, m_sum, hand, draws)
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
