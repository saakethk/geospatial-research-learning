# UNIT 10 CODE

# DEPENDENCIES
import rioxarray
import geopandas as gpd
from rasterio import features
import matplotlib.pyplot as plt
from xrspatial import zonal_stats

# Load burned index
burned = rioxarray.open_rasterio('output/burned.tif')

# Load assests polygons
assets = gpd.read_file('output/assets.gpkg')

# Reprojects so they have same crs
assets = assets.to_crs(burned.rio.crs)

# Rasterizing vector data
geom = assets[['geometry', 'code']].values.tolist()
burned_squeeze = burned.squeeze() # Drops band dimension of burned
print(burned.shape)
assets_rasterized = features.rasterize(geom, out_shape=burned_squeeze.shape, transform=burned.rio.transform())
assets_rasterized

# Zonal Statistics visualize
assets_rasterized_xarr = burned_squeeze.copy()
assets_rasterized_xarr.data = assets_rasterized
assets_rasterized_xarr.plot()

# Calculates zonal statistics
stats = zonal_stats(assets_rasterized_xarr, burned_squeeze)
print(stats)

# Shows graphs
plt.show()

