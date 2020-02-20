import enum

class Player(enum.Enum):
    black = 1
    white = 2
    
    @property
    def other(self):
        return Player.black if self == Player.white else Player.white
    
from collections import namedtuple

# This library is chosen to help with code readability.
# point.row is easier to read than point[0]

class Point(namedtuple("Point", "row col")):
    
    # This will allow us to look at the liberties of each stone
    def neighbors(self):
        return [Point(self.row - 1, self.col),
                Point(self.row + 1, self.col),
                Point(self.row, self.col - 1),
                Point(self.row, self.col + 1)]