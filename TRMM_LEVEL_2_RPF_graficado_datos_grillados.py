## script para grillar los puntos en reticulas regulares de tamanio 
## 0.25° x 0.25°, 0.5° x 0.5° o 1° x 1° 

import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset as ds
import scipy.io as sio
from matplotlib.ticker import FixedLocator
import cartopy.feature as cfeature
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from os import listdir
from datetime import datetime
from funciones_auxiliares_TRMM import * 

## se carga la topografia 
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

# con esto se regula la resolucion de la grilla
x_spac, y_spac = 0.25, 0.25
lonwest = -75.5
loneast = -60.5
latsouth = -38.5
latnorth = -10.5
# cantidad de etiquetas de latitud y longitud
sp_lat = (latnorth - latsouth) / 4
sp_lon = (loneast - lonwest) / 3

#### Por una cuestion de tamaño, se trabaja con los datos recortados de los originales
# (ver script recorte_HDF)
# cargo los netCDF recortados
salida = '.../figuras/'
path = '.../'

archivos = sorted(listdir(path))
# como los archivos los guarde con la fecha en el nombre del mismo, los convierto a objeto datetime
fechas = sorted(listdir(path))
# se transforman los archivos a objetos datetime 
for i in range(0, len(archivos)) :
    fechas[i] = (datetime.strptime(str(fechas[i][3:9]), '%Y%m'))

#### Se compone de distintas partes que hacen distintos calculos 

###################################################################### 

## cantidad total de pixeles de meses individuales
interruptor = 'off'
if interruptor == 'on' :
    for i in range(0, 1) :  # len(archivos)

        variable = 'NRPF'

        data = ds(path + archivos[i], 'r')
        var = data.variables[variable][:]
        lat = data.variables['latitude'][:]
        lon = data.variables['longitude'][:]

        var[var < 0] = np.nan

        # en este caso se construye una grilla con la suma de pixeles de una determinada variable    
        cel = crea_grilla_suma_pixeles(var, latnorth, latsouth, lonwest, loneast ,lat, lon, x_spac, y_spac)

        # se grillan las lat y lon

        x, y = np.meshgrid(np.arange(lonwest, loneast, x_spac),np.arange(latnorth,latsouth,-1*y_spac))

        fig = plt.figure(figsize=(4.5,5.75))
        ax1 = plt.subplot(1,1,1, projection=ccrs.PlateCarree())
        ax1.set_extent([lonwest, loneast, latsouth, latnorth], crs=ccrs.PlateCarree())

        cm = ax1.pcolormesh(x,y,cel, cmap = 'gist_ncar_r',transform=ccrs.PlateCarree())
        plt.title('Number of PR raining pixels')

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

        plt.colorbar(cm)
        plt.savefig(salida+'pixeleado.png', dpi = 300, bbob_inches = 'tight')
        plt.close()

## medias de cada reticula de variables para meses individuales
interruptor = 'off'
if interruptor == 'on' :
    for i in range(0, 1) :  # len(archivos)

        variable = 'MAXNSZ'

        data = ds(path + archivos[i], 'r')
        var = data.variables[variable][:]
        lat = data.variables['MAXNSZLAT'][:]
        lon = data.variables['MAXNSZLON'][:]

        var[var < 0] = np.nan

        # en este caso se construye una grilla con la suma de pixeles de una determinada variable    
        cel = crea_grilla_media_pixeles(var, latnorth, latsouth, lonwest, loneast ,lat, lon, x_spac, y_spac)

        # se grillan las lat y lon

        x, y = np.meshgrid(np.arange(lonwest, loneast, x_spac),np.arange(latnorth,latsouth,-1*y_spac))

        fig = plt.figure(figsize=(4.5,5.75))
        ax1 = plt.subplot(1,1,1, projection=ccrs.PlateCarree())
        ax1.set_extent([lonwest, loneast, latsouth, latnorth], crs=ccrs.PlateCarree())

        cm = ax1.pcolormesh(x,y,cel, cmap = 'gist_ncar_r',transform=ccrs.PlateCarree())
        plt.title('Valores maximos de reflectividad cerca de superficie', fontsize = 12)

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

        plt.colorbar(cm)
        plt.show()
        #plt.savefig(salida+'pixeleado.png', dpi = 300, bbob_inches = 'tight')
        plt.close()


