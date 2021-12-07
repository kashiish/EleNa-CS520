import osmnx
import pickle as pkl
from context import Context
from routing_actions import RoutingDijkstra, RoutingAStar, RoutingBFS, RoutingDFS
from routing_helper import RoutingHelper
import tkinter as tk
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
		self.ROUTING_METHODS = ["dijkstra", "a*"]
		self.TRANSPORTATION_MODES = ["drive", "walk", "bike"]
		self.ELEVATION_MODES = ["maximize", "minimize", ""]
		self.ROUTING_METHODS = ["dijkstra", "a*"]
		self.start = None
		self.end = None
		self.routing_method = None

	def set_user_inputs(self):
		self.start_address = ""

		while not self.start_address:
			self.start_address = input("Enter the address of your start location: ")

		self.end_address = ""

		while not self.end_address:
			self.end_address = input("Enter the address of your end location: ")

		self.routing_method = ""
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

	def strategy_find_route(self):
		if self.routing_method == "dijkstra":
			context = Context(RoutingDijkstra())
			return context.execute_routing_mode(self.graph, self.start, self.end, self.x, self.elevation_gain_mode)
		elif self.routing_method == "a*":
			context = Context(RoutingAStar())
			return context.execute_routing_mode(self.graph, self.start, self.end, self.x, self.elevation_gain_mode)
		elif self.routing_method == "bfs":
			context = Context(RoutingBFS())
			return context.execute_routing_mode(self.graph, self.start, self.end, self.x, self.elevation_gain_mode)
		elif self.routing_method  == "dfs":
			context = Context(RoutingDFS())
			return context.execute_routing_mode(self.graph, self.start, self.end, self.x, self.elevation_gain_mode)
		else:
			print("Invalid routing method selected.")
			return None
    
	def display_path(self, path, shortest_path):
		root = tk.Tk()

		canvas1 = tk.Canvas(root, width = 700, height = 600,  relief = 'raised')
		canvas1.pack()

		label_title = tk.Label(root, text='EleNa')
		label_title.config(font=('helvetica', 14))
		canvas1.create_window(350, 25, window=label_title)

		label_path = tk.Label(root, text='Path output:')
		label_path.config(font=('helvetica', 12))
		canvas1.create_window(350, 60, window=label_path)
		
		textbox = tk.Text(root)
		textbox.insert(tk.END, path)
		canvas1.create_window(350, 270, window=textbox)
		
		label_total_elevation = tk.Label(root, text='Total Elevation:')
		label_total_elevation.config(font=('helvetica', 10))
		canvas1.create_window(300, 500, window=label_total_elevation)
		
		label_total_elevation_value = tk.Label(root, text=str(round(RoutingHelper().get_path_elevation(path, self.graph), 2)) + " m")
		label_total_elevation_value.config(font=('helvetica', 10))
		canvas1.create_window(400, 500, window=label_total_elevation_value)
		
		label_total_distance = tk.Label(root, text='Total Distance:')
		label_total_distance.config(font=('helvetica', 10))
		canvas1.create_window(300, 530, window=label_total_distance)
		
		label_total_distance_value = tk.Label(root, text=str(round(RoutingHelper().get_total_path_length(path, self.graph), 2)) + " m")
		label_total_distance_value.config(font=('helvetica', 10))
		canvas1.create_window(400, 530, window=label_total_distance_value)

		label_shortest_path_elevation = tk.Label(root, text='Shortest Path Elevation:')
		label_shortest_path_elevation.config(font=('helvetica', 10))
		canvas1.create_window(300, 560, window=label_shortest_path_elevation)
		
		label_shortest_path_elevation_value = tk.Label(root, text=str(round(RoutingHelper().get_path_elevation(shortest_path, self.graph), 2)) + " m")
		label_shortest_path_elevation_value.config(font=('helvetica', 10))
		canvas1.create_window(400, 560, window=label_shortest_path_elevation_value)

		label_shortest_distance = tk.Label(root, text='Shortest Distance:')
		label_shortest_distance.config(font=('helvetica', 10))
		canvas1.create_window(290, 590, window=label_shortest_distance)

		label_shortest_distance_value = tk.Label(root, text=str(round(RoutingHelper().get_total_path_length(shortest_path, self.graph), 2)) + " m")
		label_shortest_distance_value.config(font=('helvetica', 10))
		canvas1.create_window(400, 590, window=label_shortest_distance_value)

		osmnx.plot.plot_graph_routes(self.graph, [path, shortest_path], route_colors=["r", "b"])

		root.mainloop()

def main():
	app = App()
	app.set_user_inputs()
	app.set_graph()
	app.set_start_end_nodes()
	path = app.strategy_find_route()
	if path is None:
		print("No path found.")
		return
	shortest_path = osmnx.distance.shortest_path(app.graph, app.start, app.end)
	app.display_path(path, shortest_path)

if __name__ == '__main__':
	main()
