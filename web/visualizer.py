import datetime
import pandas
import numpy as np
import matplotlib.pyplot as plt
from pandas.tools.plotting import autocorrelation_plot
from pandas.tools.plotting import lag_plot
from scipy import signal
import os

'''
Module for time series visualization
'''

# Plots the (x,y) data using matplotlib with the given labels
def yearlyPlot(ySeries,year,month,day,plotName ="Plot",yAxisName="yData"):

	date = datetime.date(year,month,day)
	dateList = []
	for x in range(len(ySeries)):
		dateList.append(date+datetime.timedelta(days=x))

	plt.plot_date(x=dateList,y=ySeries,fmt="r-")
	plt.title(plotName)
	plt.ylabel(yAxisName)
	plt.xlabel("Date")
	plt.grid(True)
        plt.savefig("output.png")
	plt.show()
	

# Plots autocorrelation factors against varying time lags for ySeries
def autoCorrPlot(ySeries,plotName="plot"):
	plt.figure()
	plt.title(plotName)
	data = pandas.Series(ySeries)
	autocorrelation_plot(data)
        plt.savefig("output.png")
	plt.show()

# Displays lag plot to determine whether time series data is non-random
def lagPlot(ySeries,plotName="plot"):
	plt.figure()
	plt.title(plotName)
	data = pandas.Series(ySeries)
	lag_plot(data, marker='2', color='green')
        plt.savefig("output.png")
	plt.show()
# Displays periodogram of the given time series <ySeries>
def periodogramPlot(ySeries,plotName="Plot",xAxisName="Frequency",yAxisName="Frequency Strength"):
	trans = signal.periodogram(ySeries)
	plt.title(plotName)
	plt.xlabel(xAxisName)
	plt.ylabel(yAxisName)
	plt.plot(trans[0], trans[1], color='green')
	plt.show()
	plt.savefig("output.png")

# Plots two time series on the same timeScale from a common date on the same plot
def comparisonPlot(year,month,day,seriesList,nameList,plotName="Comparison of Values over Time", yAxisName="Predicted"):
	print "inside ploting comparisonPlot"
	date = datetime.date(year,month,day)
	dateList = []
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	for x in range(len(seriesList[0])):
		dateList.append(date+datetime.timedelta(days=x))
	colors = ["b","g","r","c","m","y","k","w"]
	currColor = 0
	legendVars = []
	for i in range(len(seriesList)):
		x, = plt.plot_date(x=dateList,y=seriesList[i],color=colors[currColor],linestyle="-",marker=".")
		legendVars.append(x)
		currColor += 1
		if (currColor >= len(colors)):
			currColor = 0
	plt.legend(legendVars, nameList)
	plt.title(plotName)
	plt.ylabel(yAxisName)
	plt.xlabel("Date")
	plt.savefig(BASE_DIR+"\\static\\images\\output1.png")
	#plt.savefig("output.png")
	#plt.show()
	
def exectimeplot(times,name):	
	print "inside exectimeplot"
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	fig, ax = plt.subplots()
	print len(name),len(times),"length"
	print name,times
	ind  = np.arange(1, len(name)+1)
	plt.bar(ind, times)
	ax.set_xticks(ind)
	ax.set_xticklabels(name)
	ax.set_ylim([0,max(times)+1])
	ax.set_ylabel('Time in sec')
	ax.set_title('Comparison of Execution Time')
	plt.savefig(BASE_DIR+"\\static\\images\\output2.png")
	#plt.show()