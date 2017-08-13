#!/usr/bin/env python

#This code is a simulation and code base for the PennState robotics club
#entry into the Harvard PacMan robotics competition. Code written by:
#Geoffrey Billy,
#Saimun Shahee,
#Kate Heasley,
#Dimitri Lewicki
#Lauren Colwell

import random

def setupGame(row,column):

    # a location has 5 associated values: whether it is up, down, left, right linked and whether or not there is a dot
    arena = [[[True for z in range(5)] for x in range(row)] for y in range(column)]

    ghost1 = (random.randint(0, row-1), random.randint(0, column-1))
    ghost2 = (random.randint(0, row-1), random.randint(0, column-1))
    ghost3 = (random.randint(0, row-1), random.randint(0, column-1))
    ghost4 = (random.randint(0, row-1), random.randint(0, column-1))
    player =  (random.randint(0, row-1), random.randint(0, column-1))

    positions = [ghost1, ghost2, ghost3, ghost4, player]

    return arena, positions

def printBoard(arena, positions):

    #prints row-wise
    printrow = ''
    for x in range(len(arena)):

        #parses rows in arena matrix for dots or spaces
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
        for player in range(4):
            if positions[player][0] == x:
                printrow = printrow[:positions[player][1]] + str(player) + printrow[positions[player][1]+1:]
        if positions[4][0] == x:
            printrow = printrow[:positions[player][1]] + 'P' + printrow[positions[player][1]+1:]

        #outputs the row to the console and then clears it
        print printrow
        printrow = ''

        for y in range(len(arena[0])):
            if arena[x][y][0]:
                printrow = printrow + '  '
            else:
                printrow = printrow + ' -'

        print printrow
        printrow = ''

def moveGhost(ghost, pos, arena):

    distList = [1, 1, 1, 1]

    #STILL NEED TO ADD GHOST COLLISION PREVENTION

    for ii in range(4):
        if not arena[pos[ghostie][0]][pos[ghostie][1]][ii]:
            distList[ii] = 0

    return distList

def movePlayer(pos, arena):

    distList = [1, 1, 1, 1]
    distList *= avoidGhosties(distList, pos, arena)

    for ii in range(4):
        if not arena[pos[4][0]][pos[4][1]][ii]:
            distList[ii] = 0

    return distList

def runSimulation():

    gameover = False

    row = 10
    column = 10

    arena, positions = setupGame(row, column)
    printBoard(arena, positions)

runSimulation()
