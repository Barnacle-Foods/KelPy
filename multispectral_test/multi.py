# multi.py
# Chet Russell
# Last edited: 6/30/2023
# This file calculates the NDVI of an orthomosaic, and returns an image of the
# NDVI. The output of this code is Figure_1.png & Figure_2.png.
#
# This code has been tailored from:
# https://www.earthdatascience.org/courses/use-data-open-source-python/multispectral-remote-sensing/vegetation-indices-in-python/calculate-NDVI-python/

import os
from matplotlib.colors import ListedColormap

import matplotlib.pyplot as plt
import numpy as np
import rioxarray as rxr
import geopandas as gpd
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep

# Path to your orthomosaic.tif
data_path = ""
data = rxr.open_rasterio(data_path)

# View shape of the data
print(data.shape)
print(data[1])

ndvi = es.normalized_diff(data[3], data[2])

ep.plot_bands(
    ndvi,
    cmap="PiYG",
    scale=False,
    vmin=-1,
    vmax=1,
    title="NDVI (Normalized Distribution Vegetation Index)",
)
plt.show()

# Create classes and apply to NDVI results
ndvi_class_bins = [-np.inf, 0, 0.1, 0.25, 0.4, np.inf]
ndvi_class = np.digitize(ndvi, ndvi_class_bins)

# Apply the nodata mask to the newly classified NDVI data
ndvi_landsat_class = np.ma.masked_where(np.ma.getmask(ndvi), ndvi_class)
np.unique(ndvi_class)

# Define color map
nbr_colors = ["gray", "y", "yellowgreen", "g", "darkgreen"]
nbr_cmap = ListedColormap(nbr_colors)

# Define class names
ndvi_cat_names = [
    "No Vegetation",
    "Bare Area",
    "Low Vegetation",
    "Moderate Vegetation",
    "High Vegetation",
]

# Get list of classes
classes = np.unique(ndvi_class)
classes = classes.tolist()
# The mask returns a value of none in the classes. remove that
classes = classes[0:5]

# Plot your data
fig, ax = plt.subplots(figsize=(12, 12))
im = ax.imshow(ndvi_class, cmap=nbr_cmap)

ep.draw_legend(im_ax=im, classes=classes, titles=ndvi_cat_names)
ax.set_title(
    "Landsat 8 - Normalized Difference Vegetation Index (NDVI) Classes",
    fontsize=14,
)
ax.set_axis_off()

# Auto adjust subplot to fit figure size
plt.tight_layout()
plt.show()
