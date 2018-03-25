# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from neural_without import neuralNetwork
import matplotlib.pyplot as plt
import numpy as np
import os

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
	#file = request.FILES['file']
	file = request.FILES.get("file")
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	print BASE_DIR
	print file.name
	print type(file),file
	test_perc = request.POST.get("test_perc", "default")
	print test_perc

	neuralNetwork(file,test_perc);
	# today = "tuesday"
	# t = np.arange(0.0, 2.0, 0.01)
	# s = 1 + np.sin(2*np.pi*t)
	# plt.plot(t, s)

	# plt.xlabel('time (s)')
	# plt.ylabel('voltage (mV)')
	# plt.title('About as simple as it gets, folks')
	# plt.grid(True)
	# plt.savefig("test.png")
	# plt.show()

	return render(request, "output.html", {"image_dir":BASE_DIR})

