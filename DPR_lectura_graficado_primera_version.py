## SCRIPT PARA LEER LOS DPR Y GRAFICARLOS CON CARTOPY ##
## EXTRAIDO DE https://github.com/dopplerchase/DRpy/blob/master/notebooks/Example_one.ipynb ##

import drpy     # esta libreria se instala desde el Github
import time

# cargando el HDF del DPR
filename = ''

# para saber el tiempo 
stime = time.time()
dpr = drpy.core.GPMDPR(filename = filename)
dpr.read()
dpr.toxr()
etime = time.time()

### PARTE DE GRAFICADO ###

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.patheffects as PathEffects
import cartopy.io.shapereader as shpreader

from cartopy.mpl.geoaxes import GeoAxes
from mpl_toolkits.axes_grid1 import AxesGrid
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.colors as colors
import matplotlib.patheffects as PathEffects

states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='10m',
        facecolor='none',edgecolor='black')

countries = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_0_countries',
        scale='10m',
        facecolor='none',edgecolor='black')

#define box (para cortar en toda el area)
center_lat =  47.5615
center_lon = -52.7126 
corners = [center_lon - 10,center_lon +10, center_lat-5.8,center_lat+5.8]
#
dpr.corners = corners
#method 2: Cut the exisiting datset 
dpr.setboxcoords()
#drop dead weight (i.e. blank data)
dpr.xrds = dpr.xrds.dropna(dim='along_track',how='all')

#make figure
fig = plt.figure(figsize=(10, 10))
#add the map
ax = fig.add_subplot(1, 1, 1,projection=ccrs.PlateCarree())

## campo
ax.pcolormesh(dpr.xrds.lons,dpr.xrds.lats,dpr.xrds.nearsurfaceKu,vmin=12,vmax=50,cmap=drpy.graph.cmaps.HomeyerRainbow)

## agrego atributos al grafico
# Agregamos la línea de costas
ax.coastlines(resolution='10m',linewidth=0.6)
    
# Agregamos los límites de los países
ax.add_feature(countries,linewidth=0.4)
    
# Agregamos los límites de las provincias
ax.add_feature(states_provinces,linewidth=0.4)

plt.show()
