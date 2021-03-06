import osmnx
import heapq
import sys

sys.path.insert(0, '.')
from src.routing_mode import RoutingMode
from src.routing_helper import RoutingHelper

class RoutingDijkstra(RoutingMode):
	"""
	Represents Dikstra routing for path finding solution

	"""
	def __init__(self):
		super().__init__()

	def routing_action(self, graph, start, end, x=0, elevation_setting=None):
		"""
		Runs Dijkstra shortest path algorithm to find a route that either maximizes or minimizes elevation gain
		from start to end location within x% of the shortest path. 
		If elevation_setting is None, it finds the shortest path from start to end.

		params:
			graph: networkx multidigraph - the area we are searching in
			start: int - the starting location of the route
			end: int - the end location of the route
			x: float - the percentage we can deviate from the shortest path length
			elevation_setting: string - either "maximize", "minimize", or None

		return: list - a route from start to end or None if a route does not exist
		"""
		distances = {}
		elevations = {}
		previous_nodes = {}

		#priority = elevation
		queue = [] 

		#queue element stores (total elevation from start node to current node, total distance from start to current node, current node, previous node)
		heapq.heappush(queue, (0, 0, start, None))
		distances[start] = 0
		elevations[start] = 0
		previous_nodes[start] = None

		visited = set()

		max_length = RoutingHelper().find_max_length(graph, x, start, end)
		if max_length == -1:
			return None

		while queue:
			current = heapq.heappop(queue)
			current_node = current[2]

		#either we have not seen this node before or we have found a shorter path to this node
			if current_node not in distances or (distances[current_node] > current[1]):
				elevations[current_node] = current[0] if elevation_setting == "minimize" else -current[0]
				distances[current_node] = current[1]
				previous_nodes[current_node] = current[3]

			#we've found a complete path, stop searching this path
			if current_node == end:
				break

			visited.add(current_node)

			for edge in graph.edges(current_node, data=True):
				next_node = edge[1]
				#avoid self loops
				if next_node == current_node:
					continue
				distance_to_next_node = graph[current_node][next_node][0]["length"]
				total_new_distance = current[1] + distance_to_next_node
				total_old_distance = float("inf") if next_node not in distances else distances[next_node]	 

				elevation_to_next_node = RoutingHelper().get_elevation_diff(graph, current_node, next_node) 
				total_elevation = elevations[current_node] + elevation_to_next_node

				#if the total distance is greater than max length, this is an invalid path
				if total_new_distance <= max_length and (next_node not in visited or total_new_distance < total_old_distance):
					if elevation_setting == "maximize":
						heapq.heappush(queue, (-total_elevation, total_new_distance, next_node, current_node))
					elif elevation_setting == "minimize":
						heapq.heappush(queue, (total_elevation, total_new_distance, next_node, current_node))
					else:
						heapq.heappush(queue, (0, total_new_distance, next_node, current_node))

		return RoutingHelper().get_path_from_previous_nodes(previous_nodes, start, end)

class RoutingAStar(RoutingMode):
	"""
	Represents A* routing for path finding solution

	"""
	def __init__(self):
		super().__init__()

	def routing_action(self, graph, start, end, x=0, elevation_setting=None):
		"""
		Runs A* shortest path algorithm to find a route that either maximizes or minimizes elevation gain
		from start to end location within x% of the shortest path. 
		If elevation_setting is None, it finds the shortest path from start to end.
		params:
			graph: networkx multidigraph - the area we are searching in
			start: int - the starting location of the route
			end: int - the end location of the route
			x: int - the percentage we can deviate from the shortest path length
			elevation_setting: string - either "maximize", "minimize", or None
		return: list - a route from start to end or None if a route does not exist
		"""

		g_elevations = {} #for each node, stores elevation from start node to next node
		f_elevations = {} #for each node, stores elevation from start node to next node + elevation from current node to end node
		distances = {} #
		previous_nodes = {}

		queue = []

		#queue element stores (f_elevation, g_elevation, total distance from start to current node, current node, previous node)
		heapq.heappush(queue, (RoutingHelper().get_elevation_diff(graph, start, end), 0, 0, start, None))

		visited = set()
		max_length = RoutingHelper().find_max_length(graph, x, start, end)
	
		if max_length == -1:
			return None

		while queue:
			current = heapq.heappop(queue)
			current_node = current[3]
			
			#either we have not seen this node before or we have found a shorter path to this node
			if current_node not in distances or (distances[current_node] > current[2]):
				f_elevations[current_node] = current[0] if elevation_setting == "minimize" else -current[0]
				g_elevations[current_node] = current[1]
				distances[current_node] = current[2]
				previous_nodes[current_node] = current[4]

			#we've found the best path, stop searching
			if current_node == end:
				break

			visited.add(current_node)
	
			for edge in graph.edges(current_node, data=True):
				next_node = edge[1]

				#avoid self loops
				if next_node == current_node:
					continue

				g_elevation_to_next_node = RoutingHelper().get_elevation_diff(graph, current_node, next_node)
				g_total_new_elevation = g_elevations[current_node] + g_elevation_to_next_node

				distance_to_next_node = graph[current_node][next_node][0]["length"]
				total_new_distance = distances[current_node] + distance_to_next_node
				total_old_distance = float("inf") if next_node not in distances else distances[next_node]

				heuristic = RoutingHelper().get_elevation_diff(graph, next_node, end)

				#if the total distance is greater than max length, this is an invalid path
				if total_new_distance <= max_length and (next_node not in visited or total_new_distance < total_old_distance):
					if elevation_setting == "maximize":
						heapq.heappush(queue, (-g_total_new_elevation - heuristic, g_total_new_elevation, total_new_distance, next_node, current_node))
					elif elevation_setting == "minimize":
						heapq.heappush(queue, (g_total_new_elevation + heuristic, g_total_new_elevation, total_new_distance, next_node, current_node))
					else:
						heapq.heappush(queue, (0, 0, total_new_distance, next_node, current_node))

		return RoutingHelper().get_path_from_previous_nodes(previous_nodes, start, end)

