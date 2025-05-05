import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import argparse

# === Argument Parser ===
parser = argparse.ArgumentParser()
parser.add_argument('--outFile', '-o', type=str, help='Output image file')
parser.add_argument('--inFile', '-i', type=str, help='Input TSV file')
args = parser.parse_args()

# === Style ===
plt.style.use('BME163')
#plt.style.use('/Users/kashishsharma/.config/matplotlib/stylelib/BME163.mplstyle')

# === Constants ===
figureWidth = 3
figureHeight = 3

# === Colors ===
iBlue = (88/255, 85/255, 120/255)
iGreen = (120/255, 172/255, 145/255)
grey = 'grey'

# === Set up Figure ===
plt.figure(figsize=(figureWidth, figureHeight))

gap = 0.05 # small gap in inches
# Slightly shorter panel height
main_panel_height = 1.45
top_panel_height = 0.25

shift = 0.130
#y_shift = 0.09
y_shift = -0.001

scatter_ax = plt.axes([
    (0.5 + shift) / figureWidth,
    (0.5 - y_shift) / figureHeight,
    1.5 / figureWidth,
    1.5 / figureHeight
])

top_ax = plt.axes([
    (0.5 + shift) / figureWidth,
    (0.5 - y_shift + 1.5 + gap) / figureHeight,  
    1.5 / figureWidth,
    0.25 / figureHeight
])

left_ax = plt.axes([
    (0.5 - 0.25 - gap + shift) / figureWidth,
    (0.5 - y_shift) / figureHeight,
    0.25 / figureWidth,
    1.5 / figureHeight
])



# === Read Data ===
xVals = []
yVals = []
with open(args.inFile) as f:
    for line in f:
        if line.startswith('#') or line.strip() == '':
            continue
        splitLine = line.strip().split('\t')
        try:
            x = float(splitLine[1])
            y = float(splitLine[2])
            xVals.append(np.log2(x + 1))
            yVals.append(np.log2(y + 1))
        except:
            continue

xArray = np.array(xVals)
yArray = np.array(yVals)

# === Scatterplot ===
scatter_ax.plot(
    xArray, yArray,
    marker='o',
    markeredgewidth=0,
    markerfacecolor=iBlue,
    markersize=3,
    #alpha=0.09, 
    alpha=0.1,
    linestyle='None'
)

# === Top Histogram (x-axis dist) ===
xHist, xBinEdges = np.histogram(xArray, bins=np.arange(0, 19, 0.5))
for i in range(len(xHist)):
    x = xBinEdges[i]
    if x >= 14.5:  # ← skip the last one exactly
        continue
    width = xBinEdges[i + 1] - x
    height = np.log2(xHist[i] + 1)
    rect = mplpatches.Rectangle(
        (x, 0),
        width,
        height,
        facecolor=iGreen,
        edgecolor='black',
        linewidth=0.30
    )
    top_ax.add_patch(rect)



# === Left Histogram (y-axis dist) ===
yHist, yBinEdges = np.histogram(yArray, bins=np.arange(0, 20, 0.5))
for i in range(len(yHist)):
    y = yBinEdges[i]
    if y >= 14.5:  # skip bars near the very top
        continue
    height = yBinEdges[i+1] - y
    width = np.log2(yHist[i] + 1)
    rect = mplpatches.Rectangle(
    (20 - width, y),  # Flip bar from the right edge
    width,
    height,
    facecolor=grey,
    edgecolor='black',
    linewidth=0.30
)

    left_ax.add_patch(rect)

# === Scatter Axes ===
# === SCATTER PANEL (MAIN PLOT) SETTINGS ===
scatter_ax.set_xlim(0, 15)
scatter_ax.set_ylim(0, 15)
scatter_ax.set_aspect('equal', adjustable='box')

#  X-axis ticks (bottom): 0, 5, 10, 15
scatter_ax.set_xticks([0, 5, 10, 15])
scatter_ax.set_xticklabels(['0', '5', '10', '15'], fontsize=7)
scatter_ax.tick_params(
    axis='x',
    direction='out',
    length=2,
    width=0.8,
    pad=1,
    bottom=True,
    labelbottom=True,
    top=False,
    labeltop=False
)

#Y axis no tix just line 
scatter_ax.set_yticks([])
scatter_ax.set_yticklabels([])
scatter_ax.tick_params(
    axis='y',
    length=0,         # no tick lines
    width=0,
    labelleft=False   # no labels
)


# === TOP HISTOGRAM (GREEN PANEL) SETTINGS ===
top_ax.set_xlim(0, 15)
top_ax.set_ylim(0, 20)

#  Y-axis ticks: only 0 and 20
top_ax.set_yticks([0, 20])
top_ax.set_yticklabels(['0', '20'], fontsize=7)
top_ax.tick_params(
    axis='y',
    which='both',
    direction='out',
    length=2,
    width=0.8,
    pad=1,
    left=True,
    labelleft=True,
    right=False,
    labelright=False
)

#  No x-axis ticks or labels on top panel
top_ax.set_xticks([])
top_ax.set_xticklabels([])


# === LEFT HISTOGRAM (GREY PANEL) SETTINGS ===
left_ax.set_xlim(0, 20)
left_ax.set_ylim(0, 15)

#  Y-axis ticks (vertical): 0, 5, 10, 15
left_ax.set_yticks([0, 5, 10, 15])
left_ax.set_yticklabels(['0', '5', '10', '15'], fontsize=7)
left_ax.tick_params(
    axis='y',
    direction='out',
    length=2,
    width=0.8,
    pad=1,
    left=True,
    labelleft=True,
    right=False,
    labelright=False
)

#  X-axis ticks (horizontal): labels '20', '0' to match flipped bars
left_ax.set_xticks([0, 20])
left_ax.set_xticklabels(['20', '0'], fontsize=7)
left_ax.tick_params(
    axis='x',
    direction='out',
    length=2,
    width=0.8,
    pad=1,
    bottom=True,
    labelbottom=True,
    top=False,
    labeltop=False
)

plt.subplots_adjust(
    bottom=0.02  )

#Save and plot 
plt.savefig(args.outFile, dpi=600)

#remove the below command before submitting!!!!
#plt.show()
