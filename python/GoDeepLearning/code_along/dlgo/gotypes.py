
#I added all of the library loading in one place to help with 
#Readability

###
#START of Listing 3.1
##

import enum
from collections import namedtuple

#This __all__ is just a list of all of the different classes
#to help load the module

__all__ = [
    'Player',
    'Point']


class Player(enum.Enum):
    black = 1
    white = 2
    
    
    #A cute little way to switch between players
    @property
    def other(self):
        return Player.black if self == Player.white else Player.white
    
###
#END of Listing 3.1
###

###
#START of Listing 3.2
###

class Point(namedtuple('Point', 'row col')):
    
    #This sets the neighborhood of points the board.
    def neighbors(self):
        
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]

###
#END of Listing 3.2
###
    
    def __deepcopy__(self, memodict={}):
        # These are very immutable.
        return self
