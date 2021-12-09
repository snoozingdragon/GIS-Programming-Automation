from mmap import ACCESS_READ
import random
import numpy as np
import pandas as pd
import geopandas as gpd
import fiona
from shapely.geometry import Point, LineString, Polygon

layers = fiona.listlayers('D:\PythonProgramming\lab3.gpkg')
print(layers)

for layer in layers:
    huc8 = gpd.read_file('D:\PythonProgramming\lab3.gpkg', layer= 'wdbhuc8')
    huc12 = gpd.read_file('D:\PythonProgramming\lab3.gpkg', layer= 'wdbhuc12')
    ssurgo = gpd.read_file('D:\PythonProgramming\lab3.gpkg', layer= 'ssurgo_mapunits_lab3')
    
huc8Dist = []
ID= []
integers= []
sample_points = {'ID' : [], 'geometry' :[]}
for idx, row in huc8.iterrows():
    totarea = huc8.area/1000000
    extent = huc8.total_bounds
    numpoints = .05*totarea
    integers.append(round(numpoints))
    m = 0
    for items in huc8:
        ID = huc8['HUC8']
        for m in row:
            while m < 'integers':
                x = random.uniform(extent[0], extent[2])
                y = random.uniform(extent[1], extent[3])
                point = Point(x,y)
                if point.within (row.geometry):
                    sample_points['geometry'].append(point)
                    sample_points['ID'].append(ID)
dataframe8 = pd.DataFrame(sample_points)
gdf8 = GeoDataFrame(df, crs=huc8.crs)
huc8points = gpd.overlay(gdf8, ssurgo, how='intersects')
groups8 = huc8points.groupby(by='ID').mean()
means8 = groups8['aws0150'].mean()
print(means8)

huc12Dist = []
ID= []
integers= []
sample_points = {'ID' : [], 'geometry' :[]}
for idx, row in huc12.iterrows():
    totarea = huc12.area/1000000
    extent = huc12.total_bounds
    numpoints = .05*totarea
    integers.append(round(numpoints))
    m = 0
    for items in huc12:
        ID = huc12['HUC12']
        for m in row:
            while m < 'integers':
                x = random.uniform(extent[0], extent[2])
                y = random.uniform(extent[1], extent[3])
                point = Point(x,y)
                if point.within (row.geometry):
                    sample_points['geometry'].append(point)
                    sample_points['ID'].append(ID)
dataframe12 = pd.DataFrame(sample_points)
gdf12 = GeoDataFrame(df, crs=huc12.crs)
huc12points = gpd.overlay(gdf12, ssurgo, how='intersects')
groups12 = huc12points.groupby(by='ID').mean()
means12 = groups12['aws0150'].mean()
print(means12)


#I still couldn't get this process to run for me. Every time it got hung up on the sample points, and my
#trouble shooting didn't work. So I don't know if this even works, but it's already late and I'd like
#to get whatever credit I can at this point. 