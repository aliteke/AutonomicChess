#this module contains all code relevant to the autonomicChessManager object
class autonomicChessManager:
    #the initialization function for the autonomicChessManager
    #take in a path for the optimalMoveGenerator, a path for the directory containing the engine(s) for testing
    def __init__(self,optimalEnginePath,testEnginePath,manager):
        #these parameters are then used to generate an optimalMoveGenerator, a set of botDetectors, and a set of botDefeators
        #an internal paramter is additionally used to store whether the bot has been found
        pass

    #this function returns the next move which will be made on the gameboard
    def makeNextMove(self,gameBoard, timeOutInMS):
        #see if the bot has been found
            #if so attempt to execute the bot Defeator on it
            #if the defeator cannot find a solution either play a few optimal rounds or just surrender

        #if bot has not been found play an optimal move and then re-evaluate the different bots

        #this is where we could also consier which moves would offer the highest level of entropy in splitting the bots (not applied at this time)
        
        pass