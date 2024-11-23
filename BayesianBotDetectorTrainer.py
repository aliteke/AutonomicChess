import pandas as pd
import os

class bayesianBotDetectorTrainer:

    #initialize the detector trainer
    def __init__(self,manager,pathToTrainingData,Detectors):
        #store references to everything
        self.manager = manager
        self.pathToTrainingData = pathToTrainingData
        self.Detectors = Detectors

    #this function will train all of the detectors
    def trainAllDetectors(self):
        Detectors = self.Detectors
        #first we will take the detectors
        #for detector in Detectors:
        for detector in Detectors:
            #using data from the CCRL dataset we will 
            for detector in Detectors:
                name = detector.botName
                directory = os.path.join(os.path.dirname(os.path.realpath(__file__)),"train")
                for path, folders, files in os.walk(directory):
                    for file in files:
                        if name in file and 'moves' in file and '.csv' in file:
                            df = pd.read_csv(os.path.join(directory, file))
                            print(df.head)
                            #next we will throw this to a df
                            #train the detector
                            detector.train(df)

                #visualize



