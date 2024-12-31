import chess
import chess.engine
# this module will contain a "botDetector object"
class botDetector:
    
    #initialize the bot detector to detect on a set bot
    def __init__(self,botName,botOfInterestPath,manager,numAttemptsPerEval):
        self.botOfInterestPath = botOfInterestPath
        self.couldOpponentBeThisBot = True
        self.matchingScore = None
        self.previousMatchingScore = None
        self.numberOfMovesEvaluated = 0     #1         #TODO: shouldn't this start from 0?
        self.botName = botName
        self.manager = manager
        #we will take 10 attempts to evaluate if this move could have been made by this engine
        self.numAttemptsPerEval = numAttemptsPerEval
        #initialize the engine and store it
        self.botOfInterest = chess.engine.SimpleEngine.popen_uci(botOfInterestPath)
        self.pid = self.botOfInterest.transport.get_pid()

    #use the most recent move to update whether the opponent could be this board
    def updateCouldOpponentBeThisBot(self, testBoard):
        #only run if this detector is still in the running
        if(self.couldOpponentBeThisBot):
            numMatching = 0
            #pop the last move
            lastMoveMade = testBoard.pop()
            for i in range(0,self.numAttemptsPerEval):
                #run the chess engine for the test board, if the last move wouldn't have been taken eliminate the bot from consideration
                try:
                    botsChoice = self.botOfInterest.play(testBoard, chess.engine.Limit(time=self.manager.timeOutInMS)).move
                except TimeoutError:
                    print(f"DEBUG: {self.botName} (PID: {self.pid}) timed out on move {i}!")
                    continue
                #TODO: DEBUGGING
                #print(f"DEBUG: [+{i}+] {self.botName} would have played {botsChoice.uci()} instead of {lastMoveMade.uci()}")
                #print("opponents last move was",lastMoveMade.uci(),self.botName,"would have done",botsChoice.uci())
                if botsChoice.uci() == lastMoveMade.uci():
                    self.couldOpponentBeThisBot = True    
                    numMatching +=1
            #update matching score
            if self.matchingScore is None:
                self.matchingScore = (numMatching/self.numAttemptsPerEval)
            else:
                # TODO: this formula might need to be adjusted. At the moment, it is favoring the earlier moves better than the more recent ones.
                #       i.e. if the matchingScore for the first move is 0.69, and the matching score for the second move is 1.0: plain average would be 0.84; this formula evaluates to 0.79.
                #       In a game would it be more important to get similar move when the game has progressed more or at the beginning? If the latter, then this formula is fine.
                self.previousMatchingScore = self.matchingScore
                self.matchingScore = (self.matchingScore * self.numberOfMovesEvaluated + (numMatching/self.numAttemptsPerEval))/(self.numberOfMovesEvaluated + 1)

        self.numberOfMovesEvaluated +=1
        print(f"DEBUG: {self.botName} (PID: {self.pid}), #matching: {numMatching}/{self.numAttemptsPerEval}, \
              previous_matchingScore: {self.previousMatchingScore}, \
                running_matchingScore: {self.matchingScore}, \
                    numberOfMovesEvaluated: {self.numberOfMovesEvaluated}")
        