from collections import deque
import random

class Card:

    def __init__(self, val: int, suit: str):

        if val not in range(0,14): # in ace to king range (0 is joker)
            raise ValueError("The Specified Card is NOT within the correct range.")
        
        elif suit.lower() not in ['s', 'c', 'h', 'd', '*']:
            raise ValueError("The Specified Card SUIT is NOT valid.")
        
        else:
            self.val = val
            self.suit = suit
    
    def cardInfo(self): # returns a tuple of the card object so it is readable from memory
        return (self.val, self.suit)
    
    def cardInfoEasy(self): # this is just the same as cardInfo but with extra logic to prevent confusion on what 1,11,12,13 mean

        if self.val == 1:
            return("(A, '" + self.suit + "')")
        elif self.val == 11:
            return("(J, '" + self.suit + "')")
        elif self.val == 12:
            return("(Q, '" + self.suit + "')")
        elif self.val == 13:
            return("(K, '" + self.suit + "')")
        else:
            return (self.val, self.suit)

class Deck():

    def __init__(self):
        self.deckQueue = deque()

    def createDeck(self, jokers=False):
        for items in ['s', 'c', 'h', 'd']:
            for i in range(1 ,14):
                self.deckQueue.append(Card(i, items))

        if jokers: 
            self.deckQueue.append(Card(0, "*"))
            self.deckQueue.append(Card(0, "*"))
    
    def addCard(self, val, suit): # adds a card object to the bottom of the deck
        self.deckQueue.append(Card(val, suit))

    def addCard(self, c: Card): # function overloading
        self.deckQueue.append(c)

    def addTopCard(self, val, suit): # adds a card object to the top of the deck
        self.deckQueue.appendleft(Card(val,suit))

    def addTopCard(self, c: Card):
        self.deckQueue.appendleft(c)

    def checkValidDeck(self): # 
        for items in self.deckQueue:
            if items.cardInfo()[0] not in range(0,14) or items.cardInfo()[1] not in ['s', 'c', 'h', 'd', '*']:
                raise Exception("This deck contains invalid cards")
            else:
                return None
    
    def mergeDeck(self, deckToMerge): # allows the ability to merge two decks into 1 (first deck becomes larger)
        self.deckQueue.extend(deckToMerge.deckQueue) 

    def deckSize(self): # returns the number of cards within the deck
        return len(self.deckQueue)
    
    def shuffleDeck(self): # quick way to shuffle the deck
        tempDeck = list(self.deckQueue.copy())
        random.shuffle(tempDeck)
        self.deckQueue = deque(tempDeck)
        # return self.deckQueue

    def printDeck(self): # assumes that the card object works
        for item in self.deckQueue:
            print(item.cardInfoEasy())

    def revealTopNcards(self, n: int): # reveals top n cards
        miniDeck = Deck()
        if n > len(self.deckQueue) or n < 1:
            raise ValueError("Invalid N-value for deck size")
        for i in range(n):
            miniDeck.addCard(self.deckQueue[i].val, self.deckQueue[i].suit)
        return miniDeck

    def revealBottomNCards(self, n: int): # reveals bottom n cards
        miniDeck = Deck()
        if n > len(self.deckQueue) or n < 1:
            raise ValueError("Invalid N-value for deck size")
        for i in range(len(self.deckQueue) - 1, len(self.deckQueue) - n - 1, -1):
            miniDeck.addCard(self.deckQueue[i].val, self.deckQueue[i].suit)
        return miniDeck
    
    def dealNcards(self, recipient, numberOfCards: int): # this function deals N number of cards to the specified hand from a specified deck
        if numberOfCards > self.deckSize():
            raise Exception('There are not enough cards in the specified deck!')
        else:
            for _ in range(numberOfCards):
                recipient.addCard(self.deckQueue.removeTopCard())

    def sortDeck(self): # a little scuffed sorting 
        deckSuitOrder = {'s': 1, 'c': 2, 'h': 3, 'd': 4, '*': 5} # custom deck suit arrangement for sorting
        temp = self.deckQueue.copy()
        temp = list(temp)

        for i in range(len(temp)):
            temp[i] = temp[i].cardInfo() # changes the data into something easier to work with

        temp.sort(key=lambda x: (deckSuitOrder[x[1]], x[0])) # sorts according to suit then sorts the value numerically
        # print(temp)
        for i in range(len(temp)):
            temp[i] = Card(temp[i][0], temp[i][1]) # undos the changes to turn it back into a card object
        temp = deque(temp) # convert list back into deque
        self.deckQueue = temp 

    def selectRandomCard(self):
        randomIdx = random.randint(0, self.deckSize())
        return self.deckQueue[randomIdx]
    
    def removeRandomCard(self): # rather inefficient but still some functionality
        self.checkEmptyDeck()
        randomIdx = random.randint(0, self.deckSize()-1)
        randomCard = self.deckQueue[randomIdx]
        del self.deckQueue[randomIdx]
        return randomCard

    def removeTopCard(self): # removes card from the top
        self.checkEmptyDeck()
        return self.deckQueue.popleft()
    
    def removeBottomCard(self): # remove card from the top
        self.checkEmptyDeck()
        return self.deckQueue.pop()
    
    def clearDeck(self): # deletes the deck
        while self.deckSize() != 0:
            self.deckQueue.pop()
        
    def checkEmptyDeck(self):
        if self.deckSize() <= 0: # should never be less than 0 
            # if it is empty raise an exception
            raise Exception('The specified deck is empty.')
        
    # splitDeck is somewhat a confusing name.. a more appropriate one would be distribute deck evenly or something
    # note the last deck IS ALWAYS THE REMAINDER CARDS
    # slightly easier way to deal the entire deck between n amount of people
    def splitDeck(self, n: int): # splits deck into even partitions # remainder cards will go into leftover deck
        self.checkEmptyDeck() # want to check if the deck has at least 1 card

        # to avoid division errors we will want to have n < deck size

        if n > self.deckSize():
            raise Exception('The value n cannot be larger than the size of the deck.')

        partitionSize = self.deckSize() // n # integer division
        # ex. 52 card split by 3 should have each deck with 17 cards and one remainder card
        # function should return a tuple of size n+1
        splitDecks = []
        idx = 0

        for i in range(0, self.deckSize() - partitionSize, partitionSize): # skips with partition size
            splitDecks.append(Deck()) # add a new deck to the list
            for j in range(0, partitionSize): # we find which card we're at using i + j
                splitDecks[idx].addCard(Card(self.deckQueue[i+j].val, self.deckQueue[i+j].suit))

            # after exiting the innermost loop we should increment idx
            idx += 1

        # after all the partitions have been made the remainder deck is initialized
        splitDecks.append(Deck())

        # add the remainder of the cards to the deck
        # this number should always be less than partition size
        for i in range(n*partitionSize, self.deckSize()):
            splitDecks[idx].addCard(Card(self.deckQueue[i].val, self.deckQueue[i].suit))

        return tuple(splitDecks)




        

        




        
        

    