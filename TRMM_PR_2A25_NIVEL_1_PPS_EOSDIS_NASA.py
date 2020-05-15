### Para leer los 2A25 del TRMM en CRUDO
### para graficar los valores de pp estimada o reflectividad corregida
### en distintas alturas.
### Los datos estan en 
### ftp://arthurhou.pps.eosdis.nasa.gov/trmmdata/ByDate/V07/
### se necesita registro previo.

from pyhdf.SD import SD, SDC
import numpy as np
from datetime import datetime
# solo para la barra de colores
import pyart

##### selecciono la altura del corte :
altura = 3.5

## cargando el archivo de DPR
path = '.../'
salida = '.../'
filename = '2A25.20101222.74636.7.HDF'

# se lee el HDF
f = SD(path+filename, SDC.READ)
datasets_dic = f.datasets()

# para ver el contenido del HDF
#for idx,sds in enumerate(datasets_dic.keys()):
#    print (idx,sds)
#exit()

# seleccionando las variables
# la reflectividad hay que multiplicarla por 0.01
z = f.select('correctZFactor') # selecciona el SDS
z = z.get() * 0.01 # extrae los datos del SDS
# los valores inferiores a cero son de datos inexistentes
z[z < 0] = 0

# las alturas estan al reves, asi que armo un vector decreciente
# las mediciones se hacen con una escala vertical de 250 metros
h = np.arange(20, 0, -0.25)

# latitudes y longitudes 
lat = f.select('Latitude') # selecciona el SDS
lat = lat.get() # extrae los datos del SDS
lon = f.select('Longitude') # selecciona el SDS
lon = lon.get() # extrae los datos del SDS

# Para la fecha 
yy = str((f.select('Year').get())[0])
mm = str('%02i' % (f.select('Month').get())[0])
dd = str('%02i' % (f.select('DayOfMonth').get())[0])
hour = str('%02i' % (f.select('Hour').get())[0])
fecha = str(datetime.strptime(yy+mm+dd+' '+hour, '%Y%m%d %H'))

# el numero de orbita
orbita = filename[14:19]

### GRAFICADO ###

import matplotlib.pyplot as plt 
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
        facecolor='none',edgecolor='black')

countries = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_0_countries',
        scale='10m',
        facecolor='none',edgecolor='magenta')

plt.figure(figsize=(11,6))
ax = plt.axes(projection=ccrs.PlateCarree())

# cortamos el area de interes
lonwest = -62.900001525878906
loneast = -53.400001525878906
latsouth = -31.149999618530273
latnorth = -25.100000381469727
sp_lat = (latnorth - latsouth) / 4
sp_lon = (loneast - lonwest) / 4
ax.set_extent([lonwest, loneast, latsouth, latnorth], crs=ccrs.PlateCarree())

# corto en la altura y grafico
lugar = int((np.where(h == altura))[0])
pm2 = ax.pcolormesh(lon,lat,z[:,:,lugar],vmin = 15, vmax = 60,cmap = 'pyart_PD17')

# Colorbar
cbar = plt.colorbar(pm2)

# Agregamos la línea de costas
ax.coastlines(resolution='10m',linewidth=0.6)
    
# Agregamos los límites de los países
ax.add_feature(countries,linewidth=0.4)
    
# Agregamos los límites de las provincias
ax.add_feature(states_provinces,linewidth=0.4)
# Definimos donde aparecen los ticks con las latitudes y longitudes
ax.set_yticks(np.arange(latsouth,latnorth,sp_lat), crs=ccrs.PlateCarree())
ax.set_xticks(np.arange(lonwest,loneast,sp_lon), crs=ccrs.PlateCarree())

# titulamos el grafico
plt.title('Level 1 TRMM-PR reflectivity corrected a '+ str(altura) + ' km de altura \n ' + fecha + ' UTC ' + ' orbita ' + orbita + ' en CRUDO')

plt.savefig(salida+'/TRMM_PR_2A25_CRUDO_'+orbita+'_'+fecha+'.png', dpi = 300, bbox_inches = 'tight')
plt.close('all')
