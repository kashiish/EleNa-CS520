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
		assert path_elevation == 13

	def test_get_path_length(self, small_test_graph):
		path = [1, 0, 4]
		path_length = routing.get_total_path_length(path, small_test_graph)
		assert path_length == 25

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

	def test_small_shortest_path(self, small_test_graph):
		start_node = 1
		end_node = 4

		shortest_path = osmnx.distance.shortest_path(small_test_graph, start_node, end_node)
		dijkstra_path = routing.dijkstra(small_test_graph, start_node, end_node)

		shortest_length = routing.get_total_path_length(shortest_path, small_test_graph)
		dijkstra_length = routing.get_total_path_length(dijkstra_path, small_test_graph)

		assert shortest_length == dijkstra_length
		assert shortest_path == dijkstra_path

	def test_small_no_path(self, small_test_nonuniform_graph):
		start_node = 1
		end_node = 2
		shortest_path = osmnx.distance.shortest_path(small_test_nonuniform_graph, start_node, end_node)
		dijkstra_path = routing.dijkstra(small_test_nonuniform_graph, start_node, end_node)
		assert dijkstra_path == None
		assert shortest_path == None

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

		for i in range(5):
			labels[i] = i


		print(list(graph.nodes(data=True)))

		nx.draw(graph, positions)
		nx.draw_networkx_labels(graph, positions, labels, font_size=10)
		nx.draw_networkx_edge_labels(graph, positions, font_size=5)
		plt.show()

show_graph("test-small-graph2.pkl")
