from Tile import Tile
from Path import navigate
from random import random,randint,seed
import os
from time import sleep
from Pacman import Pacman
from Ghosts import Ghost, Blinky,Inky,Pinky,Clyde

class Maze:



	def __init__(self,x,y):
		self.arena=[[Tile("Space") for row in range(y)] for col in range(x)]
		if(x%2==0 or y%2==0):
			raise Exception("Mazes  must have odd width and height")
		self.x=x
		self.y=y
		self.freq=.5
		self.pacman=Pacman()
		self.ghosts=[Blinky.Blinky(),Pinky.Pinky(),Inky.Inky(),Clyde.Clyde()]
		self.__setPacmanPos(1,1)
		
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

		for i in range(1,self.x,2):
			for j in range(1,self.y,2): #visit all odd tiles
				#print("x,y",i,j)
				self.arena[i][j].type="Space"
				#print("Tile:",i,j,"\n\n")
				wallCount=0
				adjacentPositions=[]
				if self.arena[i-1][j].getType()=="Wall":
					wallCount+=1
					if(not(i-1<=0 or j<=0 or j>=y-1 or i-1>=x-1)):
						adjacentPositions.append((i-1,j))
				if self.arena[i+1][j].getType()=="Wall":
					wallCount+=1
					#print("x:",i+1,"y:",j)
					if(not(j<=0 or i+1>=x-1 or j>=y-1 or i+1<=0)):
						adjacentPositions.append((i+1,j))
				if self.arena[i][j-1].getType()=="Wall":
					wallCount+=1
					if(not(i<=0 or j-1<=0 or i>=x-1 or j-1>=y-1)):
						adjacentPositions.append((i,j-1))
				if self.arena[i][j+1].getType()=="Wall":
					wallCount+=1
					if(not(i<=0 or j+1<=0 or i>=x-1 or j+1>=y-1)):
						#print("a",i,j+1)
						adjacentPositions.append((i,j+1))


				#print(adjacentPositions)

				desiredWallCount=randint(2,2)
				#print("Desired Walls",desiredWallCount)
				while(wallCount>desiredWallCount): #randomly remove adjacent walls until they hit the max allowed number (2)
					#print("Adjacent Walls:",adjacentPositions)
					#print(i,j,len(adjacentPositions))
					if(not(adjacentPositions)):
						break
					try:
						toRemove=randint(0,len(adjacentPositions)-1)
					except ValueError: #if len(adjacentPositions) is 1, just remove the only item
						toRemove=0
					#print("Removed index",toRemove)
					#print(adjacentPositions[toRemove])
					n,m=adjacentPositions[toRemove]
					self.arena[n][m].type="Space"
					adjacentPositions.pop(toRemove)
					wallCount-=1

		for i in range(1,self.x-1):
			for j in range(1,self.y-1):
				if self.arena[i][j].type=="Space":
					self.arena[i][j].type="Dot"


	def movepacman(self,direction): #returns true if the move worked, false if pacman tried to move into a wall
		if(direction=="up"):
			x,y=self.pacmanPos
			
			if y<0 or self.arena[x][y-1].type=="Wall":
				return False
			else:
				self.arena[x][y].pacman=False
				self.__setPacmanPos(x,y-1)
				return True
		elif(direction=="left"):
			x,y=self.pacmanPos
			if x<0 or self.arena[x-1][y].type=="Wall":
				return False
			else:
				self.arena[x][y].pacman=False
				self.__setPacmanPos(x-1,y)
				return True
		elif(direction=="down"):
			x,y=self.pacmanPos
			if y>=self.y or self.arena[x][y+1].type=="Wall":
				return False
			else:
				self.arena[x][y].pacman=False
				self.__setPacmanPos(x,y+1)
				return True
		if(direction=="right"):
			x,y=self.pacmanPos
			if x>=self.x or self.arena[x+1][y].type=="Wall":
				return False
			else:
				self.arena[x][y].pacman=False
				self.__setPacmanPos(x+1,y)
				return True




	def __setPacmanPos(self,x,y):
		if(self.arena[x][y].type!="Wall"):
			self.pacmanPos=x,y
			self.arena[x][y].pacman=True
		else:
			raise Exception("Tried to place pacman on a wall")

	def getGraph(self):
		nodes=[]
		for i in range(1,self.x-1):
			for j in range(1,self.y-1):
				if self.arena[i][j].type!="Wall":
					nodes.append((i,j))

		return nodes

	def __str__(self):
		s=""
		for y in range(self.y):
			for x in range(self.x):
				s+=str(self.arena[x][y])
			s+="\n"

		return s


	def generateMap(self, file_name):
		temp = []
		fp = open(file_name, 'r')
		for line in fp:
			col = []
			for char in line:
				if char != '\n':
					col.append(int(char))
			size = len(temp)
			if size > 0 and len(temp[size - 1]) != len(col):
				raise Exception("Unequal rows")
			else:
				temp.append(col)
		fp.close()
		self.x = len(temp[0])
		self.y = len(temp)
		self.arena=[]
		for i in range(len(temp[0])):
			row = []
			for j in range(len(temp)):
				value = temp[j][i]
				if value==1:
					row.append(Tile('Wall'))
				elif value==0:
					row.append(Tile('Dot'))
				elif value==2:
					row.append(Tile('Space'))
			self.arena.append(row)
		self.__setPacmanPos(14,23)
if __name__=="__main__":
	m=Maze(19,19)
	m.generateMap("map.txt")
	#Test for Djikstra's algorithm
	start = (14,23)
	end = (26,29)
	moves = navigate(m, start, end)
	print(m)
	#moves=["right"]*6 +["down"]*2
	for move in moves:
		sleep(.05)
		m.movepacman(move)
		os.system('cls')
		print(m)
