## Script para recordar un area del Full disk del GOES 16 que descargamos
## con el script de bajada de datos automatica 
## 
## POWERED BY HUAYRATORO

import numpy as np
import numpy.ma as ma
import numpy as np
import netCDF4
from netCDF4 import Dataset
from pyproj import Proj
from datetime import datetime

    # Ruta
DataPath = '20201100.nc'    # el nc file a recortar
    # Numero de banda ####
banda = 13
banda_string= "%02i" % banda
    # disponible para dos areas, el Noroeste argentino y Argentina (norte de 54S)
area = 'NOA' 
    # Abrimos el archivo netcdf
nc_goes = Dataset(DataPath)
    # Extraemos fecha y hora de la imagen. Esto es util para luego poner en el titulo de la figura por ejemplo.
fecha= nc_goes.time_coverage_start
fecha=datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S.%fZ')
fecha_str=int(datetime.strftime(fecha, '%d%m%Y%H%M'))

    # Extraemos la altura del satélite
sat_h = nc_goes['goes_imager_projection'].perspective_point_height

    # Extraemos la longitud del punto central del disco
sat_lon = nc_goes['goes_imager_projection'].longitude_of_projection_origin

    # Extraemos el eje de rotación
sat_sweep = nc_goes['goes_imager_projection'].sweep_angle_axis

    ##### Reconstruimos las coordenadas de la proyeccion geoestacionaria #####
    # Dado que la información del fulldisk ocupa mucha memoria, vamos a tomar un área reducida 
    # En este caso se toma la reduccion del NOA (SALTA Y JUJUY)

if area == 'NOA' :
    x_min=2900
    x_max=3400
    y_min=3850
    y_max=4150
if area == 'Argentina' :
    x_min=2500
    x_max=3500
    y_min=3500
    y_max=5000
    # recortando en el area requerida
x = nc_goes['x'][x_min:x_max] * sat_h
y = nc_goes['y'][y_min:y_max] * sat_h
    # Generamos un objeto con la proyeccion del satélite
p = Proj(proj='geos', h=sat_h, lon_0=sat_lon, sweep=sat_sweep)
XX, YY = np.meshgrid(x, y)
    # Aplicamos la transformación para obtener las coordenadas en formato de latitud y longitud
lons, lats = p(XX, YY, inverse=True)
del XX,YY
    # Extraemos del netcdf la información de la variable para la región reducida    
    # Mediciones
data=nc_goes.variables['CMI'][y_min:y_max,x_min:x_max]  
    # Transformo el vector x y en np.ndarray
x = np.array(x)
y = np.array(y)

    ###### CREO EL NETCDF CON EL CORTE ######
    # genera un nc file en el directorio de trabajo
    # contiene la tbrillo junto con el tiempo y las 
    # coordenadas horizontales x e y

    ## 1 creo el netcdf
f = Dataset('area_reducida.nc','w', format='NETCDF4')
    ## 2 creo la variable a guardar
tbrillo = f.createGroup('Tbrillo')
    ## 3 se especifican las dimensiones de la variable
tbrillo.createDimension('X', len(x))
tbrillo.createDimension('Y', len(y))
tbrillo.createDimension('time', None)
    ## 4 construyo las variables
X = tbrillo.createVariable('X', 'f4', 'X')
Y = tbrillo.createVariable('Y', 'f4', 'Y')  
temp = tbrillo.createVariable('tbrillo', 'f4', ('time', 'Y', 'X'))
time = tbrillo.createVariable('Time', 'i4', 'time')
    ## 5 paso las variables al netcdf creado
X[:] = x #The "[:]" at the end of the variable instance is necessary
Y[:] = y
temp[0,:,:] = data
time[0] = fecha_str
    # 6 le agrego las unidades y otros atributos a las variables
temp.units = 'Kelvin'
    # cierro el nuevo netcdf
f.close()
