import pandas as pd
import geopandas as gpd
import os
import glob
import numpy as np

files=glob.glob(r'C:\ThesisData\7292021\*.csv')
list1= []
files2= glob.glob(r'C:\ThesisData\10262021\*.csv')
list2= []
list3=[]
dictionary= {'SensorName' : [],
             'Data' : []}
for items in files:
    x = pd.read_csv(filepath_or_buffer =items, skiprows=15, 
                encoding= 'unicode_escape', engine= 'python', names= ['Date', 'Time', 'Unit', 'Temperature'])
    x['Date/Time'] = x['Date'] + x['Time']
    y =x.drop('Date', axis=1)
    z= y.drop('Time', axis=1)
    z= z[['Date/Time', 'Unit', 'Temperature']]
    z['Date/Time']=pd.to_datetime(z['Date/Time'])

    for pieces in files2:
        a = pd.read_csv(filepath_or_buffer =pieces, skiprows=15, 
                encoding= 'unicode_escape', engine= 'python', names= ['Date/Time', 'Unit', 'Temperature'])
        a['Date/Time']=pd.to_datetime(a['Date/Time'])
    
        if items[-17 :-13 ] == pieces [-17 :-13 ]:
            together= [z, a]
            final= pd.merge_ordered(z,a, fill_method='ffill')
            dictionary['SensorName'].append(items[-17:-13])
            dictionary['Data'].append(final)
            
for measures in dictionary['Data']:
    i=0
    temps= list(measures.items())[0][i]
    i= +1 
    celsius= pd.DataFrame(measures)  
    celsius.isna().sum() 
    
df= (dictionary['SensorName'])
a=0
for measures in dictionary['Data']:
    measures['Date/Time']= pd.to_datetime(measures['Date/Time'])
    x= measures.set_index('Date/Time')
    y= x.drop('Unit', axis=1)
    val = y.loc[y.groupby(y.index.dayofyear).idxmax().iloc[0:,0]]
    val2 = y.loc[y.groupby(y.index.dayofyear).idxmin().iloc[0:,0]]
    val1= val.rename(columns= {'Temperature' : 'TempMax'})
    valtwo= val2.rename(columns = {'Temperature': 'TempMin'})
    result = pd.concat([val1, valtwo], axis=1, join='outer')
    result['SensorName']=df[a]
    a += 1
    o= result.reset_index()
    q=o.to_numpy()
    p=np.transpose(q)
    r=pd.DataFrame(p)
    r.insert(0, 'Labels', ('Time/Date', 'TempMax', 'TempMin', 'SensorName'))
    pd.DataFrame(r).to_csv('Final.csv', mode='a', index=False)