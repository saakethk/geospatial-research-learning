# UNIT 11 CODE

# DEPENDENCIES
import rioxarray
import dask
from threading import Lock

# Opens the raster array
red = rioxarray.open_rasterio("data/sentinel2/red.tif", chunks=(1, 4000, 4000))
red = rioxarray.open_rasterio('data/sentinel2/red.tif', masked=True)
nir = rioxarray.open_rasterio('data/sentinel2/nir.tif', masked=True)

# Runs normally
ndvi = (nir - red)/(nir + red)

# Runs with dask
red_dask = rioxarray.open_rasterio('data/sentinel2/red.tif', masked=True, lock=False, chunks=(1, 6144, 6144))
nir_dask = rioxarray.open_rasterio('data/sentinel2/nir.tif', masked=True, lock=False, chunks=(1, 6144, 6144))
ndvi_dask = (nir_dask - red_dask)/(nir_dask + red_dask)
ndvi_dask = ndvi_dask.persist(scheduler="threads", num_workers=4)
ndvi_dask.rio.to_raster('output/ndvi.tif', tiled=True, lock=Lock())
dask.visualize(ndvi_dask)