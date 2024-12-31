import os
from botDefeator import botDefeator
from botDetector import botDetector
from optimalMoveGenerator import optimalMoveGenerator
import pandas as pd
import numpy as np

#this module contains all code relevant to the autonomicChessManager object
class autonomicChessManager:
    #the initialization function for the autonomicChessManager
    #take in a path for the optimalMoveGenerator, a path for the directory containing the engine(s) for testing
    def __init__(self,optimalEnginePath,testEngineDirPath,timeOutInMS,optimalMatchingDict,numAttemptsPerEval):
        #these parameters are then used to generate an optimalMoveGenerator, a set of botDetectors, and a set of botDefeators
        self.optimalEnginePath = optimalEnginePath
        self.detectorsList = []
        self.defeatorsList = []
        self.optimalMatchingDict = optimalMatchingDict
        self.numAttemptsPerEval = numAttemptsPerEval
        self.detectedEngineIndex = None
        self.secondHighestEngineIndex = None
        self.engineDetected = "N/A"
        #store the timeout
        self.timeOutInMS = timeOutInMS
        #an internal parameter is additionally used to store whether the bot has been found
        self.DetectionConfidenceScore = 0.0
        #store each detector's similarity index over time to create a plot
        self.plot_x = []
        self.plot_y_lists = []
        #TODO: store the confidence score, 

        #initialiaze the searchDepth as the depth at which a search with 60 moves per layer will take ~1 min
        searchDepth =  60000 / timeOutInMS * 60     #TODO: This is not used...
        #iterate over files in the directory

        for filename in os.listdir(testEngineDirPath):
            engineFilePath = os.path.join(testEngineDirPath, filename)
            # checking if it is a file
            if os.path.isfile(engineFilePath):
                #generate the detect and defeat files
                print(f"[+] Generating detect and defeat for: {filename}")
                self.detectorsList.append(botDetector(filename,engineFilePath,self,self.numAttemptsPerEval))
                self.defeatorsList.append(botDefeator(filename,testEngineDirPath,self))
                self.plot_y_lists.append([])
        self.initialNumberOfBotsConsidered = len(self.detectorsList)
        #finally initialize the optimalMovesGenerator
        self.optimalMoveGenerator = optimalMoveGenerator(optimalEnginePath,self)
        
    #this function returns the next move which will be made on the gameboard
    def makeNextMove(self,gameBoard, opponentName):
        #see if the bot has been found
        if self.DetectionConfidenceScore < 1 or len(gameBoard.move_stack) < 15:
            #track the highest and second highest bot detection scores
            highestBotDetectorScore = 0.0
            secondHighestBotDetectorScore = 0.0
            self.plot_x.append(len(gameBoard.move_stack))
            for count, possibleBotDetector in enumerate(self.detectorsList):
                #update the detection scores with a copy of the board
                possibleBotDetector.updateCouldOpponentBeThisBot(gameBoard.copy())
                """if(possibleBotDetector.matchingScore > highestBotDetectorScore):
                    highestBotDetectorScore = possibleBotDetector.matchingScore
                    self.detectedEngineIndex = count
                elif(possibleBotDetector.matchingScore > secondHighestBotDetectorScore):
                    secondHighestBotDetectorScore = possibleBotDetector.matchingScore
                """
                self.plot_y_lists[count].append(possibleBotDetector.matchingScore)

            # TODO: there is a bug in the above if-else determining the highest and second highest bot detection scores.
            #       Here is an attempt to fix it:
            sorted_det_scores = sorted( [ det_scores[-1] for det_scores in self.plot_y_lists ] )
            highestBotDetectorScore = sorted_det_scores[-1]
            secondHighestBotDetectorScore = sorted_det_scores[-2]
            
            self.detectedEngineIndex = [ det_scores[-1] for det_scores in self.plot_y_lists ].index(highestBotDetectorScore)
            self.secondHighestEngineIndex = [ det_scores[-1] for det_scores in self.plot_y_lists ].index(secondHighestBotDetectorScore)

            min_score = np.min( sorted_det_scores )
            max_score = np.max( sorted_det_scores )
            std_dev = np.std( sorted_det_scores )
            threshold = np.percentile( sorted_det_scores, 85 )

            # we should also calculate the average detector score
            averageDetectorScore = sum([detector.matchingScore for detector in self.detectorsList]) / len(self.detectorsList)

            #now update the detector score to reflect overall system confidence in the level of detection
            #the detection confidence will be set as the difference between the highest confidence bot and the second highest *5
            self.DetectionConfidenceScore = (highestBotDetectorScore - secondHighestBotDetectorScore) * len(self.detectorsList)

            print("DEBUG: on turn: ", len(gameBoard.move_stack),
            " confidence_score: ",self.DetectionConfidenceScore, 
            f" highestBotDetectorScore ({self.defeatorsList[self.detectedEngineIndex].botName}): ", highestBotDetectorScore,
            f" secondHighestBotDetectorScore({self.defeatorsList[self.secondHighestEngineIndex].botName}): ", secondHighestBotDetectorScore,
            " averageDetectorScore:", averageDetectorScore,
            " min_score:", min_score, " max_score:", max_score, " std_dev:", std_dev, " threshold:", threshold, " #above_threshold:", len([score for score in sorted_det_scores if score > threshold]))
            #" ploy_y_lists: ", self.plot_y_lists)   #"could be",[det.botName for det in self.detectorsList])

        else:
            if self.engineDetected == "N/A":
                self.engineDetected = self.defeatorsList[self.detectedEngineIndex].botName
                print("DEBUG: engine detected as", self.engineDetected)
            print(f"DEBUG: bot defeator engine {self.engineDetected} is playing:")
            return self.defeatorsList[self.detectedEngineIndex].getOptimalMove(gameBoard)
            #if so attempt to execute the bot Defeator on it
            #if the defeator cannot find a solution either play a few optimal rounds or just surrender        

        #if bot has not been found play an optimal move and then re-evaluate the different bots
        return self.optimalMoveGenerator.getOptimalMove(gameBoard)
        #this is where we could also consier which moves would offer the highest level of entropy in splitting the bots (not applied at this time)