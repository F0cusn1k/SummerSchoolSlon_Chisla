from ast import copy_location
from collections import defaultdict
import my_numbers as nm
import numpy as np
import time

from functools import reduce

def sdvig(lst):
	new_lst = []

	for i in range(len(lst)):
		new_lst.append(lst[(i + 1) % len(lst)])

	return new_lst

#This class represents a directed graph using adjacency list representation
class Graph:
	def __init__(self, vertices):
		self.V = vertices #No. of vertices
		self.graph = defaultdict(list) # default dictionary to store graph


	# function to add an edge to graph
	def addEdge(self, u, v):
		self.graph[u].append(v)


	# A function used by DFS
	def DFSUtil(self, v, visited):
		# Mark the current node as visited and print it
		res = []
		visited[v] = True
		res.append(v)
		#Recur for all the vertices adjacent to this vertex
		for i in self.graph[v]:
			if visited[i] == False:
				res += self.DFSUtil(i, visited)
		return res


	def fillOrder(self, v, visited, stack):
		# Mark the current node as visited 
		visited[v] = True
		#Recur for all the vertices adjacent to this vertex
		for i in self.graph[v]:
			if visited[i] == False:
				self.fillOrder(i, visited, stack)
		stack = stack.append(v)


	# Function that returns reverse (or transpose) of this graph
	def getTranspose(self):
		graph = Graph(self.V)

		# Recur for all the vertices adjacent to this vertex
		for i in self.graph:
			for j in self.graph[i]:
				graph.addEdge(j, i)
		return graph


	# The main function that finds and prints all strongly
	# connected components
	def getSCCs(self):
		SCClist = []
		stack = []
		# Mark all the vertices as not visited (For first DFS)
		visited = [False] * (self.V)
		# Fill vertices in stack according to their finishing
		# times
		for i in range(self.V):
			if visited[i] == False:
				self.fillOrder(i, visited, stack)

		# Create a reversed graph
		rev_graph = self.getTranspose()
		  
		# Mark all the vertices as not visited (For second DFS)
		visited = [False] * (self.V)

		# Now process all vertices in order defined by Stack
		while stack:
			i = stack.pop()
			if visited[i] == False:
				component = rev_graph.DFSUtil(i, visited)
				if len(component) > 1:
					SCClist.append(component)
		return SCClist

	def inducedSubgraph(self, vertices):
		graph = Graph(len(vertices))
		for i, v in enumerate(vertices):
			for j, u in enumerate(vertices):
				if u in self.graph[v]:
					graph.addEdge(i, j)
		return graph

	def isCyclic(self):
		v = 0
		for i in range(self.V):
			if len(self.graph[v]) > 1:
				return False
			v = self.graph[v][0]
		return True

class Base_cycle:
	def __init__(self, points, sys_base):
		self.graph = {}
		self.sys_base = sys_base

		for point in points:
			self.graph[point] = {}

			for i in range(point ** 2, point ** 2 + point):
				num = i

				while num >= sys_base:
					num //= sys_base

				if num in points:
					self.graph[point][num] = True

	def small_cycles_rec(self, visited, start):
		small_cycles = []

		for location in self.graph[visited[-1]]:
			if location < start:
				continue
			# print(location)
			# print(self.graph[location])

			if location in visited:
				# print("cycle")
				# print(visited)

				small_cycles.append([])
				small_cycles[-1].append(location)
				i = -1
				# graph[visited[-1]][location] = False

				while visited[i] != location:
					small_cycles[-1].append(visited[i])
					i -= 1
					# graph[visited[i - 1]][visited[i]] = False
					# visited.pop()

				small_cycles[-1].reverse()

				# for i in range(len(small_cycles[-1])):
				# 	print(i)
				# 	print(self.graph[small_cycles[i - 1]])
				# 	if not self.graph[small_cycles[-1][i - 1]][small_cycles[i]]:
				# 		print("WAIT")

				start = min(small_cycles[-1])
				while small_cycles[-1][0] != start:
					# print("jo")
					# print(small_cycles[-1])
					small_cycles[-1] = sdvig(small_cycles[-1])

			else:
				tupic = True

				for edge in self.graph[location]:
					if self.graph[location][edge]:
						tupic = False
						break

				if not tupic:
					# print("new rec")
					visited.append(location)
					small_cycles += self.small_cycles_rec(visited, start)
					visited.pop()

		return small_cycles


	# def small_cycles(self):
	#   small_cycles = []
	#   graph = self.graph

	#   for start in graph:
	#       visited = [start]
	#       location = start
	#       # print(graph[location])
	#       while True:
	#           move = False

	#           for i in graph[location]:
	#               if graph[location][i]:
	#                   move = True
	#                   location = i

	#                   if location in visited:
	#                       # print("cycle", location)
	#                       small_cycles.append([])
	#                       graph[visited[-1]][location] = False
	#                       small_cycles[-1].append(location)

	#                       while visited[-1] != location:
	#                           graph[visited[-2]][visited[-1]] = False
	#                           small_cycles[-1].append(visited[-1])
	#                           visited.pop()

	#                   else:
	#                       tupic = True

	#                       for edge in graph[location]:
	#                           if graph[location][edge]:
	#                               tupic = False
	#                               break

	#                       if tupic:
	#                           # print("tupic")
	#                           graph[visited[-1]][location] = False
	#                           location = visited[-1]
	#                       else:
	#                           # print("idem")
	#                           visited.append(location)
		
	#                       break

	#           if location == start and not True in graph[location]:
	#               break

	#           if not move:
	#               if len(visited) == 1:
	#                   break
	#               else:
	#                   # print("tupic")
	#                   visited.pop()
	#                   location = visited[-1]

	#   return small_cycles

