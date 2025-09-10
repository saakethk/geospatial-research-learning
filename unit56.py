# UNIT 5, 6 CODE

# DEPENDENCIES
# https://pystac-client.readthedocs.io/en/stable/
import pystac
from pystac_client import Client
from pyproj import CRS
# https://shapely.readthedocs.io/en/2.1.1/installation.html
from shapely.geometry import Point
# https://corteva.github.io/rioxarray/stable/
import rioxarray
# https://matplotlib.org
import matplotlib.pyplot as plt

# Defines API url for sentinel 2 STAC catalog data
API_URL = "https://earth-search.aws.element84.com/v1"
COLLECTION = "sentinel-2-l2a"
POINT = Point(27.95, 36.20) # Coordinates of Rhodes

def get_search_results(file: str):
    """
    Gets search results and saves in json object to be loaded later
    """

    # Open url
    client = Client.open(url=API_URL)

    # Gets collections
    collections = client.get_collections()
    for collection in collections:
        print(collection)

    # Searches for imagery
    search = client.search(
        collections=[COLLECTION],
        intersects=POINT,
        datetime='2023-07-01/2023-08-31'
    )
    print(search.matched())

    # Gets items from search
    items = search.item_collection()
    for item in items:
        print(item)

    # Gets first item from results
    item = items[0]
    print(item.datetime)
    print(item.geometry)
    print(item.properties)
    print(item.properties['proj:code'])

    # Saves search results
    items.save_object(file)
    return file

def load_results(file: str, raster_file: str):
    """
    Loads search results from a file
    """

    # Loads items from file
    items_loaded = pystac.ItemCollection.from_file(file)

    # Loads last item
    assets = items_loaded[-1].assets

    # Gets attributes available for image
    for key, asset in assets.items():
        print(f"{key}: {asset.title}")

    # Prints oldest and newest image
    print(assets["thumbnail"].href) # oldest
    print(items_loaded[0].assets["thumbnail"].href) # newest

    # Prints red band stats
    red_href = assets["red"].href
    red = rioxarray.open_rasterio(red_href)
    print(red)

    # Saves whole image to disk
    red.rio.to_raster("red.tif")

    # Prints visual band stats
    visual_href = assets["visual"].href
    visual = rioxarray.open_rasterio(visual_href)
    print(visual)

    # Saves whole image to disk
    visual.rio.to_raster("visual.tif")

    # Saves a subset of image
    red_subset = red.rio.clip_box(
        minx=560900,
        miny=3995000,
        maxx=570900,
        maxy=4015000
    )
    red_subset.rio.to_raster(raster_file)

def load_raster(file: str):
    """
    Loads raster image
    """

    # Gets red raster for the image
    rhodes_red = rioxarray.open_rasterio(file)
    print(rhodes_red)
    print(rhodes_red.rio.crs)
    print(rhodes_red.rio.nodata)
    print(rhodes_red.rio.bounds())
    print(rhodes_red.rio.width)
    print(rhodes_red.rio.height)
    print(rhodes_red.rio.resolution())

    # Gets values of raster and plots
    print(rhodes_red.values)
    rhodes_red.plot()

    # Resampled image
    # rhodes_red_80 = rioxarray.open_rasterio(file, overview_level=2)
    # print(rhodes_red_80.rio.resolution())
    # rhodes_red_80.plot()
    # plt.show()

    # CRS
    print(rhodes_red.rio.crs)
    print(rhodes_red.rio.crs.to_epsg())
    epsg = rhodes_red.rio.crs.to_epsg()
    crs = CRS(epsg)
    print(crs)
    print(crs.area_of_use)

    # Raster statistics
    print(rhodes_red.min())
    print(rhodes_red.max())
    print(rhodes_red.mean())
    print(rhodes_red.std())
    print(rhodes_red.quantile([0.25, 0.75]))

    # Dealing with missing data
    print(rhodes_red.rio.nodata)

    # Masking
    rhodes_red_mask = rioxarray.open_rasterio(file, masked=True)
    print(rhodes_red_mask)
    rhodes_red_altmask = rhodes_red.where(rhodes_red != rhodes_red.rio.nodata)
    print(rhodes_red_altmask)

    # Masking statistics
    print(rhodes_red.min())
    print(rhodes_red_mask.min())
    print(rhodes_red.max())
    print(rhodes_red_mask.max())
    print(rhodes_red.mean())
    print(rhodes_red_mask.mean())
    print(rhodes_red.std())
    print(rhodes_red_mask.std())

    # Multiband
    rhodes_visual = rioxarray.open_rasterio('visual.tif')
    print(rhodes_visual)
    rhodes_visual.plot.imshow()
    plt.show()


# get_search_results(file="rhodes_sentinel-2.json")
# load_results(file="output/rhodes_sentinel-2.json", raster_file="red_subset.tif")
# load_raster(file="output/red.tif")
