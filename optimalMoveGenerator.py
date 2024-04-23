import chess
import chess.engine

# this module contains all code relevant to the custom "optimalMoveGenerator" class
#this object will very simply store a reference to a chess engine which is lower ranked than all in the testing set
#and return "optimal" moves from it
class optimalMoveGenerator:

    #initialize the class
    def __init__(self,optimalMoveEnginePath,manager):
        #store everything
        self.enginePath = optimalMoveEnginePath
        self.manager = manager
        #spin up and store the optimal engine
        self.optimalEngine = chess.engine.SimpleEngine.popen_uci(optimalMoveEnginePath)
        self.optimalEngine
    #this much will return the move that is predicted to be optimal
    def getOptimalMove(self,board):
        #request the next move using the engine.play function
        #note that because the optimal move engine is intended to be worse, we give it 1/3 the processing time
        return self.optimalEngine.play(board, chess.engine.Limit(time=self.manager.timeOutInMS/3)).move
        