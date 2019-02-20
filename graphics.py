import copy
import sys

import fov

COLOR_CODES = {
    99: "-", #undiscovered
     0: " ", #dark empty space
    10: "\033[100m ", #light empty space
     1: "\033[41m ", #dark wall
    11: "\033[101m ",         #light wall    
    -1: "UH OH ", #player but something has gone wrong
     9: "\033[100m@", #player 
     2: " ", #ghost (extra spooky)
    12: "\033[100mX", #ghost

}
RESET = "\033[m"

def renderAll(playerPos, ghosts, board, discBoard):
    blitBoard = copy.deepcopy(board)

  
    
    blitBoard[playerPos[0]][playerPos[1]] = -1

    for ghost in ghosts:
        blitBoard[ghost[0]][ghost[1]] = 2

    print('\033c')

    printBoard(blitBoard, playerPos, discBoard)

def printBoard(board, playerPos, discBoard):

    bufferString = ''

    for y in range(len(board[0])):
        for x in range(len(board)):

                if discBoard[x][y] == 0:
                    bufferString += COLOR_CODES[99] + RESET
                else:
                    if not fov.visible(playerPos, (x,y), board ):
                        bufferString += COLOR_CODES[board[x][y]] + RESET
                    else:
                        bufferString += COLOR_CODES[board[x][y]+10] + RESET
        bufferString += "\n"
    print(bufferString)
            
    