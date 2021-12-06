# EleNa: Elevation-based Navigation (EDIT)
Navigation systems optimize for the shortest or fastest route. However, they do not consider elevation gain. Let’s say you are hiking or biking from one location to another. 
You may want to literally go the extra mile if that saves you a couple thousand feet in elevation gain. Likewise, you may want to maximize elevation gain if you are
looking for an intense yet time-constrained workout.

The high-level goal of this project is to develop a software system that determines, given a start and an
end location, a route that maximizes or minimizes elevation gain, while limiting the total distance between
the two locations to x% of the shortest path.

## APIs

TODO

# How to Run
## Backend
To use EleNa on your system, run `pip3 install -r requirements.txt` in the root directory of EleNa. This will get you all the needed Python dependencies for you to run the project locally. 

Then, simply run `python3 src/app.py` in the root directory. Now, you will be prompted to enter details of yours desired travel, such as start and end addresses, preferred routing algorithm, mode of transporation, etc. 

Note: The current version of EleNa uses Boulder, Colorado's map so only addresses in Boulder will work. We are using a cached version of the Boulder map that was downloaded on 11/8/2021. If you would like to download an updated copy of the map or use the map of a different city please run:

`python src/map.py <city> <state> <country>`  from the root directory.

## Python GUI

TODO

# How to Validate
We have written a series of tests for the Dijkstra and A* algorithms. To run the tests, run `pytest` in the root directory. 

**NOTE: This app has only been tested with Python3**
