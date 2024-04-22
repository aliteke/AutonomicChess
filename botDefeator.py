#this module will contain all code relevant to the "botDefeator" object

#a bot defeator will be given an open-access chessBot and asked to find a sequence of moves which can be used to defeat the bot

class botDefeator:
    
    #initialize the defeator object with the path of the bot it is looking for
    # searchDepth determines how far down in the tree we bother to go
    def __init__(self,botOfInterestPath, searchDepth,manager):
        self.botOfInterestPath = botOfInterestPath
        self.searchDepth = searchDepth
        self.OptimalSequence = None
        self.OptimalSequenceIndex = None

    #get the optimal move in order to defeat the bot
    def getOptimalMove(self,board):
        #if an optimal sequence (a sequence of moves which can be used to achieve a checkmate) has been found use it

        #else
            #carry out a recursive search
            #if a result is found it will be stored in OptimalSequence, 
                
            #else return that no optimal move has been found
        pass

    #this function carries out a recursive search for an optimal sequence from this board
    def optimalMoveSearchRecursion(self,board,currentSearchDepth,currentSearchSequence):
        #return [maxInt,None] if the searchDepth is beyond self.searchDepth or if OptimalSequence is not none
        #given the current board position iterate over all moves that you could make
            #initialize a test board for each one
            #make the move on the test board
            #if the move results in a checkmate return [currentSearchDepth,the sequence that resulted in this] and store it in OptimalSequence
            
            #match it to the resulting move the opponent would make

            #call the next recursive layer for this board with a deeper depth and a larger stored sequence

        #of the child returns, return the one with the shortest first part of the child returns
        pass