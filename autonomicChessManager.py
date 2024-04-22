import os
from botDefeator import botDefeator
from botDetector import botDetector
from optimalMoveGenerator import optimalMoveGenerator
#this module contains all code relevant to the autonomicChessManager object
class autonomicChessManager:
    #the initialization function for the autonomicChessManager
    #take in a path for the optimalMoveGenerator, a path for the directory containing the engine(s) for testing
    def __init__(self,optimalEnginePath,testEngineDirPath,timeOutInMS):
        #these parameters are then used to generate an optimalMoveGenerator, a set of botDetectors, and a set of botDefeators
        self.optimalEnginePath = optimalEnginePath
        self.detectorsList = []
        self.defeatorsList = []
        #initialiaze the searchDepth as the depth at which a search with 60 moves per layer will take ~1 min
        searchDepth =  60000 / timeOutInMS * 60
        #iterate over files in the directory
        for filename in os.listdir(testEngineDirPath):
            engineFilePath = os.path.join(testEngineDirPath, filename)
            # checking if it is a file
            if os.path.isfile(engineFilePath):
                #generate the detect and defeat files
                print("generating detect and defeat for", engineFilePath)
                self.detectorsList.append(botDetector(filename,engineFilePath,self))
                self.defeatorsList.append(botDefeator(filename,engineFilePath,searchDepth,self))
                
        #finally initialize the optimalMovesGenerator
        self.optimalMoveGenerator = optimalMoveGenerator(optimalEnginePath,self)
        #store the timeout
        self.timeOutInMS = timeOutInMS
        #an internal parameter is additionally used to store whether the bot has been found
        self.DetectionConfidenceScore = 0.0

    #this function returns the next move which will be made on the gameboard
    def makeNextMove(self,gameBoard):
        #see if the bot has been found
            #if so attempt to execute the bot Defeator on it
            #if the defeator cannot find a solution either play a few optimal rounds or just surrender

        #if bot has not been found play an optimal move and then re-evaluate the different bots
        return self.optimalMoveGenerator.getOptimalMove(gameBoard)
        #this is where we could also consier which moves would offer the highest level of entropy in splitting the bots (not applied at this time)

        pass