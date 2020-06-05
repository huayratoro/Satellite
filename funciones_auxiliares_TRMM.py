## funciones auxiliares

# funcion 
def corta_region(variable, lat, lon, lon_w, lon_e, lat_n, lat_s) :
    import numpy as np
    # funcion que toma la variable a trabajar y sus coordenadas (lat, lon)
    # devuelve los lugares en el array coordenadas donde se cumplen las condiciones impuestas
    # cuantifica pixeles mayores a cero para hacer la nube de puntos
    # para todas las horas del dia
    c = np.where((variable > 0) & (lat >= lat_s) & (lat <= lat_n) & (lon >= lon_w) & (lon <= lon_e)) 
    return c
# otra funcion
def corta_region_horas(variable, lat, lon, horas, lon_w, lon_e, lat_n, lat_s, hora_i, hora_f) :
    import numpy as np
    # funcion que toma la variable a trabajar y sus coordenadas (lat, lon)
    # devuelve los lugares en el array coordenadas donde se cumplen las condiciones impuestas
    # cuantifica pixeles mayores a cero para hacer la nube de puntos
    # para ciertas horas del dia
    c = np.where((variable > 0) & (lat >= lat_s) & (lat <= lat_n) & (lon >= lon_w) & (lon <= lon_e) & (horas >= hora_i) & (horas < hora_f)) 
    return c    
# otra funcion pero sin restringir a los pixeles
def corta_region_todos_pix(lat, lon, lon_w, lon_e, lat_n, lat_s) :
    import numpy as np
    # funcion que corta en latitudes y longitudes solamente
    # devuelve los lugares en el array coordenadas donde se cumplen las condiciones impuestas
    # para todas las horas del dia
    c = np.where((lat >= lat_s) & (lat <= lat_n) & (lon >= lon_w) & (lon <= lon_e)) 
    return c
# funcion para recortar un HDF
def corta_hdf(archivo, nombre, salida) :
    # funcion que toma un HDF del PRF de Chuntao
    # selecciona algunas variables 
    # y recorta en la region de estudio
    import numpy as np
    from pyhdf.SD import SD, SDC
    from os import listdir
    from netCDF4 import Dataset as ds
    from funciones_auxiliares import corta_region, corta_region_horas, corta_region_todos_pix

    data = SD(archivo, SDC.READ)

    #for idx,sds in enumerate(datasets.keys()):
    #    print (idx,sds, data.select(sds).attributes())

    # se extraen las dimensiones LAT, LON, YEAR, MONTH, DAY, HOUR
    lat = (data.select('LAT')).get() 
    lon = (data.select('LON')).get()
    y, m = (data.select('YEAR')).get()[0], (data.select('MONTH')).get()[0]
    day = (data.select('DAY')).get() 
    hour = (data.select('HOUR')).get()
    lat_n, lat_s, lon_w, lon_e = -10, -38, -75, -60
    # se indica el o los SDS a extraer del archivo
    # las variables que se tomand del HDF son las siguientes
    lista = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 27, 28, 29, 30, 31, 32, 33, 34, 35,
    36, 62, 63, 64, 65, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 102]
    # hago un ciclo para cada variable de la lsia anterior
    # el ciclo cortara los datos de cada una 
    # y los guardara en el archivo netCDF4 'nuevo'
    import os
    os.chdir(salida)
    for i in range(0, len(lista)):   # len(lista)
        nombre_var = data.select(lista[i]).info()[0]
        atributo = data.select(lista[i]).attributes()
        # creo una variable llamada 'nombre_var'
        var = data.select(nombre_var).get()
        # se corta por region geografica cada dimension y la variable
        var_c = var[corta_region_todos_pix(lat, lon, lon_w, lon_e, lat_n, lat_s)]
        #print(lista[i])
        ## guardamos el netCDF
        if i == 0 :
            # 1.    Creamos el netCDF
            nuevo = ds(nombre, 'w', format = 'NETCDF4')
            # 2.    Se crean las dimensiones
            x = nuevo.createDimension('x', len(var_c))
            time = nuevo.createDimension('time', None)
        # 3.    Se crean las variables a guardar
        var_g = nuevo.createVariable(nombre_var, 'f4', 'x')
        # 4.    Se cargan las variables del netCDF4
        var_g[:] = var_c

    # luego se guardan las otras variables 
    # primero las dimensiones cortadas
    lat_c = lat[corta_region_todos_pix(lat, lon, lon_w, lon_e, lat_n, lat_s)]
    lon_c = lon[corta_region_todos_pix(lat, lon, lon_w, lon_e, lat_n, lat_s)]
    day_c = day[corta_region_todos_pix(lat, lon, lon_w, lon_e, lat_n, lat_s)]
    hour_c = hour[corta_region_todos_pix(lat, lon, lon_w, lon_e, lat_n, lat_s)]
    # ahora si creo las variables
    lat = nuevo.createVariable('latitude', 'f4', 'x')
    lon = nuevo.createVariable('longitude', 'f4', 'x')
    year = nuevo.createVariable('year', 'f8', 'time')
    month = nuevo.createVariable('month', 'f8', 'time')
    day = nuevo.createVariable('day', 'f4', 'x')
    hour = nuevo.createVariable('hour', 'f4', 'x')
    # cargo los datos de cada una
    lat[:] = lat_c
    lon[:] = lon_c
    year[0] = y
    month[0] = m
    day[:] = day_c
    hour[:] = hour_c
    # finalmente cierro el netCDF nuevo
    return nuevo.close()
