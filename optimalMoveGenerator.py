# this module contains all code relevant to the custom "optimalMoveGenerator" class

#this object will very simply store a reference to a chess engine which is lower ranked than all in the testing set

class optimalMoveGenerator:

    #initialize the class
    def __init__(self,optimalMoveEnginePath,manager):
        self.enginePath = optimalMoveEnginePath
        pass

    #this much will return the move that is predicted to be optimal
    def getOptimalMove(self,board):
        #load the chess engine

        #request the next move using the engine.play function

        pass