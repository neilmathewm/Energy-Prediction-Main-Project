import xlrd
import os
def fetch_data(file,days):
    xData=[]
    yData=[]
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    book = xlrd.open_workbook("%s\media\uploadedfile\%s"%(BASE_DIR,file))
    sheet = book.sheet_by_index(0)
    for rx in range(1,sheet.nrows):
        row = sheet.row(rx)[1:12] #including temps
        rowy=sheet.row(rx)[12] #total of next day
        row = [row[x].value for x in range(0,len(row))]
        rowy=rowy.value
        xData.append(row)
        yData.append(rowy)
    print "Days",days
    cu=len(xData)-720
    cutoff = len(xData)-days
    print(cutoff)
    xTrain = xData[cu:cutoff]
    yTrain = yData[cu:cutoff]
    xTest = xData[cutoff:]
    yTest = yData[cutoff:]
    return xTrain,yTrain,xTest,yTest
