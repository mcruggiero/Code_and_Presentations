
from __future__ import absolute_import
from collections import namedtuple

from dlgo.gotypes import Player, Point
# When I rewrite the code myself, I am tempted to bring Player and
# Point into this code

class Territory:
    #Starting by setting up the full score.
    def __init__(self, territory_map):  # <1>
        self.num_black_territory = 0
        self.num_white_territory = 0
        self.num_black_stones = 0
        self.num_white_stones = 0
        self.num_dame = 0
        self.dame_points = []
        
        # Updates the points as the game progresses
        for point, status in territory_map.items():  # <2>
            if status == Player.black:
                self.num_black_stones += 1
            elif status == Player.white:
                self.num_white_stones += 1
            elif status == 'territory_b':
                self.num_black_territory += 1
            elif status == 'territory_w':
                self.num_white_territory += 1
                
# In Go "dame" is a neutral space where placing a stone at the location
# won't gain either side any points.
            elif status == 'dame':
                self.num_dame += 1
                self.dame_points.append(point)

# <1> A `territory_map` splits the board into stones, territory and neutral points (dame).
# <2> Depending on the status of a point, we increment the respective counter.

class GameResult(namedtuple('GameResult', 'b w komi')):
    @property
    def winner(self):
        # In go, komi is the set of points that 
        # compenstates the white player for going second.
        if self.b > self.w + self.komi:
            return Player.black
        return Player.white

    @property
    def winning_margin(self):
        # Basically the score
        w = self.w + self.komi
        return abs(self.b - w)

    def __str__(self):
        # Score reporter
        w = self.w + self.komi
        if self.b > w:
            return 'B+%.1f' % (self.b - w,)
        return 'W+%.1f' % (w - self.b,)


""" evaluate_territory:
Map a board into territory and dame.

Any points that are completely surrounded by a single color are
counted as territory; it makes no attempt to identify even
trivially dead groups.
"""


# tag::scoring_evaluate_territory[]
def evaluate_territory(board):
    status = {}
    
    # Search through rows r and columns c. Later, I might add a vew
    # from the board print out to visualize this more completely.
    # get is defined in goboard_slow. get returns a player color if
    # the space is occupied, none otherwise.
    for r in range(1, board.num_rows + 1):
        for c in range(1, board.num_cols + 1):
            p = Point(row=r, col=c)
            if p in status:  # <1>
                continue
            stone = board.get(p)
            if stone is not None:  # <2>
                status[p] = board.get(p)
                
            # We are most interested in empty squares, this will
            # search the area for surrounding stones.
            else:
                group, neighbors = _collect_region(p, board)
                if len(neighbors) == 1:  # <3>
                    neighbor_stone = neighbors.pop()
                    stone_str = 'b' if neighbor_stone == Player.black else 'w'
                    fill_with = 'territory_' + stone_str
                else:
                    fill_with = 'dame'  # <4>
                for pos in group:
                    status[pos] = fill_with
    return Territory(status)

# <1> Skip the point, if you already visited this as part of a different group.
# <2> If the point is a stone, add it as status.
# <3> If a point is completely surrounded by black or white stones, count it as territory.
# <4> Otherwise the point has to be a neutral point, so we add it to dame.
# end::scoring_evaluate_territory[]


""" _collect_region:

Find the contiguous section of a board containing a point. Also
identify all the boundary points.
"""

def _collect_region(start_pos, board, visited=None):

    #Sets the set at the start
    if visited is None:
        visited = {}
    
    #If the position is already counted, returns emptys
    if start_pos in visited:
        return [], set()
    
    #Collection begins after the tests, starting with the first
    #Point. This function returns all_points and all_boarders
    all_points = [start_pos]
    all_borders = set()
    
    #.is_on_grid and .get are defined in goboard_slow.py
    # is.on_grid returns true if the point is on the grid
    visited[start_pos] = True
    here = board.get(start_pos)
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    #These values are from the list above taken in turn, used to 
    for delta_r, delta_c in deltas:
        
        # Point is defined by gotypes above, returns the points in 
        # the neighborhood from the delta points
        next_p = Point(row=start_pos.row + delta_r, col=start_pos.col + delta_c)
        if not board.is_on_grid(next_p):
            continue
        
        neighbor = board.get(next_p)
        if neighbor == here:
            points, borders = _collect_region(next_p, board, visited)
            
            # Add points to counter and borders to set
            all_points += points
            all_borders |= borders
        else:
            all_borders.add(neighbor)
    return all_points, all_borders

#Finishes off the calcuation
def compute_game_result(game_state):
    territory = evaluate_territory(game_state.board)
    return GameResult(
        territory.num_black_territory + territory.num_black_stones,
        territory.num_white_territory + territory.num_white_stones,
        komi=7.5)
