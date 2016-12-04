#!/usr/bin/env python

#This code is a simulation and code base for the PennState robotics club
#entry into the Harvard PacMan robotics competition. Code written by:
#Geoffrey Billy, 
#Saimun Shahee,
#Kate Heasley,
#Dimitri Lewicki
#Lauren Colwell

import random

gameover = False

def setupGame(r,c):

    # linked [x-1, x+1, y-1, y+1, dot]
    actualarena, playerknownarena = [[[False for z in range(5)] for x in range(r)] for y in range(c)]

    ghostie1 = (random.randint(0, r-1), random.randint(0, c-1))
    ghostie2 = (random.randint(0, r-1), random.randint(0, c-1))
    ghostie3 = (random.randint(0, r-1), random.randint(0, c-1))
    ghostie4 = (random.randint(0, r-1), random.randint(0, c-1))
    player =  (random.randint(0, r-1), random.randint(0, c-1))

    positions = [ghostie1, ghostie2, ghostie3, ghostie4, player]

    return actualarena, playerknownarena, positions

def ghostieMove(ghostie, pos, arena):

    distList = [1, 1, 1, 1]
    
    #STILL NEED TO ADD GHOST COLLISION PREVENTION
    
    for ii in range(4):
        if not arena[pos[ghostie][0]][pos[ghostie][1]][ii]:
            distList[ii] = 0

    return distList

def playerMove(pos, arena):

    distList = [1, 1, 1, 1]
    distList *= avoidGhosties(distList, pos, arena)

    for ii in range(4):
        if not arena[pos[4][0]][pos[4][1]][ii]:
            distList[ii] = 0

    return distList

def avoidGhosties(distList, pos, arena):

def updatePKA(p, glp, pka):

    change = -1
    for ghostie in range(4):

        if p[ghostie][0] != glp[ghostie][0]:
            if p[ghostie][0] > glp[ghostie][0]:
                change = 0
            else:
                change = 1

        else:
            if p[ghostie][1] > glp[ghostie][1]:
                change = 2
            else:
                change = 3

        pka[p[ghostie][0]][p[ghostie][1]][change] = True
        pka[glp[ghostie][0]][glp[ghostie][1]][change] = True

    return pka
    
aa, pka, p = setupGame(10,10)
glp = p

while not gameover:

    pka = updatePKA(p,glp, pka)
    
    glp = p

    if (((p[4][0] - 1), p[4][1]) in p or (((p[4][0] + 1), p[4][1]) in p or (((p[4][0]), p[4][1] - 1) in p or (((p[4][0]), p[4][1] + 1) in p:
        gameover = True

print
print "GAME OVER"
