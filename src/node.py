class Node:
    """
    Stores information about one point on the map including:
        - latitude: float
        - longitude: float
        - neighbors (the points we can go from this point): [Node]
        - elevation: float
    """
    def __init__(self, latitude, longitude, neigbors=[], elevation=0):
        self.latitude = latitude
        self.longitude = longitude
        self.neigbors = neigbors
        self.elevation = elevation
    
    def get_coordinates(self):
        return (self.latitude, self.longitude)
    
    def get_neighbors(self):
        return self.neigbors
    
    def get_elevation(self):
        return self.elevation