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
    
    drawCards(7, unoDeck, player1Hand)
    drawCards(7, unoDeck, player2Hand)

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

    while not gameOver(player1Hand, player2Hand, unoDeck):
        print("Last Card Played:", lastCard)
        print("Player 1 Hand:", player1Hand)
        print("Player 2 Hand:", player2Hand)
        print("-----------------------------------------")

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
                print("Player 1 plays:", card)
                if len(player1Hand) == 1:
                    print("Player 1 shouts 'UNO!'")
                    turn = "player2"
            else:
                drawCards(1, unoDeck, player1Hand)
                print("Player 1 draws a card")
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
                print("Player 2 plays:", card)
                if len(player2Hand) == 1:
                    print("Player 2 shouts 'UNO!'")
                    turn = "player1"
            else:
                drawCards(1, unoDeck, player2Hand)
                print("Player 2 draws a card")
                turn = "player1"

    print("-----------------------------------------")
    print("Game Over!")
    if len(unoDeck) == 0:
        print("Tie!")
    print("Last Card Played:", lastCard)
    print("Player 1 Hand:", player1Hand)
    print("Player 2 Hand:", player2Hand)
    print("-----------------------------------------")


def gameOver(player1Hand, player2Hand, unoDeck):
    """
    Check whether the game is over or not.
    """
    return len(player1Hand) == 0 or len(player2Hand) == 0 or len(unoDeck) == 0


gameStart()