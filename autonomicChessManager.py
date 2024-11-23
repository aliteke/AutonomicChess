import os
from botDefeator import botDefeator
from botDetector import botDetector
from optimalMoveGenerator import optimalMoveGenerator
import pandas as pd
#this module contains all code relevant to the autonomicChessManager object
class autonomicChessManager:
    #the initialization function for the autonomicChessManager
    #take in a path for the optimalMoveGenerator, a path for the directory containing the engine(s) for testing
    def __init__(self,optimalEnginePath,testEngineDirPath,timeOutInMS,optimalMatchingDict):
        #these parameters are then used to generate an optimalMoveGenerator, a set of botDetectors, and a set of botDefeators
        self.optimalEnginePath = optimalEnginePath
        self.detectorsList = []
        self.defeatorsList = []
        self.optimalMatchingDict = optimalMatchingDict
        self.detectedEngineIndex = None
        self.engineDetected = "N/A"

        #initialiaze the searchDepth as the depth at which a search with 60 moves per layer will take ~1 min
        searchDepth =  60000 / timeOutInMS * 60
        #iterate over files in the directory
        #store each detector's similarity index over time to create a plot
        self.plot_x = []
        self.plot_y_lists = []
        for filename in os.listdir(testEngineDirPath):
            engineFilePath = os.path.join(testEngineDirPath, filename)
            # checking if it is a file
            if os.path.isfile(engineFilePath):
                #generate the detect and defeat files
                print("generating detect and defeat for", engineFilePath)
                self.detectorsList.append(botDetector(filename,engineFilePath,self))
                self.defeatorsList.append(botDefeator(filename,testEngineDirPath,self))
                self.plot_y_lists.append([])
        self.initialNumberOfBotsConsidered = len(self.detectorsList)
        #finally initialize the optimalMovesGenerator
        self.optimalMoveGenerator = optimalMoveGenerator(optimalEnginePath,self)
        
        #store the timeout
        self.timeOutInMS = timeOutInMS
        #an internal parameter is additionally used to store whether the bot has been found
        self.DetectionConfidenceScore = 0.0
        
        

    #this function returns the next move which will be made on the gameboard
    def makeNextMove(self,gameBoard):
        #see if the bot has been found
        if self.DetectionConfidenceScore < 1 or len(gameBoard.move_stack) < 15:
            #track the highest and second highest bot detection scores
            highestBotDetectorScore = 0.0
            secondHighestBotDetectorScore = 0.0
            self.plot_x.append(len(gameBoard.move_stack))
            for count, possibleBotDetector in enumerate(self.detectorsList):
                #update the detection scores with a copy of the board
                possibleBotDetector.updateCouldOpponentBeThisBot(gameBoard.copy())
                if(possibleBotDetector.matchingScore > highestBotDetectorScore):
                    highestBotDetectorScore = possibleBotDetector.matchingScore
                    self.detectedEngineIndex = count
                elif(possibleBotDetector.matchingScore > secondHighestBotDetectorScore):
                    secondHighestBotDetectorScore = possibleBotDetector.matchingScore
                self.plot_y_lists[count].append(possibleBotDetector.matchingScore)
            
            # we should also calculate the average detector score
            averageDetectorScore = sum([detector.matchingScore for detector in self.detectorsList]) / len(self.detectorsList)

            #now update the detector score to reflect overall system confidence in the level of detection
            #the detection confidence will be set as the difference between the highest confidence bot and the second highest *5
            self.DetectionConfidenceScore = (highestBotDetectorScore - secondHighestBotDetectorScore) * 5

            print("on turn ",len(gameBoard.move_stack),"detection confidence score is",self.DetectionConfidenceScore,"could be",[det.botName for det in self.detectorsList])

        else:
            if self.engineDetected == "N/A":
                self.engineDetected = self.defeatorsList[self.detectedEngineIndex].botName
            return self.defeatorsList[self.detectedEngineIndex].getOptimalMove(gameBoard)
            #if so attempt to execute the bot Defeator on it
            #if the defeator cannot find a solution either play a few optimal rounds or just surrender
        

        #if bot has not been found play an optimal move and then re-evaluate the different bots
        return self.optimalMoveGenerator.getOptimalMove(gameBoard)
        #this is where we could also consier which moves would offer the highest level of entropy in splitting the bots (not applied at this time)