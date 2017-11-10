from Tile import Tile
from random import random,randint,seed
class NewMaze:



	def __init__(self,x,y):
		self.arena=[[Tile("Space") for row in range(y)] for col in range(x)]
		self.x=x
		self.y=y
		self.freq=.5
		#seed(5)

		wallpositions=[]
		for i in range(y): #set left and right walls
			self.arena[0][i].type="Wall"
			self.arena[x-1][i].type="Wall"

		for i in range(x): #set top and bottom walls
			self.arena[i][0].type="Wall"
			self.arena[i][y-1].type="Wall"

		for i in range(1,x-1): #set walls randomly
			for j in range(1,y-1):
				if i%2==0 and j%2==0:
					self.arena[i][j].type="Wall"

				elif random()<=self.freq:
					self.arena[i][j].type="Wall"
					wallpositions.append((i,j))

		for i in range(1,self.x-1,2):
			for j in range(1,self.y-1,2):
				print("Tile:",i,j,"\n\n")
				adjacentWalls=0
				adjacentPositions=[]
				if self.arena[i-1][j].getType()=="Wall":
					adjacentWalls+=1
					adjacentPositions.append((i-1,j))
				if self.arena[i+1][j].getType()=="Wall":
					adjacentWalls+=1
					adjacentPositions.append((i+1,j))
				if self.arena[i][j-1].getType()=="Wall":
					adjacentWalls+=1
					adjacentPositions.append((i,j-1))
				if self.arena[i][j+1].getType()=="Wall":
					adjacentWalls+=1
					adjacentPositions.append((i,j+1))



				desiredWallCount=randint(2,2)
				print("Desired Walls",desiredWallCount)
				while(len(adjacentPositions)>desiredWallCount):
					toRemove=randint(0,len(adjacentPositions)-1)
					print(adjacentPositions,toRemove)
					if ((not (i == 0 and adajecntPositions[toRemove][0] == 0) and
						))
					n,m=adjacentPositions[toRemove]
					self.arena[n][m].type="Space"
					adjacentPositions.pop(toRemove)



	def __str__(self):
		s=""
		for y in range(self.y):
			for x in range(self.x):
				s+=str(self.arena[x][y])
			s+="\n"

		return s

if __name__=="__main__":
	m=NewMaze(19,19)
	print(m)
