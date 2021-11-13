import osmnx
import routing_dijkstra as rd
import pickle as pkl

class App:
	def __init__(self):
		self.start_address = ""
		self.end_address = ""
		self.elevation_gain_mode = None
		self.x = None
		self.transportation_mode = None
		self.graph = None
		self.TRANSPORTATION_MODES = ["drive", "walk", "bike"]
		self.start = None
		self.end = None

	def set_user_inputs(self):
		self.start_address = input("Enter the address of your start location: ")
		self.end_address = input("Enter the address of your end location: ")
		self.elevation_gain_mode = input("Type 'maximize' if you want to maximize elevation gain, or 'minimize' if you want to minimize elevation gain (no quotes), or press enter to skip & to get the shortest route: ")
		self.x = input("Enter what percentage of shortest path you're able to additionally travel: ")
		
		self.transportation_mode = input("Enter one of the following options for your preferred mode of transportation: drive, walk, bike: ").lower()
		
		while self.transportation_mode not in self.TRANSPORTATION_MODES:
			self.transportation_mode = input("Please enter a valid option between drive, walk, bike: ")

	def set_graph(self):
		with open("cached_maps/boulder-{}.pkl".format(self.transportation_mode), 'rb') as file:
				self.graph = pkl.load(file)
		
	def set_start_end_nodes(self):
		start_latitude_longitude = osmnx.geocoder.geocode(self.start_address)
		self.start = osmnx.distance.nearest_nodes(self.graph, start_latitude_longitude[1], start_latitude_longitude[0])
		
		end_latitude_longitude = osmnx.geocoder.geocode(self.end_address)
		self.end = osmnx.distance.nearest_nodes(self.graph, end_latitude_longitude[1], end_latitude_longitude[0])

	def find_route(self):
		rd.dijkstra(self.graph, self.start, self.end)

def main():
	app = App()
	app.set_user_inputs()
	app.set_graph()
	app.set_start_end_nodes()
	app.find_route()

if __name__ == '__main__':
	main()
