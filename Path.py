from math import sqrt
'''
class Node:
	def __init__(self, x, y):
		self.child = None
		self.x = x
		self.y = y
		self.distance = 1 #placeholder
		self.direction = "null"
		self.visited = False
	
	def setDistance(self, dist):
		self.distance = dist
	
	def getDistance(self):
		return self.distance
	
	def setDirection(self, dir):
		self.direction = dir
	
	def markVisited(self):
		self.visited = True
	
	def isVisited(self):
		return self.visited
'''
		
def length(a, b):
	x = (b[0] - a[0])
	y = (b[1] - a[1])
	return sqrt(x**2 + y**2)

def closest(destination, graph):
	min = -1
	result = 0,0
	for v in graph:
		dist = length(destination, v)
		if min == -1 or dist < min:
			min = dist
			result = v
	return result

def min_distance(distances, destination):
	min = -1
	vertex = None
	for v in distances:
		if distances[v] == -1:
			continue
		f_cost = distances[v] + length(v, destination)
		if min == -1 or f_cost < min:
			vertex = v
			min = f_cost
	return vertex
	
def neighbors(graph, vertex):
	up = (vertex[0] - 1, vertex[1])
	down = (vertex[0] + 1, vertex[1])
	left = (vertex[0], vertex[1] - 1)
	right = (vertex[0], vertex[1] + 1)
	moves = [left, right, up, down]
	nodes = []
	for move in moves:
		if move in graph:
			nodes.append(move)
	return nodes

def path(graph, source, destination):
	distance = dict()
	prev = dict()
	for vertex in graph:
		if vertex==source:
			distance[vertex] = 0
			prev[vertex] = None
		else:
			distance[vertex] = -1
	current = None
	while len(distance) > 0 and current!= destination:
		current = min_distance(distance, destination)
		min = -1
		for node in neighbors(distance, current):
			cost = distance[current] + 1
			if distance[node] == -1 or cost < distance[node]:
				distance[node] = cost
				prev[node] = current
		distance.pop(current)
	if destination not in prev:
		current = closest(destination, prev)
	result = [current]
	x, y = current
	while prev[(x,y)] != None:
		result = [prev[(x,y)]] + result[:]
		x,y = prev[x,y]
	return result
	
def navigate(maze, source, destination):
	graph=maze.getGraph()
	route = path(graph, source, destination)
	directions = []
	for i in range(len(route) - 1):
		s = ''
		v1, v2 = route[i], route[i+1]
		x = v2[1] - v1[1]
		y = v2[0] - v1[0]
		if x==-1:
			s = 'up'
		elif x==1:
			s = 'down'
		elif y==1:
			s = 'right'
		elif y==-1:
			s = 'left'
		directions.append(s)
	return directions


			
		
		