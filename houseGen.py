from random import randint

NUM_GHOSTS = 6

def generateGameBoard(mapWidth, mapHeight, maxRooms, minSize, maxSize):

    ghosts= []
    
    board = [
            [ 1 for _ in range(mapHeight)]
            for _ in range(mapWidth)]    

    discovered = [
                 [ 0 for _ in range(mapHeight)]
                 for _ in range(mapWidth)]

    
    for i in range(maxRooms):

        cSize  = ( 
                    randint(minSize, maxSize),
                     randint(minSize, maxSize))

        cOrigin = ( 
                    randint(0, mapWidth - cSize[0] -1),
                    randint(0, mapHeight -cSize[1] -1))

        cCenter = (
                    cOrigin[0] + (cSize[0]//2),
                    cOrigin[1] + (cSize[1]//2))

        #print(cCenter)

        if clearToPlace(cOrigin, cSize, board):        
            if i == 0:
                playerFirst= cCenter
            elif (len(ghosts) < NUM_GHOSTS):
                ghosts.append(cCenter)            

        
            else:        
                if(randint(0,1)):
                    board = xTunnel(board,prevCenter[0],cCenter[0], prevCenter[1])
                    board = yTunnel(board,prevCenter[1],cCenter[1], cCenter[0])
                else:
                    board = xTunnel(board,prevCenter[0],cCenter[0], cCenter[1])
                    board = yTunnel(board,prevCenter[1],cCenter[1], prevCenter[0])
            
            for x in range(cSize[0]):
                for y in range(cSize[1]):
                    board[cOrigin[0]+x][cOrigin[1]+y] = 0



            prevCenter = cCenter 

    board = carveHallways(board)
    board = wallOutside(board)        
    return playerFirst, ghosts, board, discovered
    
def xTunnel(board, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        board[x][y] = 4
    return board

def yTunnel(board,y1,y2,x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        board[x][y] = 4
    return board

def clearToPlace(origin, size, board):
    for x in range(size[0]):
        for y in range(size[1]):
            if board[origin[0]+x][origin[1]+y] == 0:
                return False
    return True

def carveHallways(board):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == 4:
                board[x][y] = 0
    return board

def wallOutside(board):
    for x in range(len(board)):
        board[x][0] = 1
        board[x][len(board[0])-1] = 1
    for y in range(len(board[0])):
        board[0][y] = 1
        board[len(board)-1][y] = 1
    return board