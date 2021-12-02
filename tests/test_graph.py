import random
import networkx as nx
import matplotlib.pyplot as plt
import pickle as pkl
import math

# The following code has been inspired from the networkx documentation: https://networkx.org/documentation/stable/auto_examples/drawing/plot_directed.html
def make_small_uniform_graph():
	random.seed(15)
	graph = nx.generators.directed.random_uniform_k_out_graph(5, 3, seed=5)
	positions = nx.layout.spring_layout(graph, seed=15) 
	marked = {}
	for node in graph.nodes:
		graph.nodes[node]["x"] = positions[node][0] * 10
		graph.nodes[node]["y"] = positions[node][1] * 10
		graph.nodes[node]["elevation"] = random.randint(10, 50)
		remove_duplicate_edges_for_node(graph, node)

	for path in graph.edges():
		first_node = graph.nodes[path[0]]
		second_node = graph.nodes[path[1]]
		graph.edges[path[0], path[1], 0]["length"] = int(math.dist([first_node["x"], first_node["y"]], [second_node["x"], second_node["y"]]))
		graph.edges[path[0], path[1], 0]["elevation_diff"] = int(second_node["elevation"] - first_node["elevation"])

	for node in graph.nodes:
			marked[node] = node

	filename = "cached_maps/test-small-uniform-graph.pkl"
	pkl.dump(graph, open(filename, "wb"))

def make_small_nonuniform_graph():
	random.seed(15)
	graph = nx.generators.directed.random_k_out_graph(5, 3, 0.3, self_loops=False, seed=5)
	positions = nx.layout.spring_layout(graph, seed=15) 
	marked = {}
	for node in graph.nodes:
		graph.nodes[node]["x"] = positions[node][0] * 10
		graph.nodes[node]["y"] = positions[node][1] * 10
		graph.nodes[node]["elevation"] = random.randint(10, 50)
		remove_duplicate_edges_for_node(graph, node)

	for path in graph.edges():
		first_node = graph.nodes[path[0]]
		second_node = graph.nodes[path[1]]
		graph.edges[path[0], path[1], 0]["length"] = int(math.dist([first_node["x"], first_node["y"]], [second_node["x"], second_node["y"]]))
		graph.edges[path[0], path[1], 0]["elevation_diff"] = int(second_node["elevation"] - first_node["elevation"])

	for node in graph.nodes:
			marked[node] = node

	filename = "cached_maps/test-small-nonuniform-graph.pkl"
	pkl.dump(graph, open(filename, "wb"))

def make_medium_graph():
	random.seed(15)
	graph = nx.generators.directed.random_uniform_k_out_graph(15, 5, seed=5)
	positions = nx.layout.spring_layout(graph, seed=15) 
	marked = {}

	for node in graph.nodes:
		graph.nodes[node]["x"] = positions[node][0] * 10
		graph.nodes[node]["y"] = positions[node][1] * 10
		graph.nodes[node]["elevation"] = random.randint(20, 200)
		remove_duplicate_edges_for_node(graph, node)

	for path in graph.edges():
		first_node = graph.nodes[path[0]]
		second_node = graph.nodes[path[1]]
		graph.edges[path[0], path[1], 0]["length"] = int(math.dist([first_node["x"], first_node["y"]], [second_node["x"], second_node["y"]]))
		graph.edges[path[0], path[1], 0]["elevation_diff"] = int(second_node["elevation"] - first_node["elevation"])

	for node in graph.nodes:
		marked[node] = node

	filename = "cached_maps/test-medium-graph.pkl"
	pkl.dump(graph, open(filename, "wb"))


def remove_duplicate_edges_for_node(graph, node):
	duplicates = []
	incoming = {}
	outgoing = {}
	for path in graph.in_edges(node):
		if path not in incoming:
			incoming[path] = True
		else:
			duplicates.append(path)

	for path in graph.out_edges(node):
		if path not in outgoing:
			outgoing[path] = True
		else:
			duplicates.append(path)

	for path in duplicates:
		graph.remove_edge(path[0], path[1])


# if __name__ == "__main__":
		# make_small_uniform_graph()
		# make_small_nonuniform_graph()
		# make_medium_graph()
