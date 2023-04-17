import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib
import matplotlib.pyplot as plt
from compute_ERA5_z import compute_ERA5_z
from compute_ERA5_pressure import compute_ERA5_pressure

example='/ciclad-home/legras/data/flexpart_in/ERA5/'+\
        'EN-true/2012/ERA5EN20120201.grb'

#Read in an ERA5 grb file
#You need to install the cfgrib library to be able to run this
#Print the metadata
dataset=xr.open_dataset(example,engine='cfgrib')

#Read in an ERA5 grb file
#You need to install the cfgrib library to be able to run this
#Print the metadata
dataset=xr.open_dataset(example,engine='cfgrib')
print(dataset)

#Read in an ERA5 grb file and save variables
#You need to install the cfgrib library to be able to run this

#Note: I always get error messages when I open *grib files using
#xarray with the cfgrib engine but the files still load correctly

sp_dataset=xr.open_dataset(example,engine='cfgrib',\
                        backend_kwargs={'filter_by_keys':\
                                        {'shortName':'lnsp'}})

#log of surface pressure is given
#in the *grb files and must be converted
sp=np.exp(xr.DataArray.to_numpy(sp_dataset['lnsp'][:])) #surface pressure in Pa

dataset=xr.open_dataset(example,engine='cfgrib')

latitude=xr.DataArray.to_numpy(dataset['latitude'][:])
longitude=xr.DataArray.to_numpy(dataset['longitude'][:])

T=xr.DataArray.to_numpy(dataset['t'][:]) #temperature [K]
w=xr.DataArray.to_numpy(dataset['w'][:]) #pressure velocity [Pa s-1]
u=xr.DataArray.to_numpy(dataset['u'][:]) #horizontal wind [m s-1]
v=xr.DataArray.to_numpy(dataset['v'][:]) #horizontal wind [m s-1]

#Create variables for the 3D pressure
p=np.zeros(np.shape(T))

#Compute pressure for each column using surface pressure
for hour in range(np.shape(p)[0]):
    for lat in range(np.shape(p)[2]):
        for lon in range(np.shape(p)[3]):
            p[hour,:,lat,lon]=\
                    compute_ERA5_pressure(sp[hour,lat,lon]) #Pa

#Create variables for the 3D height
height=np.zeros(np.shape(T))
            
#Compute height for each column using surface pressure
for hour in range(np.shape(p)[0]):
    for lat in range(np.shape(p)[2]):
        for lon in range(np.shape(p)[3]):
            height[hour,:,lat,lon]=\
                    compute_ERA5_z(sp[hour,lat,lon],T[hour,:,lat,lon]) #m

#Plot surface pressure from ERA5 for first hour in file on a map
fig=plt.figure()
projection = ccrs.PlateCarree()
ax = fig.add_subplot(1, 1, 1, projection=projection)
ax.coastlines(color='r')
im=ax.pcolormesh(longitude,latitude,sp[0],transform=projection)
ax.set_title('Surface Pressure (Pa)')
fig.colorbar(im,shrink=.5)
fig.savefig('example_surface_pressure_map.png')

#Plot global mean temperature "curtain" (time-height plot)
fig,ax=plt.subplots()
im=ax.pcolormesh(np.linspace(0,21,8),np.mean(height,axis=(0,2,3)),np.transpose(np.mean(T,axis=(2,3))))
ax.set_title('Global mean temperature (K)')
ax.set_xlabel('Hour of 1 February 2012')
ax.set_ylabel('Global Mean Height (km)')
fig.colorbar(im)
fig.savefig('example_time_height_temperature_plot.png')


