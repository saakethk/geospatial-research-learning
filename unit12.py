# UNIT 12 CODE

# DEPENDENCIES
import geopandas
import pystac_client
import odc.stac
import matplotlib.pyplot as plt

# Opens file
rhodes = geopandas.read_file('output/rhodes.gpkg')
bbox = rhodes.total_bounds

# Searches for satellite imagery
api_url = "https://earth-search.aws.element84.com/v1"
collection_id = "sentinel-2-c1-l2a"
client = pystac_client.Client.open(api_url)
search = client.search(
    collections=[collection_id],
    datetime="2023-07-01/2023-08-31",
    bbox=bbox
)
item_collection = search.item_collection()

# ODC
ds = odc.stac.load(
    item_collection,
    groupby='solar_day',
    chunks={'x': 2048, 'y': 2048},
    use_overviews=True,
    resolution=20,
    bbox=rhodes.total_bounds,
)
print(ds)

# Working with data cube
red = ds['red']
nir = ds['nir']
scl = ds['scl']

# generate mask ("True" for pixel being cloud or water)
mask = scl.isin([
    3,  # CLOUD_SHADOWS
    6,  # WATER
    8,  # CLOUD_MEDIUM_PROBABILITY
    9,  # CLOUD_HIGH_PROBABILITY
    10  # THIN_CIRRUS
])
red_masked = red.where(~mask)
nir_masked = nir.where(~mask)
ndvi = (nir_masked - red_masked) / (nir_masked + red_masked)
ndvi_before = ndvi.sel(time="2023-07-13")
ndvi_before.plot()
ndvi_after = ndvi.sel(time="2023-08-27")
ndvi_after.plot()

# Plots data
x = 585_000
y = 3_995_000
fig, ax = plt.subplots()
ndvi_after.plot(ax=ax)
ax.scatter(x, y, marker="o", c="k")

# Calculates compute
ndvi_xy = ndvi.sel(x=x, y=y, method="nearest")
print(ndvi_xy)
ndvi_xy = ndvi_xy.compute(scheduler="threads", num_workers=4)
ndvi_xy.dropna(dim="time").plot()

# Shows graph
plt.show()





