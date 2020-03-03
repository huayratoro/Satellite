### GRAFICO DE DPR CON OTRA FUNCION Y DELIMITADO POR LINEAS NEGRAS
### EXTRAIDO DE https://github.com/dopplerchase/GPMtools/blob/master/GPM_CO.ipynb


#load in the required packages
import h5py
#this is my colormap script, can download it here: https://github.com/dopplerchase/colormaps.git
import drpy
import colormaps_new as cmaps
import numpy as np

## cargando el archivo de DPR
filename_DPR = ''
DPR = h5py.File(filename_DPR,'r')

#load in the DPR data 
lat2 = DPR['NS']['Latitude'][:,:]
lon2 = DPR['NS']['Longitude'][:,:]
z = DPR['NS']['SLV']['zFactorCorrectedNearSurface'][:]

#where are the DPR longitudes greater than or equal to -79.25
ind = np.where(lon2[:,0] >= -72)
#where are the DPR longitudes less than or equal to -77
ind2 = np.where(lon2[:,0] <= 72)
#where are both conditions satisfied 
ind3 = np.intersect1d(ind,ind2)
### GRAFICADO 
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
        facecolor='none',edgecolor='black')

#define figure
plt.figure(figsize=(10,5))
ax = plt.axes(projection=ccrs.PlateCarree())
#plot the DPR swath 
#pm2 = ax.scatter(lon2,lat2,c=z,s=25,vmin=12,vmax=60,cmap=cmaps.HomeyerRainbow,edgecolor='k',linewidth=0.001,zorder=3)
z[z < 0] = 0
pm2 = ax.contourf(lon2,lat2,z,vmin=12,vmax=60, cmap = cmaps.HomeyerRainbow)
#plot swath edges of the DPR
ax.plot(lon2[:,0]+0.03,lat2[:,0]-0.03,'--k',zorder=4)
ax.plot(lon2[:,-1]-0.03,lat2[:,-1]+0.03,'--k',zorder=4)

#plot cross-section lines, again more hard code here
ax.plot(lon2[ind3,27],lat2[ind3,27],'-w',zorder=4,lw=0.25,alpha=0.75)
ax.plot(lon2[ind3[0],27],lat2[ind3[0],27],'*w',zorder=4,lw=0.25,alpha=0.75,markerfacecolor='k',markeredgewidth=0.25)
ax.plot(lon2[2043,:],lat2[2043,:],'-w',zorder=4,lw=0.25,alpha=0.75)
ax.plot(lon2[2043,0],lat2[2043,0],'*w',zorder=4,lw=0.25,alpha=0.75,markerfacecolor='k',markeredgewidth=0.25)

#Add DPR colorbar
cbar = plt.colorbar(pm2,shrink=0.3)
cbar.set_label('Z, [dBZ]',fontsize=14)
cbar.ax.tick_params(labelsize=12)

## agrego atributos al grafico
#set the bounds of the map
#define box (para cortar en toda el area)
center_lat =  47.5615
center_lon = -52.7126 
ax.set_extent([center_lon - 10,center_lon +10, center_lat-5.8,center_lat+5.8])

# Agregamos la línea de costas
ax.coastlines(resolution='10m',linewidth=0.6)
    
# Agregamos los límites de los países
ax.add_feature(countries,linewidth=0.4)
    
# Agregamos los límites de las provincias
ax.add_feature(states_provinces,linewidth=0.4)

plt.show()
