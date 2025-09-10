# UNIT 9 CODE

# DEPENDENCIES
import rioxarray
import geopandas
import matplotlib.pyplot as plt

# Gets band with the clip
def get_band_and_clip(band_path, bbox):
    band = rioxarray.open_rasterio(band_path, masked=True)
    return band.rio.clip_box(*bbox)

# Loads the two bands necessary
red = rioxarray.open_rasterio("data/sentinel2/red.tif", masked=True)
nir = rioxarray.open_rasterio("data/sentinel2/nir.tif", masked=True) # near infrared band

# determine bounding box of Rhodes, in the projected CRS
rhodes = geopandas.read_file('output/rhodes.gpkg')
rhodes_reprojected = rhodes.to_crs(red.rio.crs)
bbox = rhodes_reprojected.total_bounds

# crop the rasters
red_clip = red.rio.clip_box(*bbox)
nir_clip = nir.rio.clip_box(*bbox)

# plot rasters
# red_clip.plot(robust=True)
# nir_clip.plot(robust=True)

# Raster math
print(red_clip.shape, nir_clip.shape)
ndvi = (nir_clip - red_clip)/ (nir_clip + red_clip) # Normalized difference vegetation index
# ndvi.plot()
# ndvi.plot.hist()

# Other rasters
data_path = 'data/sentinel2'
green_clip = get_band_and_clip(f'{data_path}/green.tif', bbox)
swir16_clip = get_band_and_clip(f'{data_path}/swir16.tif', bbox)
swir22_clip = get_band_and_clip(f'{data_path}/swir22.tif', bbox)
ndwi = (green_clip - nir_clip)/(green_clip + nir_clip)
index = (swir16_clip - swir22_clip)/(swir16_clip + swir22_clip)
# ndwi.plot(robust=True)
# index.plot(robust=True)

# Fixes resolution problem
index_match = index.rio.reproject_match(ndvi)
swir16_match = swir16_clip.rio.reproject_match(ndvi)
blue_clip = get_band_and_clip(f'{data_path}/blue.tif', bbox)

# Applies binary classification paramters
burned = (
    (ndvi <= 0.3) &
    (ndwi <= 0.1) &
    ((index_match + nir_clip/10_000) <= 0.1) &
    ((blue_clip/10_000) <= 0.1) &
    ((swir16_match/10_000) >= 0.1)
)
burned = burned.squeeze()
visual = rioxarray.open_rasterio(f'{data_path}/visual.tif')
visual_clip = visual.rio.clip_box(*bbox)
# set red channel to max (255), green and blue channels to min (0).
visual_clip[0] = visual_clip[0].where(~burned, 255)
visual_clip[1:3] = visual_clip[1:3].where(~burned, 0)
visual_clip.plot()
burned.rio.to_raster('output/burned.tif', dtype='int8')

# Shows the plotted graphs
plt.show()