## cantidad total de pixeles del total de fechas cargadas
interruptor = 'off'
if interruptor == 'on' :
    for i in range(0, len(archivos)) :  # len(archivos)

        if i == 0 :        
            data = ds(path + archivos[i], 'r')
            var = data.variables['NRPF'][:]
            lat = data.variables['latitude'][:]
            lon = data.variables['longitude'][:]
            continue

        data = ds(path + archivos[i], 'r')
        var = np.concatenate([var, data.variables['NRPF'][:]])
        lat = np.concatenate([lat, data.variables['latitude'][:]])
        lon = np.concatenate([lon, data.variables['longitude'][:]])

    var[var < 0] = 0

    cel = crea_grilla_suma_pixeles(var, latnorth, latsouth, lonwest, loneast ,lat, lon, x_spac, y_spac)

    # se grillan las lat y lon

    x, y = np.meshgrid(np.arange(lonwest, loneast, x_spac),np.arange(latnorth,latsouth,-1*y_spac))
    cel[np.where(Y <= -35.5)] = np.nan

    fig = plt.figure(figsize=(4.5,5.75))
    ax1 = plt.subplot(1,1,1, projection=ccrs.PlateCarree())

    cm = ax1.pcolormesh(x,y,cel,vmax =200,cmap = 'gist_stern_r',transform=ccrs.PlateCarree())
    plt.title('Number of radar precipitation features inside \n ' + 'Grillado ' + str(x_spac) + '° 1997-2014', fontsize = 8)

    # Se agrega el contorno del terreno mayor a 1500 mts
    l = np.arange(1500, 1501, 1)
    ax1.contour(lon_z, lat_z, z_sup, l,colors = ['sienna'])
    ax1.set_extent([lonwest, loneast, latsouth, latnorth], crs=ccrs.PlateCarree())
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

    plt.colorbar(cm)
    plt.savefig(salida+'NRPF_'+str(x_spac)+'grado.png', dpi = 300, bbob_inches = 'tight')
    plt.close()

########
## percentiles para cada variable del total de fechas cargadas

