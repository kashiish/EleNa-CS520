import pickle as pkl
import networkx as nx
import matplotlib.pyplot as plt
import pytest
import osmnx

import sys
sys.path.insert(0, '.')
from src import routing

@pytest.fixture(scope="session")
def small_test_graph():
	with open("cached_maps/test-small-uniform-graph.pkl", "rb") as file:
		graph = pkl.load(file)
		return graph

@pytest.fixture(scope="session")
def small_test_nonuniform_graph():
	with open("cached_maps/test-small-nonuniform-graph.pkl", "rb") as file:
		graph = pkl.load(file)
		return graph

@pytest.fixture(scope="session")
def medium_test_graph():
	with open("cached_maps/test-medium-graph.pkl", "rb") as file:
		graph = pkl.load(file)
		return graph

class TestUtils:
	def test_get_path_elevation(self, small_test_graph):
		path = [1, 0, 4]
		path_elevation = routing.get_path_elevation(path, small_test_graph)
		expected_path_elevation = 13
		assert path_elevation == expected_path_elevation

	def test_get_path_length(self, small_test_graph):
		path = [1, 0, 4]
		path_length = routing.get_total_path_length(path, small_test_graph)
		expected_path_length = 25
		assert path_length == expected_path_length

	def test_get_path_from_previous_nodes(self):
		expected_path = [1, 0, 4]
		previous_nodes = {1: None, 0: 1, 4: 0, 2: 0}
		path = routing.get_path_from_previous_nodes(previous_nodes, 1, 4)
		assert path == expected_path

	def test_find_max_length(self, small_test_graph):
		x = 50
		start = 1
		end = 4

		max_length = routing.find_max_length(small_test_graph, x, start, end)
		expected_max_length = 10.5
		assert max_length == expected_max_length

