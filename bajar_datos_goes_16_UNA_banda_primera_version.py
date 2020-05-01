## este es un script para bajar datos del GOES-16 con Python
## solo baja POR BANDA particular (CMIPF), no multibanda
## Primera version
##
## POWERED BY HUAYRATORO
 
import s3fs # esta libreria colecta los datos desde fuente
import numpy as np 

# se eligen las bandas, dias, horas y minutos que seran descargados

##### lo unico que hay que modificar #####
mi = 0         # minutos desde el comienzo de la hora desde 0 a 50  
hh = 0         # es la hora del dia
dd = 11         # es el dia juliano del anio
yy = 2020       # es el anio
banda = 13      # banda de medicion de 1 - 13

# Credenciales anonimas para acceso publico de datos del GOES 16
fs = s3fs.S3FileSystem(anon=True)

# para listar todo el contenido del directorio
# print(fs.ls('s3://noaa-goes16/'))

# Ahora se elige el producto de una sola banda (CMIPF)
# es una lista que contiene el anio, dia juliano, hora, minutos y bandas medidas 

## SI LAS HORAS SON DE 0 A 9
if len(str(hh)) == 1 :
    # Se seleccionan todas las horas del dia con sus minutos
    # se indexan en funcion de la longitud del string
    if len(str(dd)) == 1 :
        files = np.array(fs.ls('noaa-goes16/ABI-L2-CMIPF/'+str(yy)+'/00'+str(dd)+'/0'+str(hh)+'/'))
    if len(str(dd)) == 2 :
        files = np.array(fs.ls('noaa-goes16/ABI-L2-CMIPF/'+str(yy)+'/0'+str(dd)+'/0'+str(hh)+'/'))
    if len(str(dd)) == 3 :
        files = np.array(fs.ls('noaa-goes16/ABI-L2-CMIPF/'+str(yy)+'/'+str(dd)+'/0'+str(hh)+'/'))

    bandas = np.repeat('aa', (len(files))) 
    fechas = np.repeat('aaaaaaaaaaaaaaa', (len(files)))

    # extraigo una lista de bandas

    for i in range(0, len(files)):
        bandas[i] = files[i][56:58]

    # extraigo la lista de fechas

    for i in range(0, len(files)):
        fechas[i] = files[i][64:75]

    # consigo la fecha, banda, minuto y hora deseados
    if len(str(dd)) == 1 :
        if len(str(mi)) > 1 :
            a = np.where(fechas == (str(yy)+'00'+str(dd)+'0'+str(hh)+str(mi)))
        if len(str(mi)) == 1 :
            a = np.where(fechas == (str(yy)+'00'+str(dd)+'0'+str(hh)+'0'+str(mi)))
    if len(str(dd)) == 2 :
        if len(str(mi)) > 1 :
            a = np.where(fechas == (str(yy)+'0'+str(dd)+'0'+str(hh)+str(mi)))
        if len(str(mi)) == 1 :
            a = np.where(fechas == (str(yy)+'0'+str(dd)+'0'+str(hh)+'0'+str(mi)))    
    if len(str(dd)) == 3 :
        if len(str(mi)) > 1 :
            a = np.where(fechas == (str(yy)+str(dd)+'0'+str(hh)+str(mi)))
        if len(str(mi)) == 1 :
            a = np.where(fechas == (str(yy)+str(dd)+'0'+str(hh)+'0'+str(mi)))    
    
    if len(str(banda)) == 1 :
        b = np.where(bandas == ('0'+str(banda)))
        c = np.intersect1d(a,b)
    if len(str(banda)) > 1 :
        b = np.where(bandas == str(banda))
        c = np.intersect1d(a,b)

## SI LAS HORAS SON DE 10 A 23
## igual que el anterior
if len(str(hh)) > 1 :
    if len(str(dd)) == 1 :
        files = np.array(fs.ls('noaa-goes16/ABI-L2-CMIPF/'+str(yy)+'/00'+str(dd)+'/'+str(hh)+'/'))
    if len(str(dd)) == 2 :
        files = np.array(fs.ls('noaa-goes16/ABI-L2-CMIPF/'+str(yy)+'/0'+str(dd)+'/'+str(hh)+'/'))
    if len(str(dd)) == 3 :
        files = np.array(fs.ls('noaa-goes16/ABI-L2-CMIPF/'+str(yy)+'/'+str(dd)+'/'+str(hh)+'/'))

    bandas = np.repeat('aa', (len(files))) 
    fechas = np.repeat('aaaaaaaaaaaaaaa', (len(files)))

    # extraigo una lista de bandas

    for i in range(0, len(files)):
        bandas[i] = files[i][56:58]

    # extraigo la lista de fechas

    for i in range(0, len(files)):
        fechas[i] = files[i][64:75]

    if len(str(dd)) == 1 :
        if len(str(mi)) > 1 : 
            a = np.where(fechas == (str(yy)+'00'+str(dd)+str(hh)+str(mi)))
        if len(str(mi)) == 1 :
            a = np.where(fechas == (str(yy)+'00'+str(dd)+str(hh)+'0'+str(mi)))
    if len(str(dd)) == 2 :
        if len(str(mi)) > 1 :    
            a = np.where(fechas == (str(yy)+'0'+str(dd)+str(hh)+str(mi)))    
        if len(str(mi)) == 1 :
            a = np.where(fechas == (str(yy)+'0'+str(dd)+str(hh)+'0'+str(mi)))
    if len(str(dd)) == 3 :
        if len(str(mi)) > 1 :
            a = np.where(fechas == (str(yy)+str(dd)+str(hh)+str(mi)))
        if len(str(mi)) == 1 :
            a = np.where(fechas == (str(yy)+str(dd)+str(hh)+'0'+str(mi)))    

    if len(str(banda)) == 1 :
        b = np.where(bandas == ('0'+str(banda)))
        c = np.intersect1d(a,b)
    if len(str(banda)) > 1 :
        b = np.where(bandas == str(banda))
        c = np.intersect1d(a,b)    

print('Se descargara el archivo : ' + str(files[c][0]))
# finalmente se descarga el archivo
# indicar la ruta de salida del netcdf
fs.get(str(files[c][0]), '/home/.../'+(str(yy)+str(dd)+str(hh)+str(mi)+'.nc'))
