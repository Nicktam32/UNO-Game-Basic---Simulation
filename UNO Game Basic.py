import random

def buildDeck():
    """
    Building deck for UNO Basic game.
    The card includes 0-9 with 4 colours.
    Total number of cards is 40.
    Example card: Red 7, Green 8, Blue 9
    """
    deck = []
    colours = ["Red", "Green", "Yellow", "Blue"]
    numbersCard = [0,1,2,3,4,5,6,7,8,9]

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
    
    print("UNO Deck: ", unoDeck)
    print("player1Hand: ", player1Hand)
    print("player2Hand: ", player2Hand)
    print("-----------------------------------------")
    drawCards(5, player1Hand, unoDeck)
    drawCards(5, player2Hand, unoDeck)
    print("---------After draw----------------------")
    print("player1Hand: ", player1Hand)
    print("player2Hand: ", player2Hand)    

    turn = goFirst()

    if turn == "player1":
        lastCard = pickFirstCard(player1Hand)
        print("---------First Card------------------")
        print("Player 1 plays:", lastCard)
        playCard(lastCard, player1Hand)
        print("player1Hand: ", player1Hand)
        print("player2Hand: ", player2Hand)  
        turn = "player2"
    elif turn == "player2":
        lastCard = pickFirstCard(player1Hand)
        print("---------First Card------------------")
        print("Player 2 plays:", lastCard)
        playCard(lastCard, player2Hand)
        print("player1Hand: ", player1Hand)
        print("player2Hand: ", player2Hand) 
        turn = "player1"

    while not gameOver(player1Hand, player2Hand, unoDeck):
        if turn == "player1":
            print("---------Next Turn----------------")
            card = pickCard(lastCard, player1Hand)
            if card:
                if len(player1Hand) == 2:
                    print("Player 1 UNO!")
                print("Player 1 plays:", card)
                playCard(card, player1Hand)
                lastCard = card
            else:
                print("Player 1 draws a card")
                drawCards(1, player1Hand, unoDeck)
            turn = "player2"
        else:
            print("---------Next Turn----------------")
            card = pickCard(lastCard, player2Hand)
            if card:
                if len(player2Hand) == 2:
                    print("Player 2 UNO!")
                print("Player 2 plays:", card)
                playCard(card, player2Hand)
                lastCard = card
            else:
                print("Player 2 draws a card")
                drawCards(1, player2Hand, unoDeck)
            turn = "player1"

        print("player1Hand:", player1Hand)
        print("player2Hand:", player2Hand)

    print("Game Over!")
    if len(unoDeck) == 0:
        turn = "Tie"
        print("Tie!")


def gameOver(player1Hand, player2Hand, unoDeck):
    """
    Check whether the game is over or not.
    """
    if len(player1Hand) == 0 or len(player2Hand) == 0 or len(unoDeck) == 0:
        print('Game Over!')
        return True
    else:
        return False

gameStart()

