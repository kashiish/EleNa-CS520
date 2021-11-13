import sys
import osmnx
import pickle as pkl

class App:
	def __init__(self):
		self.start_latitude = 0
		self.start_longitude = 0
		self.end_latitude = 0
		self.end_longitude = 0
		self.elevation_gain_mode = None
		self.x = None
		self.transportation_mode = None
		self.graph = None
		self.TRANSPORTATION_MODES = ["drive", "walk", "bike"]
		self.start = None
		self.end = None

	def set_user_inputs(self):
		self.start_latitude = float(input("Enter the latitude of your start location: "))
		self.start_longitude = float(input("Enter the longitude of your start location: "))
		self.end_latitude = float(input("Enter the latitude of your end location: "))
		self.end_longitude = float(input("Enter the longitude of your end location: "))
		self.elevation_gain_mode = input("Type 'maximize' if you want to maximize elevation gain, or 'minimize' if you want to minimize elevation gain (no quotes), or press enter to skip & to get the shortest route: ")
		self.x = input("Enter what percentage of shortest path you're able to additionally travel: ")
		
		self.transportation_mode = input("Enter one of the following options for your preferred mode of transportation: drive, walk, bike: ")
		
		while self.transportation_mode not in self.TRANSPORTATION_MODES:
			self.transportation_mode = input("Please enter a valid option between drive, walk, bike: ")

	def set_graph(self):
		with open("cached_maps/boulder-{}.pkl".format(self.transportation_mode), 'rb') as file:
				self.graph = pkl.load(file)
		
	def set_start_end_nodes(self):
		start_node_id = osmnx.distance.nearest_nodes(self.graph, self.start_longitude, self.start_latitude)
		self.start = self.graph.nodes[start_node_id]
		
		end_node_id = osmnx.distance.nearest_nodes(self.graph, self.end_longitude, self.end_latitude)
		self.end = self.graph.nodes[end_node_id]

def main():
	app = App()
	app.set_user_inputs()
	app.set_graph()
	app.set_start_end_nodes()

if __name__ == '__main__':
	main()
