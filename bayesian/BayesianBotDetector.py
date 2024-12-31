#relevant imports
import chess
import chess.engine
import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import BDeuScore, K2Score, BicScore
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.estimators import HillClimbSearch

# this module will contain a "bayesianBotDetector object"
class bayesianBotDetector:
    
    #initialize the bot detector to detect on a set bot
    def __init__(self,botName,botOfInterestPath,manager,numAttemptsPerEval=30):
        self.botOfInterestPath = botOfInterestPath
        self.couldOpponentBeThisBot = True
        self.matchingScore = None
        self.numberOfMovesEvaluated = 1
        self.botName = botName
        self.manager = manager
        #we will take 10 attempts to evaluate if this move could have been made by this engine
        self.numAttemptsPerEval = numAttemptsPerEval
        #initialize the engine and store it
        #self.botOfInterest = chess.engine.SimpleEngine.popen_uci(botOfInterestPath)
        #initialize the model to be empty
        self.model = BayesianNetwork()

    #this function will be used in order to train the Bayesian Bot Detector
    def train(self, trainDf):
        #this function will simply wake the pre-defined model and fit it using the trainDf provided
        #get the model structure
        #hc = HillClimbSearch(trainDf)
        #best_model = hc.estimate(scoring_method=BicScore(trainDf))
        #print(best_model.edges())    
        #self.model = BayesianNetwork(best_model)
        #add edges for the model to support the relations among the variables as expected
        self.model.add_nodes_from(trainDf.columns)
        self.model.add_edges_from([('move_no', 'player'), ('from_square', 'player'),('to_square', 'player'),('piece', 'player')])
        # Add the CPDs to the model
        #self.model.add_cpds(*cpds)
        self.model.fit(trainDf)
        print(self.model.get_cpds())
    
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
            #print(self.botName,self.matchingScore)
            
        
        
        self.numberOfMovesEvaluated +=1
        pass
