import numpy as np
from sklearn import linear_model
from sklearn import svm
import pandas as pd
import quandl,math
import numpy as np
import statistics
import xlrd

##SVM
def reg_svm(xTrain,yTrain,xTest,yTest):
    xData=[]
    yData=[]
    print "SVM"
    clf = svm.SVR(kernel='linear')        
    clf.fit(xTrain,yTrain)
    pred=clf.predict(xTest)
    err2=statistics.mape(pred,yTest)
    mse=math.pow(statistics.normRmse(pred,yTest),2)
    accu=(1-err2)*100
    print("Error Rate :"+str(err2)+"\n\n")
    return mse,accu,pred,yTest
##LassoLars
def reg_lassolars(xTrain,yTrain,xTest,yTest):
    xData=[]
    yData=[]
    print "Lasso"
    clf = linear_model.LassoLars()        
    clf.fit(xTrain,yTrain)
    pred=clf.predict(xTest)
    err2=statistics.mape(pred,yTest)
    mse=math.pow(statistics.normRmse(pred,yTest),2)
    accu=(1-err2)*100
    print("Error Rate :"+str(err2)+"\n\n")
    return mse,accu,pred,yTest
##ARD
def reg_ard(xTrain,yTrain,xTest,yTest):
    xData=[]
    yData=[]
    print "ARD"
    clf = linear_model.ARDRegression()        
    clf.fit(xTrain,yTrain)
    pred=clf.predict(xTest)
    err2=statistics.mape(pred,yTest)
    mse=math.pow(statistics.normRmse(pred,yTest),2)
    accu=(1-err2)*100
    print("Error Rate :"+str(err2)+"\n\n")
    return mse,accu,pred,yTest
##Theilsen
def reg_theilsen(xTrain,yTrain,xTest,yTest):
    xData=[]
    yData=[]
    print "Theilsen"
    clf = linear_model.TheilSenRegressor()       
    clf.fit(xTrain,yTrain)
    pred=clf.predict(xTest)
    err2=statistics.mape(pred,yTest)
    mse=math.pow(statistics.normRmse(pred,yTest),2)
    accu=(1-err2)*100
    print("Error Rate :"+str(err2)+"\n\n")
    return mse,accu,pred,yTest
##Linear Reg
def reg_linear(xTrain,yTrain,xTest,yTest):
    xData=[]
    yData=[]
    print "Linear Regression"
    clf = linear_model.LinearRegression()       
    clf.fit(xTrain,yTrain)
    pred=clf.predict(xTest)
    err2=statistics.mape(pred,yTest)
    mse=math.pow(statistics.normRmse(pred,yTest),2)
    accu=(1-err2)*100
    print("Error Rate :"+str(err2)+"\n\n")
    return mse,accu,pred,yTest