class TestDijkstra:
	def test_small_min_elevation(self, small_test_graph):
		start_node = 3
		end_node = 4

		x = 50

		elevation_setting = "minimize"

		shortest_path = osmnx.distance.shortest_path(small_test_graph, start_node, end_node)
		dijkstra_path = routing.dijkstra(small_test_graph, start_node, end_node, x, elevation_setting)

		shortest_path_elevation = routing.get_path_elevation(shortest_path, small_test_graph)
		dijkstra_path_elevation = routing.get_path_elevation(dijkstra_path, small_test_graph)

		max_length = routing.find_max_length(small_test_graph, x, start_node, end_node)
		dijkstra_length = routing.get_total_path_length(dijkstra_path, small_test_graph)

		assert dijkstra_path_elevation < shortest_path_elevation
		assert dijkstra_length <= max_length

	def test_medium_min_elevation(self, medium_test_graph):
		start_node = 0
		end_node = 2

		x = 50

		elevation_setting = "minimize"

		shortest_path = osmnx.distance.shortest_path(medium_test_graph, start_node, end_node)
		dijkstra_path = routing.dijkstra(medium_test_graph, start_node, end_node, x, elevation_setting)

		shortest_path_elevation = routing.get_path_elevation(shortest_path, medium_test_graph)
		dijkstra_path_elevation = routing.get_path_elevation(dijkstra_path, medium_test_graph)
		
		max_length = routing.find_max_length(medium_test_graph, x, start_node, end_node)
		dijkstra_length = routing.get_total_path_length(dijkstra_path, medium_test_graph)
		
		assert dijkstra_path_elevation < shortest_path_elevation
		assert dijkstra_length <= max_length

	def test_small_max_elevation(self, small_test_graph):
		start_node = 1
		end_node = 4

		x = 400 #for testing purposes, find a path that is at max 400% longer than the shortest path

		elevation_setting = "maximize"

		shortest_path = osmnx.distance.shortest_path(small_test_graph, start_node, end_node)
		dijkstra_path = routing.dijkstra(small_test_graph, start_node, end_node, x, elevation_setting)

		shortest_path_elevation = routing.get_path_elevation(shortest_path, small_test_graph)
		dijkstra_path_elevation = routing.get_path_elevation(dijkstra_path, small_test_graph)

		max_length = routing.find_max_length(small_test_graph, x, start_node, end_node)
		dijkstra_length = routing.get_total_path_length(dijkstra_path, small_test_graph)

		assert dijkstra_path_elevation > shortest_path_elevation
		assert dijkstra_length <= max_length

	def test_medium_max_elevation(self, medium_test_graph):
		start_node = 0
		end_node = 2

		x = 75

		elevation_setting = "maximize"

		shortest_path = osmnx.distance.shortest_path(medium_test_graph, start_node, end_node)
		dijkstra_path = routing.dijkstra(medium_test_graph, start_node, end_node, x, elevation_setting)

		shortest_path_elevation = routing.get_path_elevation(shortest_path, medium_test_graph)
		dijkstra_path_elevation = routing.get_path_elevation(dijkstra_path, medium_test_graph)

		max_length = routing.find_max_length(medium_test_graph, x, start_node, end_node)
		dijkstra_length = routing.get_total_path_length(dijkstra_path, medium_test_graph)

		assert dijkstra_path_elevation > shortest_path_elevation
		assert dijkstra_length <= max_length

	def test_small_shortest_path(self, small_test_graph):
		start_node = 1
		end_node = 4

		shortest_path = osmnx.distance.shortest_path(small_test_graph, start_node, end_node)
		dijkstra_path = routing.dijkstra(small_test_graph, start_node, end_node)

		shortest_length = routing.get_total_path_length(shortest_path, small_test_graph)
		dijkstra_length = routing.get_total_path_length(dijkstra_path, small_test_graph)

		assert shortest_length == dijkstra_length
		assert shortest_path == dijkstra_path

	def test_medium_shortest_path(small, medium_test_graph):
		start_node = 0
		end_node = 2

		shortest_path = osmnx.distance.shortest_path(medium_test_graph, start_node, end_node)
		dijkstra_path = routing.dijkstra(medium_test_graph, start_node, end_node)

		shortest_length = routing.get_total_path_length(shortest_path, medium_test_graph)
		dijkstra_length = routing.get_total_path_length(dijkstra_path, medium_test_graph)

		assert shortest_length == dijkstra_length
		assert shortest_path == dijkstra_path

	def test_small_no_path(self, small_test_nonuniform_graph):
		start_node = 1
		end_node = 2
		shortest_path = osmnx.distance.shortest_path(small_test_nonuniform_graph, start_node, end_node)
		dijkstra_path = routing.dijkstra(small_test_nonuniform_graph, start_node, end_node)
		assert shortest_path == None
		assert dijkstra_path == None

