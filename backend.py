from classes import *
from main import main
import time

cardStack = []
discoverCounter = 0
player1Turn = True

#handles all the logic of when to do when a given card is clicked
def flipCard(card):
    global cardStack
    global player1Turn
    global discoverCounter

    #if this is the first card flipped after the start of a turn, store it in a stack to be compared with later cards
    #return false to indicate it is the first card
    if len(cardStack) == 0:
        cardStack.append(card)
        return False

    #if this is the second or third card turned over, it gets compared with the previously flipped cards to see if there is a match
    for oldCard in cardStack:
        #checks if the card types match
        if (oldCard.type == card.type):
            #discoverCounter keeps track of how many pairs the player found before his turn ends
            discoverCounter += 1
            for temp in cardStack:
                temp.faceDown = True
            #removes the current card that was clicked, and the one in the stack that had a matching type
            removeCards(card, oldCard)
            #empty the stack for the next pair
            cardStack = []
            #return indicates a match has been made
            return True
    
    #in the case that you have made two successful matches before, you now get three flips to try and make a match
    #this is implemented by adding the second unsuccessful flip to the stack so it can be compared with the third and final flip
    if discoverCounter >= 2 and len(cardStack) <= 1:
        cardStack.append(card)
        return True

    #if the player fails to make a match on the second or third flip, cards are set face down,
    #the player's turn changes, and the discoverd cards counter resets to 0
    for oldCard in cardStack:
        oldCard.faceDown = True

    card.faceDown = True
    cardStack = []
    player1Turn = not player1Turn
    discoverCounter = 0

    return True

#handles the case of a player making a successful match
#sets both matching cards to removed, decrease the counter for the number of cards in play by 2, 
#increases the respective players score by 1, checks to see if there is no cards left
def removeCards(card1, card2):
    global player1Turn
    card1.removed = True
    card2.removed = True
    globalVs.numberOfUnmatchedCards -= 2

    scoreGiven = 1
    if (card1.type == 'R'): scoreGiven = 2
    if (player1Turn):
        globalVs.players[0].numberOfPairs += scoreGiven
    else:
        globalVs.players[1].numberOfPairs += scoreGiven
    #if no cards are left, the game ends
    if (globalVs.numberOfUnmatchedCards <= 0):
        endGame()
    print(globalVs.numberOfUnmatchedCards)

#determines the winner of the game 
def endGame ():
    #picks the winner, and sets the text for what will be displayed. Ex. "Player 1 wins" or "Tie"
    if globalVs.players[0].numberOfPairs > globalVs.players[1].numberOfPairs:
        globalVs.victoryText = globalVs.players[0].name + ' Wins'
    elif globalVs.players[0].numberOfPairs < globalVs.players[1].numberOfPairs:
        globalVs.victoryText = globalVs.players[1].name + ' Wins'
    else:
        globalVs.victoryText = 'Tie'
    globalVs.gameEnd = True
    
#resets the game
def restartGame():
    print("thing")
    global player1Trurn
    player1Trurn = True
    globalVs.resetToBeging()