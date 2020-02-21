import copy
from gotypes import Player

# This import is interesting, we are already coding
# above, I think I will make a new .py file and add it the current 
# working directory


class Move():
    
    # In the game of Go an action is defined as either a play, 
    # a pass or resign. Plays are defined as placing a stone.
    
    
    def __init__ (self,
                  point = None,
                  is_pass = False, 
                  is_resign = False):
        assert (point is not None) ^ is_pass ^ is_resign
        
        # The carrot here (^) is the pythonic XOR operator.
        # assert allows us to interupt the program unless 
        # one of these is true. Notice that if two or more are
        # true, then this will also break the line.
        
        @classmethod 
        def play(cls, point):
            return Move(point = point)
        
        @classmethod
        def pass_turn(cls):
            return Move(is_pass = True)
        
        @classmethod
        def resign(cls):
            return Move(is_resign = True)
        
class GoString():  # <1>
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    def remove_liberty(self, point):
        self.liberties.remove(point)

    def add_liberty(self, point):
        self.liberties.add(point)

    def merged_with(self, go_string):  # <2>
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | go_string.liberties) - combined_stones)

    @property
    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self, other):
        return isinstance(other, GoString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties
    
class Board():
    
    #We initialize an empty grid with the number of rows and columns
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}
        
  
        