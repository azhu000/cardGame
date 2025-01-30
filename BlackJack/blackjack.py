# from Cards import card as cds
import sys

sys.path.append('/Users/anthonyzhu/Desktop/cards')
import BlackJack.blackjacksetup as bjs

# the blackjack game

# dealer and player
# does not have betting system atm

def blackjack():
    bjs.bjGame()
    
blackjack()