class TestAStar:
	def test_small_min_elevation(self, small_test_graph):
		start_node = 3
		end_node = 4

		x = 50

		elevation_setting = "minimize"

		shortest_path = osmnx.distance.shortest_path(small_test_graph, start_node, end_node)
		a_star_path = routing.a_star(small_test_graph, start_node, end_node, x, elevation_setting)

		shortest_path_elevation = routing.get_path_elevation(shortest_path, small_test_graph)
		a_star_path_elevation = routing.get_path_elevation(a_star_path, small_test_graph)

		max_length = routing.find_max_length(small_test_graph, x, start_node, end_node)
		a_star_length = routing.get_total_path_length(a_star_path, small_test_graph)

		assert a_star_path_elevation < shortest_path_elevation
		assert a_star_length <= max_length

	def test_medium_min_elevation(self, medium_test_graph):
		start_node = 0
		end_node = 2

		x = 50

		elevation_setting = "minimize"

		shortest_path = osmnx.distance.shortest_path(medium_test_graph, start_node, end_node)
		a_star_path = routing.a_star(medium_test_graph, start_node, end_node, x, elevation_setting)

		shortest_path_elevation = routing.get_path_elevation(shortest_path, medium_test_graph)
		a_star_path_elevation = routing.get_path_elevation(a_star_path, medium_test_graph)

		max_length = routing.find_max_length(medium_test_graph, x, start_node, end_node)
		a_star_length = routing.get_total_path_length(a_star_path, medium_test_graph)

		assert a_star_path_elevation < shortest_path_elevation
		assert a_star_length <= max_length

	def test_small_max_elevation(self, small_test_graph):
		start_node = 1
		end_node = 4

		x = 400 #for testing purposes, find a path that is at max 400% longer than the shortest path

		elevation_setting = "maximize"

		shortest_path = osmnx.distance.shortest_path(small_test_graph, start_node, end_node)
		a_star_path = routing.a_star(small_test_graph, start_node, end_node, x, elevation_setting)

		shortest_path_elevation = routing.get_path_elevation(shortest_path, small_test_graph)
		a_star_path_elevation = routing.get_path_elevation(a_star_path, small_test_graph)

		max_length = routing.find_max_length(small_test_graph, x, start_node, end_node)
		a_star_length = routing.get_total_path_length(a_star_path, small_test_graph)

		assert a_star_path_elevation > shortest_path_elevation
		assert a_star_length <= max_length

	def test_medium_max_elevation(self, medium_test_graph):
		start_node = 0
		end_node = 2

		x = 75

		elevation_setting = "maximize"

		shortest_path = osmnx.distance.shortest_path(medium_test_graph, start_node, end_node)
		a_star_path = routing.a_star(medium_test_graph, start_node, end_node, x, elevation_setting)

		shortest_path_elevation = routing.get_path_elevation(shortest_path, medium_test_graph)
		a_star_path_elevation = routing.get_path_elevation(a_star_path, medium_test_graph)

		max_length = routing.find_max_length(medium_test_graph, x, start_node, end_node)
		a_star_length = routing.get_total_path_length(a_star_path, medium_test_graph)

		assert a_star_path_elevation > shortest_path_elevation
		assert a_star_length <= max_length

	def test_small_shortest_path(self, small_test_graph):
		start_node = 1
		end_node = 4

		shortest_path = osmnx.distance.shortest_path(small_test_graph, start_node, end_node)
		a_star_path = routing.a_star(small_test_graph, start_node, end_node)

		shortest_length = routing.get_total_path_length(shortest_path, small_test_graph)
		a_star_length = routing.get_total_path_length(a_star_path, small_test_graph)

		assert shortest_length == a_star_length
		assert shortest_path == a_star_path

	def test_medium_shortest_path(small, medium_test_graph):
		start_node = 0
		end_node = 2

		shortest_path = osmnx.distance.shortest_path(medium_test_graph, start_node, end_node)
		a_star_path = routing.a_star(medium_test_graph, start_node, end_node)

		shortest_length = routing.get_total_path_length(shortest_path, medium_test_graph)
		a_star_length = routing.get_total_path_length(a_star_path, medium_test_graph)

		assert shortest_length == a_star_length
		assert shortest_path == a_star_path

	def test_small_no_path(self, small_test_nonuniform_graph):
		start_node = 1
		end_node = 2
		shortest_path = osmnx.distance.shortest_path(small_test_nonuniform_graph, start_node, end_node)
		a_star_path = routing.a_star(small_test_nonuniform_graph, start_node, end_node)
		
		assert shortest_path == None
		assert a_star_path == None

# class TestBFS:
# 	def test_small_graph(self, small_test_graph):
# 		start_node = 1
# 		end_node = 4

# 		shortest_path = osmnx.distance.shortest_path(small_test_graph, start_node, end_node)
# 		bfs_path = routing.bfs(small_test_graph, start_node, end_node)

# 		print("shortest path", shortest_path)
# 		print("bfs path", bfs_path)

