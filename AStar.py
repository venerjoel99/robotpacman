
def AStar(start,end): #start and end are ordered (x,y) coordinates
	openSet=[start]
	closedSet=[]

	while(openSet):
		pass




def manhattanDistance(start,end):
	return abs(end[1]-start[1]) + abs(end[0]-start[0])

class Node:
	def __init__(self,g,h):
		self.g=g
		self.h=h

	def f(self):
		return self.g+self.h