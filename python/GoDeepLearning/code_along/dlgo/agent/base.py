
__all__ = [
    'Agent',
]

###
#START of Listing 3.16
###
# tag::agent[]
class Agent:
    def __init__(self):
        pass

    def select_move(self, game_state):
        raise NotImplementedError()
# end::agent[]

###
#END of Listing 3.16
###

    def diagnostics(self):
        return {}
