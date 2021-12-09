import pandas as pd
import geopandas as gpd
import os
import glob
from rasterstats import zonal_stats
from shapely.geometry import Point, LineString, Polygon

dictionary= {'dist': [], 'num_coords': [], 'poly':[]}
files=glob.glob(r'D:\PythonProgramming\data\districts\*.txt')
for items in files:
    x = pd.read_csv(items, delim_whitespace=True)
    coords = list(zip(x['X'],x['Y'])) 
    poly = Polygon(coords)
    dictionary['dist'].append(items[-6:-4])
    dictionary['num_coords'].append(len(coords))
    dictionary['poly'].append(poly)

dataframe= pd.DataFrame(dictionary)
gdf = gpd.GeoDataFrame(dataframe, geometry = 'poly')
gdf = gdf.set_crs('epsg:4326')
distshp = gdf.to_file(driver = 'ESRI Shapefile', filename = 'districts.shp')

AgDict = {'dist' :['01', '05', '06', '01', '05', '06'], 
          'year': ['2004', '2004', '2004', '2009', '2009', '2009'],
          'perc_cover': [] }
Tif_List = glob.glob(r'D:\PythonProgramming\data\agriculture\*.tif')
          

for layers in Tif_List:
    stats = pd.DataFrame(zonal_stats('districts.shp', layers, stats = ['count', 'sum']))
    count = list(stats['count'])
    summation = list(stats['sum'])
    perc = ([m/n for m, n in zip(summation, count)])
    print(perc)
    for percentage in perc:
             AgDict['perc_cover'].append(percentage*100)
            
AgDictFinal = pd.DataFrame(AgDict)

AgDictFinal
