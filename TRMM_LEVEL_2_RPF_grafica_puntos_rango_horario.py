# script para graficar las nubes de puntos para un mes particular de un conjunto de variables 
# del producto de level-2 TRMM data con topografia  

import matplotlib.pyplot as plt
import numpy as np
from pyhdf.SD import SD, SDC
import scipy.io as sio
from matplotlib.ticker import FixedLocator
import cartopy.feature as cfeature
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from os import listdir
from netCDF4 import Dataset as ds
from funciones_auxiliares_TRMM import corta_region, corta_region_horas

## se carga la topografia
# en este caso se utiliza la del ERA5 
topografia = '.../orografia_cortada.nc'  

top = ds(topografia, 'r')
z_sup = top.variables[u'z'][:]
lat_z  = top.variables[u'latitude'][:]
lon_z  = top.variables[u'longitude'][:]
top.close()
z_sup = z_sup[0,:,:] / 9.81

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

# abriendo el HDF
salida = '.../'
path = '.../pf_201001_level2.HDF'
data = SD(path, SDC.READ)

# para ver las variables y dimensiones : 
datasets = data.datasets()

# para ver las variables y dimensiones :

#for idx,sds in enumerate(datasets.keys()):
#    print (idx,sds, data.select(sds).attributes())
#exit()

## Como variables, me interesan VOLRAIN_2A25, por ejemplo
# selecciono la o las variables del HDF
var_1 = (data.select('NPIXELS_20DBZ')).get()
var_2 = (data.select('NPIXELS_30DBZ')).get()
var_3 = (data.select('NPIXELS_40DBZ')).get()
var_4 = (data.select('NPIXELS_50DBZ')).get()

## Como dimensiones, LAT y LON, YEAR, MONTH, DAY, HOUR
lat = (data.select('LAT')).get()    # latitudes de los puntos 
lon = (data.select('LON')).get()    # longitudes de los puntos
y, month = (data.select('YEAR')).get()[0], (data.select('MONTH')).get()[0]  # anios y meses
day = (data.select('DAY')).get()    # los dias del mes     
hour = (data.select('HOUR')).get()  # horas del dia en UTC (cuidado!! las 11:30 estan como 11.5 !)

## Si se quiere se le pueden imponer condiciones a las variables, como quedarse con todos los valores
## de MAXNSZ superiores a tal umbral e indexar, o seleccionar por rango horario

# se grafican las nubes de puntos
plt.figure(figsize=(11,6))
ax1 = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree())

# Definimos los limites del area a visualizar

lonwest = -75
loneast = -52
latsouth = -38
latnorth = -20
# cantidad de etiquetas de latitud y longitud
sp_lat = (latnorth - latsouth) / 4
sp_lon = (loneast - lonwest) / 3
ax1.set_extent([lonwest, loneast, latsouth, latnorth], crs=ccrs.PlateCarree())
# la funcion para hacer nubes de puntos es 'scatter'

## En este caso se grafica por horas del dia 

# primero establecemos los limites de lat, lon y horas
# se toman los puntos dentro de estos limites geograficos
lat_n, lat_s, lon_w, lon_e = -20, -38, -75, -50

# los rangos horarios considerados son maniana [9-15), tarde [15-22), noche [22-3) y madrugada [3-9)
# vale para Argentina
rango_h = [9, 15, 22, 3]    # recordar que son UTC
h1, h2 = rango_h[0], rango_h[1]

# luego, para seleccionar los datos por horas del dia y region geografica utilizo el paquete de funciones
# auxiliares de TRMM en el repositorio.
#  
ax1.scatter(lon[corta_region_horas(var_1, lat, lon, hour, lon_w, lon_e, lat_n, lat_s, h1, h2)], 
lat[corta_region_horas(var_1, lat, lon, hour, lon_w, lon_e, lat_n, lat_s, h1, h2)], color = 'blue',marker = '+', transform=ccrs.PlateCarree(), label = 'NPIXEL 20dBZ')

ax1.scatter(lon[corta_region_horas(var_2, lat, lon, hour, lon_w, lon_e, lat_n, lat_s, h1, h2)], 
lat[corta_region_horas(var_2, lat, lon, hour, lon_w, lon_e, lat_n, lat_s, h1, h2)], color = 'green',marker = '+', transform=ccrs.PlateCarree(), label = 'NPIXEL 30dBZ')

ax1.scatter(lon[corta_region_horas(var_3, lat, lon, hour, lon_w, lon_e, lat_n, lat_s, h1, h2)], 
lat[corta_region_horas(var_3, lat, lon, hour, lon_w, lon_e, lat_n, lat_s, h1, h2)], color = 'orange',marker = '+', transform=ccrs.PlateCarree(), label = 'NPIXEL 40dBZ')

ax1.scatter(lon[corta_region_horas(var_4, lat, lon, hour, lon_w, lon_e, lat_n, lat_s, h1, h2)],
lat[corta_region_horas(var_4, lat, lon, hour, lon_w, lon_e, lat_n, lat_s, h1, h2)], color = 'red',marker = '+',transform=ccrs.PlateCarree(), label = 'NPIXEL 50dBZ')

# la legenda del grafico
ax1.legend()

# Se agrega el contorno del terreno mayor a 1500 mts
l = np.arange(1500, 1501, 1)
ax1.contour(lon_z, lat_z, z_sup, l,colors = ['brown'])

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

plt.title('Para la fecha ' + str(y) + '-' + str(month))

plt.savefig(salida+'nube_de_puntos'+str(y)+str(month)+'.png', dpi = 300, bbox_inches = 'tight')