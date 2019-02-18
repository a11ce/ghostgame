#!/usr/bin/env python3
import tdl
from random import randint
import colors
from math import sqrt

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

FOV_ALGO = 'PERMISSIVE2'  #default FOV algorithm
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

firstX = 0
firstY = 0

MAP_WIDTH = SCREEN_WIDTH
MAP_HEIGHT = SCREEN_HEIGHT - 5

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 100
ROOM_MAX_MONSTERS = 3

color_dark_wall = (102,32,32)
color_light_wall = (139,35,35)
color_dark_ground = (56,56,56)
color_light_ground = (94,94,94)

root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Ghost Game Prototype", fullscreen=False)
con = tdl.Console(SCREEN_WIDTH, SCREEN_HEIGHT)

objects = []

def create_room(room):
    global mainMap
    for x in range(room.x1+1, room.x2):
        for y in range(room.y1+1, room.y2):
            try:
                mainMap[x][y].blocked = False
                mainMap[x][y].block_sight = False

            except Exception as e:
                pass

def place_monsters(room):

    
    x = randint(room.x1+1, room.x2-1)
    y = randint(room.y1+1, room.y2-1)
    ghost = GameObject(x,y,'X',(255,255,255),con,mainMap,'X',True)
    objects.append(ghost)

def create_h_tunnel(x1, x2, y):
    global mainMap
    for x in range(min(x1, x2), max(x1, x2) + 1):
            mainMap[x][y].blocked = False
            mainMap[x][y].block_sight = False



def create_v_tunnel(y1, y2, x):
    global mainMap
    #vertical tunnel
    for y in range(min(y1, y2), max(y1, y2) + 1):
        mainMap[x][y].blocked = False
        mainMap[x][y].block_sight = False

def is_visible_tile(x, y):
    global mainMap

    if x >= MAP_WIDTH or x < 0:
        return False
    elif y >= MAP_HEIGHT or y < 0:
        return False
    elif mainMap[x][y].blocked == True:
        return False
    elif mainMap[x][y].block_sight == True:
        return False
    else:
        return True


def make_map():
    global mainMap

    #fill map with "unblocked" tiles
    mainMap = [[ Tile(True)
        for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH) ]

    rooms = []
    numRooms = 0
    flag = False
    for i in range(MAX_ROOMS):
        w = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        x = randint(0, MAP_WIDTH-w-1)
        y = randint(0, MAP_HEIGHT-h-1)

        newRoom = Room(x,y,w,h)

        intersection = False
        for other_room in rooms:
            if newRoom.intersect(other_room):
                intersection = True
                break
        if not intersection:
            create_room(newRoom)

            (new_x, new_y) = newRoom.center()

            if numRooms == 0:
                global firstX
                firstX = new_x
                global firstY
                firstY = new_y

            else:
                (prev_x, prev_y) = rooms[numRooms-1].center()
                if randint(0, 1):
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)
                else:
                    #first move vertically, then horizontally
                    create_h_tunnel(prev_x, new_x, new_y)
                    create_v_tunnel(prev_y, new_y, prev_x)
                    
            if not flag:
                if(randint(0,100)>75):
                    place_monsters(newRoom)
                    flag = False
                if(i == MAX_ROOMS-1):
                    place_monsters(newRoom)
            rooms.append(newRoom)
            numRooms += 1

def render_all():

    global fov_recompute
    global visible_tiles

    if fov_recompute:
        visible_tiles = tdl.map.quickFOV(player.x, player.y,
                                         is_visible_tile,
                                         fov=FOV_ALGO,
                                         radius=TORCH_RADIUS,
                                         lightWalls=FOV_LIGHT_WALLS)

        #go through all tiles, and set their background color according to the FOV
        drawTime()
        
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                visible = (x, y) in visible_tiles
                wall = mainMap[x][y].block_sight
                if not visible:
                    if mainMap[x][y].explored:
                    #it's out of the player's FOV
                        if wall:
                            con.draw_char(x, y, None, fg=None, bg=color_dark_wall)
                        else:
                            con.draw_char(x, y, None, fg=None, bg=color_dark_ground)
                else:
                    #it's visible
                    if wall:
                        con.draw_char(x, y, None, fg=None, bg=color_light_wall)
                    else:
                        con.draw_char(x, y, None, fg=None, bg=color_light_ground)
                    mainMap[x][y].explored = True
    #draw all objects in the list
    for obj in objects:
        obj.draw()

    root.blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)

def drawTime():
    i = 0
    for c in str(time):
        print(time)
        con.draw_char(3+i,SCREEN_HEIGHT-3,c)
        i = i+1
    

def handle_keys():
    global playerx, playery

    user_input = tdl.event.key_wait()

    #movement keys
    if user_input.key == 'UP':
        player.move(0, -1)
        fov_recompute = True

    elif user_input.key == 'DOWN':
        player.move(0, 1)
        fov_recompute = True


    elif user_input.key == 'LEFT':
        player.move(-1, 0)
        fov_recompute = True


    elif user_input.key == 'RIGHT':
        player.move(1, 0)
        fov_recompute = True





class GameObject:

    def __init__(self, x, y, char, color, console, gMap, name, blocks):
        self.name = name
        self.blocks = blocks
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.console = console
        self.gMap = gMap


    def move(self, dx, dy):
        print(str(self.y) + "," + str(self.x))
        if not self.gMap[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy

    def draw(self):
        global visible_tiles
        #draw the character that represents this object at its position
        if (self.x, self.y) in visible_tiles:
            self.console.draw_char(self.x, self.y, self.char, self.color)

    def clear(self):
        #erase the character that represents this object
        self.console.draw_char(self.x, self.y, ' ', self.color, bg=None)

class Tile:
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        self.explored = False
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight

class Room:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return (center_x, center_y)

    def intersect(self, other):
        #returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


def getDistance(obj1, obj2):
    return int( sqrt( ((obj1.x - obj2.x)**2) +  ((obj1.x-obj2.x)**2)) )

def ghostMove(ghost, target):
    xdiff = target.x - ghost.x
    ydiff = target.y - ghost.y

    diffT = abs(xdiff) + abs(ydiff)

    if(randint(0,diffT)>abs(xdiff)):
        if ydiff>0:
            yNorm = 1
        else:
            yNorm = -1
        return (0,yNorm)
    else:
        if xdiff>0:
            xNorm = 1
        else:
            xNorm = -1
        return (xNorm,0)


make_map()
player = GameObject(firstX, firstY, '@', (255,255,255), con, mainMap, 'player', blocks=True)
objects.append(player)


fov_recompute = True
time = 0
dead = False

while not tdl.event.is_window_closed():
    
    render_all()

    tdl.flush()

    for obj in objects:
        obj.clear()
    minDist = 99999

    if not dead:
            exit_now = handle_keys()
            time = time +1
            
    for obj in objects:
        print(obj.char)
        if(obj.char == 'X'):
            tDist = getDistance(obj, player)
            if tDist < minDist:
                minDist = tDist
        
            if(abs(obj.x-player.x)<2 and abs(obj.y-player.y)<2):
                dead = True
                i = 0
                for c in str("You have died of ghost"):
                    
                    con.draw_char(3+i,SCREEN_HEIGHT-5,c)
                    i = i+1
                    player.char = " "
            ghostDir = ghostMove(obj, player)
            obj.move(*ghostDir)

    i = 0
    for c in (str(minDist) + " "):
        con.draw_char(3+i, SCREEN_HEIGHT-6,c)
        i= i+1
    
    
    if exit_now:
        break
