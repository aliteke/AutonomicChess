from BayesianBotDetector import bayesianBotDetector
from BayesianBotDetectorTrainer import bayesianBotDetectorTrainer
import os 

trainPath = directory = os.path.join(os.path.dirname(os.path.realpath(__file__)),"train")
#initialize a single detector for Alexandria
alex_detect = bayesianBotDetector('Alexandria_6_1_0_64-bit',None,None,None)
detectors = [alex_detect]
trainer = bayesianBotDetectorTrainer(None,pathToTrainingData=trainPath,Detectors=detectors)
trainer.trainAllDetectors()
model = alex_detect.model

model_daft = model.to_daft()
# To open the plot
model_daft.render()
# Save the plot
model_daft.savefig('test.png')
