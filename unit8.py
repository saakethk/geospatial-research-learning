# UNIT 8 CODE

# DEPENDENCIES
import rioxarray
import geopandas as gpd
import matplotlib.pyplot as plt
import geopandas as gpd

# Loads the raster file
path_visual = 'data/sentinel2/visual.tif'
visual = rioxarray.open_rasterio(path_visual, overview_level=1)
visual.plot.imshow()
print(visual)

# Loads vector file made in unit 7
assets = gpd.read_file('output/assets.gpkg')
# Reproject
assets = assets.to_crs(visual.rio.crs)
# Check the new bounding box
print(assets.total_bounds)
# Crop the raster with the bounding box
visual_clipbox = visual.rio.clip_box(*assets.total_bounds)
# Visualize the cropped image
visual_clipbox.plot.imshow()
# Crop the raster with the polygon
visual_clip = visual_clipbox.rio.clip(assets["geometry"])
# Visualize the cropped image
visual_clip.plot.imshow()

# Clips red band
gdf_greece = gpd.read_file('./data/gadm/ADM_ADM_3.gpkg')
gdf_rhodes = gdf_greece[gdf_greece['NAME_3']=='Rhodos']
path_red = './data/sentinel2/red.tif'
red = rioxarray.open_rasterio(path_red, overview_level=1)
gdf_rhodes = gdf_rhodes.to_crs(red.rio.crs)
red_clip = red.rio.clip(gdf_rhodes["geometry"])
red_clip_nan = red_clip.where(red_clip!=red_clip.rio.nodata)
red_clip_nan.plot()

# Loads digital elevation model (DEM)
dem = rioxarray.open_rasterio('./data/dem/rhodes_dem.tif')
dem.plot()
print(dem.rio.crs)
print(visual_clip.rio.crs)
dem_matched = dem.rio.reproject_match(visual_clip)
dem_matched.plot()
dem_matched.rio.to_raster('output/dem_rhodes_match.tif', driver='COG') # COG - Cloud optimized geotiff file

# Displays graphs
plt.show()