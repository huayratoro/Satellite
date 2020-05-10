### SCRIPT PARA GRAFICAR UN CAMPO DE REFLECTANCIAS DE LA BANDA 01 DEL GOES 13
### LOS DATOS SE PUEDEN CONSEGUIR DE :
### https://www.avl.class.noaa.gov/saa/products/search?sub_id=0&datatype_family=GVAR_IMG&submit.x=13&submit.y=9
### SE NECESITA UNA SUBSCRIPCION
### POWERED BY HUAYRATORO

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

entrada = '.../'
salida = '.../'

## CAMBIAR LA RUTA
data=Dataset(entrada+'goes13.2013.365.160928.BAND_01.nc','r')

## SE LEEN LAS VARIABLES
variables = data.variables.keys()
ref = data.variables['data'][0,:,:] / np.max(data.variables['data'][0,:,:])
lat = data.variables['lat'][:]
lon = data.variables['lon'][:]

# PARA SABER EL AREA EN LA CUAL ESTAN LOS DATOS
#print(np.min(lon), np.max(lon))

## graficado

import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.patheffects as PathEffects
import cartopy.io.shapereader as shpreader

states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='10m',
        facecolor='none',edgecolor='red')

countries = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_0_countries',
        scale='10m',
        facecolor='none',edgecolor='red')

fig = plt.figure(figsize=(11,6))
ax = plt.axes(projection=ccrs.PlateCarree())
## reflectancias
l = np.arange(0,1,0.005)
cm = ax.contourf(lon, lat, ref, l, cmap = 'Greys_r')
lat_n = -21
lat_s = -26.75
lon_w = -70
lon_e = -61
ax.set_extent([lon_w,lon_e,lat_s,lat_n])

# Agregamos la línea de costas
ax.coastlines(resolution='10m',linewidth=0.6)    
# Agregamos los límites de los países
ax.add_feature(countries,linewidth=0.4)
# Agregamos los límites de las provincias
ax.add_feature(states_provinces,linewidth=0.4)

# Definimos donde aparecen los ticks con las latitudes y longitudes
ax.set_yticks(np.arange(lat_s,lat_s,1.5), crs=ccrs.PlateCarree())
ax.set_xticks(np.arange(lon_w,lon_e,2), crs=ccrs.PlateCarree())

plt.colorbar(cm)
plt.title('Agregar cualquier titulo')

plt.savefig(salida+'GOES_13_fecha_BANDA_1.png', dpi = 300)