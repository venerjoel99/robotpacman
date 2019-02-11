#!/usr/bin/env python

#This code is a simulation and code base for the PennState robotics club
#entry into the Harvard PacMan robotics competition. Code written by:
#Geoffrey Billy
#Saimun Shahee

import random
import enum

class ARENA_BIT_MASK(enum.Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3
    DOT = 4

def setupArena(row, column):
    """
    sets up the the arena, as a 5 bit mask at each x,y coordinate representing the presence of adjacent coordinate positions and the bit for the existance of a dot(pac bot dot to eat)

    Parameters
    ----------
    row : integer
        how many rows are in the arena
    column : integer
        how many columns are in the arena

    Returns
    -------
    arena : List 3 dim
        an arena of the binary list at each coordinate location <x,y>
    """

    # a location has 5 associated values: up, down, left, right linked and exsistence of a dot
    connectivityMap = lambda : [True for i in range(5)]
    rowMap = lambda : [connectivityMap() for i in range(row)]
    fullMap = lambda : [rowMap() for i in range(column)]

    return fullMap()

def setupPositionsRandom(charactercount, positions, row, column):

    """
    given a set of positions add a given number of new position that is not already in the list, and add it into the list. New unique position are selected randomly.

    Parameters:
    -----------
    charactercount : int
        number of positions to append to the positions list
    positions: list<positions>
        a list of the existing positions to append new position into
    row : int
        the limit for the row count which positions can be choosen randomly from
    column : int
        the limit for the column count which position can be choosen randomly from

    Returns:
    --------
    positions : list<position>
        a list of positions with added positions appended to the end of it
    """
    randomCol = lambda : random.randint(0, column-1)
    randomRow = lambda : random.randint(0, row-1)

    randomlyMakePosition = lambda : [randomRow(), randomCol()]

    notUnique = lambda position: position in positions

    for x in range(charactercount):
        nextPosition = [randomlyMakePosition()]

        while notUnique(nextPosition[0]): 
            nextPosition = [randomlyMakePosition()]

        #adds it to the rest of the positions
        positions = positions + nextPosition

    return positions

def setupPositionsRandomNonAdjacent(charactercount, positions, row, column):

    """
    
    given a set of positions add a given number of new position that is unique not already in the list and not adjacent (not including diagonal) to an existing item in the list, and add it into the list. New unique position are selected randomly.

    Parameters:
    -----------
    charactercount : int
        number of positions to append to the positions list
    positions: list<positions>
        a list of the existing positions to append new position into
    row : int
        the limit for the row count which positions can be choosen randomly from
    column : int
        the limit for the column count which position can be choosen randomly from

    Returns:
    --------
    positions : list<position>
        a list of positions with added positions appended to the end of it
    """

    randomCol = lambda : random.randint(0, column-1)
    randomRow = lambda : random.randint(0, row-1)

    randomlyMakePosition = lambda : [randomRow(), randomCol()]

    notUnique = lambda position: position in positions

    def getAdjacent(x,y):
        return [x-1,y], [x+1,y], [x,y-1], [x,y+1]

    for g in range(charactercount):

        #generates a unique nonadjacent position in the row column matrix
        position = [randomlyMakePosition()]
        
        inPosition = lambda pos : pos in positions

        xPos = position[0][0]
        yPos = position[0][1]

        while ( notUnique(position[0]) or True in map(inPosition, getAdjacent(xPos, yPos)) ):
              position = [randomlyMakePosition()]

        #adds it to the rest of the positions
        positions = positions + position

    return positions

def setBorderWalls(arena):

    """
    assigns the adjacnet neighbors for the binary mask in the edge coordinates of the arena map

    Parmaeters:
    -----------
    arena : List <Dim 3>
        the arena connected binary mask to assign side of edge without neighbors

    Returns:
    arena : List <Dim 3>
        the arena after all coordinates who cannot have neighbors have been assigned
    """

    def setFalse(maskID):
        col = maskID[0]
        row = maskID[1]
        maskIndex = maskID[2]
        arena[col][row][maskIndex] = False

    def getMaskID(col, row, maskIndex):
        return [col, row, maskIndex]

    lastRow = len(arena[0])-1
    lastCol = len(arena)-1

    #adds all border walls for game bounding
    for i in range(len(arena)):

        leftBorder = getMaskID(col=0, row=i, maskIndex=ARENA_BIT_MASK.LEFT.value)
        topBorder = getMaskID(col=i, row=0,  maskIndex=ARENA_BIT_MASK.UP.value)
        rightBorder = getMaskID(col=lastCol ,row=i, maskIndex=ARENA_BIT_MASK.RIGHT.value)
        bottomBorder = getMaskID(col=i, row=lastRow, maskIndex=ARENA_BIT_MASK.DOWN.value)

        setFalse(leftBorder)
        setFalse(topBorder)
        setFalse(bottomBorder)
        setFalse(rightBorder)
        
    return arena

def setWallsRandom(arena, wallfrequency):

    """
    randomly assigns certain tiles where verticle or horizontal movement is blocked (i.e. generate walls above/below or left/right) of the tileand on the other side of the wall to assign a wall on an adjacent tile's respectively opposite side

    Parameters
    ----------
    arena : List <dim 3>
        the bit mask telling the connection information at each coordinate which can be move into
    wallfrequency : float
        an index to indicate the unliklihood for a wall to appear
    """

    shouldBuildWall = lambda : random.random() >= wallfrequency

    for col in range(len(arena)):
        for row in range(len(arena[0]) - 1):
            #horizontal walls between 2 tiles based on frequency
            if shouldBuildWall():
                currTile = arena[col][row]
                topTile = arena[col][row+1]

                topTile[ARENA_BIT_MASK.DOWN.value] = False
                currTile[ARENA_BIT_MASK.UP.value] = False

    for col in range(len(arena) - 1):
        for row in range(len(arena[0])):
            #vertical wall between 2 tiles based on the frequency
            if shouldBuildWall():
                currTile = arena[col][row]
                rightTile = arena[col+1][row]

                currTile[ARENA_BIT_MASK.RIGHT.value] = False
                rightTile[ARENA_BIT_MASK.LEFT.value] = False

    return arena

def removeIsolatingWalls(arena, maxwallcount):
    
    """
    keeps removing walls until walls which causes certain regions to be completly boxed in from the rest of the maze are removed

    Parameters:
    -----------
    arena : List <dim 3>
        the bit mask list mapped to each coordinate location to determine connectivity between coordinate locations
    maxwallcount: int
        maximum number of walls surronding a given tile before it can be classified as an isolated tile

    Precondition:(not certain)
    -------------
    arena bit list, dot attribute is default True???. Otherwise we may need to change wall count to dis-include it
    """

    for col in range(len(arena)):
        for row in range(len(arena[col])):

            #counts the walls
            wallcount = 0
            for bit_index in range(len(arena[col][row])):
                if(arena[col][row][bit_index]):
                    wallPresent = 0
                else:
                    wallPresent = 1

                wallcount += wallPresent

            #randomly removes walls until there are few enough for a dot not to be isolated
            while wallcount > maxwallcount:
                removeside = random.randint(0,3)

                if ((not (x == 0 and removeside == 0)) and
                    (not (x == (len(arena) - 1) and removeside == 1)) and
                    (not (y == 0 and removeside == 2)) and
                    (not (y == (len(arena[x]) - 1) and removeside == 3))):

                    #remove the first instance of the wall reference
                    arena[x][y][removeside] = True

                    if removeside == 0:
                        #remove bottom wall second reference
                        arena[x - 1][y][1] = True

                    elif removeside == 1:
                        #remove top wall second reference
                        arena[x + 1][y][0] = True

                    elif removeside == 2:
                        #remove right wall second reference
                        arena[x][y - 1][3] = True

                    elif removeside == 3:
                        #remove left wall of isolated point
                        arena[x][y + 1][2] = True

                    #recount walls for the while loop check
                    wallcount = 0
                    for z in range(len(arena[x][y])):
                        wallcount = wallcount + 1 - int(arena[x][y][z])

    return arena

def eatDot(arena, positions, playercount):

        for player in range(playercount):
            #dot is now false on the player location for all possible players
            arena[positions[player][0]][positions[player][1]][4] = False

def moveCharacter(positions, directionlist, character, arena):  #NEEDS DEBUGGING / CHECKED FOR ACCURACY, ALSO NEEDS CHARACTER OVERLAP DETECTION AND WALL IMPLEMENTATIONS

    for direction in directionlist:

        #moves down unless it will go out of bounds
        if direction == 0 and positions[character][1] > 0:
            positions[character][1] = positions[character][1] - 1
            return positions

        #moves up unless it will go out of bounds
        elif direction == 1 and positions[character][1] - 1 < len(arena[0]):
            positions[character][1] = positions[character][1] + 1
            return positions

        #moves right unless it will go out of bounds
        elif direction == 2 and positions[character][0] - 1 < len(arena):
            positions[character][1] = positions[character][1] + 1
            return positions

        #moves left unless it will go out of bounds
        elif direction == 3 and positions[character][0] > 0:
            positions[character][1] = positions[character][1] - 1
            return positions

def gameOverCheck(positions, charactercount):   #NEEDS DEBUGGING / CHECKED FOR ACCURACY

    for g in range(charactercount - 1):
        if (position[0] in positions or
        [position[len(positions) - 1][0] - 1, position[len(positions) - 1][1]] in positions or
        [position[len(positions) - 1][0] + 1, position[len(positions) - 1][1]] in positions or
        [position[len(positions) - 1][0], position[len(positions) - 1][1] - 1] in positions or
        [position[len(positions) - 1][0], position[len(positions) - 1][1] + 1] in positions):
            return True

    return False

def printBoard(arena, positions, ghostcount):

    printrow = ''
    wallcharacter = unichr(0x2588)
    playercharacter = 'P'

    #adds border wall on the top
    for y in range(len(arena[0]) * 2 + 1):
        printrow = printrow + wallcharacter
    print printrow
    printrow = ''

    #iterates row-wise
    for x in range(len(arena)):

        #parses rows for dots or spaces with vertical walls intersparced when needed
        for y in range(len(arena[0])):
            if arena[x][y][2]:
                printrow = printrow + ' '
            else:
                printrow = printrow + wallcharacter

            if arena[x][y][4]:
                printrow = printrow + '.'
            else:
                printrow = printrow + ' '

        #adds border wall on right side
        printrow = printrow + wallcharacter

        #replaces the the dot or space for the character when needed
        for player in range(len(positions)):
            if positions[player][0] == x and player < ghostcount:
                printrow = printrow[:positions[player][1] * 2 + 1] + str(player) + printrow[positions[player][1] * 2 + 2:]
            elif positions[player][0] == x:
                printrow = printrow[:positions[player][1] * 2 + 1] + playercharacter + printrow[positions[player][1] * 2 + 2:]


        #outputs the row of dots + vertical walls to the console and then clears it
        print printrow
        printrow = wallcharacter

        #parses rows for horizontal walls when needed
        for y in range(len(arena[0])):
            if arena[x][y][1]:
                printrow = printrow + ' ' + wallcharacter
            else:
                printrow = printrow + wallcharacter + wallcharacter

        #outputs the row of horiontal walls to the console and then clears it
        print printrow
        printrow = ''

    #separates this board from future boards
    print '\n'

def ghostLastVectorApproach(positions, character):

    directionlist = []

    #closer in the y direction
    if (abs(positions[character][0] - positions[len(positions) - 1][0]) >=
        abs(positions[character][1] - positions[len(positions) - 1][1])):

        if positions[character][0] >= positions[len(positions) - 1][0]:
            directionlist.append(0)
        else:
            directionlist.append(1)

        if positions[character][1] >= positions[len(positions) - 1][1]:
            directionlist.append(2)
            directionlist.append(3)
        else:
            directionlist.append(3)
            directionlist.append(2)

    #closer in the x direction
    else:
        if positions[character][1] >= positions[len(positions) - 1][1]:
            directionlist.append(2)
        else:
            directionlist.append(3)

        if positions[character][0] >= positions[len(positions) - 1][0]:
            directionlist.append(0)
            directionlist.append(1)
        else:
            directionlist.append(1)
            directionlist.append(0)

    return directionlist

def runSimulation():

    gameover = False

    #default game values
    runcount = 100
    row =  23
    column = row
    ghostcount = 4
    playercount = 1
    positions = []
    wallfrequency = 0.5
    maxwallcount = 2

    for x in range(runcount):

        #sets up arena
        arena = setupArena(row, column)

        #sets ghosts positions
        positions = setupPositionsRandom(ghostcount, [], row, column)

        #sets player positions
        positions = setupPositionsRandomNonAdjacent(playercount, positions, row, column)

        #sets standard borderwalls around the arena
        arena = setBorderWalls(arena)

        #sets random walls in the arena
        arena = setWallsRandom(arena, wallfrequency)

        #removes walls that isolate dots or obstruct a two way pathway
        arena = removeIsolatingWalls(arena, maxwallcount)

        #removes dot based on where the player(s) position
        eatDot(arena, positions, playercount)

        #prints the board
        printBoard(arena, positions, ghostcount)

        while not gameOverCheck(positions, playercount):

                #removes dot based on where the player(s) position
                eatDot(arena, positions, playercount)

                #prints the board
                printBoard(arena, positions, ghostcount)

                for character in range(ghostcount):

                    directionlist = ghostLastVectorApproach(positions, character)

                    #moves the characters using the direction list map
                    moveCharacter(positions, directionlist, character, arena)

        print "\n\n\nGAME OVER"

runSimulation()
