import chess
import chess.engine
# this module will contain a "botDetector object"
class botDetector:
    
    #initialize the bot detector to detect on a set bot
    def __init__(self,botName,botOfInterestPath,manager):
        self.botOfInterestPath = botOfInterestPath
        self.couldOpponentBeThisBot = True
        self.matchingScore = None
        self.numberOfMovesEvaluated = 1
        self.botName = botName
        self.manager = manager
        #we will take 10 attempts to evaluate if this move could have been made by this engine
        self.numAttemptsPerEval = 10
        #initialize the engine and store it
        self.botOfInterest = chess.engine.SimpleEngine.popen_uci(botOfInterestPath)

    #use the most recent move to update whether the opponent could be this board
    def updateCouldOpponentBeThisBot(self, testBoard):
        #only run if this detector is still in the running
        if(self.couldOpponentBeThisBot):
            
            numMatching = 0
            #pop the last move
            peekAtLastMove = testBoard.peek()
            lastMoveMade = testBoard.pop()
            for i in range(0,self.numAttemptsPerEval):
                #run the chess engine for the test board, if the last move wouldn't have been taken eliminate the bot from consideration
                botsChoice = self.botOfInterest.play(testBoard, chess.engine.Limit(time=self.manager.timeOutInMS)).move
                #print("opponents last move was",lastMoveMade.uci(),self.botName,"would have done",botsChoice.uci())
                if botsChoice.uci() == lastMoveMade.uci():
                    self.couldOpponentBeThisBot = True    
                    numMatching +=1
            #update matching score
            if self.matchingScore is None:
                self.matchingScore = (numMatching/self.numAttemptsPerEval)
            else:
                self.matchingScore = (self.matchingScore * self.numberOfMovesEvaluated + (numMatching/self.numAttemptsPerEval))/(self.numberOfMovesEvaluated + 1)
            print(self.botName,self.matchingScore)
            #if the confidence score is under a certain threshold and we have played a sufficient number of moves, eliminate the detector
            #if self.numberOfMovesEvaluated > 9 and self.matchingScore < 0.5:
            #    print("the bot is not",self.botName)
            #    self.couldOpponentBeThisBot = False
            
        
        
        self.numberOfMovesEvaluated +=1
        pass
