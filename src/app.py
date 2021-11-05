class App:
	def __init__(self):
		self.start_latitude = None
		self.start_longitude = None
		self.end_latitude = None
		self.end_longitude = None
		self.elevation_gain_mode = None
		self.x = None
		self.transportation_mode = None

	def get_user_inputs(self):
		self.start_latitude = input("Enter the latitude of your start location ")
		self.start_longitude = input("Enter the longitude of your start location ")
		self.end_latitude = input("Enter the latitude of your end location ")
		self.end_longitude = input("Enter the longitude of your end location ")
		self.elevation_gain_mode = input("Type 'maximize' if you want to maximize elevation gain, or 'minimize' if you want to minimize elevation gain (no quotes) ")
		self.x = input("Enter how much you're able to travel additional to the shortest route ")
		self.transportation_mode = input("Enter one of the following options for your preferred mode of transportation: drive, walk, bike ")

def main():
	app = App()
	app.get_user_inputs()

if __name__ == '__main__':
	main()


