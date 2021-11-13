import sys
import osmnx as osmnx

class App:
	def __init__(self):
		self.start_latitude = None
		self.start_longitude = None
		self.end_latitude = None
		self.end_longitude = None
		self.elevation_gain_mode = None
		self.x = None
		self.transportation_mode = None
		self.graph = None
		self.TRANSPORTATION_MODES = ["drive", "walk", "bike"]
		self.start = None
		self.end = None

	def get_user_inputs(self):
		self.start_latitude = float(input("Enter the latitude of your start location: "))
		self.start_longitude = float(input("Enter the longitude of your start location: "))
		self.end_latitude = float(input("Enter the latitude of your end location: "))
		self.end_longitude = float(input("Enter the longitude of your end location: "))
		self.elevation_gain_mode = input("Type 'maximize' if you want to maximize elevation gain, or 'minimize' if you want to minimize elevation gain (no quotes), or press enter to skip & to get the shortest route: ")
		self.x = input("Enter how much you're able to travel additional to the shortest route: ")
		
		self.transportation_mode = input("Enter one of the following options for your preferred mode of transportation: drive, walk, bike: ")
		
		if self.transportation_mode not in self.TRANSPORTATION_MODES:
			print("Please enter a valid option between drive, walk, bike next time: ")
			sys.exit()

	def get_graph(self):
		if self.transportation_mode == "drive":
			with open("boulder-drive.pkl", 'rb') as file:
				self.graph = pkl.load(file)
				print(list(self.graph.nodes(data=True)))

		if self.transportation_mode == "walk":
			with open("boulder-walk.pkl", 'rb') as file:
				self.graph = pkl.load(file)
				print(list(self.graph.nodes(data=True)))

		if self.transportation_mode == "bike":
			with open("boulder-bike.pkl", 'rb') as file:
				self.graph = pkl.load(file)
				print(list(self.graph.nodes(data=True)))
		
		self.start = osmnx.get_nearest_node(self.graph, self.start_latitude, self.start_longitude)
		print(self.start)
		self.end = osmnx.get_nearest_node(self.graph, self.end_latitude, self.end_longitude)
		print(self.end)

def main():
	app = App()
	app.get_user_inputs()
	app.get_graph()

if __name__ == '__main__':
	main()


