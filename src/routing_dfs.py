import osmnx

def dfs(graph, start, end, x, elevation_setting=None):
    """
        Runs DFS path algorithm from start to end location to find shortest path

        params:
            graph: networkx multidigraph - the area we are searching in
		    start: int - the starting location of the route
		    end: int - the end location of the route
		    x: int - the percentage we can deviate from the shortest path length
		    elevation_setting: string - either "maximize", "minimize", or None

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