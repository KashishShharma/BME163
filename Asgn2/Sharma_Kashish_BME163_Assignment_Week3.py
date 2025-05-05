import matplotlib.pyplot as plt
import numpy as np
import argparse
import matplotlib.patheffects
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1 import make_axes_locatable


# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--position', required=True)
parser.add_argument('-c', '--celltype', required=True)
parser.add_argument('-o', '--outFile', required=True)
args = parser.parse_args()

# Load position data
positions = {}
with open(args.position) as f:
    for line in f:
        name, x, y = line.strip().split()
        positions[name] = (float(x), float(y))

# Load cell types
celltypes = {}
with open(args.celltype) as f:
    f.readline()  # Skip header
    for line in f:
        _, celltype, name = line.strip().split()
        celltypes[name] = celltype

# Group cells by type
grouped = {}
for name in positions:
    x, y = positions[name]
    celltype = celltypes.get(name, 'Unknown')
    grouped.setdefault(celltype, []).append((x, y))


#CHANGE THIS BEFORE SUBMITTING
#plt.style.use('/Users/kashishsharma/.config/matplotlib/stylelib/BME163.mplstyle')
plt.style.use('BME163')

# Set up the figure size
figureWidth = 5
figureHeight = 3
#fig = plt.figure(figsize=(figureWidth, figureHeight))
plt.figure(figsize=(figureWidth,figureHeight))
# Panel dimensions in inches
panelWidth = 1.5
panelHeight = 1.5

# Convert to relative units
relativePanelWidth=panelWidth/figureWidth
relativePanelHeight=panelHeight/figureHeight

#Given by the Professor - Panels 
panel1=plt.axes([0.5/figureWidth,0.5/figureHeight,relativePanelWidth,relativePanelHeight])
panel2=plt.axes([2.5/figureWidth,0.5/figureHeight,relativePanelWidth,relativePanelHeight])
panel3=plt.axes([4.0/figureWidth,1.1/figureHeight,0.1/figureWidth,0.3/figureHeight])


# Color map setup
color_map = {
    'tCell': (0.4, 0.7, 0.6),        # deeper green-teal
    'monocyte': (0.6, 0.6, 0.6),     # solid medium gray
    'bCell': (0.35, 0.35, 0.55)      # richer muted blue
}


# --- PANEL 1: Plot points by type ---
for ctype, points in grouped.items():
    xs, ys = zip(*points)
    color = color_map.get(ctype, (0.7, 0.7, 0.7))
    panel1.scatter(xs, ys,
               facecolor=color,
               edgecolor='black',
               linewidth=0.1,  # visible outline
               s=13)            # marker size

    # Text at median position
    median_x = np.median(xs)
    median_y = np.median(ys)
    panel1.text(median_x,
            median_y,
            ctype,
            ha='center',
            va='center',
            fontsize=8,
            color='black',
            weight='normal',
            path_effects=[
                matplotlib.patheffects.withStroke(linewidth=1, foreground='white')
            ])

panel1.set_xlabel('tSNE 2')
panel1.set_ylabel('tSNE 1')


# --- PANEL 2: Density based ---
all_points = list(positions.values())
xs, ys = zip(*all_points)
xs = np.array(xs)
ys = np.array(ys)

# Get limits of panel2
x0, x1 = panel2.get_xlim()
y0, y1 = panel2.get_ylim()

# Calculate inches per data unit
x_inch = panelWidth / (x1 - x0)
y_inch = panelHeight / (y1 - y0)

density = []
threshold = 7.2
#scatter = panel2.scatter(xs, ys, c=density, cmap='viridis', s=13, edgecolor='none', alpha=0.8)
#scatter.set_clim(0, 100)

for i in range(len(xs)):
    dx = (xs - xs[i]) * x_inch
    dy = (ys - ys[i]) * y_inch
    dists = np.sqrt(dx**2 + dy**2)
    close_count = np.sum(dists < threshold) - 1  # exclude self
    density.append(min(close_count, 100))  # cap at 100

#DEBUG
#print("Min density:", min(density))
#print("Max density:", max(density))
#print("First 10 density values:", density[:10])
                     
#  Panel 2 scatter
scatter = panel2.scatter (xs, ys,
                         c=density,
                         cmap='viridis',
                         s=16,
                         edgecolor='none',
                         linewidth=0.1,
                         vmin=0,
                         vmax=100,
                         alpha=1)  

scatter.set_clim(0, 100)
                         
#Adding the word density 
panel2.text(
    min(xs) - 1,               
    min(ys) - 1,               
    "Density",
    ha='left',
    va='bottom',
    fontsize=8.5
)

# Colorbar
# PANEL 2: plot with density color scale
#scatter = panel2.scatter(xs, ys, c=density, cmap='viridis', s=5, edgecolor='none')
#scatter.set_clim(0, 100)  # ensure full colormap span

# Small colorbar panel next to panel2

#panel3 = plt.axes([4.25/figureWidth, 1.2/figureHeight, 0.1/figureWidth, 0.3/figureHeight])
cbar = fig.colorbar(scatter, cax=panel3)
cbar.set_ticks([0, 25, 50, 75, 100])
cbar.ax.set_yticklabels(['Min', '', '', '', 'Max'])
cbar.ax.tick_params(labelsize=8)
#Figure width divide by 1.3 or 1.2


#Check if this is allowed 
#from mpl_toolkits.axes_grid1 import make_axes_locatable

# Attach small colorbar to the right of panel2
#divider = make_axes_locatable(panel2)
#cax = divider.append_axes("right", size="2%", pad=0.05)  # ← controls size and spacing

# Draw colorbar
#cbar = fig.colorbar(scatter, cax=cax)
cbar.ax.set_yticks([0, 100])
cbar.ax.set_yticklabels(['Min', 'Max'])

# Label vertically, centered
#cbar.set_label('Density', rotation=270, labelpad=5, fontsize=7, va='center')


panel2.set_xlabel('tSNE 2')
panel2.set_ylabel('tSNE 1')

# Save IMAGE 
plt.savefig(args.outFile, dpi=600)

#Remember to remove this before submitting 
plt.show()