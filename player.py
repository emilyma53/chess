import pieces

class Player():

    def __init__(self, name):
        self.captured = {}
        self.curr_pieces = {}
        self.name = name

    def get_score(self):
        ''' 
        Returns the player's current score (int), which is the sum of a player's
        current pieces and pieces captured from the other player.
        '''
        score = 0
        for piece in self.curr_pieces:
            value = self.curr_pieces[piece]
            score += value
        for piece in self.captured:
            value = self.captured[piece]
            score += value
        return score