def find_image_gap(current_node1, current_node2, next_node1, next_node2, base):
	if current_node1 == current_node2 and abs(next_node1 - next_node2) >= 2:
		return False
	if current_node2 < current_node1:
		current_node2, current_node_1 = current_node1, current_node2
		next_node2, next_node_1 = next_node1, next_node2
	if current_node1 - current_node2 == 1:
		last = current_node1*(current_node1+1)
		if last > base:
			last = last // base
		first = current_node2**2
		if first > base:
			first = first // base
		if next_node1 == last and next_node2 == first:
			return False
	return True

def find_cycle_gap(cycle1, cycle2, base):
	for i in range(max(len(cycle1), len(cycle2))):
		if find_image_gap(cycle1[i%len(cycle1)], cycle2[i%len(cycle2)], cycle1[(i+1)%len(cycle1)], cycle2[(i+1)%len(cycle2)], base):
			return True
	return False

def find_joined_cycles(base):
	l = nm.all_for_loop(base)
	converted_l = nm.convertor(l)
	stable_cycles = []
	# cycles_witout_two = list([i + 1, 0] for i in range(base))
	cycles_witout_gap = []

	for n, i in enumerate(converted_l):
		graph = Graph(base)
		for j in i:
			graph.addEdge(j[0], j[1])
		print(n+2)
		for c in graph.getSCCs():
			if not graph.inducedSubgraph(c).isCyclic():
				print(c)
				print()

				base_cycle = Base_cycle(c, n + 2)
				cycles = []
				for f in base_cycle.graph:
					new_cycles = base_cycle.small_cycles_rec([f], f)
					for cycle in new_cycles:
						if cycle not in cycles:
							cycles.append(cycle)

				# delete_list = []
				# for f in range(len(cycles)):
				#   if cycles[f] in cycles[:f]:
				#       delete_list.append(f)

				# delete_list.reverse()
				# for f in delete_list:
				#   cycles[f], cycles[-1] = cycles[-1], cycles[f]
				#   cycles.pop()
				cycles.sort()
				values = []
				ind = 0

				for cycle in cycles:
					value = reduce(lambda x, y: x * y if x * y < n + 2 else x * y / (n + 2), cycle)
					while np.abs(np.log(value)) > np.abs(np.log(value/(n+2))):
						value /= n + 2
					if value == 1 and n + 2 not in stable_cycles:
						stable_cycles.append((n+2, cycle))
					print(ind, cycle, value)
					ind += 1
					values.append(value)

					# if not (2 in cycle) and not (n + 2 in cycles_witout_two):
					# 	cycles_witout_two[n + 1][1] += 1

				print()

				for i in range(len(cycles)):
					for j in range(i, len(cycles)):
						if i == j:
							continue

						if not find_cycle_gap(cycles[i], cycles[j], n + 2): #and not find_cycle_gap(cycles[j], cycles[i], n + 2)
							cycles_witout_gap.append((cycles[i], cycles[j], n + 2))

				#           # if cycles[i][j] > cycles[i - 1][j] and cycles[i][j - 1] == cycles[i - 1][j - 1] and values[i] < 1 and values[i - 1]:
				#           #   for l in range(min(cycles[i][j], cycles[i - 1][j]) + 1, max(cycles[i][j], cycles[i - 1][j])):


	for a in stable_cycles:
		print(a[0], a[1])

	print()

	# for a in cycles_witout_two:
	# 	print(*a)

	# print("jo")

	for a in cycles_witout_gap:
		print(a[0], "   ", a[1], a[3])

def convertor(lst):
	res = []
	for i in lst:
		l = []
		for j in range(len(i)):
			for k in range(len(i[j])):
				l.append([j + 1, i[j][k]])
		res.append(l)
	return res

def main():
	print ("[*]")
	find_joined_cycles(85)

if __name__ == '__main__':
	main()