# funcion para armar una grilla de pixeles (vieja, NO SIRVE !)
def crea_grilla_suma_valores_deprecated(var, lat_n, lat_s, lon_w, lon_e, lat, lon, x_spac, y_spac) :
    # crea una grilla de pixeles de x_spac x y_spac con la suma de pixeles
    # devuelve la grilla de shape (x_spac, y_spac)
    ## Defino los limites de la grilla
    # puede ser cada 1°, 0.5° o 0.25°
    import numpy as np
    x = np.arange(lon_w, lon_e, x_spac)
    y = np.arange(lat_s, lat_n, y_spac)
    # lleno los datos de la nueva matriz
    # vector de la matriz (m_ij) puestos a lo largo
    cel = np.zeros([len(x)*len(y)])
    m = 0
    # se asigna cada valor a cada pixel
    for k in range(1, len(y)) :
        for l in range(1, len(x)) :
            # se define la operacion que se hara con los valores que caen dentro de cada pixel
            cel[m] = np.sum(var[np.where((lat >= y[k-1]) & (lat < y[k]) & (lon >= x[l-1]) & (lon < x[l]))]) 
            m = m+1
    # se grillan los datos 
    cel = np.reshape(cel, (-1, len(x)))     
    return cel 
# funcion para armar una grilla de pixeles (hasta ahora funciona Xp)
def crea_grilla_media_pixeles(var, lat_n, lat_s, lon_w, lon_e, lat, lon, x_spac, y_spac) :
    # crea una grilla de pixeles de x_spac x y_spac con la suma de pixeles
    # devuelve la grilla de shape (x_spac, y_spac)
    ## Defino los limites de la grilla
    # puede ser cada 1°, 0.5° o 0.25°
    import numpy as np
    x = np.arange(lon_w,lon_e, x_spac)
    y = np.arange(lat_s,lat_n,y_spac)
    # lleno los datos de la nueva matriz
    # vector de la matriz (m_ij) puestos a lo largo
    cel = np.zeros([(len(x))*(len(y))])
    cel = np.reshape(cel, (-1, (len(x))))
    # se asigna cada valor a cada pixel
    for i in range(0,len(y)-1):
        for j in range(0,len(x)-1):
            # se define la operacion que se hara con los valores que caen dentro de cada pixel
            cel[i, j] = np.nanmean(var[np.where( (lat >= y[i]) & (lat < y[i+1]) & (lon >= x[j]) & (lon < x[j+1]) )]) 
    return cel 
# funcion para armar una grilla de pixeles (hasta ahora funciona Xp)
def crea_grilla_suma_pixeles(var, lat_n, lat_s, lon_w, lon_e, lat, lon, x_spac, y_spac) :
    # crea una grilla de pixeles de x_spac x y_spac con la suma de pixeles
    # devuelve la grilla de shape (x_spac, y_spac)
    ## Defino los limites de la grilla
    # puede ser cada 1°, 0.5° o 0.25°
    import numpy as np
    x = np.arange(lon_w,lon_e, x_spac)
    y = np.arange(lat_s,lat_n,y_spac)
    # lleno los datos de la nueva matriz
    # vector de la matriz (m_ij) puestos a lo largo
    cel = np.zeros([(len(x))*(len(y))])
    cel = np.reshape(cel, (-1, (len(x))))
    # se asigna cada valor a cada pixel
    for i in range(0,len(y)-1):
        for j in range(0,len(x)-1):
            # se define la operacion que se hara con los valores que caen dentro de cada pixel
            cel[i, j] = sum(var[np.where( (lat >= y[i]) & (lat < y[i+1]) & (lon >= x[j]) & (lon < x[j+1]) )]) 
    return cel 
