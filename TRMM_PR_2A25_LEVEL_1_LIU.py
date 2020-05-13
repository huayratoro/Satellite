## SCIPT para leer y graficar los datos de NIVEL 1 del sensor TRMM-PR (producto 2A25)
## Los datos estan libres en la pagina :
## http://atmos.tamucc.edu/trmm/data/trmm/level_1/
## revisar bien la orbita antes de bajar !!
## se puede hacer con el GES DISC
## POWERED BY HUAYRATORO

import matplotlib.pyplot as plt
import numpy as np
from pyhdf.SD import SD, SDC
import scipy.io as sio
from matplotlib.ticker import FixedLocator
import cartopy.feature as cfeature
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from os import listdir
from datetime import datetime
## solo para la barra de colores
import pyart

# abriendo el archivo

path = '.../'
salida = '.../'
hdf = '1Z09.20101222.74636.7.HDF'
data = SD(path+hdf, SDC.READ)

fecha = str(datetime.strptime(hdf[5:13], '%Y%m%d').date())
orbita = str(hdf[16:19])  

datasets = data.datasets()
#for idx,sds in enumerate(datasets.keys()):
#    print (idx,sds)

# me interesan las variables pr.nearSurfZ, pr.nearSurfRain, y 
# las dimensiones scan, ray, pr.lon, pr.lat

# selecciono estas variables 

# cuidado que los valores de ref estan en una escala de
# 0.01 dBZ (multiplicar por 0.01)
pr_dbz = data.select('pr.nearSurfZ')
pr_dbz = pr_dbz.get() * 0.01
# la lluvia esta en mm/hr
pr_rain = data.select('pr.nearSurfRain')
pr_rain = pr_rain.get()

# selecciono las dimensiones
# cuidado que estan en centrigrado ????
pr_lat = (data.select('pr.lat')).get() / 100
pr_lon = (data.select('pr.lon')).get() / 100

#print(((data.select('tmilis.viewtime.tai93_start')).get()).shape)
#print(np.min(pr_rain), np.max(pr_rain))
#print(pr_lon/100)
#pr_rain[pr_rain > 100] = 0
#exit()
#### Probando el grafico de los datos 

# Cargamos los límites de países y provincias para poder graficarlas en los mapas

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
ax1 = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree())

# Definimos los limites del area a visualizar

lonwest = -64
loneast = -50
latsouth = -30
latnorth = -24
sp_lat = (latnorth - latsouth) / 2.5
sp_lon = (loneast - lonwest) / 2.5
ax1.set_extent([lonwest, loneast, latsouth, latnorth], crs=ccrs.PlateCarree())

# la barra de colores
# la lista coompleta esta en : https://github.com/jjhelmus/pyart_colormaps_and_limits/blob/master/plot_all_colormaps.py
variable = 'rain'

if variable == 'ref' :
    barra = 'pyart_HomeyerRainbow'
    l = np.arange(np.min(pr_dbz), np.max(pr_dbz))
    cm = ax1.contourf(pr_lon, pr_lat, pr_dbz, l[l != 0], cmap = barra)

if variable == 'rain' :
    barra = 'pyart_RRate11'
    l = np.arange(np.min(pr_rain), np.max(pr_rain))
    cm = ax1.contourf(pr_lon, pr_lat, pr_rain, l[l != 0], cmap = barra)

plt.colorbar(cm)

# Agregamos la línea de costas
ax1.coastlines(resolution='10m',linewidth=0.6)

    # Agregamos los límites de los países
ax1.add_feature(countries,linewidth=0.4)

    # Agregamos los límites de las provincias
ax1.add_feature(states_provinces,linewidth=0.4)

    # Definimos donde aparecen los ticks con las latitudes y longitudes
ax1.set_yticks(np.arange(latsouth,latnorth,sp_lat), crs=ccrs.PlateCarree())
ax1.set_xticks(np.arange(lonwest,loneast,sp_lon), crs=ccrs.PlateCarree())

    # Le damos formato a las etiquetas de los ticks
lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax1.xaxis.set_major_formatter(lon_formatter)
ax1.yaxis.set_major_formatter(lat_formatter)

if variable == 'ref':
    plt.title('Level 1 TRMM-PR reflectivity corrected near surface \n ' + fecha + ' orbita ' + orbita)
if variable == 'rain' :
    plt.title('Level 1 TRMM-PR near surface rain \n ' + fecha + ' orbita ' + orbita)
    
plt.savefig(salida+'/TRMM_PR_2A25_'+variable+'_'+fecha+'_'+orbita+'.png', dpi = 300, bbox_inches = 'tight')
