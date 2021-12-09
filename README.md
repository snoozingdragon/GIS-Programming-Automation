# GIS-Programming-Automation
Coding Samples from Class

Lab 5
This code takes LandSat 5 data from 2002-2011, a fire perimeter raster, and a DEM raster all from the Rocky Mountain National Park area.
The goal was to conclude rate of recovery for burned vegetation in this area based on slope and aspect. 

The DEM file was split into 8 cardinal directions, as well as 10 slope classes. 
NDVI was calculated from band 3 and 4 of the Landsat 5 data. 
Recovery Ratio was then calculated using the average of healthy forest(outside the burned area) and the NDVI for each pixel. 
Polyfit was used to create a slope through the 10 recovery ratio values generated for each pixel. This indicated whether a pixel was recovering or not. 

Zonal Statistics were calculated for the mean, standard deviation, minimum and maximum counts. 
Statistics were also calculated based on the cardinal direction and slope generated at the beginning. 
The final results of these statistics were used to create a GeoTiff file. 