interruptor = 'off'
if interruptor == 'on' :

    varss = ['VOLRAIN_2A25', 'VOLRAIN_20DBZ', 'VOLRAIN_20MM', 'VOLRAIN_30DBZ', 'VOLRAIN_30MM',
    'VOLRAIN_40DBZ', 'VOLRAIN_40MM','VOLRAIN_50DBZ', 'VOLRAIN_50MM', 'VOLRAIN_100MM']

    vmaxx = [500000, 50000, 35000, 25000, 35000, 55000, 
    75000, 15000, 15000, 15000]
    
    perc = [90, 95, 99, 99.9, 99.99]

    import matplotlib as mpl
    label_size = 6
    mpl.rcParams['xtick.labelsize'] = label_size
    mpl.rcParams['ytick.labelsize'] = label_size

    # un ciclo para cada variable, guarda una imagen
    for jj in range(1, len(varss)) :

        for i in range(0, len(archivos)) :  # len(archivos)

            variable = varss[jj]
            if i == 0 :        
                data = ds(path + archivos[i], 'r')
                var = data.variables[variable][:]
                lat = data.variables['latitude'][:]
                lon = data.variables['longitude'][:]
                continue

            data = ds(path + archivos[i], 'r')
            var = np.concatenate([var, data.variables[variable][:]])
            lat = np.concatenate([lat, data.variables['latitude'][:]])
            lon = np.concatenate([lon, data.variables['longitude'][:]])

        var[var < 0] = np.nan

        # se grillan las lat y lon

        x, y = np.meshgrid(np.arange(lonwest, loneast, x_spac),np.arange(latsouth,latnorth,y_spac))

        fig = plt.figure(figsize=(7.75,3))
        
        ax1 = plt.subplot(1,5,1, projection=ccrs.PlateCarree())
        ax2 = plt.subplot(1,5,2, projection=ccrs.PlateCarree())
        ax3 = plt.subplot(1,5,3, projection=ccrs.PlateCarree())
        ax4 = plt.subplot(1,5,4, projection=ccrs.PlateCarree())
        ax5 = plt.subplot(1,5,5, projection=ccrs.PlateCarree())

        cm = ax1.pcolormesh(x,y,crea_grilla_025_percentiles(var, latnorth, latsouth, lonwest, loneast ,lat, lon, perc[0]),vmax = vmaxx[jj],cmap = 'gist_stern_r',transform=ccrs.PlateCarree())
        ax1.set_title('Percentil ' + str(perc[0]), fontsize = 8)
        ax2.pcolormesh(x,y,crea_grilla_025_percentiles(var, latnorth, latsouth, lonwest, loneast ,lat, lon, perc[1]),vmax = vmaxx[jj],cmap = 'gist_stern_r',transform=ccrs.PlateCarree())
        ax2.set_title('Percentil ' + str(perc[1]), fontsize = 8)
        ax3.pcolormesh(x,y,crea_grilla_025_percentiles(var, latnorth, latsouth, lonwest, loneast ,lat, lon, perc[2]),vmax = vmaxx[jj],cmap = 'gist_stern_r',transform=ccrs.PlateCarree())
        ax3.set_title('Percentil ' + str(perc[2]), fontsize = 8)
        ax4.pcolormesh(x,y,crea_grilla_025_percentiles(var, latnorth, latsouth, lonwest, loneast ,lat, lon, perc[3]),vmax = vmaxx[jj],cmap = 'gist_stern_r',transform=ccrs.PlateCarree())
        ax4.set_title('Percentil ' + str(perc[3]), fontsize = 8)
        ax5.pcolormesh(x,y,crea_grilla_025_percentiles(var, latnorth, latsouth, lonwest, loneast ,lat, lon, perc[4]),vmax = vmaxx[jj],cmap = 'gist_stern_r',transform=ccrs.PlateCarree())
        ax5.set_title('Percentil ' + str(perc[4]), fontsize = 8)

        plt.suptitle(varss[jj] + '\n ' + 'Grillado ' + str(x_spac) + '° 1998-2013', fontsize = 8)

        # Se agrega el contorno del terreno mayor a 1500 mts
        l = np.arange(1500, 1501, 1)
        ax1.contour(lon_z, lat_z, z_sup, l,colors = ['sienna'])
        ax2.contour(lon_z, lat_z, z_sup, l,colors = ['sienna'])
        ax3.contour(lon_z, lat_z, z_sup, l,colors = ['sienna'])
        ax4.contour(lon_z, lat_z, z_sup, l,colors = ['sienna'])
        ax5.contour(lon_z, lat_z, z_sup, l,colors = ['sienna'])

        ax1.set_extent([lonwest, loneast, -35.5, latnorth], crs=ccrs.PlateCarree())
        ax2.set_extent([lonwest, loneast, -35.5, latnorth], crs=ccrs.PlateCarree())
        ax3.set_extent([lonwest, loneast, -35.5, latnorth], crs=ccrs.PlateCarree())
        ax4.set_extent([lonwest, loneast, -35.5, latnorth], crs=ccrs.PlateCarree())
        ax5.set_extent([lonwest, loneast, -35.5, latnorth], crs=ccrs.PlateCarree())
        # Agregamos la línea de costas
        ax1.coastlines(resolution='10m',linewidth=0.6)
        ax2.coastlines(resolution='10m',linewidth=0.6)
        ax3.coastlines(resolution='10m',linewidth=0.6)
        ax4.coastlines(resolution='10m',linewidth=0.6)
        ax5.coastlines(resolution='10m',linewidth=0.6)
        # Agregamos los límites de los países
        ax1.add_feature(countries,linewidth=0.4)
        ax2.add_feature(countries,linewidth=0.4)
        ax3.add_feature(countries,linewidth=0.4)
        ax4.add_feature(countries,linewidth=0.4)
        ax5.add_feature(countries,linewidth=0.4)
        # Agregamos los límites de las provincias
        ax1.add_feature(states_provinces,linewidth=0.4)
        ax2.add_feature(states_provinces,linewidth=0.4)
        ax3.add_feature(states_provinces,linewidth=0.4)
        ax4.add_feature(states_provinces,linewidth=0.4)
        ax5.add_feature(states_provinces,linewidth=0.4)
        # Definimos donde aparecen los ticks con las latitudes y longitudes
        ax1.set_yticks(np.arange(-35.5,latnorth,sp_lat), crs=ccrs.PlateCarree())
        ax1.set_xticks(np.arange(lonwest,loneast,sp_lon), crs=ccrs.PlateCarree())
        ax2.set_xticks(np.arange(lonwest,loneast,sp_lon), crs=ccrs.PlateCarree())
        ax3.set_xticks(np.arange(lonwest,loneast,sp_lon), crs=ccrs.PlateCarree())
        ax4.set_xticks(np.arange(lonwest,loneast,sp_lon), crs=ccrs.PlateCarree())
        ax5.set_xticks(np.arange(lonwest,loneast,sp_lon), crs=ccrs.PlateCarree())
        # Le damos formato a las etiquetas de los ticks
        lon_formatter = LongitudeFormatter(zero_direction_label=True)
        lat_formatter = LatitudeFormatter()
        ax1.xaxis.set_major_formatter(lon_formatter)
        ax2.xaxis.set_major_formatter(lon_formatter)
        ax3.xaxis.set_major_formatter(lon_formatter)
        ax4.xaxis.set_major_formatter(lon_formatter)
        ax5.xaxis.set_major_formatter(lon_formatter)
        ax1.yaxis.set_major_formatter(lat_formatter)

        fig.subplots_adjust(bottom=0.0, top=1.0, left=0.055, right=0.82, wspace=0.025, hspace=0.02)
        cb_ax = fig.add_axes([0.83, 0.1, 0.02, 0.8])
        cbar = fig.colorbar(cm, cax=cb_ax)
        
        plt.savefig(salida+'pixeles_distribuciones/'+varss[jj]+'_percentiles.png', dpi = 300, bbob_inches = 'tight')
        plt.close()

