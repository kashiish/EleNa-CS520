import osmnx
import heapq
import sys
sys.path.insert(0, '.')
from src.routing_mode import RoutingMode

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

		max_length = super(RoutingDijkstra, self).find_max_length(graph, x, start, end)
		if max_length == -1:
			return None

		while queue:
			current = heapq.heappop(queue)
			current_node = current[2]

			if current_node not in elevations or (elevation_setting == "maximize" and elevations[current_node] < -current[0]) or (elevation_setting == "minimize" and elevations[current_node] > current[0]):
				elevations[current_node] = current[0] if elevation_setting == "minimize" else -current[0]
				distances[current_node] = current[1]
				previous_nodes[current_node] = current[3]

			#we've found a complete path, stop searching this path
			if current_node == end:
				continue

			visited.add(current_node)

			for edge in graph.edges(current_node, data=True):
				next_node = edge[1]
				#avoid self loops
				if next_node == current_node:
					continue
				distance_to_next_node = graph[current_node][next_node][0]["length"]
				total_new_distance = distances[current_node] + distance_to_next_node    

				elevation_to_next_node = super(RoutingDijkstra, self).get_elevation_diff(graph, current_node, next_node) 
				total_elevation = elevations[current_node] + elevation_to_next_node

				#if the total distance is greater than max length, this is an invalid path
				if total_new_distance <= max_length and next_node not in visited:
					if elevation_setting == "maximize":
						heapq.heappush(queue, (-total_elevation, total_new_distance, next_node, current_node))
					elif elevation_setting == "minimize":
						heapq.heappush(queue, (total_elevation, total_new_distance, next_node, current_node))
					else:
						heapq.heappush(queue, (0, total_new_distance, next_node, current_node))

		return super(RoutingDijkstra, self).get_path_from_previous_nodes(previous_nodes, start, end)

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

		g_elevations = {} #for each node, stores elevation from current node to next node
		f_elevations = {} #for each node, stores elevation from current node to next node + elevation from current node to end node
		distances = {} #
		previous_nodes = {}

		queue = []

		#queue element stores (f_elevation, g_elevation, total distance from start to current node, current node, previous node)
		heapq.heappush(queue, (super(RoutingAStar, self).get_elevation_diff(graph, start, end), 0, 0, start, None))

		visited = set()
		max_length = super(RoutingAStar, self).find_max_length(graph, x, start, end)
	
		if max_length == -1:
			return None

		while queue:
			current = heapq.heappop(queue)
			current_node = current[3]

			if current_node not in f_elevations or (elevation_setting == "maximize" and f_elevations[current_node] < -current[0]) or (elevation_setting == "minimize" and f_elevations[current_node] > current[0]):
				f_elevations[current_node] = current[0] if elevation_setting == "minimize" else -current[0]
				g_elevations[current_node] = current[1]
				distances[current_node] = current[2]
				previous_nodes[current_node] = current[4]

			#we've found a complete path, stop searching this path
			if current_node == end:
				continue

			visited.add(current_node)
	
			for edge in graph.edges(current_node, data=True):
				next_node = edge[1]

				#avoid self loops
				if next_node == current_node:
					continue

				g_elevation_to_next_node = super(RoutingAStar, self).get_elevation_diff(graph, current_node, next_node)
				g_total_new_elevation = g_elevations[current_node] + g_elevation_to_next_node

				distance_to_next_node = graph[current_node][next_node][0]["length"]
				total_new_distance = distances[current_node] + distance_to_next_node

				heuristic = super(RoutingAStar, self).get_elevation_diff(graph, next_node, end)

				#if the total distance is greater than max length, this is an invalid path
				if total_new_distance <= max_length and next_node not in visited:
					if elevation_setting == "maximize":
						heapq.heappush(queue, (-g_total_new_elevation - heuristic, g_total_new_elevation, total_new_distance, next_node, current_node))
					elif elevation_setting == "minimize":
						heapq.heappush(queue, (g_total_new_elevation + heuristic, g_total_new_elevation, total_new_distance, next_node, current_node))
					else:
						heapq.heappush(queue, (0, 0, total_new_distance, next_node, current_node))

		return super(RoutingAStar, self).get_path_from_previous_nodes(previous_nodes, start, end)

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

class RoutingDFS(RoutingMode):
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
						return super(RoutingDFS, self).get_path_from_previous_nodes(previous_nodes, start, end)
	
		return None