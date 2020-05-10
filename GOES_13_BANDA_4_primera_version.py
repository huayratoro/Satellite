### SCRIPT PARA GRAFICAR UN CAMPO DE REFLECTANCIAS DE LA BANDA 04 (10.7) DEL GOES 13
### LOS DATOS SE PUEDEN CONSEGUIR DE :
### https://www.avl.class.noaa.gov/saa/products/search?sub_id=0&datatype_family=GVAR_IMG&submit.x=13&submit.y=9
### SE NECESITA UNA SUBSCRIPCION
### POWERED BY HUAYRATORO

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

entrada = '.../'
salida = '.../'

## CAMBIAR LA RUTA
data=Dataset(entrada+'goes13.2013.365.170927.BAND_04.nc','r')

## SE LEEN LAS VARIABLES
variables = data.variables.keys()
t = data.variables['data'][0,:,:]/32
lat = data.variables['lat'][:]
lon = data.variables['lon'][:]

## hay que transformar los datos a temperatura de brillo
R=(t-15.6854)/5.2285
C1=1.438833*937.27
C2= 1 + 1.191066e-5*(937.27**3)/R
TB=C1/np.log(C2) 

# PARA SABER EL AREA EN LA CUAL ESTAN LOS DATOS
#print(np.min(TB), np.max(TB))

## la hora de medicion
time = str(datetime.strptime(str(data.variables['crDate'][0]) + str(data.variables['crTime'][0]), '%Y%j%H%M%S'))

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

## barra de colores 
from barra_goes16_IR import loadCPT
from matplotlib.colors import LinearSegmentedColormap
# Converts the CPT file to be used in Python
# barra de colores del goes 16
cpt = loadCPT('.../IR4AVHRR6.cpt')
# Makes a linear interpolation with the CPT file
cpt_convert = LinearSegmentedColormap('cpt', cpt)
##
fig = plt.figure(figsize=(11,6))
ax = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree())
## reflectancias
l = np.arange(-103, 105, 1.5)
cm = ax.contourf(lon, lat, TB-273, l, cmap = cpt_convert, transform=ccrs.PlateCarree())
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
ax.set_yticks(np.arange(lat_s,lat_n,1.5), crs=ccrs.PlateCarree())
ax.set_xticks(np.arange(lon_w,lon_e,2), crs=ccrs.PlateCarree())

plt.colorbar(cm)
plt.title(time + ' Z')

plt.savefig(salida+'GOES_13_fecha_BANDA_4_'+time+'.png', dpi = 300)