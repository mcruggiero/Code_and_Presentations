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