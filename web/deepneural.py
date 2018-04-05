#! /usr/bin/python

import visualizer
import math
import statistics
import numpy as np
import xlrd
import os
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import FullConnection
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error

# Neural Network load forecasting
def neuralNetwork(file,days):
 

  xData=[]
  yData=[]
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  book = xlrd.open_workbook("%s\media\uploadedfile\%s"%(BASE_DIR,file))
  sheet = book.sheet_by_index(0)
  for rx in range(1,sheet.nrows):
      #row = sheet.row(rx)[3:]
      #row = [row[x].value for x in range(0,len(row)-4)]
      row = sheet.row(rx)[1:12] #including temps
      rowy=sheet.row(rx)[12] #total of next day
      row = [row[x].value for x in range(0,len(row))]
      rowy=rowy.value
      xData.append(row)
      yData.append(rowy)
  #print (xData)
  #print (yData)
  cu=len(xData)-720
  cutoff = len(xData)-days
  #print(cutoff)
  xTrain = xData[cu:cutoff]
  
  yTrain = yData[cu:cutoff]
  xTest = xData[cutoff:]
  yTest = yData[cutoff:]
  # Fill in missing values denoted by zeroes as an average of
  # both neighbors
  statistics.estimateMissing(xTrain,0.0)
  statistics.estimateMissing(xTest,0.0)

  xTrain = [[math.log(y) for y in x] for x in xTrain]
  xTest = [[math.log(y) for y in x] for x in xTest]
  yTrain = [math.log(x) for x in yTrain]

  # Detrend the time series
  indices = np.arange(len(xData))
  #print ('ho')
  #print (indices)
  trainIndices = indices[cu:cutoff]
  testIndices = indices[cutoff:]
  detrended,slope,intercept = statistics.detrend(trainIndices,yTrain)
  yTrain = detrended

  dimensions = [7,8,10,11]
  neurons = [300,500,500,500]

  names = []
  for x in range(len(dimensions)):
    s = "d=" + str(dimensions[x]) + ",h=" + str(neurons[x])
    names.append(s)
  preds = []
  trendedPred=[]
  accu=[]
  mse=[]
  for x in range(len(dimensions)):

    # Perform dimensionality reduction on the feature vectors
    pca = PCA(n_components=dimensions[x])
    pca.fit(xTrain)
    xTrainRed = pca.transform(xTrain)
    xTestRed = pca.transform(xTest)

    pred = fit_predict(xTrainRed,yTrain,xTestRed,100,neurons[x])

    # Add the trend back into the predictions
    temp1 = statistics.reapplyTrend(testIndices,pred,slope,intercept)
    # Reverse the normalization
    trendedPred.append([math.exp(z) for z in temp1])
    # Compute the NRMSE
    err = statistics.normRmse(yTest,trendedPred[x])
    err2=statistics.mape(yTest,trendedPred[x])
    accu.append((1-err2)*100)
    mse.append(math.pow(err,2))
    # Append computed predictions to list for classifier predictions
    preds.append(trendedPred[x])
    print("Error Rate :"+str(err2)+"\n\n")
  #  print "The NRMSE for the neural network is " + str(err) + "..."
  #  print "The %Accuracy for the neural network is " + str((1-err2)*100) + "...\n"
  max_val=max(accu) 
  index_max=accu.index(max_val)
  return mse[index_max],accu[index_max],trendedPred[index_max],yTest
  '''
  preds.append(yTest)
  names.append("actual")

  visualizer.comparisonPlot(2014,1,1,preds,names,plotName="Neural Network Load Predictions vs. Actual", 
        yAxisName="Predicted Kilowatts")
  '''
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


