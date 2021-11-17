import numpy as np
import pandas as pd
import geopandas as gpd
from math import pi
import numpy.ma as ma
from scipy import ndimage
import rasterio
import glob
import operator
from matplotlib import pyplot as plt

def slopeAspect(dem, cs):
    """Calculates slope and aspect using the 3rd-order finite difference method

    Parameters
    ----------
    dem : numpy array
        A numpy array of a DEM
    cs : float
        The cell size of the original DEM

    Returns
    -------
    numpy arrays
        Slope and Aspect arrays
    """

    from math import pi
    from scipy import ndimage
    kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    dzdx = ndimage.convolve(dem, kernel, mode='mirror') / (8 * cs)
    dzdy = ndimage.convolve(dem, kernel.T, mode='mirror') / (8 * cs)
    slp = np.arctan((dzdx ** 2 + dzdy ** 2) ** 0.5) * 180 / pi
    ang = np.arctan2(-dzdy, dzdx) * 180 / pi
    aspect = np.where(ang > 90, 450 - ang, 90 - ang)
    return slp, aspect


def reclassAspect(npArray):
    """Reclassify aspect array to 8 cardinal directions (N,NE,E,SE,S,SW,W,NW),
    encoded 1 to 8, respectively (same as ArcGIS aspect classes).

    Parameters
    ----------
    npArray : numpy array
        numpy array with aspect values 0 to 360

    Returns
    -------
    numpy array
        numpy array with cardinal directions
    """
    return np.where((npArray > 22.5) & (npArray <= 67.5), 2,
    np.where((npArray > 67.5) & (npArray <= 112.5), 3,
    np.where((npArray > 112.5) & (npArray <= 157.5), 4,
    np.where((npArray > 157.5) & (npArray <= 202.5), 5,
    np.where((npArray > 202.5) & (npArray <= 247.5), 6,
    np.where((npArray > 247.5) & (npArray <= 292.5), 7,
    np.where((npArray > 292.5) & (npArray <= 337.5), 8, 1)))))))

def reclassByHisto(npArray, bins):
    """Reclassify np array based on a histogram approach using a specified
    number of bins. Returns the reclassified numpy array and the classes from
    the histogram.

    Parameters
    ----------
    npArray : numpy array
        Array to be reclassified
    bins : int
        Number of bins

    Returns
    -------
    numpy array
        umpy array with reclassified values
    """
    histo = np.histogram(npArray, bins)[1]
    rClss = np.zeros_like(npArray)
    for i in range(bins):
        rClss = np.where((npArray >= histo[i]) & (npArray <= histo[i + 1]),
                         i + 1, rClss)
    return rClss

DEM = rasterio.open(r'D:\OneDrive\Documents\College Shit\Graduate School\Semester 5\data\bigElk_dem.tif')
DEMdata = DEM.read(1)
cellsize = 30 #meters
slopeasp =slopeAspect(DEMdata, cellsize)
slope, asp= slopeasp
aspect360 = reclassAspect(asp)
slopeclasses = reclassByHisto(slope, 10)

def NDVI(year):
    for files in glob.glob(r'D:\OneDrive\Documents\College Shit\Graduate School\Semester 5\data\L5_big_elk\*.tif'):
        if files[-11:-7] == year:
            rasters = rasterio.open(files)
            
            if files[-6:-4] == 'B3':
                B3= rasters.read(1)
                
            if files[-6:-4] == 'B4':
                B4 = rasters.read(1)
         
                NDVIyear = np.divide((np.subtract((B4), (B3))), (np.add((B4), (B3))))
                return(NDVIyear)
NDVI('2002')
NDVI('2003')
NDVI('2004')
NDVI('2005')
NDVI('2006')
NDVI('2007')
NDVI('2008')
NDVI('2009')
NDVI('2010')
NDVI('2011')

        #stays the same for each year
