#! /usr/bin/python

import visualizer
import math
import statistics
import numpy as np
import xlrd
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import FullConnection
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from sklearn.decomposition import PCA
import os

# Neural Network load forecasting
def neuralNetwork(file,test_perc):
  
  # Retrieve time series data & apply preprocessing
  #print tdata
  # 2014 had 365 days, but we take the last 364 days since
  # the last day has no numerical value
  xData=[]
  yData=[]
  print("hello");
  # book = xlrd.open_workbook("data/data_only.xlsx")
  print file
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  book = xlrd.open_workbook("%s\media\uploadedfile\%s"%(BASE_DIR,file))

  sheet = book.sheet_by_index(0)
  for rx in range(1,sheet.nrows-1):
      #row = sheet.row(rx)[3:]
      #row = [row[x].value for x in range(0,len(row)-4)]
      row = sheet.row(rx)[1:50] #including temps
      rowy=sheet.row(rx+1)[49] #total of next day
      row = [row[x].value for x in range(0,len(row)-1)]
      rowy=rowy.value
      xData.append(row)
      yData.append(rowy)
    #print "cutoff"+str(cutoff)
  #print (xData)
  #print (yData)
  cutoff = len(xData)-89
  print(cutoff)
  xTrain = xData[0:cutoff]
  
  #print xTrain[47]
  #print xTrain
  yTrain = yData[0:cutoff]
  xTest = xData[cutoff:]
  #print cutoff
  #print xTest[0]
  yTest = yData[cutoff:]
  print (yTest)
  # Fill in missing values denoted by zeroes as an average of
  # both neighbors
  statistics.estimateMissing(xTrain,0.0)
  statistics.estimateMissing(xTest,0.0)

  xTrain = [[math.log(y) for y in x] for x in xTrain]
  xTest = [[math.log(y) for y in x] for x in xTest]
  yTrain = [math.log(x) for x in yTrain]

  # Detrend the time series
  indices = np.arange(len(xData))
  print ('ho')
  print (indices)
  trainIndices = indices[0:cutoff]
  testIndices = indices[cutoff:]
  detrended,slope,intercept = statistics.detrend(trainIndices,yTrain)
  yTrain = detrended

  dimensions = [6,10,12]
  neurons = [30,50,50]

  names = []
  for x in range(len(dimensions)):
    s = "d=" + str(dimensions[x]) + ",h=" + str(neurons[x])
    names.append(s)

  preds = []

  for x in range(len(dimensions)):

    # Perform dimensionality reduction on the feature vectors
    pca = PCA(n_components=dimensions[x])
    pca.fit(xTrain)
    xTrainRed = pca.transform(xTrain)
    xTestRed = pca.transform(xTest)

    pred = fit_predict(xTrainRed,yTrain,xTestRed,40,neurons[x])

    # Add the trend back into the predictions
    trendedPred = statistics.reapplyTrend(testIndices,pred,slope,intercept)
    # Reverse the normalization
    trendedPred = [math.exp(x) for x in trendedPred]
    # Compute the NRMSE
    err = statistics.normRmse(yTest,trendedPred)
    
    # Append computed predictions to list for classifier predictions
    preds.append(trendedPred)

    print "The NRMSE for the neural network is " + str(err) + "..."
  
  preds.append(yTest)
  names.append("actual")
  return err,trendedPred
  visualizer.comparisonPlot(2014,1,1,preds,names,plotName="Neural Network Load Predictions vs. Actual", 
        yAxisName="Predicted Kilowatts")


# Constructs and fits a neural network with the given number of neurons
# to the training data for the specified number of epochs and returns a 
# vector of the predicted values for the given test data - assumes the target 
# is univariate (e.g. single valued output)
def fit_predict(xTrain,yTrain,xTest,epochs,neurons):

  # Check edge cases
  if (not len(xTrain) == len(yTrain) or len(xTrain) == 0 or 
    len(xTest) == 0 or epochs <= 0):
    return

  # Randomize the training data (probably not necessary but pybrain might
  # not shuffle the data itself, so perform as safety check)
  indices = np.arange(len(xTrain))
  np.random.shuffle(indices)

  trainSwapX = [xTrain[x] for x in indices]
  trainSwapY = [yTrain[x] for x in indices]

  supTrain = SupervisedDataSet(len(xTrain[0]),1)
  for x in range(len(trainSwapX)):
    supTrain.addSample(trainSwapX[x],trainSwapY[x])

  # Construct the feed-forward neural network

  n = FeedForwardNetwork()

  inLayer = LinearLayer(len(xTrain[0]))
  hiddenLayer1 = SigmoidLayer(neurons)
  outLayer = LinearLayer(1)

  n.addInputModule(inLayer)
  n.addModule(hiddenLayer1)
  n.addOutputModule(outLayer)

  in_to_hidden = FullConnection(inLayer, hiddenLayer1)
  hidden_to_out = FullConnection(hiddenLayer1, outLayer)
  
  n.addConnection(in_to_hidden)
  n.addConnection(hidden_to_out)

  n.sortModules() 

  # Train the neural network on the training partition, validating
  # the training progress on the validation partition

  trainer = BackpropTrainer(n,dataset=supTrain,momentum=0.1,learningrate=0.01
    ,verbose=False,weightdecay=0.01)
  
  trainer.trainUntilConvergence(dataset=supTrain,
    maxEpochs=epochs,validationProportion=0.30)

  outputs = []
  for x in xTest:
    outputs.append(n.activate(x))

  return outputs

if __name__ == "__main__":
  neuralNetwork()
