import osmnx
import heapq
import pickle as pkl

def dijkstra(graph, start, end, x=0, elevation_setting=None):
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

	heapq.heappush(queue, (0, 0, start, None))
	distances[start] = 0
	elevations[start] = 0
	previous_nodes[start] = None

	visited = set()

	max_length = find_max_length(graph, x, start, end)
	if max_length == -1:
		return None

	while queue:
		current = heapq.heappop(queue)
		current_node = current[2]

		if current_node not in elevations or (elevation_setting == "maximize" and elevations[current_node] < -current[0]) or (elevation_setting == "minimize" and elevations[current_node] > current[0]):
			elevations[current_node] = current[0] if elevation_setting == "minimize" else -current[0]
			distances[current_node] = current[1]
			previous_nodes[current_node] = current[3]

		if current_node == end:
			continue

		visited.add(current_node)

		for edge in graph.edges(current_node, data=True):
			next_node = edge[1]
			if next_node == current_node:
				continue
			distance_to_next_node = graph[current_node][next_node][0]["length"]
			total_new_distance = distances[current_node] + distance_to_next_node	

			elevation_to_next_node = get_elevation_diff(graph, current_node, next_node) 
			total_elevation = elevations[current_node]
			if elevation_to_next_node > 0:
				total_elevation += elevation_to_next_node

			if total_new_distance <= max_length and next_node not in visited:
				if elevation_setting == "maximize":
					heapq.heappush(queue, (-total_elevation, total_new_distance, next_node, current_node))
				elif elevation_setting == "minimize":
					heapq.heappush(queue, (total_elevation, total_new_distance, next_node, current_node))
				else:
					heapq.heappush(queue, (0, total_new_distance, next_node, current_node))

	return get_path_from_previous_nodes(previous_nodes, start, end)

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

	visited = set()
	max_length = find_max_length(graph, x, start, end)
	if max_length == -1:
		return None

	while queue:
		current_node = heapq.heappop(queue)[2]
		visited.add(current_node)
		
		if current_node == end and f_distances[current_node] <= max_length:
				break
		for edge in graph.edges(current_node, data=True):
			next_node = edge[1]
			temp_g_distance_to_next_node = graph[current_node][next_node][0]["length"]
			elevation_to_next_node = graph.nodes[next_node]["elevation"] - graph.nodes[current_node]["elevation"]
			temp_g_total_new_distance = g_distances[current_node] + temp_g_distance_to_next_node
			temp_g_total_old_distance = float("inf") if next_node not in g_distances else g_distances[next_node]
			if temp_g_total_new_distance <= max_length and next_node not in visited:
				elevations[next_node] = elevations[current_node]
				if elevation_to_next_node > 0:
					elevations[next_node] += elevation_to_next_node
				g_distances[next_node] = temp_g_total_new_distance
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

def bfs(graph, start, end):
    """
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

def dfs(graph, start, end):
    """
        Runs DFS path algorithm from start to end location to find shortest path

        params:
            graph: networkx multidigraph - the area we are searching in
		    start: int - the starting location of the route
		    end: int - the end location of the route

        return: list - a route from start to end or None if a route does not exist
    """
        
    stack = []
    visited = []
    previous_nodes = {}

    stack.append(start)
    visited.append(start)
    previous_nodes[start] = None

    while (len(stack) > 0):
        current_node = stack.pop()

        for edge in graph.edges(current_node, data=True):
            next_node = edge[1]

            if next_node not in visited:
                stack.append(next_node)
                visited.add(next_node)
                previous_nodes[next_node] = current_node

                if next_node == end:
                    return get_path_from_previous_nodes(previous_nodes, start, end)
    
    return None


def find_max_length(graph, x, start, end):
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

	max_length = (1 + (float(x)/100)) * get_total_path_length(shortest_path, graph)
	return max_length

def get_elevation_diff(graph, node1, node2):
	"""
	Finds the elevation difference between two nodes.

	params:
		graph: networkx multidigraph - the area we are searching in
		node1: int
		node2: int

	return: float
	"""
	return graph.nodes[node2]["elevation"] - graph.nodes[node1]["elevation"]

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
		elevation += max(0, graph.nodes[nodes[i+1]]["elevation"] - graph.nodes[nodes[i]]["elevation"])

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
