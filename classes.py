import pygame
import enum

class Card(object):
    width = 70
    height = 95

    def __init__(self, name):
        self.name = name
        #extracts only the type information from the card name parameter
        self.type = self.name[1:]
        self.faceDown = True
        self.removed = False
        self.position = [0,0]
    
    #returns if a click was withing the bounds of the card
    def checkBounds(self, x, y):
        if (x > self.position[0] and x < self.position[0] + Card.width
            and y > self.position[1] and y < self.position[1] + Card.height):
            self.faceDown = not self.faceDown
            return True
        return False

class Player(object):
    def __init__(self, name, nameSpot, scoreSpot):
        self.name = name
        self.numberOfPairs = 0
        self.nameSpot = nameSpot
        self.scoreSpot = scoreSpot

class globalVs(object):

    textDisplay = ''
    victoryText = None
    gameEnd = False
    cardsInPlay = [[] for x in range(9)]
    players = []
    screenWidth = 1200
    screenHeight = 700
    player1Turn = True

    #resets the game
    @staticmethod
    def resetToBeging():
        print("reseting to beggining")
        globalVs.gameEnd = False
        globalVs.victoryText = None
        globalVs.numberOfUnmatchedCards = len(globalVs.cardsInPlay)
        for cardSet in globalVs.cardsInPlay:
            for card in cardSet:
                card.faceDown = True
                card.removed = False
        for player in globalVs.players:
            player.numberOfPairs = 0