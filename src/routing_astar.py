import osmnx
import heapq

def find_max_length(graph, start, end):
	shortest_path = osmnx.distance.shortest_path(graph, start, end)
	if shortest_path is None:
		return None

	max_length = (1 + (x/100)) + get_total_path_length(shortest_path, graph)
	return max_length

def get_elevation_diff(graph, start, end):
	return graph.nodes[start]["elevation"] - graph.nodes[end]["elevation"]

def a_star(graph, start, end, x, elevation_setting=None):
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
	heuristic = 0
	g_distances = {}
	f_distances = {}
	elevations = {}
	previous_nodes = {}

	#priority = distance + elevation diff between nodes
	queue = []

	heapq.heappush(queue, (0, 0, start))
	g_distances[start] = 0 # ordinary distance
	f_distances[start] = 0 # addition of heuristic
	elevations[start] = 0
	previous_nodes[start] = None

	max_length = find_max_length(graph, start, end)

	#no visited set in case we need to backtrack

	while queue:
		current_node = heapq.heappop(queue)[2]
		
		if current_node == end and f_distances[current_node] <= max_length:
				break
		for edge in graph.edges(current_node, data=True):
			next_node = edge[1]
			temp_g_distance_to_next_node = graph[current_node][next_node][0]["length"]
			elevation_to_next_node = graph.nodes[next_node]["elevation"] - graph.nodes[current_node]["elevation"]
			temp_g_total_new_distance = g_distances[current_node] + temp_g_distance_to_next_node
			temp_g_total_old_distance = float("inf") if next_node not in g_distances else g_distances[next_node]
			if temp_g_total_new_distance <= max_length and temp_g_total_new_distance < temp_g_total_old_distance:
				elevations[next_node] = elevation_to_next_node + elevations[current_node]
				g_distances[next_node] = total_new_distance
				heuristic = get_elevation_diff(graph, next_node, end)
				f_distances[next_node] = temp_g_total_new_distance + heuristic
				
				if elevation_setting == "maximize":
					heapq.heappush(queue, (f_distances[next_node], -elevations[next_node], next_node))
				elif elevation_setting == "minimize":
					heapq.heappush(queue, (f_distances[next_node], elevations[next_node], next_node))
				else:
					heapq.heappush(queue, (g_distances[next_node], next_node))

				previous_nodes[next_node] = current_node
	return get_path_from_previous_nodes(previous_nodes, start, end)

def get_path_elevation(nodes, graph):
	"""
	Calculates the total elevation gain of the path containing `nodes`.
	
	params:
		nodes: list of ints (node IDs)
		graph: networkx multidigraph - the area we are searching in, contains `nodes`
	return: int, the total elevation from start to end node in the path
	"""
	elevation = 0

	for i in range(len(nodes)-1):
		elevation += graph.nodes[nodes[i+1]]["elevation"] - graph.nodes[nodes[i]]["elevation"]

	return elevation

def get_total_path_length(nodes, graph):
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


def get_path_from_previous_nodes(previous_nodes, start, end):
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
	return path

