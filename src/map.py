import osmnx
import pickle as pkl
import networkx as nx
import requests

def get_map_data(place_query):
	transport_methods = ["drive", "bike", "walk"]
	for transport_method in transport_methods:
		graph = osmnx.graph_from_place(place_query, network_type="drive")
		add_elevation_data(graph)
		filename = "cached_maps/{}-{}.pkl".format(place_query["city"].lower(), transport_method)
		pkl.dump(graph, open(filename, "wb"))

def add_elevation_data(graph):
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

	
#get map data for Boulder
get_map_data({"city": "Boulder", "state": "Colorado", "country": "USA"})

# to load cached map
# with open("Boulder-drive.pkl", 'rb') as file:
# 		graph = pkl.load(file)
# 		print(list(graph.nodes(data=True)))
