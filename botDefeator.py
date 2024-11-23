#this module will contain all code relevant to the "botDefeator" object
import chess
import chess.engine
import os
#a bot defeator will be given an open-access chessBot and asked to find a sequence of moves which can be used to defeat the bot

class botDefeator:
    
    #initialize the defeator object with the path of the bot it is looking for
    # searchDepth determines how far down in the tree we bother to go
    def __init__(self,botName,testEngineDirPath,manager):
        self.botName = botName
        self.manager = manager
        self.optimalOpponentEnginePath = os.path.join(testEngineDirPath,self.manager.optimalMatchingDict[botName])
        self.optimalEngine = None
    #get the optimal move in order to defeat the bot
    def getOptimalMove(self,board):
        #spin up and store the optimal opponent engine if applicable
        if self.optimalEngine is None:
            self.optimalEngine = chess.engine.SimpleEngine.popen_uci(self.optimalOpponentEnginePath)
        #using the knowledge base of known bot strengths, pick the optimal opponent for it and play out the game from there
        return self.optimalEngine.play(board, chess.engine.Limit(time=self.manager.timeOutInMS)).move