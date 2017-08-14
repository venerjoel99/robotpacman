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
        while position[0] in positions or [position[0][0] - 1, position[0][1]] in positions or [position[0][0] + 1, position[0][1]] in positions or [position[0][0], position[0][1] - 1] in positions or [position[0][0], position[0][1] + 1] in positions:
              position = [[random.randint(0, row-1), random.randint(0, column-1)]]

        #adds it to the rest of the positions
        positions = positions + position

    return positions

def setWallsRandom(wallpattern, arena):

    return

def printBoard(arena, positions):

    #prints row-wise
    printrow = ''
    for x in range(len(arena)):

        #parses rows for dots or spaces with vertical walls intersparced when needed
        for y in range(len(arena[0])):
            if arena[x][y][3]:
                printrow = printrow + ' '
            else:
                printrow = printrow + '|'

            if arena[x][y][4]:
                printrow = printrow + '.'
            else:
                printrow = printrow + 'o'

        #replaces the the dot or space for the character when needed
        for player in range(len(positions)):
            if positions[player][0] == x:
                printrow = printrow[:positions[player][1] * 2 + 1] + str(player) + printrow[positions[player][1] * 2 + 2:]

        #outputs the row of dots + vertical walls to the console and then clears it
        print printrow
        printrow = ''

        #parses rows for horizontal walls when needed
        for y in range(len(arena[0])):
            if arena[x][y][0]:
                printrow = printrow + '  '
            else:
                printrow = printrow + ' -'

        #outputs the row of hori to the console and then clears it
        print printrow
        printrow = ''

    #separates this board from future boards
    print '\n'

def moveGhost(ghost, pos, arena): #OLD

    distList = [1, 1, 1, 1]

    #STILL NEED TO ADD GHOST COLLISION PREVENTION

    for ii in range(4):
        if not arena[pos[ghostie][0]][pos[ghostie][1]][ii]:
            distList[ii] = 0

    return distList

def movePlayer(pos, arena): #OLD

    distList = [1, 1, 1, 1]
    distList *= avoidGhosties(distList, pos, arena)

    for ii in range(4):
        if not arena[pos[4][0]][pos[4][1]][ii]:
            distList[ii] = 0

    return distList

def runSimulation():

    gameover = False

    #default game values
    runcount = 100
    row = 10
    column = row
    ghostcount = 4
    playercount = 1
    positions = []

    for x in range(runcount):

        arena = setupArena(row, column)
        positions = setupPositionsRandom(ghostcount, [], row, column)
        positions = setupPositionsRandomNonAdjacent(playercount, positions, row, column)

        printBoard(arena, positions)

runSimulation()
