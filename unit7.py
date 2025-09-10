# UNIT 7 CODE

# DEPENDENCIES
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Function to allow us to buffer
def buffer_crs(gdf, size, meter_crs=32631, target_crs=4326):
    return gdf.to_crs(meter_crs).buffer(size).to_crs(target_crs)

# Loads dataset
gdf_greece = gpd.read_file('data/gadm/ADM_ADM_3.gpkg')
gdf_greece.plot()
print(gdf_greece)

# Gets subset of dataset
gdf_rhodes = gdf_greece.loc[gdf_greece['NAME_3']=='Rhodos']
gdf_rhodes.plot()
gdf_rhodes.to_file('output/rhodes.gpkg')

# Gets roads (Step 1)
gdf_roads = gpd.read_file('data/osm/osm_roads.gpkg')
gdf_roads = gpd.read_file('data/osm/osm_roads.gpkg', mask=gdf_rhodes)
gdf_roads.plot()

# Gets types of roads
gdf_roads['fclass'].unique()
key_infra_labels = ['primary', 'secondary', 'tertiary']
key_infra = gdf_roads[gdf_roads['fclass'].isin(key_infra_labels)]
key_infra.plot()

# Creating 100m buffer
# epsg_code = 32631
# key_infra_meters = key_infra.to_crs(epsg_code)
# key_infra_meters_buffer = key_infra_meters.buffer(100)
# key_infra_buffer = key_infra_meters_buffer.to_crs(key_infra.crs)
# print(key_infra.crs)

# Creating 200m buffer
key_infra_buffer = buffer_crs(key_infra, 10)
key_infra_buffer_200 = buffer_crs(key_infra, 200)

# Read data with a mask of Rhodes
gdf_landuse = gpd.read_file('./data/osm/osm_landuse.gpkg', mask=gdf_rhodes)

# Find number of unique landuse types
print(len(gdf_landuse['fclass'].unique()))

# Extract built-up regions
builtup_labels = ['commercial', 'industrial', 'residential']
builtup = gdf_landuse[gdf_landuse['fclass'].isin(builtup_labels)]

# Create 10m buffer around the built-up regions
builtup_buffer = buffer_crs(builtup, 10)

# Get the number of entries
print(len(builtup_buffer))

# Visualize the buffer
builtup_buffer.plot()

# Merges infrastructure and built-up regions
data = {'geometry': key_infra_buffer, 'type': 'infrastructure', 'code': 1}
gdf_infra = gpd.GeoDataFrame(data)
data = {'geometry': builtup_buffer, 'type': 'builtup', 'code': 2}
gdf_builtup = gpd.GeoDataFrame(data)
gdf_assets = pd.concat([gdf_infra, gdf_builtup]).reset_index(drop=True)
gdf_assets.plot(column='type', legend=True)
gdf_assets.to_file('output/assets.gpkg')

# Shows all plots
plt.show()