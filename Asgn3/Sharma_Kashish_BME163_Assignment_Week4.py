
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import time

# Style sheet
plt.style.use('./BME163.mplstyle')

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('--outFile','-o' ,type=str,action='store',help='output file')
parser.add_argument('--inFile','-i' ,type=str,action='store',help='identity file')
parser.add_argument('--inFile2','-c' ,type=str,action='store',help='coverage file')
args = parser.parse_args()

outFile = args.outFile
input = args.inFile
input2 = args.inFile2

# Create figure and panel
figureHeight = 2.5
figureWidth = 6
panelWidth = 4.5
panelHeight = 1.5

plt.figure(figsize=(figureWidth, figureHeight))
panelCenter = plt.axes([0.5/figureWidth, 0.15, panelWidth/figureWidth, panelHeight/figureHeight])

# Axis limits and labels
panelCenter.set_xlim(0.5, 4.5)
panelCenter.set_ylim(75, 100)
panelCenter.set_xticks([1, 2, 3, 4])
panelCenter.set_xticklabels(['1-3', '4-6', '7-9', '>=10'], fontsize=8)
panelCenter.set_yticks([75, 80, 85, 90, 95, 100])
panelCenter.set_yticklabels([75, 80, 85, 90, 95, 100], fontsize=8)
panelCenter.set_xlabel('Subread Coverage', fontsize=8)
panelCenter.set_ylabel('Identity (%)', fontsize=8)

# Colors
#Using what the Prof said 
iBlue = (44/255, 86/255, 134/255)
iGreen = (32/255, 100/255, 113/255)
iYellow = (248/255, 174/255, 51/255)
iOrange = (230/255, 87/255, 43/255)
colors = [iBlue, iGreen, iYellow, iOrange]

# Read input files

identityDict = {}
with open(input) as f:
    for line in f:
        name, identity = line.strip().split('\t')
        identityDict[name] = float(identity)

#Opens the coverage file 
#Itterates over each line of the file 
#Splits in two parts 

coverageDict = {}
with open(input2) as f:
    for line in f:
        name, coverage = line.strip().split('\t')
        coverageDict[name] = int(coverage)

# Bin identities by coverage
bins = {0: [], 1: [], 2: [], 3: []}
for name in identityDict:
    if name in coverageDict:
        coverage = coverageDict[name]
        identity = identityDict[name]
        if 1 <= coverage <= 3:
            bins[0].append(identity)
        elif 4 <= coverage <= 6:
            bins[1].append(identity)
        elif 7 <= coverage <= 9:
            bins[2].append(identity)
        elif coverage >= 10:
            bins[3].append(identity)

# Subsample and shuffle
for k in bins:
    bins[k] = random.sample(bins[k], min(500, len(bins[k])))
    random.shuffle(bins[k])

#Add below 
# Plot each bin
#for bin_index, xPos in enumerate([1, 2, 3, 4]):
 #   swarmplot(panelCenter, xPos, bins[bin_index], colors[bin_index])


# Swarm plot function
def swarmplot(panel, xPos, yvalues, color):
    markersize = 2
    marker_spacing = markersize / 72
    xrange = 4
    yrange = 25
    panel_width = 4.5
    panel_height = 1.5
    increment = (marker_spacing / 10) * xrange / panel_width
    max_offset = 0.45
    offsets = []
    for i in range(int(max_offset // increment) + 1):
        offsets.append(xPos + i * increment)
        offsets.append(xPos - i * increment)
    plotted_points = []
    missed = 0
    for y in yvalues:
        placed = False
        for x in offsets:
            if all((((x - x2)/xrange * panel_width)**2 + ((y - y2)/yrange * panel_height)**2)**0.5 > marker_spacing
                   for x2, y2 in plotted_points):
                plotted_points.append((x, y))
                panel.plot(x, y, marker='o', markersize=markersize, markeredgewidth=0, color=color)
                placed = True
                break
        if not placed:
           # missed += 1
            break #Stop trying more y values 
    missed = 500 - len(plotted_points)
        
    if missed > 0:
        print(f"{missed} points could not be plotted at position {xPos}")
    #For checking 
    # if missed >0:
     #   print(f"Trying to plot {len(yvalues)} points at position {xPos}")
      #  print(f"Actually plotted {len(plotted_points)} points")
       # print(f"{missed} points could not be plotted at position {xPos}")


         
        
# Plot each bin
for bin_index, xPos in enumerate([1, 2, 3, 4]):
    swarmplot(panelCenter, xPos, bins[bin_index], colors[bin_index])        

# Save
plt.savefig(outFile, dpi=600)
#Remmeber to remove this before submission 
#plt.show()

