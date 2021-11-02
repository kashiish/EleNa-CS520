class Node:
    """
    Stores information about one point on the map including:
        - latitude: float
        - longitude: float
        - neighbors (the points we can go from this point): [Node]
        - elevation: float
    """
    def __init__(self, latitude, longitude, neighbors=[], elevation=0):
        self.latitude = latitude
        self.longitude = longitude
        self.neighbors = neighbors
        self.elevation = elevation
    
    def get_coordinates(self):
        return (self.latitude, self.longitude)
    
    def get_neighbors(self):
        return self.neighbors
    
    def get_elevation(self):
        return self.elevation

