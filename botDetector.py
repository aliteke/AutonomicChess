
# this module will contain a "botDetector object"
class botDetector:
    
    #initialize the bot detector to detect on a set bot
    def __init__(self,botOfInterestPath):
        self.botOfInterestPath = botOfInterestPath
        self.estimatedLikeliness = 0.5

    #given a move or set of moves, what is the likeliness that these moves were taken by this bot
    def updateLikelinessThisOpponentIsThisBot(self, moveSet,testBoard):
        #run the chess engine for the test board
        
        #return whether this bot had this move in its top 5 most likely
        
        

        pass