# funcion de suma de valores pero normalizada por la cantidad de pasadas
def crea_grilla_025_suma_normalizada_pixeles(var, lat_n, lat_s, lon_w, lon_e, lat, lon) :
    # crea una grilla de pixeles de x_spac x y_spac con la suma de pixeles
    # devuelve la grilla de shape (x_spac, y_spac)
    ## Defino los limites de la grilla
    # solo 0.25°
    import numpy as np
    # cargo las pasadas en una grilla de 
    from netCDF4 import Dataset as ds
    netcdf = ds('.../pixeles_con_pasada_025grados.nc', 'r')
    pasadas = netcdf.variables['pasadas'][:]
    pasadas[pasadas==0] = np.nan
    # armo la grilla
    x = np.arange(lon_w,lon_e, 0.25)
    y = np.arange(lat_s,lat_n,0.25)
    # lleno los datos de la nueva matriz
    # vector de la matriz (m_ij) puestos a lo largo
    cel = np.zeros([(len(x))*(len(y))])
    cel = np.reshape(cel, (-1, (len(x))))
    # se asigna cada valor a cada pixel
    for i in range(0,len(y)-1):
        for j in range(0,len(x)-1):
            # se define la operacion que se hara con los valores que caen dentro de cada pixel
            cel[i, j] = sum(var[np.where( (lat >= y[i]) & (lat < y[i+1]) & (lon >= x[j]) & (lon < x[j+1]) )]) 
    cel = cel / pasadas 
    return cel 
# funcion para armar una grilla de pixeles con percentiles de una CDF
def crea_grilla_025_percentiles(var, lat_n, lat_s, lon_w, lon_e, lat, lon, percentil) :
    # crea una grilla de pixeles de x_spac x y_spac con la suma de pixeles
    # devuelve la grilla de shape (x_spac, y_spac)
    ## Defino los limites de la grilla
    # puede ser cada 1°, 0.5° o 0.25°
    import numpy as np
    # cargo las pasadas en una grilla de 
    from netCDF4 import Dataset as ds
    netcdf = ds('.../pixeles_con_pasada_025grados.nc', 'r')
    pasadas = netcdf.variables['pasadas'][:]
    pasadas[pasadas==0] = np.nan
    # ahora armo la grilla
    x = np.arange(lon_w,lon_e, 0.25)
    y = np.arange(lat_s,lat_n,0.25)
    # lleno los datos de la nueva matriz
    # vector de la matriz (m_ij) puestos a lo largo
    cel = np.zeros([(len(x))*(len(y))])
    cel = np.reshape(cel, (-1, (len(x))))
    # se asigna cada valor a cada pixel
    for i in range(0,len(y)-1):
        for j in range(0,len(x)-1):
            # se define la operacion que se hara con los valores que caen dentro de cada pixel
            cel[i, j] = np.nanpercentile(var[np.where( (lat >= y[i]) & (lat < y[i+1]) & (lon >= x[j]) & (lon < x[j+1]) )], percentil) 
    cel[np.where(y <= -35.5)] = np.nan
    return cel 
# funcion igual a la anterior pero para cantidad de pixeles normalizada
def crea_grilla_025_percentiles_normalizadas(var, lat_n, lat_s, lon_w, lon_e, lat, lon, percentil) :
    # crea una grilla de pixeles de x_spac x y_spac con la suma de pixeles
    # devuelve la grilla de shape (x_spac, y_spac)
    ## Defino los limites de la grilla
    # puede ser cada 1°, 0.5° o 0.25°
    import numpy as np
    # cargo las pasadas en una grilla de 
    from netCDF4 import Dataset as ds
    netcdf = ds('.../pixeles_con_pasada_025grados.nc', 'r')
    pasadas = netcdf.variables['pasadas'][:]
    pasadas[pasadas==0] = np.nan
    # ahora armo la grilla
    x = np.arange(lon_w,lon_e, 0.25)
    y = np.arange(lat_s,lat_n,0.25)
    # lleno los datos de la nueva matriz
    # vector de la matriz (m_ij) puestos a lo largo
    cel = np.zeros([(len(x))*(len(y))])
    cel = np.reshape(cel, (-1, (len(x))))
    # se asigna cada valor a cada pixel
    for i in range(0,len(y)-1):
        for j in range(0,len(x)-1):
            # se define la operacion que se hara con los valores que caen dentro de cada pixel
            cel[i, j] = np.nanpercentile(( np.array(var[np.where( (lat >= y[i]) & (lat < y[i+1]) & (lon >= x[j]) & (lon < x[j+1]) )]) / pasadas[i,j] ), percentil) 
    
    cel[np.where(y <= -35.5)] = np.nan
    return cel