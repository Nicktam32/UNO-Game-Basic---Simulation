import random

def buildDeck():
    """
    Building deck for UNO Basic game.
    The card includes 0-9 with 4 colours and 4 draw cards.
    Total number of cards is 44.
    Example card: Red 7, Green 8, Blue 9
    """
    deck = []
    colours = ["Red", "Green", "Yellow", "Blue"]
    numbersCard = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    for colour in colours:
        for numbers in numbersCard:
            cards = colour + " " + str(numbers)
            deck.append(cards)

    return deck


def shuffleDeck(deck):
    """
    Shuffles a list of items passed into it.
    """
    random.shuffle(deck)
    return deck


def drawCards(numbers_of_draws, deck_on_hand, deck):
    """
    Remove the first card on deck and draw card on playerHand.
    """
    for times in range(numbers_of_draws):
        deck_on_hand.append(deck.pop(0))


def goFirst():
    """
    Randomly determine which player goes first.
    """
    return random.choice(["player1", "player2"])


def pickFirstCard(hand):
    color_lst = []
    for card in hand:
        color_lst.append(card[:-2])

    colourFrequencies = {}
    for i in set(color_lst):
        colourFrequencies[i] = color_lst.count(i)

    maxColor = max(colourFrequencies, key=colourFrequencies.get)

    return hand[color_lst.index(maxColor)]


def playCard(card, hand):
    """
    Play a card from the player's hand.
    """
    hand.remove(card)


def pickCard(last_card, hand):
    """
    Pick a card from the player's hand that matches the color or number of the last card played.
    """
    last_card_color = last_card.split()[0]
    last_card_number = last_card.split()[1]

    same_color_cards = [card for card in hand if card.startswith(last_card_color)]
    same_number_cards = [card for card in hand if card.endswith(last_card_number)]

    if same_color_cards:
        return random.choice(same_color_cards)
    elif same_number_cards:
        return random.choice(same_number_cards)
    else:
        return None


def gameStart():
    """
    Game Start!
    It will recall all the function built before
    """
    unoDeck = shuffleDeck(buildDeck())
    player1Hand = []
    player2Hand = []

    drawCards(5, player1Hand, unoDeck)
    drawCards(5, player2Hand, unoDeck)

    turn = goFirst()

    if turn == "player1":
        lastCard = pickFirstCard(player1Hand)
        playCard(lastCard, player1Hand)
        turn = "player2"
    else:
        lastCard = pickFirstCard(player2Hand)
        playCard(lastCard, player2Hand)
        turn = "player1"

    rounds = 1

    while not gameOver(player1Hand, player2Hand, unoDeck):
        if turn == "player1":
            card = pickCard(lastCard, player1Hand)
            if card:
                playCard(card, player1Hand)
                lastCard = card
            else:
                drawCards(1, player1Hand, unoDeck)
            turn = "player2"
        else:
            card = pickCard(lastCard, player2Hand)
            if card:
                playCard(card, player2Hand)
                lastCard = card
            else:
                drawCards(1, player2Hand, unoDeck)
            turn = "player1"

        rounds += 1

    if len(player1Hand) == 0:
        return "player1", rounds
    elif len(player2Hand) == 0:
        return "player2", rounds
    else:
        return "Tie", rounds


def gameOver(player1Hand, player2Hand, unoDeck):
    """
    Check whether the game is over or not.
    """
    if len(player1Hand) == 0 or len(player2Hand) == 0 or len(unoDeck) == 0:
        return True
    else:
        return False


def simulateGames(num_games):
    player1_wins = 0
    player2_wins = 0
    tie_count = 0
    player1_first_wins = 0
    player2_first_wins = 0
    total_rounds = 0

    for _ in range(num_games):
        result, rounds = gameStart()
        if result == "player1":
            player1_wins += 1
            if rounds % 2 == 1:
                player1_first_wins += 1
        elif result == "player2":
            player2_wins += 1
            if rounds % 2 == 0:
                player2_first_wins += 1
        else:
            tie_count += 1

        total_rounds += rounds

    player1_win_rate = (player1_wins / num_games) * 100
    player2_win_rate = (player2_wins / num_games) * 100
    tie_rate = (tie_count / num_games) * 100
    player1_first_win_rate = (player1_first_wins / (player1_first_wins + player2_first_wins)) * 100
    player2_first_win_rate = (player2_first_wins / (player1_first_wins + player2_first_wins)) * 100
    avg_rounds = total_rounds / num_games

    return player1_win_rate, player2_win_rate, tie_rate, player1_first_win_rate, player2_first_win_rate, avg_rounds


# Run simulation for 10,000 games
player1_win_rate, player2_win_rate, tie_rate, player1_first_win_rate, player2_first_win_rate, avg_rounds = simulateGames(10000)
print("Fair Win rate: "   , 0.5)
print("player1_win_rate: ", player1_win_rate)
print("player2_win_rate: ", player2_win_rate)
print("tie_rate: ", tie_rate)
print("player1_first_win_rate: ", player1_first_win_rate)
print("player2_first_win_rate: ", player2_first_win_rate)
print("avg_rounds: ", avg_rounds)

import matplotlib.pyplot as plt

# Create a bar chart
labels = ['Player 1', 'Player 2', "Tie"]
win_rates = [player1_win_rate, player2_win_rate, tie_rate]
fair_win_rate = 50

plt.bar(labels, win_rates)
plt.axhline(y=fair_win_rate, color='r', linestyle='--', label='Fair Win Rate')
plt.xlabel('Players')
plt.ylabel('Win Rate (%)')
plt.title('Win Rates of Player 1, Player 2 and Tie')
plt.ylim([0, 100])
plt.legend()

# Display the bar chart
plt.show()