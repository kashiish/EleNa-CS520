# EleNa: Elevation-based Navigation (EDIT)
Navigation systems optimize for the shortest or fastest route. However, they do not consider elevation gain. Let’s say you are hiking or biking from one location to another. 
You may want to literally go the extra mile if that saves you a couple thousand feet in elevation gain. Likewise, you may want to maximize elevation gain if you are
looking for an intense yet time-constrained workout.

The high-level goal of this project is to develop a software system that determines, given a start and an
end location, a route that maximizes or minimizes elevation gain, while limiting the total distance between
the two locations to x% of the shortest path.

## APIs 
We get our graph data using the [`OpenStreetMap(OSM)`](https://osmnx.readthedocs.io/en/stable/osmnx.html) API which returns a `networkx` multidigraph of the city. Since OSM does not provide elevation data, we use [`Open-Elevation`](https://open-elevation.com/) API to retrieve the elevation data for each node of the graph. We also use the OSM API to get the default shortest path between a start and end location. We compare and test our paths against this path for accuracy.

## Python GUI
The GUI interface allows the user to view the path returned by the chosen algorithm and the corresponding information such as total elevation and total distance of the path compared with the shortest path possible. The GUI utilizes the OSM API to visualize the path in the city's graph and `tkinter` to display the corresponding data.

**Note: Tkinter may need to be installed manually according to your operating system** 

# How to Run
## Backend
To use EleNa on your system, run `pip3 install -r requirements.txt` in the root directory of EleNa. This will get you all the needed Python dependencies for you to run the project locally. 

Then, simply run `python3 src/app.py` in the root directory. Now, you will be prompted to enter details of yours desired travel, such as start and end addresses, preferred routing algorithm, mode of transporation, etc. 

Note: The current version of EleNa uses Boulder, Colorado's map so only addresses in Boulder will work. We are using a cached version of the Boulder map that was downloaded on 11/8/2021. If you would like to download an updated copy of the map or use the map of a different city please run:

`python src/map.py <city> <state> <country>`  from the root directory.

# How to Validate
We have written a series of tests for the Dijkstra and A* algorithms. To run the tests, run `pytest` in the root directory. 

**NOTE: This app has only been tested with Python3**
