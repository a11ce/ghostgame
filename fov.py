import math

CLEARLINE_STEPS = 100   #100
VIEW_DISTANCE = 10 #10

def visible(playerLoc, point, board):
    distance = math.sqrt( (playerLoc[0]-point[0])**2 + (playerLoc[1]-point[1])**2    )
    
    if(distance < VIEW_DISTANCE):
        return clearLine(playerLoc, point, board) or adjacentWall(playerLoc, point, board)
    return False


def discover(playerPos, gameBoard, discovered):

    for x in range(len(gameBoard)):
        for y in range(len(gameBoard[0])):
            if( visible(playerPos, (x,y), gameBoard ) ):
                discovered[x][y] = 1
    return discovered

def adjacentWall(playerLoc, point, board):
    if board[point[0]][point[1]] == 0:
        return False
    return (
           clearLine(playerLoc, (point[0]+1, point[1]  ), board) or 
           clearLine(playerLoc, (point[0]-1, point[1]  ), board) or
           clearLine(playerLoc, (point[0]  , point[1]+1), board) or
           clearLine(playerLoc, (point[0]  , point[1]-1), board) 
           )

def clearLine(p1, p2, board):
    vector = (p2[0] - p1[0], p2[1] - p1[1])
    vector = (vector[0] / CLEARLINE_STEPS ,vector[1] / CLEARLINE_STEPS)

    curPoint = (p1[0], p1[1])
    
    while (abs(curPoint[0] - p2[0]) > 1) or (abs(curPoint[1] - p2[1]) > 1):
        if(board[int(curPoint[0])][int(curPoint[1])]) == 1:
            return False
        curPoint = (curPoint[0] + vector[0], curPoint[1]+ vector[1])
    return True
       