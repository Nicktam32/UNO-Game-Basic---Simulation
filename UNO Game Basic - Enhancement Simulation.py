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
    specialCards = ["Draw Two", "Reverse", "Skip"]


    for colour in colours:
        for number in numbersCard:
            card = colour + " " + str(number)
            deck.append(card)

        for special in specialCards:
            card = colour + " " + special
            deck.append(card)

    return deck


def shuffleDeck(deck):
    """
    Shuffles a list of items passed into it.
    """
    random.shuffle(deck)


def drawCards(num_of_draws, deck, hand):
    """
    Remove the first num_of_draws cards from the deck and add them to the player's hand.
    """
    for _ in range(num_of_draws):
        if deck:
            hand.append(deck.pop(0))


def goFirst():
    """
    Randomly determine which player goes first.
    """
    return random.choice(["player1", "player2"])


def pickFirstCard(hand):
    """
    Pick a card from the player's hand to start the game.
    """
    valid_cards = [card for card in hand if not card.startswith("Wild")]
    if valid_cards:
        return random.choice(valid_cards)
    return None


def playCard(card, hand, discard_pile):
    """
    Play a card from the player's hand and add it to the discard pile.
    """
    hand.remove(card)
    discard_pile.append(card)
    

def pickCard(last_card, hand):
    """
    Pick a card from the player's hand that matches the color or number of the last card played.
    """
    last_card_color = last_card.split()[0]
    last_card_number = last_card.split()[1]

    matching_cards = [card for card in hand if card.startswith(last_card_color) or card.endswith(last_card_number)]
    
    if matching_cards:
        return random.choice(matching_cards)
    return None


def gameStart():
    """
    Game Start!
    """
    unoDeck = buildDeck()
    shuffleDeck(unoDeck)

    player1Hand = []
    player2Hand = []
    discardPile = []
    
    drawCards(5, unoDeck, player1Hand)
    drawCards(5, unoDeck, player2Hand)

    turn = goFirst()

    if turn == "player1":
        lastCard = pickFirstCard(player1Hand)
        if lastCard.endswith("Draw Two"):
            drawCards(2, unoDeck, player1Hand)
            turn = "player2"
        elif lastCard.endswith("Reverse") or lastCard.endswith("Skip"):
            playCard(lastCard, player1Hand, discardPile)
            turn = "player1"
        else:
            playCard(lastCard, player1Hand, discardPile)
            turn = "player2"
    else:
        lastCard = pickFirstCard(player2Hand)
        if lastCard.endswith("Draw Two"):
            drawCards(2, unoDeck, player2Hand)
            turn = "player1"
        elif lastCard.endswith("Reverse") or lastCard.endswith("Skip"):
            playCard(lastCard, player2Hand, discardPile)
            turn = "player2"
        else:
            playCard(lastCard, player2Hand, discardPile)
            turn = "player1"

    rounds = 1

    while not gameOver(player1Hand, player2Hand, unoDeck):
        if turn == "player1":
            card = pickCard(lastCard, player1Hand)
            if card:
                if card.endswith("Draw Two"):
                    drawCards(2, unoDeck, player1Hand)
                    turn = "player2"
                elif card.endswith("Reverse") or card.endswith("Skip"):
                    playCard(card, player1Hand, discardPile)
                    turn = "player1" 
                else:
                    playCard(card, player1Hand, discardPile)
                    turn = "player2"
                lastCard = card
                if len(player1Hand) == 1:
                    turn = "player2"
            else:
                drawCards(1, unoDeck, player1Hand)
                turn = "player2"

        else:
            card = pickCard(lastCard, player2Hand)
            if card:
                if card.endswith("Draw Two"):
                    drawCards(2, unoDeck, player2Hand)
                    turn = "player1"
                elif card.endswith("Reverse") or card.endswith("Skip"):
                    playCard(card, player2Hand, discardPile)
                    turn = "player2" 
                else:
                    playCard(card, player2Hand, discardPile)
                    turn = "player1"
                lastCard = card
                if len(player2Hand) == 1:
                    turn = "player1"
            else:
                drawCards(1, unoDeck, player2Hand)
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
    return len(player1Hand) == 0 or len(player2Hand) == 0 or len(unoDeck) == 0


gameStart()

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


import matplotlib.pyplot as plt
# Run simulation for 10,000 games
player1_win_rate, player2_win_rate, tie_rate, player1_first_win_rate, player2_first_win_rate, avg_rounds = simulateGames(10000)
print("Fair Win rate: "   , 0.5)
print("player1_win_rate: ", player1_win_rate)
print("player2_win_rate: ", player2_win_rate)
print("tie_rate: ", tie_rate)
print("player1_first_win_rate: ", player1_first_win_rate)
print("player2_first_win_rate: ", player2_first_win_rate)
print("avg_rounds: ", avg_rounds)

# Create a bar chart
labels = ['Player 1', 'Player 2', 'Tie']
win_rates = [player1_win_rate, player2_win_rate, tie_rate]
fair_win_rate = 50

plt.bar(labels, win_rates)
plt.axhline(y=fair_win_rate, color='r', linestyle='--', label='Fair Win Rate')
plt.xlabel('Players')
plt.ylabel('Win Rate (%)')
plt.title('Win Rates of Player 1, Player 2, and Tie')
plt.ylim([0, 100])
plt.legend()

# Display the bar chart
plt.show()