########
## estudio de funciones de densidad poblacional
## solo variables con cantidad de pixeles

interruptor = 'off'
if interruptor == 'on' :

    varss = ['NRAINPIXELS_2A25', 'NPIXELS_20DBZ', 'NPIXELS_20MM', 'NPIXELS_30DBZ', 'NPIXELS_30MM', 
    'NPIXELS_40DBZ', 'NPIXELS_40MM', 'NPIXELS_50DBZ', 'NPIXELS_50MM', 'NPIXELS_100MM']

    vmaxx = [0.05, 0.025, 0.025, 0.01, 0.01, 0.0025, 0.0025, 0.001, 0.001, 0.0001]
    
    perc = [90, 95, 99, 99.9, 99.99]

    import matplotlib as mpl
    label_size = 6
    mpl.rcParams['xtick.labelsize'] = label_size
    mpl.rcParams['ytick.labelsize'] = label_size
    
    # un ciclo para cada variable, guarda una imagen
    for jj in range(1, len(varss)) :     # len(varss) 
        # carga todos los meses de verano y construye la var cel sobre la que se calculan los percentiles
        for i in range(0, len(archivos)) :  # len(archivos)
            # 
            variable = varss[jj]
            if i == 0 :        
                data = ds(path + archivos[i], 'r')
                var = data.variables[variable][:]
                lat = data.variables['latitude'][:]
                lon = data.variables['longitude'][:]
                continue

            data = ds(path + archivos[i], 'r')
            var = np.concatenate([var, data.variables[variable][:]])
            lat = np.concatenate([lat, data.variables['latitude'][:]])
            lon = np.concatenate([lon, data.variables['longitude'][:]])

        var[var < 0] = np.nan

        # se grillan las lat y lon

        x, y = np.meshgrid(np.arange(lonwest, loneast, x_spac),np.arange(latsouth,latnorth,y_spac))

        ## graficado
        fig = plt.figure(figsize=(7.75,3))
        
        ax1 = plt.subplot(1,5,1, projection=ccrs.PlateCarree())
        ax2 = plt.subplot(1,5,2, projection=ccrs.PlateCarree())
        ax3 = plt.subplot(1,5,3, projection=ccrs.PlateCarree())
        ax4 = plt.subplot(1,5,4, projection=ccrs.PlateCarree())
        ax5 = plt.subplot(1,5,5, projection=ccrs.PlateCarree())

        cm = ax1.pcolormesh(x,y,crea_grilla_025_percentiles_normalizadas(var, latnorth, latsouth, lonwest, loneast ,lat, lon, perc[0]),vmax = vmaxx[jj],cmap = 'gist_stern_r',transform=ccrs.PlateCarree())
        ax1.set_title('Percentil ' + str(perc[0]), fontsize = 8)
        ax2.pcolormesh(x,y,crea_grilla_025_percentiles_normalizadas(var, latnorth, latsouth, lonwest, loneast ,lat, lon, perc[1]),vmax = vmaxx[jj],cmap = 'gist_stern_r',transform=ccrs.PlateCarree())
        ax2.set_title('Percentil ' + str(perc[1]), fontsize = 8)
        ax3.pcolormesh(x,y,crea_grilla_025_percentiles_normalizadas(var, latnorth, latsouth, lonwest, loneast ,lat, lon, perc[2]),vmax = vmaxx[jj],cmap = 'gist_stern_r',transform=ccrs.PlateCarree())
        ax3.set_title('Percentil ' + str(perc[2]), fontsize = 8)
        ax4.pcolormesh(x,y,crea_grilla_025_percentiles_normalizadas(var, latnorth, latsouth, lonwest, loneast ,lat, lon, perc[3]),vmax = vmaxx[jj],cmap = 'gist_stern_r',transform=ccrs.PlateCarree())
        ax4.set_title('Percentil ' + str(perc[3]), fontsize = 8)
        ax5.pcolormesh(x,y,crea_grilla_025_percentiles_normalizadas(var, latnorth, latsouth, lonwest, loneast ,lat, lon, perc[4]),vmax = vmaxx[jj],cmap = 'gist_stern_r',transform=ccrs.PlateCarree())
        ax5.set_title('Percentil ' + str(perc[4]), fontsize = 8)
        
        plt.suptitle(varss[jj] + '\n ' + 'Grillado ' + str(x_spac) + '° 1998-2013 Normalizados', fontsize = 8)

        # Se agrega el contorno del terreno mayor a 1500 mts
        l = np.arange(1500, 1501, 1)
        ax1.contour(lon_z, lat_z, z_sup, l,colors = ['sienna'])
        ax2.contour(lon_z, lat_z, z_sup, l,colors = ['sienna'])
        ax3.contour(lon_z, lat_z, z_sup, l,colors = ['sienna'])
        ax4.contour(lon_z, lat_z, z_sup, l,colors = ['sienna'])
        ax5.contour(lon_z, lat_z, z_sup, l,colors = ['sienna'])

        ax1.set_extent([lonwest, loneast, -35.5, latnorth], crs=ccrs.PlateCarree())
        ax2.set_extent([lonwest, loneast, -35.5, latnorth], crs=ccrs.PlateCarree())
        ax3.set_extent([lonwest, loneast, -35.5, latnorth], crs=ccrs.PlateCarree())
        ax4.set_extent([lonwest, loneast, -35.5, latnorth], crs=ccrs.PlateCarree())
        ax5.set_extent([lonwest, loneast, -35.5, latnorth], crs=ccrs.PlateCarree())
        # Agregamos la línea de costas
        ax1.coastlines(resolution='10m',linewidth=0.6)
        ax2.coastlines(resolution='10m',linewidth=0.6)
        ax3.coastlines(resolution='10m',linewidth=0.6)
        ax4.coastlines(resolution='10m',linewidth=0.6)
        ax5.coastlines(resolution='10m',linewidth=0.6)
        # Agregamos los límites de los países
        ax1.add_feature(countries,linewidth=0.4)
        ax2.add_feature(countries,linewidth=0.4)
        ax3.add_feature(countries,linewidth=0.4)
        ax4.add_feature(countries,linewidth=0.4)
        ax5.add_feature(countries,linewidth=0.4)
        # Agregamos los límites de las provincias
        ax1.add_feature(states_provinces,linewidth=0.4)
        ax2.add_feature(states_provinces,linewidth=0.4)
        ax3.add_feature(states_provinces,linewidth=0.4)
        ax4.add_feature(states_provinces,linewidth=0.4)
        ax5.add_feature(states_provinces,linewidth=0.4)
        # Definimos donde aparecen los ticks con las latitudes y longitudes
        ax1.set_yticks(np.arange(-35.5,latnorth,sp_lat), crs=ccrs.PlateCarree())
        ax1.set_xticks(np.arange(lonwest,loneast,sp_lon), crs=ccrs.PlateCarree())
        ax2.set_xticks(np.arange(lonwest,loneast,sp_lon), crs=ccrs.PlateCarree())
        ax3.set_xticks(np.arange(lonwest,loneast,sp_lon), crs=ccrs.PlateCarree())
        ax4.set_xticks(np.arange(lonwest,loneast,sp_lon), crs=ccrs.PlateCarree())
        ax5.set_xticks(np.arange(lonwest,loneast,sp_lon), crs=ccrs.PlateCarree())
        # Le damos formato a las etiquetas de los ticks
        lon_formatter = LongitudeFormatter(zero_direction_label=True)
        lat_formatter = LatitudeFormatter()
        ax1.xaxis.set_major_formatter(lon_formatter)
        ax2.xaxis.set_major_formatter(lon_formatter)
        ax3.xaxis.set_major_formatter(lon_formatter)
        ax4.xaxis.set_major_formatter(lon_formatter)
        ax5.xaxis.set_major_formatter(lon_formatter)
        ax1.yaxis.set_major_formatter(lat_formatter)

        fig.subplots_adjust(bottom=0.0, top=1.0, left=0.055, right=0.82, wspace=0.025, hspace=0.02)
        cb_ax = fig.add_axes([0.83, 0.1, 0.02, 0.8])
        cbar = fig.colorbar(cm, cax=cb_ax)
        
        plt.savefig(salida+'pixeles_distribuciones/'+varss[jj]+'_percentiles.png', dpi = 300, bbob_inches = 'tight')
        #plt.show()
        plt.close()
