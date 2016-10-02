#!/usr/bin/env python

import random
def setupArena(r,c):
    arena = [[0 for x in range(r)] for y in range(c)]
    g1 = (random.randint(0,r-1),random.randint(0,c-1))
    g1=  (0,5)
    g2 = (random.randint(0,r-1),random.randint(0,c-1))
    g3 = (random.randint(0,r-1),random.randint(0,c-1))
    g4 = (random.randint(0,r-1),random.randint(0,c-1))
    for i in range(0,r):
        for j in range(0,c):
            arena[i][j] = u"\u2610"
    arena[g1[0]][g1[1]] = "G1"
    arena[g2[0]][g2[1]] = "G2"
    arena[g3[0]][g3[1]] = "G3"
    arena[g4[0]][g4[1]] = "G4"
    lstGhstPos = [g1,g2,g3,g4]
    for i in range(0,len(arena)):
        for j in range(0,len(arena[0])):
            print(arena[i][j],end = " ")
        print()
    return arena,lstGhstPos

def updatePosGhost(posG,arena,mvDist,num):
    x = posG[0]
    y = posG[1]
    changeX,changeY = 0,0
    arena[x][y] = u"\u2610"
    if max(mvDist) == mvDist[0]:
        changeX = -1
    elif max(mvDist) == mvDist[2]:
        changeX = 1
    elif max(mvDist) == mvDist[1]:
        changeY = -1
    elif max(mvDist) == mvDist[3]:
        changeY = 1
    arena[x + changeX][y + changeY] = "G"+str(num)
    for i in range(0,len(arena)):
        for j in range(0,len(arena[0])):
            print(arena[i][j],end = " ")
        print()
    return arena,(x + changeX,y + changeY)

def mvDist(posG,arena):
    distList = []
    for k in range(0,5):
        distList.append(random.random())
    if posG[0] == 0:
        distList[0] = 0
    if posG[1] == 0:
        distList[1] = 0
    if posG[0] == len(arena):
        distList[2] = 0       
    if posG[1] == len(arena[0]):
        distList[3] = 0
    return distList


board,listOfGhostPositions = setupArena(10,10)

for ii in range(10):
    print()
    board,listOfGhostPositions[0] = updatePosGhost(listOfGhostPositions[0],board,mvDist(listOfGhostPositions[0],board),1)
