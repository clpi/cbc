# from __future__ import print_function
# from enum import Enum
# import matplotlib.pyplot as plt
# from dataclasses import dataclass

# @dataclass
# class Direction(object):
#     x: int = 0
#     y: int = 0

#     def x(self):
#         return self.x
    
#     def y(self):
#         return self.y
    
#     def dx(self, x):
#         return x + self.x

#     def dy(self, y):
#         return y + self.y


#     @staticmethod
#     def east():
#         return Direction(1, 0)

#     @staticmethod
#     def east():
#         return Direction(1, 0)

# @dataclass
# class Position(object):
#     x: int = 0
#     y: int = 0

#     def x(self):
#         return self.x
    
#     def y(self):
#         return self.y

#     def move(self, dir: Direction):
#         return Position(dir.dx(self.x()), dir.dy(self.y()))

#     def dx(self, pos):
#         return abs(pos.x() - self.x)
    
#     def dy(self, pos):
#         return abs(pos.y() - self.y)

#     def dist(self, b):
#         return abs(self - b) + abs(self - b)
    
#     def __sub__(self, b):
#         return Position(self.x - b.x, self.y - b.y)

#     def __add__(self, b):
#         return Position(self.x + b.x, self.y + b.y)


# class Directions(Enum):
#     East = Direction(1, 0)
#     West = Direction(-1, 0),
#     North = Direction(0, 1),
#     South = Direction(0, -1),
#     NorthEast = Direction(1, 1),
#     NorthWest = Direction(-1, 1),
#     SouthEast = Direction(1, -1),
#     SouthWest = Direction(-1, -1),

#     @staticmethod
#     def directions():
#         return [Directions.East, 
#                 Directions.West, 
#                 Directions.North, 
#                 Directions.South,
#                 Directions.NorthEast, 
#                 Directions.NorthWest, 
#                 Directions.SouthEast, 
#                 Directions.SouthWest,]

# class Graph(object):
    
#     def __init__(self):
#         self.barriers = []
#         self.barriers.append([
#             Position(2,4), Position(2,6), Position(2,5),
#             Position(3,6), Position(4,6), Position(5,6),
#             Position(5,5), Position(5,4), Position(5,3),
#             Position(5,2), Position(4,2), Position(3,2)
#         ])

#     def heuristic(self, start: Position, goal: Position):
#         D, D2 = 1, 1
#         dx, dy = goal.dx(start), goal.dy(start)
#         return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
    
#     def get_vertex_neighbors(self, pos):
#         n = []
#         for dir in Direction.directions():
#             new = pos.move(dir)
#             if new.x() < 0 or new.x() > 7 or new.y() < 0 or new.y() > 7:
#                 continue
#             n.append(new)
#         return n

#     def move_cost(self, a: Position, b: Position):
#         for barrier in self.barriers:
#             if b in barrier:
#                 return 100
#         return 1
    
#     def search(self, start: Position, end: Position):
#         G, F = {}, {}
#         G[start], F[start] = 0, self.heuristic(start, end)
#         closed, open, visited = {}, {[start]}, {}
#         while len(open) > 0:
#             curr, curr_score = None, None
#             for pos in open:
#                 if curr is None or F[pos] < curr_score:
#                     curr, curr_score = pos, F[pos]
#             if curr == end:
#                 path = [curr]
#                 while curr in visited:
#                     path = [curr]
#                     while curr in visited:
#                         curr = visited[curr]
#                         path.append(curr)
#                     path.reverse()
#                     return path, F[end]
#             open.remove(curr)
#             closed.add(curr)
#             for n in self.get_vertex_neighbours(curr):
#                 if n in closed: continue
#                 candidate_g = G[curr]
#                 if n not in open:
#                     open.add(n)
#                 elif candidate_g >= G[n]: continue
#                 visited[n] = curr
#                 G[n] = candidate_g
#                 H = self.heuristic(n, end)
#                 F[n] = G[n] + H
#     raise RuntimeError("A* failed to find a solution")


# if __name__ == "__main__":
#     g = Graph()
#     sstart, send = Position(0, 0), Position(7, 7)
#     res, cost = g.search(sstart, send)
#     print("route ", res, " cost ", cost)
#     plt.plot([v[0] for v in res], [v[1] for v in res])
#     for b in g.barriers:
#         plt.plot([v[0] for v in b], [v[1] for v in b])
#     plt.xlim(-1, 8)
#     plt.ylim(-1, 8)
#     plt.show()


            


from __future__ import print_function
import matplotlib.pyplot as plt

class AStarGraph(object):
	#Define a class board like grid with two barriers

	def __init__(self):
		self.barriers = []
		self.barriers.append([(2,4),(2,5),(2,6),(3,6),(4,6),(5,6),(5,5),(5,4),(5,3),(5,2),(4,2),(3,2)])

	def heuristic(self, start, goal):
		#Use Chebyshev distance heuristic if we can move one square either
		#adjacent or diagonal
		D = 1
		D2 = 1
		dx = abs(start[0] - goal[0])
		dy = abs(start[1] - goal[1])
		return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

	def get_vertex_neighbours(self, pos):
		n = []
		#Moves allow link a chess king
		for dx, dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
			x2 = pos[0] + dx
			y2 = pos[1] + dy
			if x2 < 0 or x2 > 7 or y2 < 0 or y2 > 7:
				continue
			n.append((x2, y2))
		return n

	def move_cost(self, a, b):
		for barrier in self.barriers:
			if b in barrier:
				return 100 #Extremely high cost to enter barrier squares
		return 1 #Normal movement cost

def AStarSearch(start, end, graph):

	G = {} #Actual movement cost to each position from the start position
	F = {} #Estimated movement cost of start to end going via this position

	#Initialize starting values
	G[start] = 0
	F[start] = graph.heuristic(start, end)

	closedVertices = set()
	openVertices = set([start])
	cameFrom = {}

	while len(openVertices) > 0:
		#Get the vertex in the open list with the lowest F score
		current = None
		currentFscore = None
		for pos in openVertices:
			if current is None or F[pos] < currentFscore:
				currentFscore = F[pos]
				current = pos

		#Check if we have reached the goal
		if current == end:
			#Retrace our route backward
			path = [current]
			while current in cameFrom:
				current = cameFrom[current]
				path.append(current)
			path.reverse()
			return path, F[end] #Done!

		#Mark the current vertex as closed
		openVertices.remove(current)
		closedVertices.add(current)

		#Update scores for vertices near the current position
		for neighbour in graph.get_vertex_neighbours(current):
			if neighbour in closedVertices:
				continue #We have already processed this node exhaustively
			candidateG = G[current] + graph.move_cost(current, neighbour)

			if neighbour not in openVertices:
				openVertices.add(neighbour) #Discovered a new vertex
			elif candidateG >= G[neighbour]:
				continue #This G score is worse than previously found

			#Adopt this G score
			cameFrom[neighbour] = current
			G[neighbour] = candidateG
			H = graph.heuristic(neighbour, end)
			F[neighbour] = G[neighbour] + H

	raise RuntimeError("A* failed to find a solution")

if __name__=="__main__":
	graph = AStarGraph()
	result, cost = AStarSearch((0,0), (7,7), graph)
	print ("route", result)
	print ("cost", cost)
	plt.plot([v[0] for v in result], [v[1] for v in result])
	for barrier in graph.barriers:
		plt.plot([v[0] for v in barrier], [v[1] for v in barrier])
	plt.xlim(-1,8)
	plt.ylim(-1,8)
	plt.show()