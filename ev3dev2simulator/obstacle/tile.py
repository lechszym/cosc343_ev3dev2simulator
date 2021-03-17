"""
Module lake containing the class Lake, an obstacle on the playground.
"""

import arcade
from arcade import Shape, PointList, create_rectangle_filled

from ev3dev2simulator.obstacle.color_obstacle import ColorObstacle
from ev3dev2simulator.util.point import Point
from ev3dev2simulator.util.dimensions import Dimensions
from ev3dev2simulator.util.util import get_rectangle_points, to_color_code


class Tile(ColorObstacle):
    """
    This class represents a 'lake'. Lakes consist of a transparent circle
    with a thick colored border.
    """

    def __init__(self,
                 pos: Point,
                 dims: Dimensions,
                 color: arcade.Color,
                 ):
        super(Tile, self).__init__(to_color_code(color))

        self.x = pos.x
        self.y = pos.y

        self.width = dims.width
        self.height = dims.height

        # visualisation
        self.center_x = None
        self.center_y = None
        self.color = color
        self.shape = None
        self.scale = None

    def get_shapes(self):
        """
        Returns the lake shape.
        """
        return [self.shape]

    def create_shape(self, scale):
        """
        Creates the shape of lake.
        """
        self.scale = scale
        self.center_x = self.x * scale
        self.center_y = self.y * scale
        self.shape = self._create_shape(scale)

    @classmethod
    def from_config(cls, config):
        """
        Creates a lakes based on the given config.
        """
        pos = Point(config['x'], config['y'])
        dims = Dimensions(config['width'], config['height'])
        color = tuple(config['color'])

        return cls(pos, dims, color)

    def _create_points(self, scale) -> PointList:
        """
        Create a list of points representing this Lake in 2D space.
        :return: a PointList object.
        """

        return get_rectangle_points(self.center_x,
                                 self.center_y,
                                 self.width * scale,
                                 self.height * scale)

    def _create_shape(self, scale) -> Shape:
        """
        Create a shape representing this lake.
        :return: a Arcade shape object.
        """
        return create_rectangle_filled(self.center_x, self.center_y, self.width * scale, self.height * scale, self.color)


    def collided_with(self, x: float, y: float) -> bool:
        """
        Check if the lake overlaps with a robot.
        """
        #if self.hole is not None:
        #    return (self.inner_radius * self.scale) < distance <\
        #           ((self.outer_radius + (self.border_width/2)) * self.scale)
        #return distance < (self.outer_radius * self.scale)
        left_x = self.center_x - self.width*self.scale/2
        right_x = self.center_x + self.width*self.scale/2

        bottom_y = self.center_y - self.height*self.scale/2
        top_y = self.center_y + self.height*self.scale/2

        if x >= left_x and x <= right_x and y >= bottom_y and y<= top_y:
            return True

        return False