# 		shortest_length = routing.get_total_path_length(shortest_path, small_test_graph)
# 		bfs_length = routing.get_total_path_length(bfs_path, small_test_graph)

# 		print("shortest length", shortest_length)
# 		print("bfs length", bfs_length)

# 		assert shortest_length == bfs_length

# 	def test_medium_graph(self, medium_test_graph):
# 		start_node = 0
# 		end_node = 2

# 		shortest_path = osmnx.distance.shortest_path(medium_test_graph, start_node, end_node)
# 		bfs_path = routing.bfs(medium_test_graph, start_node, end_node)

# 		print("shortest path", shortest_path)
# 		print("bfs path", bfs_path)

# 		shortest_length = routing.get_total_path_length(shortest_path, medium_test_graph)
# 		bfs_length = routing.get_total_path_length(bfs_path, medium_test_graph)

# 		print("shortest length", shortest_length)
# 		print("bfs length", bfs_length)

# 		assert shortest_length == bfs_length

# 	def test_small_no_path(self, small_test_nonuniform_graph):
# 		start_node = 1
# 		end_node = 2

# 		shortest_path = osmnx.distance.shortest_path(small_test_nonuniform_graph, start_node, end_node)
# 		bfs_path = routing.bfs(small_test_nonuniform_graph, start_node, end_node)
		
# 		assert shortest_path == None
# 		assert bfs_path == None

class TestDFS:
	def test_small_graph(self, small_test_graph):
		start_node = 1
		end_node = 4
		x = 40

		shortest_path = osmnx.distance.shortest_path(small_test_graph, start_node, end_node)
		dfs_path = routing.dfs(small_test_graph, start_node, end_node,x)

		
		print("shortest path", shortest_path)
		print("dfs path", dfs_path)
		assert(False)
# 		shortest_length = routing.get_total_path_length(shortest_path, small_test_graph)
# 		dfs_length = routing.get_total_path_length(dfs_path, small_test_graph)

# 		print("shortest length", shortest_length)
# 		print("dfs length", dfs_length)

# 		assert shortest_length == dfs_length

# 	def test_medium_graph(self, medium_test_graph):
# 		start_node = 0
# 		end_node = 2

# 		shortest_path = osmnx.distance.shortest_path(medium_test_graph, start_node, end_node)
# 		dfs_path = routing.dfs(medium_test_graph, start_node, end_node)

# 		print("shortest path", shortest_path)
# 		print("dfs path", dfs_path)

# 		shortest_length = routing.get_total_path_length(shortest_path, medium_test_graph)
# 		dfs_length = routing.get_total_path_length(dfs_path, medium_test_graph)

# 		print("shortest length", shortest_length)
# 		print("dfs length", dfs_length)

# 		assert shortest_length == dfs_length

# 	def test_small_no_path(self, small_test_nonuniform_graph):
# 		start_node = 1
# 		end_node = 2
		
# 		shortest_path = osmnx.distance.shortest_path(small_test_nonuniform_graph, start_node, end_node)
# 		dfs_path = routing.dfs(small_test_nonuniform_graph, start_node, end_node)
		
# 		assert shortest_path == None
# 		assert dfs_path == None
	


def show_graph(graph_name):
	with open("cached_maps/{}".format(graph_name), 'rb') as file:
		graph = pkl.load(file)
		positions = {}
		labels = {}

		for node in list(graph.nodes(data=True)):
			xy = []

			xy.append(node[1]['x'])
			xy.append(node[1]['y'])

			positions[int(node[0])] = xy

		for i in range(len(list(graph.nodes))):
			labels[i] = i


		print(list(graph.nodes(data=True)))

		nx.draw(graph, positions)
		nx.draw_networkx_labels(graph, positions, labels, font_size=10)
		nx.draw_networkx_edge_labels(graph, positions, font_size=5)
		plt.show()

# show_graph("test-small-uniform-graph.pkl")
