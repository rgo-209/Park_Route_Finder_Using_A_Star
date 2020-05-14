"""
    This is the main file for finding the route in
    park using terrain data provided.

    By Rahul Golhar
"""
import time
from PathFinderClass import PathFinder


def main():
    """
        This is the main function for the algorithm.
    :return: None
    """
    # Image file to be used for terrain
    imageFileToUse = "TerrainImageAndElevation/terrain.png"
    # Elevation file to be used
    elevationFileToUse = "TerrainImageAndElevation/elevations.txt"

    # Create a path finder object
    pathFinder = PathFinder(imageFileToUse, elevationFileToUse)

    start = time.time()

    # Find the paths for all seasons
    pathFinder.findPathsForAllSeasons()

    print("\n\n********************************************")

    print("Total time taken to traverse all: ", time.time() - start)

    print("\n\n********************************************")

if __name__ == '__main__':
    main()
