"""
    This is the file for declaring the class to store the pixel properties.

    By Rahul Golhar
"""


class PixelData():

    """
        This class is used to store the
        data about a pixel location.
    """
    __slots__ = 'elevation', 'color', 'speed'

    def __init__(self, elevation, color, speed):
        """
            This is the constructor for the class.
        :param elevation:   The elevation at a certain point
        :param color:       The color of the pixel
        :param speed:       The speed than can be achieved at the location
        """
        self.elevation = elevation
        self.color = color
        self.speed = speed