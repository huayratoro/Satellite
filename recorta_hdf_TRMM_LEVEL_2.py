## script que recorta un area geografica de los puntos de los HDF y los guarda en un  
## netCDF4 que pesa muuucho menos 
## la funcion ademas selecciona solo algunas variables a guardar
##### TENER CUIDADO que hay variables con dimensiones distintas a las LAT LON globales
import numpy as np
from pyhdf.SD import SD, SDC
from os import listdir
from netCDF4 import Dataset as ds
# esta funcion esta en el repositorio
from funciones_auxiliares_TRMM import corta_region, corta_region_horas, corta_region_todos_pix, corta_hdf

# en este dir estan los HDF a cortar
path = '.../'
archivos = sorted(listdir(path)) 

# un ciclo que corta cada HDF y los guarda en algun otro directorio salida

salida = '.../'

for i in range(0, len(archivos)) :
    corta_hdf(path+archivos[i], archivos[i].replace('.HDF', '') + '_reducido.nc',salida)
