#!/usr/bin/env python3

import random
import math

import houseGen
import graphics
import fov
from getch import getch

SCREEN_WIDTH = 80   #80
SCREEN_HEIGHT = 40 #40
HUD_HEIGHT = 1 # currently just time

ROOM_MIN_SIZE = 6
ROOM_MAX_SIZE = 10
MAX_ROOMS = 100

DEBUG = False

def main():
    playAgain = True
    while playAgain:
        playAgain = playGame()
    
def playGame():

    time = 0
    
    playerPos, ghosts, gameBoard, discBoard = houseGen.generateGameBoard(
                                                                 SCREEN_WIDTH,
                                                                 SCREEN_HEIGHT - HUD_HEIGHT,
                                                                 MAX_ROOMS,
                                                                 ROOM_MIN_SIZE,
                                                                 ROOM_MAX_SIZE)

    dead = False
    done = False
    while not (dead or done):
        #print('\033c')
        
        discBoard = fov.discover(playerPos, gameBoard, discBoard)
        graphics.renderAll(playerPos, ghosts, gameBoard, discBoard)
        print("Turns: " + str(time))
     

        time = time+1


        dead = checkDead(playerPos, ghosts) and not DEBUG
        done = checkDone(discBoard, gameBoard)
        
        if dead:
            print("you have died of ghost! you survived for " + str(time) + " turns. there were " + str(len(ghosts)) + " ghosts")
            return askToPlayAgain(getch)
        elif done:
            graphics.renderAll(playerPos, ghosts, gameBoard, discBoard)
            
            print("you win! you did it in  " + str(time) + " turns. there were " + str(len(ghosts)) + " ghosts")
            print("your score is " + str(score(time, len(ghosts))))
            
            return askToPlayAgain(getch)
        else:
            ghostMove(playerPos, ghosts, gameBoard)
            playerPos = playerMove(playerPos, gameBoard)

def askToPlayAgain(getch):
    while(True):
        print("play again? y/n")
        inp = getch()
        
        if inp == 'y':
            return True
        elif inp == 'n':
            print("bye!")
            return False

def checkDead(playerPos, ghosts):

    
    
    for ghost in ghosts:
        #print(ghost)
        if(playerPos[0] == ghost[0] and playerPos[1] == ghost[1]):
            return True
    return False

def checkDone(discBoard, gameBoard):
    for x in range(len(gameBoard)):
        for y in range(len(gameBoard[0])):
            if(gameBoard[x][y] == 0 and discBoard[x][y] == 0):
                return False
    return True

def score(t, ghostNum):
    screenSize = (SCREEN_HEIGHT-HUD_HEIGHT)
    return int(1000 * (screenSize / t) * ((ghostNum + 2)/3))

def ghostMove(playerPos, ghosts, board):
    for i in range(len(ghosts)):
        ghost = ghosts[i]
        distance = (playerPos[0] - ghost[0] , playerPos[1] - ghost[1])
        taxiDistance = abs(distance[0]) + abs(distance[1]) 

        if(random.randint(0,taxiDistance) > abs(distance[0])):
            newPos = (ghost[0], ghost[1] + (1 if distance[1]>0 else -1)  )
        else:
            newPos = (ghost[0] + (1 if distance[0] > 0 else -1), ghost[1])    
        if wallCheck(newPos, board, 0,0) and (not hasGhost(newPos, ghosts)):
            ghosts[i] = newPos
            
def hasGhost(point, ghosts):
    for ghost in ghosts:
        if point == ghost:
            return True
    return False

def playerMove(pos, board):

    while True:

        inp = getch()
        
        if inp.lower() == 'q':
            exit(0)

        if inp.lower() == 'l':
            print("hi laurie!")

        if inp.lower() == 'v':
            global DEBUG 
            DEBUG = not DEBUG

        if inp.lower() == 'w':
            if wallCheck(pos, board, 0, -1) or DEBUG:
                pos = (pos[0],pos[1]-1)
            return pos
            
        if inp.lower() == 's':
            if wallCheck(pos, board, 0,  1) or DEBUG:
                pos = (pos[0],pos[1]+1)
            return pos
            
        if inp.lower() == 'a':
            if wallCheck(pos, board, -1, 0) or DEBUG:
                pos = (pos[0]-1,pos[1])
            return pos
            
        if inp.lower() == 'd':
            if wallCheck(pos, board, +1, 0) or DEBUG:
                pos = (pos[0]+1,pos[1])
            return pos


def wallCheck(pos, board, x, y):
    if(board[pos[0]+x][pos[1]+y] == 0):
        return True
    return False


if __name__ == "__main__":
    main()