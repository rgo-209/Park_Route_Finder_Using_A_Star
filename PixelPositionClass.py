"""
    This is the file for declaring the class to be
    used for getting data of the neighbours of the pixel..

    By Rahul Golhar
"""


class PixelPosition():
    """
        This class stored the data about the position of a point.
    """
    __slots__ = 'xCoordinate', 'yCoordinate', 'value'

    def __init__(self, x, y):
        """
            This is the constructor for the class.
        :param x: the x coordinate of point to initialize
        :param y: the y coordinate of point to initialize
        """
        self.xCoordinate = x
        self.yCoordinate = y
        self.value = None

    def __eq__(self, secondPoint):
        """
            This function overloads the inbuilt equals function.
        :param secondPoint: the point to be compared with
        :return:            true if both points have same
                            x and y coordinates
        """
        return self.xCoordinate == secondPoint.xCoordinate and self.yCoordinate == secondPoint.yCoordinate

    def __hash__(self):
        """
            This function overloads the inbuilt hash function.
        :return: the hash value to be used
        """
        return hash(str(self.xCoordinate) + '_' + str(self.yCoordinate))

    def __cmp__(self, secondPoint):
        """
            This function overloads the inbuilt compare function and
            compared the values of two points.
        :param secondPoint: point to be compared with
        :return: comparison of values of both points
        """
        return __cmp__(self.value, secondPoint.value)

    def __lt__(self, secondPoint):
        """
            This function checks whether the value of
            point passed is less that the current point.
        :param secondPoint: point to be compared with
        :return:            result of current point value
                            less than passed point value
        """
        return self.value < secondPoint.value

    def findNeighbours(self):
        """
            This function returns the list of all neighbours
            of the point.
        :return: the list of all neighbours
        """
        neighbours = []

        for i in range(self.xCoordinate - 1, self.xCoordinate + 2):
            for j in range(self.yCoordinate - 1, self.yCoordinate + 2):
                if (not (i == self.xCoordinate and j == self.yCoordinate)) and (0 <= i <= 394 and 0 <= j <= 499):
                    neighbours.append(PixelPosition(i, j))

        return neighbours

    def findImmediateNeighbours(self):
        """
            This function returns the immediate neighbours
            in 4 directions of the point.
        :return: the list of immediate neighbours
        """
        immediateNeighbours = []

        if self.xCoordinate - 1 > 0:
            immediateNeighbours.append(PixelPosition(self.xCoordinate - 1, self.yCoordinate))

        if self.xCoordinate + 1 < 395:
            immediateNeighbours.append(PixelPosition(self.xCoordinate + 1, self.yCoordinate))

        if self.yCoordinate + 1 < 500:
            immediateNeighbours.append(PixelPosition(self.xCoordinate, self.yCoordinate + 1))

        if self.yCoordinate - 1 > 0:
            immediateNeighbours.append(PixelPosition(self.xCoordinate, self.yCoordinate - 1))

        return immediateNeighbours

    def __str__(self):
        return "(" + str(self.xCoordinate) + "," + str(self.yCoordinate) + ")"

    def __repr__(self):
        return str(self)
