# EleNa: Elevation-based Navigation (EDIT)
Navigation systems optimize for the shortest or fastest route. However, they do not consider elevation gain. Let’s say you are hiking or biking from one location to another. 
You may want to literally go the extra mile if that saves you a couple thousand feet in elevation gain. Likewise, you may want to maximize elevation gain if you are
looking for an intense yet time-constrained workout.

The high-level goal of this project is to develop a software system that determines, given a start and an
end location, a route that maximizes or minimizes elevation gain, while limiting the total distance between
the two locations to x% of the shortest path.

# How to Run
## Backend
To use EleNa on your system, run `pip3 install -r requirements.txt` in the root directory of EleNa. This will get you all the needed Python dependencies for you have the project run locally. 

Then, simply run `python3 src/app.py` in the root directory. Now, you will be prompted to enter details of yours desired travel, such as start and end location, preferred routing algorithm, mode of transporation, etc. 

## Python GUI

# How to Validate (ADD TESTING)
