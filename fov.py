import math

# See clearLine()
CLEARLINE_STEPS = 100   #100

# The distance the player is able to see, possibly lantern range
VIEW_DISTANCE = 10 #10

# Returns whether the location 'point' is visible from the location 'playerLoc'
def visible(playerLoc, point, board):

    # Distance between the points
    distance = math.sqrt( (playerLoc[0]-point[0])**2 + (playerLoc[1]-point[1])**2    )
    
    if(distance < VIEW_DISTANCE):
        return clearLine(playerLoc, point, board) or adjacentWall(playerLoc, point, board)
    return False

# Marks newly discovered points on the map based on what is visible to the player
def discover(playerPos, gameBoard, discovered):

    for x in range(len(gameBoard)):
        for y in range(len(gameBoard[0])):
            if( visible(playerPos, (x,y), gameBoard ) ):
                # 1 means the point has been discovered, 0 has not
                discovered[x][y] = 1
    return discovered

# Returns true if 'point' is a wall adjacent to an unobstructed empty space
# This is more intuitive for the player
def adjacentWall(playerLoc, point, board):
    if board[point[0]][point[1]] == 0:
        return False
    return (
           # Check all non-diagonal adjacent spaces
           clearLine(playerLoc, (point[0]+1, point[1]  ), board) or 
           clearLine(playerLoc, (point[0]-1, point[1]  ), board) or
           clearLine(playerLoc, (point[0]  , point[1]+1), board) or
           clearLine(playerLoc, (point[0]  , point[1]-1), board) 
           )

def clearLine(p1, p2, board):
    # The vector from p1 to p2
    vector = (p2[0] - p1[0], p2[1] - p1[1])

    # CLEARLINE_STEPS points are checked between p1 and p2  
    vector = (vector[0] / CLEARLINE_STEPS ,vector[1] / CLEARLINE_STEPS)

    # Start the check at p1
    curPoint = (p1[0], p1[1])

    # Stop when point being checked is less than one away from p2
    while (abs(curPoint[0] - p2[0]) > 1) or (abs(curPoint[1] - p2[1]) > 1):
    
        # Return false if there is a wall between the points
        if(board[int(curPoint[0])][int(curPoint[1])]) == 1:
            return False

        # Add the divided vector, stepping forward on the line
        # This will happen about CLEARLINE_STEPS times
        curPoint = (curPoint[0] + vector[0], curPoint[1]+ vector[1])

    # If there is no obstruction between the points, there is a clear line between them
    return True