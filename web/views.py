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
	if len(model)==1 and model[0]=="neural":
		print "Only Neural Selected"
	else:
		print("Fetching Dataset")
		xTrain,yTrain,xTest,yTest=fetch_data(file,period)
	# neuralNetwork(xTrain,yTrain,xTest,yTest)
	models={"neural":neuralNetwork,"linear":reg_linear,"svm":reg_svm,"lasso":reg_lassolars,"theilsen":reg_theilsen,"ard":reg_ard}
	accu={"neural":0.0,"linear":0.0,"svm":0.0,"lasso":0.0,"theilsen":0.0,"ard":0.0}
	pred={"neural":[],"linear":[],"svm":[],"lasso":[],"theilsen":[],"ard":[]}
	mse={"neural":0.0,"linear":0.0,"svm":0.0,"lasso":0.0,"theilsen":0.0,"ard":0.0}
	print period
	
	for x in range(len(model)):
		print model[x]
		#print models[model[x]]
		if model[x]=="neural":
			mse[model[x]],accu[model[x]],pred[model[x]],act=models[model[x]](file,period)
		else:
			mse[model[x]],accu[model[x]],pred[model[x]],act=models[model[x]](xTrain,yTrain,xTest,yTest)
		
		print "MSE: "+str(mse[model[x]]),"ACC :"+str(accu[model[x]])+"\n"
		

	
	#neuralNetwork(file,period)
	
	return render(request, "output.html", {"image_dir":'/static/'})

