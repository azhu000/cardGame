import Cards.card as cds

def initializeGame(deckCount=4):
        # initialize deck
        dealerHand = cds.Deck() # player and dealer hands (empty at initialization)
        playerHand = cds.Deck()

        if deckCount > 4 or deckCount <= 0:
            raise Exception("The number of decks in invalid.")
        
        mainDeck = cds.Deck() # always have an original deck
        mainDeck.createDeck()

        for i in range(deckCount-1): # iterate/merge n-1 times
            tempDeck = cds.Deck()
            tempDeck.createDeck()
            mainDeck.mergeDeck(tempDeck)

        mainDeck.checkValidDeck()
        # shuffle the deck after merging
        mainDeck.shuffleDeck()

        # deal the first two cards
        for _ in range(2):
            dealerHand.addCard(mainDeck.removeTopCard())
            playerHand.addCard(mainDeck.removeTopCard())

        return (mainDeck, dealerHand, playerHand)

def continueGame(mainDeck, dealer, player): # here we assume we have a valid deck already
    # what needs to be done is to empty the current hands of both players
    # we won't need to shuffle the deck again
    dealer.clearDeck()
    player.clearDeck()

    for _ in range(2):
        dealer.addCard(mainDeck.removeTopCard())
        player.addCard(mainDeck.removeTopCard())

    mainDeck.checkValidDeck()

    return (mainDeck, dealer, player)

def showHands(dH, pH): # shows the hand of the dealer and player
        # takes in two hands and shows them both to the player
        print('===================================================')
        print("This is your current hand:")
        pH.printDeck()
        playerSum = checkHandValue(pH)
        print("Sum of PLAYERS's hand:", playerSum)
        print('***************************************************')
        print("This is the dealer's current hand:")
        dH.printDeck()
        dealerSum = checkHandValue(dH)
        print("Sum of DEALER's hand:", dealerSum)
        if dealerSum >= 17 and dealerSum <= 21:
            print("Dealer Stands!")
        print('===================================================')

    
def checkHandValue(hand):
    handSum = 0
    aceCount = 0
    for item in hand.deckQueue:

        # ace mechanics need working 
        # current issues: the ace needs to be able to act as both an 11 and a 1.
        # let's look the aces last then
        # look at the current hand aside from the aces 
        
        if item.cardInfo()[0] == 1: # ace mechanics
            aceCount += 1 # increment the number of aces

        if item.cardInfo()[0] >= 10:
            handSum += 10
        elif item.cardInfo()[0] < 10 and item.cardInfo()[0] > 1:
            handSum += item.cardInfo()[0]

        while aceCount != 0: # while we have aces left to count
            if handSum + 11 > 21: # if the sum is greater than 21 by adding 11 then add 1
                handSum += 1
            else:  # else add 11
                handSum += 11
            aceCount -= 1 # decrement the number of aces
             
    return handSum
    
def playerHit(player, mainDeck, dealer):
    player.addCard(mainDeck.removeTopCard())
    showHands(dealer, player)

def dealerHit(dealer, mainDeck, player):
    dealer.addCard(mainDeck.removeTopCard())
    showHands(dealer, player) 

    dealerSum = checkHandValue(dealer)

def calculateWinner(dealer, player):
    # this score calculation assumes that both players have not busted
    if dealer < player: 
        return 1 # 1 indicates that player wins
    elif dealer > player:
        return 0 # 0 indicates dealer wins
    
    elif dealer == player:
        return 2 # 2 indicates a tie

     
def bjGame():

    game = initializeGame(deckCount=4)

    showHands(game[1], game[2])
    print('\n\n')

    userInput = ''

    while game[0].deckSize() > 20: # some arbituary value to stop the game from breaking
        print('Cards left in deck:', game[0].deckSize())
        userInput = input('What would you like to do? type !help for commands!\n\n')

        if userInput.lower() == "!help":
            print('The available commands are !showhands, !hit, !stand, !quit')
        
        elif userInput.lower() == "!showhands":
            showHands(game[1], game[2])

        elif userInput.lower() == '!hit':
            playerHit(game[2], game[0], game[1])

            if checkHandValue(game[2]) > 21:
                print('You bust! You have lost...\n\n')

                askQuestion = input('Would you like to play again? Please answer yes or no. Any answer other than yes will quit.\n\n')

                if askQuestion.lower() == 'yes':
                    continueGame(game[0], game[1], game[2])
                    showHands(game[1], game[2])
                    continue
                else:
                    break

        elif userInput.lower() == '!stand':
            print("You stood! It's now the dealers turn...")

            while checkHandValue(game[1]) < 17:
                dealerHit(game[1], game[0], game[2])

            if checkHandValue(game[1]) <= 21:
                print('The dealer has 17 or more and stands!')
            elif checkHandValue(game[1]) > 21:
                print('The dealer busts! You win!')
                askQuestion = input('Would you like to play again? Please answer yes or no. Any answer other than yes will quit.\n\n')
    
                if askQuestion.lower() == 'yes':
                    continueGame(game[0], game[1], game[2])
                    showHands(game[1], game[2])
                    continue
                else:
                    break
            # calculate scores here

            winner = calculateWinner(checkHandValue(game[1]), checkHandValue(game[2]))

            print('Your score is', checkHandValue(game[2]), "the dealer's score is", checkHandValue(game[1]))

            if winner == 0:
                print('Unfortunately you have lost....')
            
            elif winner == 1:
                print('Congratulations you have won!')

            else:
                print("You have tied!")

            askQuestion = input('Would you like to play again? Please answer yes or no. Any answer other than yes will quit.\n\n')

            if askQuestion.lower() == 'yes':
                continueGame(game[0], game[1], game[2])
                showHands(game[1], game[2])
                continue
            else:
                break
        
        elif userInput.lower() == '!quit':
            break

        else:
            print('Sorry, but that does not seem to be a valid command.')
            
        print('\n\n')

    if game[0].deckSize() < 20:
        print('Current deck has insufficient number of cards. Please restart to continue.')

    print('Thanks for playing!')

