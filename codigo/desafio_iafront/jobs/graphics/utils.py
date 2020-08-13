import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.transform import factor_cmap


def plot(dataframe: pd.DataFrame, x_axis, y_axis, cluster_label, title=""):
    clusters = [label for label in dataframe[cluster_label]]

    colors = [set_color(_) for _ in clusters]

    p = figure(title=title)

    p.scatter(dataframe[x_axis].tolist(), dataframe[y_axis].tolist(), fill_color=colors)

    return p

def plot_clusters(dataframe: pd.DataFrame, x_axis, y_axis, cluster_label, title=""):

    clusters = dataframe[cluster_label].unique()
    colors = [set_color(_) for _ in clusters]
    colors=factor_cmap(cluster_label, palette=colors, factors=np.sort(clusters))
        
    print(clusters, colors)
    p = figure(title=title)

    p.scatter(x_axis, y_axis,  source=dataframe,  fill_color=colors, legend=cluster_label)

    return p

def hist(dataframe: pd.DataFrame, x_axis, title=""):
    p = figure(title=title)

    hist, edges = np.histogram(dataframe[x_axis], density=True, bins=30)
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color="navy", line_color="white", alpha=0.5)

    p.y_range.start = 0
    p.legend.location = "center_right"
    p.legend.background_fill_color = "#fefefe"
    p.xaxis.axis_label = x_axis
    p.yaxis.axis_label = 'Frequência'
    p.grid.grid_line_color="white"

    return p

def _unique(original):
    return list(set(original))


def set_color(color):
    COLORS = ["green", "blue", "red", "orange", "purple"]
    index = int(color) % len(COLORS)

    return COLORS[index]