FirePeri = rasterio.open(r'D:\OneDrive\Documents\College Shit\Graduate School\Semester 5\data\fire_perimeter.tif')
FireData= FirePeri.read(1)
healthyforest= np.where(FireData == 2, 1, 0) 
        #1 now equals healthy forest, 0 is all else
    
def RR(year):
    temp_arr= np.zeros_like(NDVI(year))
    totalofyear= np.multiply(NDVI(year), healthyforest)
    hello= totalofyear[totalofyear !=0]
    meanyear= np.mean(hello)
    RRyear= np.divide(NDVI(year), meanyear)
    flatboi = RRyear.flatten()
    final= list(flatboi)
    return final

TotalRR=np.column_stack([RR('2002'), RR('2003'), RR('2004'), RR('2005'), RR('2006'), RR('2007'), RR('2008'), RR('2009')
                      , RR('2010'), RR('2011')])
AllRR= np.transpose(TotalRR)

year= np.array(['2002','2003','2004','2005','2006','2007','2008','2009','2010','2011'], dtype='float64')
RRline =np.polyfit(year, AllRR, 1)
onlyslopeofline = np.delete(RRline, 1, 0)
backtonormal= np.reshape(onlyslopeofline, (280, 459))
healthonly= backtonormal[healthyforest ==0]
print(('The mean coefficient of recovery is'), healthonly.mean())

def RRMean(Year):
    meanrr = sum(RR(Year))/len(RR(Year))
    return meanrr

print(RRMean('2002'))
print(RRMean('2003'))
print(RRMean('2004'))
print(RRMean('2005'))
print(RRMean('2006'))
print(RRMean('2007'))
print(RRMean('2008'))
print(RRMean('2009'))
print(RRMean('2010'))
print(RRMean('2011'))

def ZonalStats (RecovRatio, SlopeorAsp, csvname):
    eachzone= np.unique(SlopeorAsp)
    dictionary= {'zones': [], 'mean':[], 'max':[], 'min':[], 'sd':[], 'count':[]}
    x=1
    for zones in list(eachzone):
        dictionary['zones'].append(x)
        onlyzone= np.where(SlopeorAsp ==x,1,np.nan)
        dictionary['mean'].append(np.nanmean(onlyzone*RecovRatio))
        dictionary['max'].append(np.nanmax(onlyzone*RecovRatio))
        dictionary['min'].append(np.nanmin(onlyzone*RecovRatio))
        dictionary['sd'].append(np.nanstd(onlyzone*RecovRatio))
        dictionary['count'].append(np.nansum(onlyzone))
        x=x+1
    df= pd.DataFrame(dictionary)
    csvname=df.to_csv(csvname)
    
ZonalStats(backtonormal, slopeclasses, 'SlopeStatsAll.csv')
ZonalStats(backtonormal, aspect360, 'AspectStatsAll.csv')

healthyforestreverse= np.where(FireData == 2, 0, 1)
burnedcoeff= np.where(healthyforestreverse ==1, backtonormal, 0)

with rasterio.open(r'D:\PythonProgramming\data\Lab5Finale.tif', 'w',
                    driver = "Gtiff",
                    height = burnedcoeff.shape[0],
                    width= burnedcoeff.shape[1],
                    count = 1,
                    dtype = 'float32',
                    crs = FirePeri.crs,
                    transform = FirePeri.transform,
                    nodata= 0,
                )as out_raster:
                out_raster.write(burnedcoeff,1)    
                       
print("According to the final output .tif, the areas with the best coefficient of recovery \n" 
"were the areas that were in river valleys, and on northern and western slopes. The driving factor for \n"
"this is likely precipitation. Eastern slopes are in a rain shadow, and southern slopes \n"
"receive the most sun, which will impact how much moisture absorption and retention vegetation has. \n"
"Finally, erosion and runoff are big issues after fire, so the moisture received on steeper slopes \n"
"was not as utilizable to the recovering vegetation there.")