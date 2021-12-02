import osmnx
import routing
import pickle as pkl
import networkx as nx
import matplotlib.pyplot as plt


class App:
	def __init__(self):
		self.start_address = ""
		self.end_address = ""
		self.elevation_gain_mode = None
		self.x = None
		self.transportation_mode = None
		self.graph = None
		self.TRANSPORTATION_MODES = ["drive", "walk", "bike"]
		self.ELEVATION_MODES = ["maximize", "minimize", ""]
		self.ROUTING_METHODS = ["dijkstra", "a*"]
		self.start = None
		self.end = None
		self.routing_method = None

	def set_user_inputs(self):
		self.start_address = input("Enter the address of your start location: ")
		self.end_address = input("Enter the address of your end location: ")
		self.routing_method = input("Enter the routing algorithm you would like to use (Dijkstra, A*): ").lower()

		while self.routing_method not in self.ROUTING_METHODS:
			self.routing_method = input("Enter the routing algorithm you would like to use (Dijkstra, A*): ").lower()

		self.elevation_gain_mode = input("Type 'maximize' if you want to maximize elevation gain, or 'minimize' if you want to minimize elevation gain (no quotes), or press enter to skip & to get the shortest route: ")
		while self.elevation_gain_mode not in self.ELEVATION_MODES:
			self.elevation_gain_mode = input("Please enter a valid option between maximize, minimize, or enter to skip and get shortest route: ")
		
		self.x = input("Enter what (x) percentage of shortest path you're able to additionally travel: ")

		flag = True

		while flag:
			try:
				x_as_float = float(self.x)
				flag = False
			except ValueError:
				self.x = input("Please enter a valid float number for x percentage: ")
		
		self.transportation_mode = input("Enter one of the following options for your preferred mode of transportation: drive, walk, bike: ").lower()

		while self.transportation_mode not in self.TRANSPORTATION_MODES:
			self.transportation_mode = input("Please enter a valid option between drive, walk, bike: ")

	def set_graph(self):
		with open("cached_maps/boulder-{}.pkl".format(self.transportation_mode), "rb") as file:
				self.graph = pkl.load(file)
		
	def set_start_end_nodes(self):
		start_latitude_longitude = osmnx.geocoder.geocode(self.start_address)
		self.start = osmnx.distance.nearest_nodes(self.graph, start_latitude_longitude[1], start_latitude_longitude[0])
		
		end_latitude_longitude = osmnx.geocoder.geocode(self.end_address)
		self.end = osmnx.distance.nearest_nodes(self.graph, end_latitude_longitude[1], end_latitude_longitude[0])

	def find_route(self):
		if self.routing_method == "dijkstra":
			return routing.dijkstra(self.graph, self.start, self.end, self.x, self.elevation_gain_mode)
		elif self.routing_method == "a*":
			return routing.a_star(self.graph, self.start, self.end, self.x, self.elevation_gain_mode)
		elif self.routing_method == "bfs":
			return routing.bfs(self.graph, self.start, self.end)
		elif self.routing_method  == "dfs":
			return routing.dfs(self.graph, self.start, self.end)
		else:
			print("Invalid routing method selected.")
			return None

	def display_path(self, path):
		positions = {}

		for node in list(self.graph.nodes(data=True)):
			xy = []

			xy.append(node[1]['x'])
			xy.append(node[1]['y'])

			positions[int(node[0])] = xy

		h = self.graph.subgraph(path)
		nx.draw_networkx_nodes(h,pos=positions, node_color='b', node_size=5) #or even nx.draw(h,pos=pos,node_color='b') to get nodes and edges in one command
		nx.draw_networkx_edges(h,pos=positions)
		plt.axis('equal')
		plt.show() 

def main():
	app = App()
	app.set_user_inputs()
	app.set_graph()
	app.set_start_end_nodes()
	path = app.find_route()
	app.display_path(path)

if __name__ == '__main__':
	main()
