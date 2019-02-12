#!/usr/bin/env python

#This code is a simulation and code base for the PennState robotics club
#entry into the Harvard PacMan robotics competition. 

#Code based on original code @gcb5083/robotpacman by: Geoffrey Billy and Saimun Shahee

import random
import enum

class Position(object):
    """
    a class to represent a specific x,y location
    """
    def __init__(self, x, y):
        super(Position, self).__init__()
        
        self.x = x
        self.y = y

    def getX(self):
        return self.x
    def getY(self):
        return self.y

    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y

    def __eq__(self, pos):
        if( not isinstance(pos, Position)):
            return False

        x_test = self.x is pos.getX()
        y_test = self.y is pos.getY()

        return x_test and y_test

    

class ARENA_BIT_MASK(enum.Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3
    DOT = 4

class ConnectivityMask(object):
    """
    A class representing for each tile the connections that each tile make to one another.
    From this tile can another tile be directly reached. Also if a dot is still present here

    """
    def __init__(self):
        super(ConnectivityMask, self).__init__()
        self.right = True
        self.left = True
        self.up = True
        self.down = True
        self.containFood = True

    def removeFood(self):
        """
        mutator function to remove the food from the tile when pacbot eats it
        """
        self.containFood = False

    def canGoRight(self):
        return self.right

    def canGoLeft(self):
        return self.left

    def canGoDown(self):
        return self.down

    def canGoUp(self):
        return self.up
    
    def isFoodPresent(self):
        return self.containFood

    def setLeft(self, left):
        self.left = left

    def setRight(self, right):
        self.right = right

    def setUp(self, up):
        self.up = up

    def setDown(self, down):
        self.down = down

    def getWallCount(self):
        possibleWalls = [self.up, self.down, self.right, self.left]
        findWalls = lambda opening: opening is False

        wall_list = map(findWalls, possibleWalls)

        countWalls = lambda totalWalls, nextWall: totalWalls + int(nextWall)
        
        return reduce(countWalls, wall_list)

    def __eq__(self, mask):
        if(not isinstance(mask, ConnectivityMask)):
            return False

        right_test = self.right is mask.canGoRight()
        left_test = self.left is mask.canGoLeft()
        up_test = self.up is mask.canGoUp()
        down_test = self.down is mask.canGoDown()
        food_test = self.containFood is mask.isFoodPresent()

        return right_test and left_test and up_test and down_test and food_test



class Arena(object):
    """
    A 2 - dim array of conenctivity masks representing a connecitivity mask at each coordinate of the maze

    (x,y) are represented from origin (0,0) at bottom-left
    (col, row) are represented from origin (0,0) at top-left
    """

    def __init__(self, row, col):
    
        """
        sets up the the arena (2-dim list <ConnectivityMask>)

        Parameters
        ----------
        row : integer
            how many rows are in the arena
        column : integer
            how many columns are in the arena

        """

        # a location has 5 associated values: up, down, left, right linked and exsistence of a dot
        rowMap = lambda : [ConnectivityMask() for i in range(row)]
        fullMap = lambda : [rowMap() for i in range(col)]

        super(Arena, self).__init__()
        self.rows = row
        self.cols = col
        self.maze = fullMap()

    def buildWallBetween(self, pos1, pos2):
        """

        a mutator function to prevent 2 directly adjacent connectivity mask positions from being able to connect
        to one another. (i.e. a wall that sperates the 2)

        Preconditions:
        --------------
        under the presumption that the 2 positions are directly adjacent

        either vertically directly ontop each other OR horizontally right next to eachother
               BUT not diagonally away from each other

        Parameters:
        -----------
        pos1 : Position
            position of the first ConnectivityMask to block
        pos2 : Position
            position of the second ConnectivityMask to block

        """
        row1 = self.rows - pos1.getY() - 1
        col1 = pos1.getX()

        row2 = self.rows - pos2.getY() - 1
        col2 = pos2.getX()

        if(row1 == row2):
            sharedRow = row1
            col_lst = [col1, col2]
            col_lst.sort()
            smallerCol, largerCol = col_lst

            self.maze[smallerCol][sharedRow].setRight(False)
            self.maze[largerCol][sharedRow].setLeft(False)

        else: # col1 == col2
            sharedCol = col1
            row_lst = [row1, row2]
            row_lst.sort()
            smallerRow, largerRow = row_lst

            self.maze[sharedCol][smallerRow].setDown(False)
            self.maze[sharedCol][largerRow].setUp(False)

    def initalizeBoundryWall(self):
        """
        assigns the adjacent neighbors for the binary mask in the edge coordinates of the arena map

        Parmaeters:
        -----------
        arena : List <Dim 3>
            the arena connected binary mask to assign side of edge without neighbors

        Returns:
        arena : List <Dim 3>
            the arena after all coordinates who cannot have neighbors have been assigned
        """

        for col in range(self.cols):
            topRow = 0
            bottomRow = self.rows-1

            self.maze[col][topRow].setUp(False)
            self.maze[col][bottomRow].setDown(False)

        for row in range(self.rows):
            leftCol = 0
            rightCol = self.cols-1

            self.maze[leftCol][row].setLeft(False)
            self.maze[rightCol][row].setRight(False)

    def getRows(self):
        return self.rows

    def getCols(self):
        return self.cols

    def __eq__(self, arena):
        if(not isinstance(arena, Arena)):
            return False

        row_test = arena.getRows() is self.rows
        col_test = arena.getCols() is self.cols
        maze_test = (arena.maze == self.maze)

        return maze_test and row_test and col_test


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


def setWallsRandom(arena, wallfrequency):

    """
    mutator

    randomly assigns certain tiles where verticle or horizontal movement is blocked (i.e. generate walls above/below or left/right) of the tileand on the other side of the wall to assign a wall on an adjacent tile's respectively opposite side

    Parameters
    ----------
    arena : List <dim 3>
        the bit mask telling the connection information at each coordinate which can be move into
    wallfrequency : float
        an index to indicate the unliklihood for a wall to appear
    """

    shouldBuildWall = lambda : random.random() >= wallfrequency

    for col in range(arena.getCols()):
        rows_with_row_below = arena.getRows() -1
        for row in range(rows_with_row_below):
            #horizontal walls between 2 tiles based on frequency
            if shouldBuildWall():
                xLoc = col
                yLoc = arena.getRows() - row - 1

                currTile = Position(xLoc, yLoc)
                belowTile = Position(xLoc, yLoc - 1)

                arena.buildWallBetween(currTile, belowTile)

    cols_with_right_col = arena.getCols() - 1

    for col in range(cols_with_right_col):
        for row in range(arena.getRows()):
            #vertical wall between 2 tiles based on the frequency
            if shouldBuildWall():
                xLoc = col
                yLoc = arena.getRows() - row - 1
                
                currTile = Position(xLoc, yLoc)
                rightTile = Position(xLoc + 1, yLoc)

                arena.buildWallBetween(currTile, rightTile)

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

    for col in range(arena.getCols()):
        for row in range(arena.getRows()):

            x = col
            y = row

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

                if ((not (x == 0 and removeside == 0)) and  # only remove if that side is not the boundry wall
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

#runSimulation()
