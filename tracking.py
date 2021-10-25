import json
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
import inspect
import numpy as np



"""This file is used in step3 in order to track the abnormal nodes given the output 'tracking/trackingResults.json' 
generated in step3
"""

with open("./tracking/trackingResults.json") as f:
    data = json.loads(f.read())

length = len(data)
numOfRows = 2
numOfColumns = int(length/2) if length % 2 == 0 else int(length/2) + 1

"""Change data stucture"""
parsedData = []
## datumTrack is a list of string
for datumTrack in data:
    parsedDatum = []
    for datum in datumTrack:
        x, y = datum.split(",")
        parsedDatum.append((float(x),float(y)))
    parsedData.append(parsedDatum)

print(parsedData)
tLength = len(parsedData[0])
"""end change data structure"""
xMin = min([item[0] for sublist in parsedData for item in sublist])*0.97
xMax = max([item[0] for sublist in parsedData for item in sublist])*1.03
yMin = min([item[1] for sublist in parsedData for item in sublist])*0.97
yMax = max([item[1] for sublist in parsedData for item in sublist])*1.03

print(xMin, xMax, yMin, yMax)
colors = cm.winter(np.linspace(0.0, 1.0, tLength))

fig = plt.figure(figsize=(4000, 3000))
for index, dataList in enumerate(parsedData):
    ax = fig.add_subplot(numOfRows, numOfColumns, index+1)
    ax.set_xlim((xMin, xMax))
    ax.set_ylim((yMin, yMax))
    # ax.set_color(sns.color_palette("flare", as_cmap=True))
    ax.scatter([x[0] for x in dataList], [x[1] for x in dataList], c=colors)

plt.show()

