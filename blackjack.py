"""A simple terminal blackjack game. Run with: python blackjack.py"""

import random


def make_deck():
    deck = [(rank, suit) for suit in ("Clubs", "Diamonds", "Hearts", "Spades")
            for rank in ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")]
    random.shuffle(deck)
    return deck


def hand_value(hand):
    total = 0
    aces = 0
    for rank, _ in hand:
        if rank == "A":
            total += 11
            aces += 1
        else:
            total += 10 if rank in ("J", "Q", "K") else int(rank)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def show_hand(name, hand, hidden=False):
    visible = hand[:1] if hidden else hand
    cards = ", ".join(f"{rank} of {suit}" for rank, suit in visible)
    if hidden:
        print(f"{name}: {cards}, [hidden card]")
    else:
        print(f"{name}: {cards} (total: {hand_value(hand)})")


def ask(prompt, choices):
    while True:
        answer = input(prompt).strip().lower()
        if answer in choices:
            return answer
        print("Please enter one of: " + ", ".join(choices))


def play_round():
    deck = make_deck()
    player, dealer = [], []
    for _ in range(2):
        player.append(deck.pop())
        dealer.append(deck.pop())

    print("\n--- New round ---")
    show_hand("Dealer", dealer, hidden=True)
    show_hand("You", player)

    if hand_value(player) == 21 or hand_value(dealer) == 21:
        show_hand("Dealer", dealer)
        if hand_value(player) == hand_value(dealer):
            print("Both have blackjack! It's a tie.")
        elif hand_value(player) == 21:
            print("Blackjack! You win!")
        else:
            print("Dealer has blackjack. Dealer wins.")
        return

    while hand_value(player) < 21:
        action = ask("Hit or stay? [h/s]: ", ("h", "hit", "s", "stay"))
        if action in ("s", "stay"):
            break
        player.append(deck.pop())
        show_hand("You", player)

    if hand_value(player) > 21:
        show_hand("Dealer", dealer)
        print("You bust! Dealer wins.")
        return

    print("\nDealer's turn:")
    show_hand("Dealer", dealer)
    while hand_value(dealer) < 18:
        print("Dealer hits.")
        dealer.append(deck.pop())
        show_hand("Dealer", dealer)

    player_total, dealer_total = hand_value(player), hand_value(dealer)
    if dealer_total > 21:
        print("Dealer busts! You win!")
    elif player_total > dealer_total:
        print("You win!")
    elif player_total < dealer_total:
        print("Dealer wins.")
    else:
        print("It's a tie!")


def main():
    print("Welcome to Blackjack!")
    print("Get as close to 21 as possible without going over.")
    print("Aces count as 1 or 11. The dealer stays on all 18s.")
    try:
        while True:
            play_round()
            if ask("\nPlay again? [y/n]: ", ("y", "yes", "n", "no")) in ("n", "no"):
                break
    except (EOFError, KeyboardInterrupt):
        print()
    print("Thanks for playing!")


if __name__ == "__main__":
    main()
