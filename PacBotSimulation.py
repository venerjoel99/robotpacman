#!/usr/bin/env python

#This code is a simulation and code base for the PennState robotics club
#entry into the Harvard PacMan robotics competition. Code written by:
#Geoffrey Billy
#Saimun Shahee

import random

def setupArena(row, column):

    # a location has 5 associated values: up, down, left, right linked and exsistence of a dot
    arena = [[[True for z in range(5)] for x in range(row)] for y in range(column)]

    return arena

def setupPositionsRandom(charactercount, positions, row, column):

    for g in range(charactercount):

        #generates a unique position in the row column matrix
        position = [[random.randint(0, row-1), random.randint(0, column-1)]]
        while position[0] in positions:
            position = [[random.randint(0, row-1), random.randint(0, column-1)]]

        #adds it to the rest of the positions
        positions = positions + position

    return positions

def setupPositionsRandomNonAdjacent(charactercount, positions, row, column):

    for g in range(charactercount):

        #generates a unique nonadjacent position in the row column matrix
        position = [[random.randint(0, row-1), random.randint(0, column-1)]]
        while (position[0] in positions or
        [position[0][0] - 1, position[0][1]] in positions or
        [position[0][0] + 1, position[0][1]] in positions or
        [position[0][0], position[0][1] - 1] in positions or
        [position[0][0], position[0][1] + 1] in positions):
              position = [[random.randint(0, row-1), random.randint(0, column-1)]]

        #adds it to the rest of the positions
        positions = positions + position

    return positions

def setBorderWalls(arena):

    #adds all border walls for game bounding
    for border in range(len(arena)):
        arena[0][border][0] = False
        arena[border][0][2] = False
        arena[len(arena) - 1][border][1] = False
        arena[border][len(arena) - 1][3] = False

    return arena

def setWallsRandom(arena, wallfrequency):

    for x in range(len(arena)):
        for y in range(len(arena[0]) - 1):
            #horizontal wall based on the frequency
            if random.random() >= wallfrequency:
                arena[x][y + 1][2] = False
                arena[x][y][3] = False

    for x in range(len(arena) - 1):
        for y in range(len(arena[0])):
            #vertical wall based on the frequency
            if random.random() >= wallfrequency:
                arena[x][y][1] = False
                arena[x + 1][y][0] = False

    return arena

def removeIsolatingWalls(arena, maxwallcount):

    for x in range(len(arena)):
        for y in range(len(arena[x])):

            #counts the walls
            wallcount = 0
            for z in range(len(arena[x][y])):
                wallcount = wallcount + (1 - int(arena[x][y][z]))

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
