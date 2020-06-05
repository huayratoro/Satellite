import matplotlib.pyplot as plt
import numpy as np
from pyhdf.SD import SD, SDC
import scipy.io as sio
from matplotlib.ticker import FixedLocator
import cartopy.feature as cfeature
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from os import listdir
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

## se carga la topografia
# en este caso se utiliza la del ERA5 
topografia = '.../orografia_cortada.nc'  
from netCDF4 import Dataset as ds
top = ds(topografia, 'r')
z_sup = top.variables[u'z'][:]
lat_z  = top.variables[u'latitude'][:]
lon_z  = top.variables[u'longitude'][:]
top.close()
z_sup = z_sup[0,:,:] / 9.81

# abriendo el archivo
salida = '.../'
path = '.../pf_201001_level2.HDF'
data = SD(path, SDC.READ)

datasets = data.datasets()
#  se enumeran los atributos y variables del HDF

#for idx,sds in enumerate(datasets.keys()):
#    print (idx,sds, data.select(sds).attributes())
#exit()

## Selecciono dimensiones, LAT y LON, YEAR, MONTH, DAY, HOUR de las variables
############## TENER CUIDADO !!
## ALGUNAS VARIABLES TIENEN SUS PROPIAS LAT LON MAS ALLA DE LAS LAT-LON GLOBALES
# este es un ejemplo, sino cargar las lat-lon globales 
#lat = (data.select('LAT')).get() 
#lon = (data.select('LON')).get()
lat_var1 = (data.select('MINIRLAT')).get() 
lon_var1 = (data.select('MINIRLON')).get()  # de minimum 10.8 um Tb
lat_var2 = (data.select('MAXNSZLAT')).get() # de maximum near surface reflectivity 
lon_var2 = (data.select('MAXNSZLON')).get()

y, month = (data.select('YEAR')).get()[0], (data.select('MONTH')).get()[0]
day = (data.select('DAY')).get() 
hour = (data.select('HOUR')).get()

#### para que no grafique tantos puntos, se puede imponer condiciones a las variables, como 
# umbrales minimos o maximos :
minir = data.select('MINIR').get()
# quiero los puntos de TB 10.8 menores a 220 K (topes de conveccion humeda profunda)
lat_var1 = lat_var1[np.where(minir <= 220)]
lon_var1 = lon_var1[np.where(minir <= 220)]
# y los valores de ref max superiores a 55 dBZ
mnsz = data.select('MAXNSZ').get()
lat_var2 = lat_var2[np.where(mnsz >= 55)]
lon_var2 = lon_var2[np.where(mnsz >= 55)]
### grafico

plt.figure(figsize=(11,6))
ax1 = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree())

# Definimos los limites del area a visualizar

lonwest = -75
loneast = -55
latsouth = -38
latnorth = -10.5
# la cantidad de etiquetas de latitudes y longitudes en el grafico es el divisor 
sp_lat = (latnorth - latsouth) / 5
sp_lon = (loneast - lonwest) / 3
ax1.set_extent([lonwest, loneast, latsouth, latnorth], crs=ccrs.PlateCarree())

ax1.scatter(lon_var1, lat_var1, color = 'blue',marker = '+', transform=ccrs.PlateCarree(), label = 'min 10.8 um Tb < 220 k')
ax1.scatter(lon_var2, lat_var2, color = 'red',marker = '^', transform=ccrs.PlateCarree(), label = 'max near surf reflect > 55 dBZ')

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