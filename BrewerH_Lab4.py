import pandas as pd
import geopandas as gpd
import rasterio
import os 
import glob
import numpy as np
import matplotlib
from rasterio.plot import show
import scipy
from shapely.geometry import Point
from numpy import loadtxt
from itertools import product

slope = rasterio.open(r'D:\PythonProgramming\data\slope.tif')
slopedata = slope.read(1)
urban_areas = rasterio.open(r'D:\PythonProgramming\data\urban_areas.tif')
urbandata = urban_areas.read(1)
windspeed = rasterio.open(r'D:\PythonProgramming\data\ws80m.tif')
winddata= windspeed.read(1)
water = rasterio.open(r'D:\PythonProgramming\data\water_bodies.tif')
waterdata = water.read(1)
protectedareas = rasterio.open(r'D:\PythonProgramming\data\protected_areas.tif')
protecteddata = protectedareas.read(1)

def mean_suitability(layer):
        temp_arr= np.zeros_like(layer)
        for row in range(0, layer.shape[0]):
            for col in range(0, layer.shape[1]):        
                win = layer[row : row + 11, col : col +  9]  
                temp_arr[row, col] = win.mean()
                layer = temp_arr
                
mean_suitability(slopedata)
mean_suitability(urbandata)
mean_suitability(windspeed)
mean_suitability(waterdata)
mean_suitability(protecteddata)

boolslope= np.where(slopedata < 15, 1, 0)
boolwater= np.where(waterdata < .02, 1, 0)
boolurban = np.where(urbandata ==1, 0, 1)
boolwind = np.where(winddata > 8.5, 1, 0)
boolprotect= np.where(protecteddata < .05, 1, 0)

wonttakemorethan2 = np.add(boolslope, boolwater)
addanother= np.add(wonttakemorethan2, boolurban)
allthemarbles = np.add(addanother, boolwind)
everything = np.add(allthemarbles, boolprotect)
unique, counts = np.unique(everything, return_counts= True)
print(np.asarray((unique,counts)))

with rasterio.open(r'D:\PythonProgramming\data\finalrasters.tif', 'w',
                       driver='GTiff',
                       height=everything.shape[0],
                       width=everything.shape[1],
                       count=1,
                       dtype='float32',
                       crs=slope.crs,
                       #transform=new_transform,
                       #nodata=slope.nodata,
    ) as out_raster:
        data = everything.astype('int8')
        out_raster.write(data, indexes=1)
        
hello = rasterio.open(r'D:\PythonProgramming\data\finalraster.tif')
show(hello)

variable =pd.read_csv(r'D:\PythonProgramming\data\transmission_stations.txt')
resultss= np.where(everything ==5)
rez = pd.DataFrame(np.transpose(resultss))

#convert dataframes into numpy arrays
df1_arr = np.array([np.array(x) for x in rez.values])
df2_arr = np.array([np.array(x) for x in variable.values])

cart_arr = np.array([x for x in product(df1_arr,df2_arr)])

#compute Euclidian distance (or norm) between pairs of elements in two arrays
#outputs new array with one value per pair of coordinates
norms_arr = np.linalg.norm(np.diff(cart_arr, axis=1)[:,0,:],axis=1)

min(norms_arr)
max(norms_arr)