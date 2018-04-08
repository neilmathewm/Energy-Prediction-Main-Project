# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import numpy as np
import os
from models import Document
from forms import DocumentForm
from regression import reg_linear,reg_svm,reg_lassolars,reg_theilsen,reg_ard
from deepneural import neuralNetwork
from createdata import fetch_data
import visualizer
import time
# Create your views here.
def hello(request):
   text = """<h1>welcome to my app !</h1>"""
   return HttpResponse(text)

def test(request, number):
   
   text = "<h1>welcome to my app number %s!</h1>"% number
   return HttpResponse(text)

def passval(request):
   today = "tuesday"
   return render(request, "param.html", {"today" : today})

def main(request):
   today = "tuesday"
   return render(request, "index.html", {})

def some(request):
	return render(request,"index.html",{})


def predict(request):

	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	file = request.FILES.get("file")
	print request.POST,request.FILES #print requests
	#get post parameters
	period = int(request.POST.get("period", "default"))
	model = request.POST.getlist("model", "default")

	form = DocumentForm(request.FILES)
	##path to save
	print BASE_DIR+"\\media\\uploadedfile\\"+file.name
	if(os.path.isfile(BASE_DIR+"\\media\\uploadedfile\\"+file.name)):
		print "file exist"
		os.remove(BASE_DIR+"\\media\\uploadedfile\\"+file.name)
		print "old file removed"
	else:
		print "file not present"

	newdoc = Document(docfile = request.FILES['file'])
	newdoc.save()
	print "file saved successfully"

	##Fetch data
	if len(model)==1 and model[0]=="Neural":
		print "Only Neural Selected"
	else:
		print("Fetching Dataset")
		fetchtime=time.time()
		xTrain,yTrain,xTest,yTest=fetch_data(file,period)
		fetchtime=time.time()-fetchtime
		print("Time to fetch"+str(fetchtime))
	# neuralNetwork(xTrain,yTrain,xTest,yTest)
	models={"Neural":neuralNetwork,"Linear Regression":reg_linear,"SVM":reg_svm,"Lasso-Lars Regression":reg_lassolars,"Theilsen Regression":reg_theilsen,"ARD":reg_ard}
	accu={"Neural":0.0,"Linear Regression":0.0,"SVM":0.0,"Lasso-Lars Regression":0.0,"Theilsen Regression":0.0,"ARD":0.0}
	pred={"Neural":[],"Linear Regression":[],"SVM":[],"Lasso-Lars Regression":[],"Theilsen Regression":[],"ARD":[]}
	mse={"Neural":0.0,"Linear Regression":0.0,"SVM":0.0,"Lasso-Lars Regression":0.0,"Theilsen Regression":0.0,"ARD":0.0}
	print period
	obj = []
	preds = []
	names = []
	name2=[]
	times=[]
	for x in range(len(model)):
		print model[x]
		
		#print models[model[x]]
		if model[x]=="Neural":
			strt_time=time.time()
			mse[model[x]],accu[model[x]],pred[model[x]],act=models[model[x]](file,period)
			times.append(time.time()-strt_time-fetchtime)
		else:
			strt_time=time.time()
			mse[model[x]],accu[model[x]],pred[model[x]],act=models[model[x]](xTrain,yTrain,xTest,yTest)
			times.append(time.time()-strt_time)

		obj.append({'model':model[x],'mse':mse[model[x]],'accu':accu[model[x]],'time':times[x]})
		print "MSE: "+str(mse[model[x]]),"ACC :"+str(accu[model[x]])+"\n"
		preds.append(pred[model[x]])
		names.append(model[x])
		name2.append(model[x])
		
	preds.append(act)
	names.append("Actual")
	print obj
	print times
	#print preds,names
	#neuralNetwork(file,period)
	imgurl=BASE_DIR+"\\media\\images\\output1.png"
	visualizer.comparisonPlot(2014,1,1,preds,names,plotName="Comparison of Models based on the Predicted Load", 
        yAxisName="Predicted Kilowatts")

	visualizer.exectimeplot(times,name2)
	return render(request, "output.html", {'obj':obj,'imgurl':imgurl})

