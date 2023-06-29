import os

import matplotlib.pyplot as plt
import numpy as np
import rioxarray as rxr
import geopandas as gpd
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep

# Get data and set your home working directory
#data = et.data.get_data("vignette-landsat")

#os.chdir(os.path.join(et.io.HOME, "earth-analytics"))

data_path = "C:\\Users\\matt\\Documents\\GitHub\\New-ortho\\tlt\\code\\odm_orthophoto\\odm_orthophoto.tif"
data = rxr.open_rasterio(data_path)

# View shape of the data
print(data.shape)

#ep.plot_bands(data[0],
#              title="RGB Imagery - Band 0",
#              cbar=False)
#plt.show()
#
#ep.plot_bands(data[1],
#              title="RGB Imagery - Band 1",
#              cbar=False)
#plt.show()
#
#ep.plot_bands(data[2],
#              title="RGB Imagery - Band 2",
#              cbar=False)
#plt.show()
#
#ep.plot_bands(data[3],
#              title="RGB Imagery - Band 3",
#              cbar=False)
#plt.show()



ep.plot_rgb(data.values,
            rgb=[3, 0, 1],
            title="RGB Composite image")
plt.show()

ndvi = es.normalized_diff(data[3], data[2])

ep.plot_bands(ndvi,
              cmap='PiYG',
              scale=False,
              vmin=-1, vmax=1,
              title="NDVI (Normalized Distribution Vegetation Index)")
plt.show()

ep.hist(ndvi.values,
        figsize=(12, 6),
        title=["NDVI: Distribution of pixels"])

plt.show()