class RoutingDFS(RoutingMode):
	"""
	Represents DFS routing for path finding solution

	"""
	def __init__(self):
		super().__init__()

	def routing_action(self, graph, start, end, x=0, elevation_setting=None):
		"""
		Runs DFS path algorithm from start to end location and finds the path that has a length <= max length 
		and then finds a route that either maximizes or minimizes elevation gain from start to end location 
		If elevation_setting is None, it finds the shortest path from start to end.

			params:
				graph: networkx multidigraph - the area we are searching in
				start: int - the starting location of the route
				end: int - the end location of the route
			return: list - a route from start to end or None if a route does not exist
		"""
		
		visited = {}
		for node in graph.nodes:
			visited[node] = 0

		path = []

		max_length = RoutingHelper().find_max_length(graph, x, start, end)
		if max_length == -1:
			return None


		all_paths = []

		def dfs_get_all_paths(graph, current, visited, path, depth):
			if current == end:
				if RoutingHelper().get_total_path_length(path, graph) <= max_length:
					all_paths.append(path[:])
				return

			if depth == 0:
				return

			for edge in graph.edges(current, data=True):

				next_node = edge[1]

				if visited[next_node] == 0:
					visited[next_node] = 1
					path.append(next_node)
					dfs_get_all_paths(graph, next_node, visited, path, depth - 1)
					path.remove(next_node)
					visited[next_node] = 0


		path.append(start)
		visited[start] = 1
		depth = 50
		dfs_get_all_paths(graph,start,visited,path, depth)

		# finds the maximum/minimum/shortest path
		elevation = []
		shortest = sys.maxsize
		shortest_path = 0

		# find the shortest path by finding the path length of each path in all paths
		# find the elevation of each path and add it to elevation list
		for p in all_paths:
			elevation.append((p, RoutingHelper().get_path_elevation(p, graph)))
			path_len = RoutingHelper().get_total_path_length(p,graph)
			if path_len<shortest:
				shortest = path_len
				shortest_path = p

		finalPath = []

		# sort elevation list based on elevation 
		elevation.sort(key=lambda x: x[1])

		if elevation_setting == "maximize":
			max_elevation = elevation[-1][0]
			finalPath = max_elevation
		elif elevation_setting == "minimize":
			min_elevation = elevation[0][0]
			finalPath = min_elevation
		else:
			finalPath = shortest_path

		return finalPath

class RoutingBFS(RoutingMode):
	"""
	Represents BFS routing for path finding solution

	"""
	def __init__(self):
		super().__init__()

	def routing_action(self, graph, start, end, x=0, elevation_setting=None):
		"""
		**EXPERIMENTAL USE ONLY**
		Runs BFS shortest path algorithm to find a shortest path from start to end location.

		params:
			graph: networkx multidigraph - the area we are searching in
			start: int - the starting location of the route
			end: int - the end location of the route

			return: list - a route from start to end or None if a route does not exist
		"""
		queue = []
		queue.append([start])
		visited = []

		if start == end:
			return [end]

		# keep on iterating until every path has been explored
		while queue:
			# pop first path
			currPath = queue.pop(0)
			# getting last node from current path
			lastNode = currPath[-1]
			if lastNode not in visited:
				# looking at all the neighbors 
				for edge in graph.edges(lastNode, data=True):
					neighbor = edge[1]
					newCurPath = list(currPath)
					newCurPath.append(neighbor)
					queue.append(newCurPath)
					# mark node as visited 
					visited.append(lastNode)
					if neighbor == end:
						return newCurPath
	
		# if no paths found return None
		return None

class RoutingOldDFS(RoutingMode):
	"""
	Represents DFS routing for path finding solution

	"""
	def __init__(self):
		super().__init__()

	def routing_action(self, graph, start, end, x=0, elevation_setting=None):
		"""
		**EXPERIMENTAL USE ONLY**
			Runs DFS path algorithm from start to end location to find shortest path

			params:
				graph: networkx multidigraph - the area we are searching in
				start: int - the starting location of the route
				end: int - the end location of the route

			return: list - a route from start to end or None if a route does not exist
		"""
		
		stack = []
		visited = set()
		previous_nodes = {}

		stack.append(start)
		visited.add(start)
		previous_nodes[start] = None

		while (len(stack) > 0):
			current_node = stack.pop()

			if current_node in visited:
				continue

			visited.add(next_node)

			for edge in graph.edges(current_node, data=True):
				next_node = edge[1]

				if next_node not in visited:
					stack.append((next_node))
					previous_nodes[next_node] = current_node

					if next_node == end:
						return RoutingHelper().get_path_from_previous_nodes(previous_nodes, start, end)
	
		return None