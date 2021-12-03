from abc import ABC, abstractmethod
import osmnx

class RoutingMode(ABC):
	"""
		RoutingMode interface defines actions that will be used by all the routing modes, but implemented with different behavior. It will also have the shared operations that will be used across all routings.

		The Context class can use this routing strategy. 

		Cite: https://www.tutorialspoint.com/design_pattern/strategy_pattern.html
	"""

	def __init__(self, graph, start, end, x, elevation_setting):
		self.graph = graph
		self.start = start
		self.end = end
		self.x = x
		self.elevation_setting = elevation_setting

	def find_max_length(self, graph, x, start, end):
		"""
		Uses the osmnx API to find the shortest possible route from start to end node and multiplies
		this number by x to find the longest possible route we can create. Returns -1 if no possible
		path exists. 

		params:
			graph: networkx multidigraph - the area we are searching in
			x: float, the percentage we can deviate from the shortest path length
			start: int - the starting location of the route
			end: int - the end location of the route

		return: float, length of the longest possible route

		"""
		shortest_path = osmnx.distance.shortest_path(graph, start, end)
		if shortest_path is None:
			return -1

		max_length = (1 + (float(x)/100)) * self.get_total_path_length(shortest_path, graph)
		return max_length

	def get_elevation_diff(self, graph, node1, node2):
		"""
		Finds the elevation difference between two nodes.

		params:
			graph: networkx multidigraph - the area we are searching in
			node1: int
			node2: int

		return: float
		"""
		return max(0, graph.nodes[node2]["elevation"] - graph.nodes[node1]["elevation"])

	def get_path_elevation(self, nodes, graph):
		"""
		Calculates the total elevation gain of the path containing `nodes`.
	
		params:
			nodes: list of ints (node IDs)
			graph: networkx multidigraph - the area we are searching in, contains `nodes`

		return: int, the total elevation from start to end node in the path
		"""
		elevation = 0

		for i in range(len(nodes)-1):
			elevation += max(0, graph.nodes[nodes[i+1]]["elevation"] - graph.nodes[nodes[i]]["elevation"])

		return elevation

	def get_total_path_length(self, nodes, graph):
		"""
		Calculates the total length of the path containing `nodes`. 

		params:
			nodes: list of ints (node IDs)
			graph: networkx multidigraph - the area we are searching in, contains `nodes`

		return: int, the total distance from start to end node in the path
		"""
		distance = 0

		for i in range(len(nodes)-1):
			distance += graph.edges[nodes[i], nodes[i+1], 0]['length']
		return distance

	def get_path_from_previous_nodes(self, previous_nodes, start, end):
		"""
		Returns a list of the path using `previous_nodes` (specific to Dijkstra).

		params:
			previous_nodes: dict, key is a node ID and value is the ID of node that points to the key node in this path
			start: int, node ID
			end: int, node ID

			return: list of ints, the complete path from start to end node
		"""
		path = [end]

		current_node = end
		while current_node != start:
			current_node = previous_nodes[current_node]
			path.append(current_node)
		path.reverse()
		#print(path)
		return path

	@abstractmethod
	def routing_action(self, graph, start, end, x, elevation_setting):
		pass
