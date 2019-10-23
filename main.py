from classes import *
from backend import *
import backend
from random import shuffle
import time
import pygame
import os
import enum

def main():
    
    setupGame()
    globalVs.win.fill((0,0,0))
    #creates and renders the static elements of the screen
    #these are the player names
    setUpScreen()
    run = True

    #main game loop that runs until exit button is pressed
    while run:
        for event in pygame.event.get():
            #event that handles closing the game
            if event.type == pygame.QUIT:
                run = False
            #event that registers button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if game has ended, the button click will restart the game
                if globalVs.gameEnd == True:
                    print("game end click")
                    restartGame()
                    renderScreen()
                else:
                    #if the game is in play, clicks are handled by this function
                    #parameter is the position of the mouse when it was clicked
                    onClick(event.pos)
            #this is a custom event that I trigger when I want to render the screen after a given time delay
            if event.type == 31:
                renderScreen()
                pygame.time.set_timer(31,0)

    pygame.quit()


#called when a click is made and the game is in play
#calculated index of card in matrix based on position of the mouse
def onClick(pos):
    print (pos)
    levelX = max(0, min((pos[0] - 130) // 100, 8))
    levelY = max(0, min((pos[1] - 20) // 107, 5))
    print(levelY)
    card = globalVs.cardsInPlay[levelX][levelY]
    if not card.removed and card.checkBounds(pos[0], pos[1]) == True:
        renderScreen()
        #checks if the pair of clicked cards were incorrect and turned back face down
        if (flipCard(card) == True):
            #triggers the custom event that waits 1 second and renders the screen
            #this is what gives the players time to see the incorrect pair before it is flipped back over
            pygame.time.set_timer(31, 1000)

#positions and renders the player names
def setUpScreen():
    widthPadding = 300
    heightPadding = 50
    playerName1 = globalVs.myfont.render(globalVs.players[0].name, False, (255,255,255))
    playerName2 = globalVs.myfont.render(globalVs.players[1].name, False, (255,255,255))
    globalVs.win.blit(playerName1, globalVs.players[0].nameSpot)
    globalVs.win.blit(playerName2, globalVs.players[1].nameSpot)
    pygame.display.update()

    #determins the position of each card, and saves this position in the card object
    for x in range(9):
        for y in range(6):
            temp = globalVs.cardsInPlay[x][y]
            temp.position = [((globalVs.screenWidth - widthPadding)//9) * x + (widthPadding/2), 
                ((globalVs.screenHeight-heightPadding)//6) * y + (heightPadding/2)]
    #calls render screen to render the cards in their new position
    renderScreen()

def renderScreen():
    #sets parts of the screen black so the card and score renders don't overlap with the previous frame
    globalVs.win.fill((0,0,0), pygame.Rect(100,0,1000,globalVs.screenHeight))
    bottomFillY = globalVs.players[0].scoreSpot[1]
    globalVs.win.fill((0,0,0), pygame.Rect(0, bottomFillY, globalVs.screenWidth, globalVs.screenHeight))
    #highlights the player who's turn it is with a green score
    if backend.player1Turn:
        playerScore1 = globalVs.myfont.render(str(globalVs.players[0].numberOfPairs), False, (0,255,0))
        playerScore2 = globalVs.myfont.render(str(globalVs.players[1].numberOfPairs), False, (255,255,255))
    else:
        playerScore1 = globalVs.myfont.render(str(globalVs.players[0].numberOfPairs), False, (255,255,255))
        playerScore2 = globalVs.myfont.render(str(globalVs.players[1].numberOfPairs), False, (0,255,0))
    globalVs.win.blit(playerScore1, globalVs.players[0].scoreSpot)
    globalVs.win.blit(playerScore2, globalVs.players[1].scoreSpot)

    #checks if game is over and displays the winner of the game
    if globalVs.gameEnd:
        victoryFont = pygame.font.SysFont('Comic Sans MS', 90)
        endGameTitle = victoryFont.render(globalVs.victoryText, False, (255,255,255))
        globalVs.win.blit(endGameTitle, [globalVs.screenWidth/2 - victoryFont.size(globalVs.victoryText)[0]/2, 
            globalVs.screenHeight/2])

    #loops through all the cards and renders them as face up or down. 
    #Or, if they have been removed, they don't get rendered at all
    for x in range(len(globalVs.cardsInPlay)):
        for y in range(len(globalVs.cardsInPlay[x])):
            temp = globalVs.cardsInPlay[x][y]
            if temp.removed == False:
                if temp.faceDown:
                    globalVs.win.blit(globalVs.cardBack, (temp.position[0], temp.position[1]))
                else:
                    globalVs.win.blit(temp.image, (temp.position[0], temp.position[1]))
    pygame.display.update()


def setupGame():
    #Sets up pygame environment and window
    pygame.init()
    pygame.font.init()
    globalVs.win = pygame.display.set_mode((globalVs.screenWidth, globalVs.screenHeight))

    #imports card images, and stores them in a dictionary with the key being the card name
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    clubsOG = {'C8': pygame.image.load('cards/cardClubs8.png'), 'D8': pygame.image.load('cards/cardDiamonds8.png'), 
                    'S8': pygame.image.load('cards/cardSpades8.png'), 'H8': pygame.image.load('cards/cardHearts8.png'),
                    'RR': pygame.image.load('cards/cardRedJoker.png'), 'BR': pygame.image.load('cards/cardBlackJoker.png'), 
                    'C2': pygame.image.load('cards/cardClubs2.png'), 'C3': pygame.image.load('cards/cardClubs3.png'), 
                    'C4': pygame.image.load('cards/cardClubs4.png'), 'C5': pygame.image.load('cards/cardClubs5.png'),
                    'C6': pygame.image.load('cards/cardClubs6.png'), 'C7': pygame.image.load('cards/cardClubs7.png'), 
                    'C9': pygame.image.load('cards/cardClubs9.png'), 'C10': pygame.image.load('cards/cardClubs10.png'), 
                    'CJ': pygame.image.load('cards/cardClubsJ.png'), 'CQ': pygame.image.load('cards/cardClubsQ.png'), 
                    'CK': pygame.image.load('cards/cardClubsK.png'),'CA': pygame.image.load('cards/cardClubsA.png'), 
                    'D2': pygame.image.load('cards/cardDiamonds2.png'), 'D3': pygame.image.load('cards/cardDiamonds3.png'), 
                    'D4': pygame.image.load('cards/cardDiamonds4.png'), 'D5': pygame.image.load('cards/cardDiamonds5.png'), 
                    'D6': pygame.image.load('cards/cardDiamonds6.png'), 'D7': pygame.image.load('cards/cardDiamonds7.png'),
                    'D9': pygame.image.load('cards/cardDiamonds9.png'), 'D10': pygame.image.load('cards/cardDiamonds10.png'), 
                    'DJ': pygame.image.load('cards/cardDiamondsJ.png'), 'DQ': pygame.image.load('cards/cardDiamondsQ.png'), 
                    'DK': pygame.image.load('cards/cardDiamondsK.png'), 'DA': pygame.image.load('cards/cardDiamondsA.png'), 
                    'H2': pygame.image.load('cards/cardHearts2.png'), 'H3': pygame.image.load('cards/cardHearts3.png'), 
                    'H4': pygame.image.load('cards/cardHearts4.png'), 'H5': pygame.image.load('cards/cardHearts5.png'), 
                    'H6': pygame.image.load('cards/cardHearts6.png'), 'H7': pygame.image.load('cards/cardHearts7.png'), 
                    'H9': pygame.image.load('cards/cardHearts9.png'), 'H10': pygame.image.load('cards/cardHearts10.png'), 
                    'HJ': pygame.image.load('cards/cardHeartsJ.png'), 'HQ': pygame.image.load('cards/cardHeartsQ.png'), 
                    'HK': pygame.image.load('cards/cardHeartsK.png'), 'HA': pygame.image.load('cards/cardHeartsA.png'), 
                    'S2': pygame.image.load('cards/cardSpades2.png'), 'S3': pygame.image.load('cards/cardSpades3.png'), 
                    'S4': pygame.image.load('cards/cardSpades4.png'), 'S5': pygame.image.load('cards/cardSpades5.png'), 
                    'S6': pygame.image.load('cards/cardSpades6.png'), 'S7': pygame.image.load('cards/cardSpades7.png'),
                    'S9': pygame.image.load('cards/cardSpades9.png'), 'S10': pygame.image.load('cards/cardSpades10.png'),
                    'SJ': pygame.image.load('cards/cardSpadesJ.png'), 'SQ': pygame.image.load('cards/cardSpadesQ.png'),
                    'SK': pygame.image.load('cards/cardSpadesK.png'), 'SA': pygame.image.load('cards/cardSpadesA.png'),                 
    }

    #creates card objects from card images and names.
    #stores these objects in a list (which gets randomized) in a global object called globalVs
    counter = 0
    list_key_value = [ [k,v] for k, v in clubsOG.items() ]
    shuffle(list_key_value)
    
    for cardSet in list_key_value:
        temp = Card(cardSet[0])
        #globalVs.cardsInPlay.append(temp)
        globalVs.cardsInPlay[counter // 6].append(temp)
        #stores the pygame image into the card object
        temp.image = pygame.transform.scale(cardSet[1], (Card.width, Card.height))
        counter += 1


        #if counter > 54: break
    print (counter)
    
    #creates pygame fonts, imports and saves the card back image, creates two player objects
    #sets the number of unmatched cards to the full 54 card amount
    globalVs.myfont = pygame.font.SysFont('Comic Sans MS', 30)
    cardBack = pygame.image.load('cards/cardBack.png')
    globalVs.cardBack = pygame.transform.scale(cardBack, (70, 95))
    globalVs.players.append(Player('Player 1', [10,100], [10, 100 + globalVs.myfont.size('Player 1')[1]]))
    pos = globalVs.myfont.size('Player 2')
    globalVs.players.append(Player('Player 2', [globalVs.screenWidth - pos[0] - 10, 100], [globalVs.screenWidth - pos[0] - 10, 100 + pos[1]]))
    globalVs.numberOfUnmatchedCards = len(globalVs.cardsInPlay) * 6
    print(globalVs.numberOfUnmatchedCards)


if __name__ == "__main__":
    main()