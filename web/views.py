# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from neural_without import neuralNetwork
import matplotlib.pyplot as plt
import numpy as np
import os
from models import Document
from forms import DocumentForm


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


def predict(request):

	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	file = request.FILES.get("file")
	print request.POST,request.FILES #print requests
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

	#get post parameters
	period = request.POST.get("period", "default")
	models={"neural":neuralNetwork(file,period),"linear":"","svm":"","lasso":"","theilsen":"","ard":""}
	
	print period
	model = request.POST.getlist("model", "default")
	for x in range(len(model)):
		print model[x]
		print models[model[x]]
		k,j=models[model[x]]
		print k,j

	
	#neuralNetwork(file,period)
	
	return render(request, "output.html", {"image_dir":'/static/'})

