import osmnx
import pickle as pkl
import networkx as nx
import requests
import sys

def download_map(place_query):
	"""
	Downloads a map for the specified location from the OSM API. Elevation data for each node in the map (networkx.MultiDiGraph)
	is added from the Open Elevation API. Each edge has stores length (in meters) from node1 to node2.
	This graph is stored in a pickle file in `/cached_maps`. 

	params: 
		place_query: dict of city, state, country
	"""
	transport_methods = ["drive", "bike", "walk"]
	try:
		for transport_method in transport_methods:
			graph = osmnx.graph_from_place(place_query, network_type=transport_method)
			add_elevation_data(graph)
			filename = "cached_maps/{}-{}.pkl".format(place_query["city"].lower(), transport_method)
			pkl.dump(graph, open(filename, "wb"))
	except ValueError:
		print("No results for the specified location.")

def add_elevation_data(graph):
	"""
	Adds elevation data for each node in `graph` using the Open Elevation API. 
	
	params:
		graph: networkx.MultiDiGraph where each node contains latitude and longitude data

	return: graph where nodes contain latitude, longitude, and elevation data
	"""
	max_batch_size = 100

	nodes_data = list(graph.nodes(data=True))

	results = {}

	api = "https://api.open-elevation.com/api/v1/lookup"
	elevation_results = []
	for i in range(0, len(nodes_data), max_batch_size):
		locations = []
		node_ids = []
		for j in range(i, i + max_batch_size):
			if j >= len(nodes_data):
				break
			locations.append({"latitude": nodes_data[j][1]["y"], "longitude": nodes_data[j][1]["x"]})
			node_ids.append(nodes_data[j][0])

		node_elevation_data = requests.post(api, json={"locations": locations}).json()["results"]

		for j in range(len(node_elevation_data)):
			node = node_elevation_data[j]
			results[node_ids[j]] = node["elevation"]

	nx.set_node_attributes(graph, name="elevation", values=results)

	return graph

if __name__ == '__main__':
	if len(sys.argv) != 4:
		print("Expected: python src/map.py <city> <state> <country>")
		exit()

	location = {"city": sys.argv[1], "state": sys.argv[2], "country": sys.argv[3]}

	download_map(location)
