"""
    This file implements every function required for finding the route.

    By Rahul Golhar
"""
import time
from PixelDataClass import PixelData
from PixelPositionClass import PixelPosition
from math import sqrt, degrees, atan
from PIL import Image
from queue import PriorityQueue
from collections import deque

class PathFinder():
    """
        This class implements the functions
        and actions for finding various paths.
    """
    __slots__ = 'pixelInfoMapping', 'imagePixelForm', 'imageUsed', 'terrainSpeedMap', 'imageFilePath', 'elevationFilePath'

    # *************************************** Assign colors for different areas ***************************
    openLandA = '#f89412'  # (248,148,18) #
    roughMeadowsB = '#ffc000'  # (255,192,0)
    easyForestCnD = '#ffffff'  # (255,255,255)
    slowRunForestE = '#02d03c'  # (2,208,60)
    walkForestF = '#028828'  # (2,136,40)
    impassibleVegetationG = '#054918'  # (5,73,24)
    waterHnInJ = '#0000ff'  # (0,0,255)
    pavedRoadKnL = '#473303'  # (71,51,3)
    footpathMnN = '#000000'  # (0,0,0)
    outside = '#cd0065'  # (205,0,101)

    # *************************************** Assign colors for different seasons ***************************
    fallColor = '#f08080'
    winterColor = '#5cf2ed'
    springColor = '#8b6508'

    # *************************************** Assign distance covered per unit ***************************
    xDistLongitude = 10.29
    yDistLatitude = 7.55
    diagonalDist = sqrt(xDistLongitude ** 2 + yDistLatitude ** 2)

    # *************************************** Assign seasons and files with path coordinates ***************************
    pathsToTrace = ["brown.txt", "white.txt", "red.txt"]
    seasonsToConsider = ['summer', 'fall', 'winter', 'spring']

    def __init__(self, imageFilePath, elevationFilePath):
        """
            This is the constructor for the class.
        :param imageFilePath:       this is path of the image to use for terrain
        :param elevationFilePath:   this is path with the elevation data for the terrain
        """
        self.imageFilePath = imageFilePath
        self.elevationFilePath = elevationFilePath
        self.pixelInfoMapping = {}
        self.terrainSpeedMap = {}
        self.terrainSpeedMapping()
        self.loadTerrainImage()
        self.loadElevationData()

    def rgbaToHex(self, rgbaValue):
        """
            This function returns the hex value of the rgba value passed
        :param rgbaValue:   the rgba value passed
        :return:            hex value of color paased
        """
        return '#%02x%02x%02x' % rgbaValue[0:3]

    def terrainSpeedMapping(self):
        """
            Thus function maps the areas and the respective speeds.
        :return:    None
        """
        self.terrainSpeedMap[self.openLandA] = 1.2
        self.terrainSpeedMap[self.roughMeadowsB] = 0.45
        self.terrainSpeedMap[self.easyForestCnD] = 0.85
        self.terrainSpeedMap[self.slowRunForestE] = 0.65
        self.terrainSpeedMap[self.walkForestF] = 0.55
        self.terrainSpeedMap[self.impassibleVegetationG] = 0
        self.terrainSpeedMap[self.waterHnInJ] = 0.15
        self.terrainSpeedMap[self.pavedRoadKnL] = 1.5
        self.terrainSpeedMap[self.footpathMnN] = 1.1
        self.terrainSpeedMap[self.outside] = 0

        self.terrainSpeedMap[self.fallColor] = 0.4
        self.terrainSpeedMap[self.winterColor] = 0.7
        self.terrainSpeedMap[self.springColor] = 0.2

    def loadTerrainImage(self):
        """
            This function loads the image of the terrain.
        :return:   None
        """
        self.imageUsed = Image.open(self.imageFilePath)
        self.imagePixelForm = self.imageUsed.load()

    def loadElevationData(self):
        """
            This function loads the elevation data of terrain.
        :return: None
        """
        elevationFile = open(self.elevationFilePath, "r")

        elevationData = []

        # read line by line
        for line in elevationFile:
            linesList = []
            lineArray = line.strip().split("   ")
            for i in range(0, 395):
                linesList.append(float(lineArray[i]))
            elevationData.append(linesList)

        # assign data to respective pixel positions
        for i in range(0, 395):
            for j in range(0, 500):
                color = self.rgbaToHex(self.imagePixelForm[i, j])
                value = PixelData(elevationData[j][i], color, self.terrainSpeedMap[color])
                self.pixelInfoMapping[PixelPosition(i, j)] = value

    def resetPixelData(self):
        """
            This function is used to reset the pixel data.
        :return: None
        """
        for i in range(0, 395):
            for j in range(0, 500):
                key = PixelPosition(i, j)
                color = self.rgbaToHex(self.imagePixelForm[i, j])
                self.pixelInfoMapping[key].color = color
                self.pixelInfoMapping[key].speed = self.terrainSpeedMap[color]

    def heuristic1(self, currentPoint, endPoint):
        """
            This is the heuristic function used.
        :param currentPoint:    the first end point data
        :param endPoint:        the other end point data
        :return: the result of heuristic function
        """
        dx = abs(currentPoint.xCoordinate - endPoint.xCoordinate)
        dy = abs(currentPoint.yCoordinate - endPoint.yCoordinate)
        return (min(dx, dy) + abs(dx - dy)) / 5

    def heuristic2(self, currentPoint, endPoint):
        """
            This is the heuristic function used.
        :param currentPoint:    the first end point data
        :param endPoint:        the other end point data
        :return: the result of heuristic function
        """
        dx = abs(currentPoint.xCoordinate - endPoint.xCoordinate)
        dy = abs(currentPoint.yCoordinate - endPoint.yCoordinate)
        dz = self.pixelInfoMapping[currentPoint].elevation - self.pixelInfoMapping[endPoint].elevation
        return (dx + dy) - (dz / 12)

    def setVisitedColor(self, currentPoint, imagePixelForm):
        """
            This function changes the color of the visited color
        :param currentPoint:    point to change the color of
        :param imagePixelForm:  the image pixel data
        :return:  None
        """
        for pixel in currentPoint.findNeighbours():
            imagePixelForm[pixel.xCoordinate, pixel.yCoordinate] = (255, 0, 255, 255)

    def findElevationAngle(self, p1, p2):
        """
            This function returns the angle of
            elevation between 2 points.
        :param p1:  first point to check for
        :param p2:  second point to check for
        :return:    the angle of elevation between 2 points
        """
        return degrees(atan(
            (self.pixelInfoMapping[p1].elevation - self.pixelInfoMapping[p2].elevation) / self.calculateDistance(p1,p2)))

    def aStarImplementation(self, startPoint, endPoint):
        """
            This function implements the A* Algorithm for
            path between the 2 given points.
        :param startPoint:  the starting points
        :param endPoint:    the ending point
        :return:            the path between the 2 given points
                            and the distance so far
        """
        startPoint.value = 0

        # Priority queue for storing points
        queue = PriorityQueue()
        queue.put(startPoint)

        # list to store previous points
        previousPoint = {}
        previousPoint[startPoint] = None

        # list to store cost
        costTillNow = {}
        costTillNow[startPoint] = 0

        # list to store distance
        distanceTillNow = {}
        distanceTillNow[startPoint] = 0

        while not queue.empty():

            currentPoint = queue.get()

            # if the destination is reached
            if currentPoint == endPoint:
                break

            # find best neighbour
            for point in currentPoint.findNeighbours():
                if self.isValidPoint(point):
                    # Calculate distance to neighbour
                    distance = self.calculateDistance(currentPoint, point)
                    # Calculate elevation angle between current point and next point
                    elevation_angle = self.findElevationAngle(currentPoint, point)
                    # find the speed at new pixel
                    pixel_speed = self.pixelInfoMapping[point].speed
                    # find the speed with which we can move
                    speed = pixel_speed - (pixel_speed * elevation_angle / 100)
                    # find the new cost and append
                    new_cost = costTillNow[currentPoint] + distance / speed

                    # find the neighbour with least cost
                    if point not in costTillNow or new_cost < costTillNow[point]:
                        distanceTillNow[point] = distanceTillNow[currentPoint] + distance
                        point.value = new_cost + self.heuristic1(point, endPoint) / self.pixelInfoMapping[point].speed
                        costTillNow[point] = new_cost
                        queue.put(point)
                        previousPoint[point] = currentPoint

        current = endPoint
        path = []
        # add all elements to the path array
        while current != startPoint:
            path.append(current)
            current = previousPoint[current]
        # the path between the 2 given points and the distance so far
        return path, distanceTillNow[endPoint]

    def tracePath(self, path, imagePixelForm):
        """
            This function sets the color of the points on the path.
        :param path:            the points in the path
        :param imagePixelForm:  the image in pixel form
        :return:                None
        """
        for pixel in path:
            imagePixelForm[pixel.xCoordinate, pixel.yCoordinate] = (255, 0, 0, 255)

    def isValidPoint(self, pixel):
        """
            This function checks whether the given point
            is a valid location that can be entered or not.
        :param pixel:   the pixel data of the point to check for
        :return:        True if the point is valid else false
        """
        # point is invalid if it is out of bounds or it is an impassible vegetation
        if (str(self.pixelInfoMapping[pixel].color) == str(self.outside)) or \
                (str(self.pixelInfoMapping[pixel].color) == str(self.impassibleVegetationG)):
            return False
        else:
            return True

    def calculateDistance(self, point1, point2):
        """
            This function calculates the distance between 2 points.
        :param point1: first point to use
        :param point2: second point to use
        :return: the distance between those points
        """
        dx = abs(point1.xCoordinate - point2.xCoordinate)
        dy = abs(point1.yCoordinate - point2.yCoordinate)

        if (dx == 1 and dy == 1):
            return self.diagonalDist
        elif (dx == 1 and dy == 0):
            return self.xDistLongitude
        else:
            return self.yDistLatitude

    def resetImageToUse(self):
        """
            This function resets the image data to initial image data.
        :return: None
        """
        self.imageUsed = Image.open(self.imageFilePath)
        self.imagePixelForm = self.imageUsed.load()
        self.resetPixelData()

    def getPointsOnRoute(self, pathFile):
        """
            This function returns the points to be traced given in file.
        :param pathFile:    file to read and find the coordinates
        :return:            list of points to be traced
        """
        pointsOnRoute = []
        file = open(("PathFiles/"+pathFile), "r")
        for line in file:
            point = line.strip().split(" ")
            pointsOnRoute.append(PixelPosition(int(point[0]), int(point[1])))
        return pointsOnRoute

    def traceAllRoutesForSeason(self, season):
        """
                This function is used to trace routes for
                a given seasons one by one.
        :param season:  the season to be considered
        :return:        None
        """
        for i in range(0, 3):
            self.traceRoute(self.pathsToTrace[i], season)

    def findPathsForSummer(self):
        """
            This function traces the path for the Summer season.
        :return:    None
        """
        self.traceAllRoutesForSeason(self.seasonsToConsider[0])

    def setupImageForFall(self):
        """
            This functions manipulates the image data according to the Fall season.

            "In the fall, leaves fall. In the park, what happens is that paths through
            the woods can become covered and hard to follow. So, for fall, you should
            increase the time for any paths through (that is, adjacent to) easy movement
            forest (but only those paths)."

        :return:    None
        """
        for i in range(0, 395):
            for j in range(0, 500):
                currentPixel = PixelPosition(i, j)

                if self.pixelInfoMapping[currentPixel].color == self.easyForestCnD:
                    neighbours = currentPixel.findNeighbours()
                    for pixel in neighbours:
                        if self.pixelInfoMapping[pixel].color != self.easyForestCnD:
                            self.imagePixelForm[pixel.xCoordinate, pixel.yCoordinate] = (240, 128, 128, 255)  # f08080

    def findPathsForFall(self):
        """
            This function traces the paths for the Fall season.
        :return:    None
        """
        self.resetImageToUse()
        self.setupImageForFall()
        self.resetPixelData()
        self.traceAllRoutesForSeason(self.seasonsToConsider[1])

    def findingLakeEdge(self):
        """
            This function finds the edges of the lake in the terrain.
        :return:    coordinates of the edges of the lake
        """
        coordinatesOfEdges = []
        for i in range(0, 395):
            for j in range(0, 500):
                pixel = PixelPosition(i, j)
                if self.pixelInfoMapping[pixel].color == self.waterHnInJ:
                    neighbours = pixel.findNeighbours()
                    for neighbour in neighbours:
                        if self.pixelInfoMapping[neighbour].color != self.waterHnInJ:
                            coordinatesOfEdges.append(neighbour)
                            break
        return coordinatesOfEdges

    def setupImageForWinter(self):
        """
            This functions manipulates the image data according to the Winter season.

            "In winter, the waters can freeze. For this particular assignment, we will
             assume that any water within seven pixels of non-water is safe to walk on.
             Please note: you should not handle this by looking seven pixels out from
             every water pixel - it is much more efficient to find the edges of the waters
             and search out from there all at once. This can and should be cast as a BFS
             problem. You will be deducted points if you only perform a naive (and costly) search.
"
        :return:    None
        """
        coordinatesOfEdges = self.findingLakeEdge()

        for edge in coordinatesOfEdges:

            queue = deque()
            queue.append(edge)

            visitedEdges = set()
            visitedEdges.add(edge)

            while (queue):
                pixel = queue.popleft()
                dx = abs(pixel.xCoordinate - edge.xCoordinate)
                dy = abs(pixel.yCoordinate - edge.yCoordinate)
                if dx == 7 or dy == 7:
                    break
                if dx < 7 or dy < 7:
                    self.imagePixelForm[pixel.xCoordinate, pixel.yCoordinate] = (92, 242, 237, 255)
                for p in pixel.findImmediateNeighbours():
                    if p not in visitedEdges and self.pixelInfoMapping[p].color == self.waterHnInJ:
                        queue.append(p)
                        visitedEdges.add(p)
        self.imageUsed.show()

    def findPathsForWinter(self):
        """
            This function traces the paths for the Winter season.
        :return:    None
        """
        self.resetImageToUse()
        self.setupImageForWinter()
        self.resetPixelData()
        self.traceAllRoutesForSeason(self.seasonsToConsider[2])

    def setupImageForSpring(self):
        """
            This functions manipulates the image data according to the Spring season.

            "aka "mud season". Any pixels within fifteen pixels of water that can be
            reached from a water pixel without gaining more than one meter of
            elevation(total) are now underwater. (Note that the water pixels represent
            different ponds and are therefore at different heights. The best thing to
            do is probably to start at water pixels and search outward to the non-water
            adjacent, but keeping track of the elevation of the particular water pixel
            that you came from for each non-water pixel.) You may choose whether you
            wish to run through this water or not :) but note that one of the controls
            on the white course linked above should now be underwater! Like in the case
            of Winter, this can and should be cast as a BFS problem."

        :return:    None
        """
        coordinatesOfEdges = self.findingLakeEdge()

        for curr in coordinatesOfEdges:

            queue = deque()
            queue.append(curr)
            visited = set()
            visited.add(curr)

            while (queue):
                pixel = queue.popleft()

                dx = abs(pixel.xCoordinate - curr.xCoordinate)
                dy = abs(pixel.yCoordinate - curr.yCoordinate)

                if dx == 15 or dy == 15:
                    break

                if self.pixelInfoMapping[curr].elevation - self.pixelInfoMapping[pixel].elevation > - 1:
                    self.imagePixelForm[pixel.xCoordinate, pixel.yCoordinate] = (139, 101, 8, 255)

                for p in pixel.findImmediateNeighbours():
                    if p not in visited and self.pixelInfoMapping[p].color != self.waterHnInJ and \
                            self.pixelInfoMapping[p].color != self.outside:
                        visited.add(p)
                        elevation_diff = self.pixelInfoMapping[curr].elevation - self.pixelInfoMapping[p].elevation
                        if elevation_diff > -1:
                            queue.append(p)
        self.imageUsed.show()

    def findPathsForSpring(self):
        """
            This function traces the paths for the Spring season.
        :return:    None
        """
        self.resetImageToUse()
        self.setupImageForSpring()
        self.resetPixelData()
        self.traceAllRoutesForSeason(self.seasonsToConsider[3])

    def traceRoute(self, routeFile, seasonToUse):
        """
            This function traces the route given in the file passed
            and uses the given season.
        :param routeFile:       the file to use for getting points on path
        :param seasonToUse:     the season to use for terrain path
        :return: None
        """
        # find the points on the route to be traced
        pointsOnRoute = self.getPointsOnRoute(routeFile)
        start = time.time()

        startPoint = pointsOnRoute[0]

        total_distance = 0

        # get the image to be used
        newImageToLoad = Image.new("RGB", (395, 500), "white")
        newImageToLoad.paste(self.imageUsed, (0, 0))
        imagePixelForm = newImageToLoad.load()

        # set the red color at the start point
        self.setVisitedColor(startPoint, imagePixelForm)

        # traverse the points on the route
        for point in range(1, len(pointsOnRoute)):
            endPoint = pointsOnRoute[point]
            # assign red color to new point
            self.setVisitedColor(endPoint, imagePixelForm)

            # find the minimum path and the distance to reach next point
            path, distance = self.aStarImplementation(startPoint, endPoint)

            # calculate the total distace
            total_distance += distance
            # color the path between the 2 points
            self.tracePath(path, imagePixelForm)
            startPoint = endPoint

        # *********************************** Print output ***************************************

        print("\n\t\t----- "+str(routeFile)+"----- ")

        print("Total Distance: " + str(total_distance))
        print("Total Time Taken:" + str(time.time() - start))

        # Save the image with path
        filename = seasonToUse + routeFile
        filename = filename[0:len(filename) - 4] + ".png"
        newImageToLoad.save("GeneratedPaths/"+filename)

        # *********** Comment this if u don't want the image to pop up when its generated. ***********
        newImageToLoad.show()

    def findPathsForAllSeasons(self):
        """
            This function traces the paths
            for all seasons one by one.
        :return:    None
        """
        print(    "************** SUMMER **************")
        self.findPathsForSummer()
        print("\n\n*************** FALL ***************")
        self.findPathsForFall()
        print("\n\n************** WINTER **************")
        self.findPathsForWinter()
        print("\n\n************** SPRING **************")
        self.findPathsForSpring()