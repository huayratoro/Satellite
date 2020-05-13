## SCIPT para leer y graficar los datos de NIVEL 1 del sensor GPM-DPR
## Los datos estan libres en la pagina :
## http://atmos.tamucc.edu/trmm/data/gpm/level_1/
## POWERED BY HUAYRATORO

#load in the required packages
import h5py
import numpy as np
from datetime import datetime

## cargando el archivo de DPR
filename = '.HDF5'
salida = '.../'

f = h5py.File(filename,'r')

# para ver el contenido del archivo
#print(list(f.keys()))
# me interesarian las variables de : DPR__NSZ, DPR__NSPRECIP.
# los puntos sin dato son -9999.9
# la escala de refelctividad es en dBZ
nsz = f['DPR__NSZ'][:]
nsz[nsz == -9999.9] = 0
# la escala de precipitacion es en mm hr-1
nsp = f['DPR__NSPRECIP'][:]
# luego las dimensiones de : DPR__LAT, DPR__LON, DPR__YEAR, DPR__MONTH, DPR__DAY, DPR__MINUTE.
lat = f['DPR__LAT'][:]
lon = f['DPR__LON'][:]
yy = str(f['DPR__YEAR'][0])
mm = str('%02i' % f['DPR__MONTH'][0])
dd = str('%02i' % f['DPR__DAY'][0])
hr_i = str('%02i' % f['DPR__HOUR'][0])
hr_f = str('%02i' % f['DPR__HOUR'][len(f['DPR__HOUR'])-1])
#print(nsz.shape, lat.shape, lon.shape)
fecha_i = str(datetime.strptime(yy+mm+dd+' '+hr_i, '%Y%m%d %H'))
fecha_f = str(datetime.strptime(yy+mm+dd+' '+hr_i, '%Y%m%d %H'))

## GRAFICADO ##
import matplotlib.pyplot as plt 
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.patheffects as PathEffects
import cartopy.io.shapereader as shpreader
# solo para la barra de colores
import pyart

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

lonwest = -65
loneast = -54
latsouth = -35
latnorth = -27
sp_lat = (latnorth - latsouth) / 4
sp_lon = (loneast - lonwest) / 4
ax1.set_extent([lonwest, loneast, latsouth, latnorth], crs=ccrs.PlateCarree())

# la barra de colores
# la lista coompleta esta en : https://github.com/jjhelmus/pyart_colormaps_and_limits/blob/master/plot_all_colormaps.py
variable = 'rain'

if variable == 'ref' :
    barra = 'pyart_HomeyerRainbow'
    l = np.arange(0, 60)
    cm = ax1.contourf(lon, lat, nsz, l, cmap = barra)

if variable == 'rain' :
    barra = 'pyart_RRate11'
    l = np.arange(0, 110)
    cm = ax1.contourf(lon, lat, nsp, l[l != 0], cmap = barra)

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
    plt.title('Level 1 DPR Ku_Ka reflectivity corrected near surface \n para ' + fecha_i)
if variable == 'rain' :
    plt.title('Level 1 DPR Ku_Ka near surface rain \n para ' + fecha_i)
    
plt.savefig(salida+'DPR_'+variable+'_'+fecha_f+'.png', dpi = 300, bbox_inches = 'tight')