"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

#•••••••••••••••••••••••••••••••••••••••••
#   Importaciones
#•••••••••••••••••••••••••••••••••••••••••

import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as merge
assert cf
from datetime import date

"""

    Se define la estructura de un catálogo de obras y artsitas. El catálogo tendrá 12 maps, entre esas,
    hay una creada especificamente para el almacenamiento de los artistas y otra para el almacenamiento
    de las obras, las demas son de referenciacion para la facilidad de la busqueda de datos.

"""

#•••••••••••••••••••••••••••••••••••••••••
#   Inicializacion del catalogo
#•••••••••••••••••••••••••••••••••••••••••

#----------------------------------------

def newCatalog():

    """

        Inicializa el catálogo de obras y artistas.

        Se crean indices (Maps) por los siguientes criterios:
        Obras.
        Artistas.
        Medios.
        Departamentos.
        Años.
        IDs de los artistas.
        Fechas de adquisicion.
        Nombres de los artistas.
        Paises.

        Retorna el catalogo inicializado.

    """

    catalog = {'books': None,
                'Artistas':None,
                'Medios': None,
                'Departamento': None,
                'years':None,
                'Codigos_Artistas':None,
                'AdquisicionFecha': None,
                'Nombres_Artistas': None,
                "Artistas_nacion": None,
                "Orden_naciones": None,
                "Naciones_cantidad": None,
                "Codigos_orden": None
                }

    catalog['books'] = lt.newList(
                                    'SINGLE_LINKED', 
                                    compareBookIds
                                )

    catalog['Artistas'] = mp.newMap(
                                    20000,
                                    maptype='PROBING',
                                    loadfactor=0.5, 
                                    comparefunction=compareAuthorsByName
                                    )

    catalog['Medios'] = mp.newMap(
                                    1000,
                                    maptype='CHAINING',
                                    loadfactor=4.0,
                                    comparefunction=compareAuthorsByName
                                )
    
    catalog['Departamento'] = mp.newMap(
                                        1000,
                                        maptype='CHAINING',
                                        loadfactor=4.0,
                                        comparefunction=compareAuthorsByName
                                        )
                                
    catalog['years'] = mp.newMap(
                                    15000,
                                    maptype='PROBING',
                                    loadfactor=0.5,
                                    comparefunction=compareMapYear
                                )
    
    catalog['Codigos_Artistas'] = mp.newMap(
                                            150000,
                                            maptype='CHAINING',
                                            loadfactor=4.0,
                                            comparefunction=compareAuthorsByName
                                            )

    catalog['AdquisicionFecha'] = mp.newMap(
                                            150000,
                                            maptype='PROBING',
                                            loadfactor=0.5,
                                            comparefunction=compareMapYear
                                            )

    catalog['Nombres_Artistas'] = mp.newMap(
                                            150000,
                                            maptype='CHAINING',
                                            loadfactor=4.0,
                                            comparefunction=compareAuthorsByName
                                            )

    catalog["Artistas_nacion"] = mp.newMap(
                                            150000,
                                            maptype='CHAINING',
                                            loadfactor=4.0
                                            )
    catalog["Orden_naciones"] = mp.newMap(
                                            1000,
                                            maptype='CHAINING',
                                            loadfactor=4.0
                                        )

    catalog["Naciones_cantidad"]= mp.newMap(
                                            1000,
                                            maptype='CHAINING',
                                            loadfactor=4.0
                                            )

    catalog["Codigos_orden"]= mp.newMap(
                                        1000,
                                        maptype='CHAINING',
                                        loadfactor=4.0
                                        )

    return catalog

#----------------------------------------

#•••••••••••••••••••••••••••••••••••••••••
# Funciones para agregar informacion al catalogo
#•••••••••••••••••••••••••••••••••••••••••

#----------------------------------------

def addBook(catalog, book):

    """

        Esta funcion adiciona una obra a la lista de obras,
        adicionalmente lo guarda en un Map usando como llave
        el codigo del artista que la creo, Map usando como
        llave el departamento de la obra y en uno ultimo en
        donde lo referencia por la fecha de su adquisicion.

    """

    lt.addLast(catalog['books'], book)
    
    artistas = book['ConstituentID'].replace("[","")
    artistas = artistas.replace("]","")
    artistas = artistas.split(",")

    for codigo in artistas:
        addBookAuthor(catalog, codigo.strip(), book)
    addDepartamento(catalog, book['Department'].strip(), book)
    addAdquisionFecha(catalog, book)

#----------------------------------------

def addArtistas(catalog,book):

    """

        Esta función adiciona un artista al Map de artistas
        y los referencia en otros dos Maps por sus
        identificadores y nacionalidades.

    """
    
    author = newartista(book['DisplayName'],book['ConstituentID'])

    addBookYear(catalog, book)
    mp.put(catalog['Artistas'], book['ConstituentID'], author)
    mp.put(catalog['Nombres_Artistas'], book['DisplayName'], book['ConstituentID'])
    mp.put(catalog["Artistas_nacion"], book['ConstituentID'], book['Nationality'])

#----------------------------------------

def addBookYear(catalog, book):

    """
        Esta funcion adiciona una obra a un Map el cual tiene como
        referencia el año de las obras.

        Los años se guardan en un Map, donde la llave es el año
        y el valor la lista de obras de ese año.

    """

    try:
        years = catalog['years']
        if (book['BeginDate'] != ''):
            pubyear = book['BeginDate']
            pubyear = int(float(pubyear))
        else:
            pubyear = 2020
        existyear = mp.contains(years, pubyear)
        if existyear:
            entry = mp.get(years, pubyear)
            year = me.getValue(entry)
        else:
            year = newYear(pubyear)
            mp.put(years, pubyear, year)
        lt.addLast(year['books'], book)
    except Exception:
        return None

#----------------------------------------

def addAdquisionFecha(catalog, book):

    """

        Esta funcion adiciona una obra a la lista de obras que
        fueron adquiridas en un mismo año.

        Los años se guardan en un Map, donde la llave es el año
        y el valor la lista de obras de ese año.

    """

    try:
        years = catalog['AdquisicionFecha']
        if (book['DateAcquired'] != ''):
            pubyear = book['DateAcquired']
            pubyear = int((date.fromisoformat(pubyear)).strftime("%Y%m%d%H%M%S"))
        elif (book['DateAcquired'] == ''):
            pubyear = 0
        existyear = mp.contains(years, pubyear)
        if existyear:
            entry = mp.get(years, pubyear)
            year = me.getValue(entry)
        else:
            year = newYear(pubyear)
            mp.put(years, pubyear, year)
        lt.addLast(year['books'], book)
    except Exception:

        return None

#----------------------------------------

def addDepartamento(catalog, authorname, book):

    """

        Esta función adiciona una obra a la lista de obras que
        se encuentran en un mismo departamento.

        Los departamentos se guardan en un Map, donde la llave
        es el departamento y el valor la lista de obras que se
        encuentran en ese departamento.

    """

    authors = catalog['Departamento']
    existauthor = mp.contains(authors, authorname)
    if existauthor:
        entry = mp.get(authors, authorname)
        author = me.getValue(entry)
    else:
        author = newdepartamento(authorname)
        mp.put(authors, authorname, author)
    lt.addLast(author['books'], book)

#----------------------------------------

def addBookAuthor(catalog, authorname, book):

    """

        Esta función adiciona una obra a la lista de obras publicadas
        por un mismo artista.

        Los departamentos se guardan en un Map, donde la llave
        es el artista y el valor la lista de obras que fueron
        creadas por ese artista.

    """

    authors = catalog['Codigos_Artistas']
    existauthor = mp.contains(authors, authorname)

    if existauthor:
        entry = mp.get(authors, authorname)
        author = me.getValue(entry)
    else:
        author = newAuthor(authorname)
        mp.put(authors, authorname, author)

    lt.addLast(author['obras'], book)

#----------------------------------------

def addcodigoautor(catalog, authorname, book):

    """
    
        Esta función adiciona un artista referenciandolo por
        su ID

    """
    authors = catalog['Artistas']
    author = newartista(authorname,book['ConstituentID'])
    mp.put(authors, authorname, author)

#----------------------------------------

def addtecnica(catalog, authorname, book):

    """

        Esta función adiciona una obra a la lista de obras creadas
        con una misma tecnica.

        Las obras se guardan en un Map, donde la tecnica y el valor
        la lista de obras que fueron creadas con esa misma tecnica.

    """

    existauthor = mp.contains(catalog, authorname)

    if existauthor:
        entry = mp.get(catalog, authorname)
        author = me.getValue(entry)
    else:
        author = newTecnica_lista(authorname)
        mp.put(catalog, authorname, author)

    lt.addLast(author['obras'], book)

#----------------------------------------

#•••••••••••••••••••••••••••••••••••••••••
# Funciones para creacion de datos
#•••••••••••••••••••••••••••••••••••••••••

#----------------------------------------

def newAuthor(name):

    """

    Crea una nueva estructura para modelar las obras de un artista.
    Se crea una lista para guardar las obras de dicho artista.
    
    """
    artista = {
                'codigo': "",
                "obras": None,}

    artista['codigo'] = name
    artista['obras'] = lt.newList(
                                    'ARRAY_LIST',
                                    compareAuthorsByName
                                )

    return artista

#----------------------------------------

def newartista(name,codigo):

    """

        Crea una nueva estructura para modelar el nombre y el codigo
        de un artista.

    """

    artista = {
                'Nombre': "",
                 "Codigo": ''
                }

    artista['Nombre'] = name
    artista['Codigo'] = codigo

    return artista

#----------------------------------------

def newTecnica(nombre_tecnica):

    """

        Crea una nueva estructura para modelar una tecnica
        por su nombre y la cantidad de obras creadas por esta tecnica.

    """

    tecnica = {
                'Tecnica': "",
                "Cantidad": 0
                }

    tecnica['Tecnica'] = nombre_tecnica
    tecnica['Cantidad'] = None

    return tecnica

#----------------------------------------

def newTecnica_lista(nombre_tecnica):

    """

        Crea una nueva estructura para modelar una tecnica
        por su nombre y una lista de obras creadas por esta tecnica.

    """

    tecnica = {
                'Tecnica': "",
                "Cantidad": 0
                }

    tecnica['Tecnica'] = nombre_tecnica
    tecnica['obras'] = lt.newList('ARRAY_LIST')

#----------------------------------------

def newCosto(codigo_obra,costo,peso,titulo,artistas,clasificacion,fecha,dimensiones,tecnica):

    """

        Crea una nueva estructura para modelar el costo de sus 
        obras.

    """
    artista = {
                'codigo': "",
                "costo": None,
                "peso": None
            }

    artista['codigo'] = codigo_obra
    artista['costo'] = costo
    artista['peso'] = peso
    artista['titulo'] = titulo
    artista['artistas'] = artistas
    artista['clasificacion'] = clasificacion
    artista['fecha'] = fecha
    artista['dimensiones'] = dimensiones
    artista['tecnica'] = tecnica

    return artista

#----------------------------------------

def newYear(pubyear):

    """

        Esta funcion crea la estructura de obras asociadas
        a un mismo año de publicacion.

    """
    entry = {
                'year': "",
                "books": None
            }

    entry['year'] = pubyear

    entry['books'] = lt.newList(
                                'ARRAY_LIST', 
                                compareYears
                                )

    return entry

#----------------------------------------

def newdepartamento(pubyear):
    """
        Esta funcion crea la estructura de obras asociadas
        a un mismo departamento.

    """

    entry = {
                'Departamento': "",
                "books": None
            }

    entry['Departamento'] = pubyear

    entry['books'] = lt.newList(
                                'ARRAY_LIST',
                                compareYears
                                )

    return entry

#----------------------------------------

#•••••••••••••••••••••••••••••••••••••••••
# Funciones auxiliares
#•••••••••••••••••••••••••••••••••••••••••

#----------------------------------------

def getBooksByAuthor(catalog, authorname):

    """

        Retorna un artista con sus obras a partir del nombre del artista.

    """

    author = mp.get(catalog['Medios'], authorname)
    out = None

    if author:
        out =  me.getValue(author)

    return out

#----------------------------------------

def getBooksByYear(catalog, year):

    """

        Retorna las obras publicadas en un año.

    """

    year = mp.get(catalog['years'], year)
    out = None

    if year:
        out =  me.getValue(year)['books']

    return out

#----------------------------------------

def cantidad_tecnicas(artistas):

    """

        Retorna la cantidad de tecnicas.

    """

    cantidad_de_tecnicas_veces = lt.newList('ARRAY_LIST',cmpfunction=comparetecnicas)
    tecnicas_final = lt.newList('ARRAY_LIST')
    for partes in lt.iterator(artistas['obras']):
        lt.addLast(tecnicas_final,partes['Medium'])

    for i in lt.iterator(tecnicas_final):
        posauthor = lt.isPresent(cantidad_de_tecnicas_veces, i)
        if posauthor > 0:
            artista = lt.getElement(cantidad_de_tecnicas_veces, posauthor)
            artista['Cantidad'] += 1
        else:
            artista = newTecnica(i)
            artista['Cantidad'] = 1
            lt.addLast(cantidad_de_tecnicas_veces, artista)
        
    k = 0
    for p in lt.iterator(cantidad_de_tecnicas_veces):
        if int(p['Cantidad']) > k:
            k = p['Cantidad']
            maximo = p['Tecnica']
    
    return maximo,cantidad_de_tecnicas_veces,lt.size(cantidad_de_tecnicas_veces)

#----------------------------------------

def calculo_de_transporte(catalog):

    """

        Calcula el costo del transporte de las obras.

    """

    obras = lt.newList('ARRAY_LIST')
    for obra in lt.iterator(catalog):

        peso = obra['Weight (kg)'] 
        altura = obra['Height (cm)'] 
        ancho = obra['Width (cm)'] 
        profundidad = obra['Depth (cm)']
        longitud = obra['Length (cm)']
        diametro = obra['Diameter (cm)']

        if (altura == 0 or altura == '') and (ancho == 0 or ancho == ''):
            costo = 48.00

        elif (longitud != 0 and longitud != '') and (ancho != 0 and ancho != '') and (altura == 0 or altura == ''):
            costo = (float(longitud)*float(ancho)*72)/10000 

        elif (altura != 0 and altura != '') and (ancho != 0 and ancho != ''):
            costo = (float(altura)*float(ancho)*72)/10000
            if (profundidad != 0 and profundidad != ''):
                costo = max((float(altura)*float(ancho)*72)/10000,(float(altura)*float(ancho)*72*float(profundidad))/1000000)
            if (peso != 0 and peso != '') and (profundidad != 0 and profundidad != ''):
                costo = max((float(peso) * 72),(float(altura)*float(ancho)*72)/10000,(float(altura)*float(ancho)*72*float(profundidad))/1000000)
            elif (peso != 0 and peso != '') and (profundidad == 0 or profundidad == ''):
                costo = max((float(peso) * 72),(float(altura)*float(ancho)*72)/10000)
        elif (peso != 0 and peso != ''):
            costo1 = (float(peso) * 72)
            costo = max(costo1,costo)

        if (diametro != 0 and diametro != '') and (altura != 0 and altura != ''):
            costo = (((float(diametro)/2)**2)*float(altura)*72*3.14)/1000000
        elif (diametro != 0 and diametro != '') and (altura == 0 and altura == ''):
            costo = (((float(diametro)/2)**2)*72*3.14)/10000 
            
        if (peso == 0 or peso == ''):
            pesar = 0
        else: 
            pesar = peso 
        precio = newCosto(obra['ObjectID'],costo,pesar,obra['Title'],obra['ConstituentID'],obra['Classification'],obra['Date'],obra['Dimensions'],obra['Medium'])

        if precio['costo'] == 0:
            precio['costo'] = 48.00
        lt.addLast(obras,precio)

    return obras

#----------------------------------------

def suma_costo(catalog):

    suma = 0
    for p in lt.iterator(catalog):
        suma += p['costo']

    return float(suma)

#----------------------------------------

def suma_peso(catalog):

    suma = 0
    for p in lt.iterator(catalog):
        suma += float(p['peso'])

    return float(suma)

#----------------------------------------

def obtener_antiguas(catalog):

    """
    
        Retorna los tres ultimos artistas cargados.

    """

    ordenadas = sortantiguasobras(catalog)
    con_fecha = lt.newList()
    orden = lt.newList()

    for obra in lt.iterator(ordenadas):
        if obra['fecha'] != '':
            lt.addLast(con_fecha, obra)

    orden = lt.subList(con_fecha,1,5)

    return orden

#----------------------------------------

def cuarto_req_10Primeros(lista,catalogo):

    primeros_10_nomb = lt.newList('ARRAY_LIST')
    primeros_10_valor = lt.newList('ARRAY_LIST')
    comp = 10
    for numero in lt.iterator(lista):
        pais = me.getValue(mp.get(catalogo["Naciones_cantidad"], numero))
        lt.addLast(primeros_10_nomb, pais)
        lt.addLast(primeros_10_valor, numero)

        if comp == 1:
            break
        comp -= 1

    return primeros_10_nomb,primeros_10_valor

#----------------------------------------

def primeros_ultimos(lista_nombres, catalogo):

    pais_mayor = lt.getElement(lista_nombres, 1)
    codigos_paises = catalogo["Codigos_orden"]
    codigos_mayor = me.getValue(mp.get(codigos_paises, pais_mayor))

    primeros = lt.subList(codigos_mayor, 1, 3)
    ultimos = lt.subList(codigos_mayor, int(lt.size(codigos_mayor)-2), 3)

    primeros_3 = lt.newList('ARRAY_LIST')
    ultimos_3 = lt.newList('ARRAY_LIST')


    for pri in lt.iterator(primeros):
        for obras in lt.iterator(catalogo["books"]):
            if pri == obras["ObjectID"]:
                lt.addLast(primeros_3, obras)

    for ult in lt.iterator(ultimos):
        for obras in lt.iterator(catalogo["books"]):
            if ult == obras["ObjectID"]:
                lt.addLast(ultimos_3, obras)
        
    return primeros_3, ultimos_3

#----------------------------------------

#•••••••••••••••••••••••••••••••••••••••••
# Funciones de comparacion
#•••••••••••••••••••••••••••••••••••••••••

#----------------------------------------

def compareAuthorsByName(keyname, author):

    """

        Compara los nombres de dos artistas. El primero es una cadena
        y el segundo un entry de un map.

    """

    authentry = me.getKey(author)

    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

#----------------------------------------

def compareBookIds(id1, id2):

    """

        Compara los IDs de las obras.

    """

    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

#----------------------------------------

def compareantiguas(artista1, artista2):

    """

        Compara los IDs de las obras.
        
    """

    return ((artista1['Date']) < (artista2['Date']))

#----------------------------------------

def compareantiguasobras(artista1, artista2):

    """

        Compara la fecha de dos obras.
        
    """

    return ((artista1['fecha']) < (artista2['fecha']))

#----------------------------------------

def compareMapYear(id, tag):

    """

        Compara la fecha de dos obras.
        
    """

    tagentry = me.getKey(tag)
    if (id == tagentry):
        return 0
    elif (id > tagentry):
        return 1
    else:
        return 0

#----------------------------------------

def comparenacidos(artista1, artista2):

    """

        Compara la fecha de nacimiento de dos artistas.
        
    """

    return ((artista1['BeginDate']) < (artista2['BeginDate']))

#----------------------------------------

def comparetecnicas(tecnica1, tecnica):

    out = -1

    if (tecnica1.lower().strip() == tecnica['Tecnica'].lower().strip()):
        out = 0

    return out

#----------------------------------------

def comparecanitdad(artista1, artista2):

    """

        Compara la cantidad de obras de dos artistas.
        
    """

    return (float(artista1['Cantidad']) > float(artista2['Cantidad']))

#----------------------------------------

def comparacostos(artista1, artista2):

    """

        Compara el costo de las obras de dos artistas.
        
    """

    return (float(artista1['costo']) > float(artista2['costo']))

#----------------------------------------

def comppaises(pais1, pais2):

    """

        Compara la cantidad de aritstas de dos paises.
        
    """

    return (int(pais1) > int(pais2))

#----------------------------------------

def compareYears(year1, year2):

    """

        Compara dos años.
        
    """

    if (int(year1) == int(year2)):
        return 0
    elif (int(year1) > int(year2)):
        return 1
    else:
        return 0

#----------------------------------------

def cmpArtworkByDateAcquired(artwork1, artwork2):

    """

        Compara las fechas de adquisicon de dos obras.

        
    """

    if artwork1['DateAcquired'] == '':

        fecha1 = 0
    else: 
        fecha1 = int((date.fromisoformat(artwork1['DateAcquired'])).strftime("%Y%m%d%H%M%S"))

    if artwork2['DateAcquired'] == '':

        fecha2 = 0

    else:
        fecha2 = int((date.fromisoformat(artwork2['DateAcquired'])).strftime("%Y%m%d%H%M%S"))

    return fecha1 < fecha2

#----------------------------------------

#•••••••••••••••••••••••••••••••••••••••••
# Funciones de ordenamiento
#•••••••••••••••••••••••••••••••••••••••••

#----------------------------------------

def sortantiguasobras(catalog):

    """

        Ordena las obras por fecha.
        
    """

    orden = merge.sort(catalog, compareantiguasobras)
    return orden

#----------------------------------------

def sortantiguas(catalog,size):


    """

        Ordena las obras por fecha.
        
    """

    sub_list = lt.subList(catalog, 1, size)
    sub_list = sub_list.copy()
    orden = merge.sort(sub_list, compareantiguas)

    return orden

#----------------------------------------

def sortnacidos(catalog):

    """

        Ordena los artistas por fecha de nacimiento.
        
    """

    orden = merge.sort(catalog, comparenacidos)

    return orden

#----------------------------------------

def sortCantidades(catalog):

    """

        Ordena cantidades.
        
    """

    orden = merge.sort(catalog, comparecanitdad)
    return orden

#----------------------------------------

def sortobras(catalog):

    """

        Ordena obras por fecha de adquisicion.
        
    """

    sorted_list = merge.sort(catalog, cmpArtworkByDateAcquired)
    return sorted_list

#----------------------------------------

def sortcostos(catalog):

    """

        Ordena por costos.
        
    """

    orden = merge.sort(catalog, comparacostos)
    return orden

#----------------------------------------

def sortnaciones(lista):

    """

        Ordena por costos.
        
    """

    orden = merge.sort(lista, comppaises)
    return orden

#----------------------------------------

#•••••••••••••••••••••••••••••••••••••••••
#Funciones de consulta
#•••••••••••••••••••••••••••••••••••••••••

#----------------------------------------

def primer_req(catalogo,año1,año2):

    """

        Responde al primer requerimiento.
        
    """

    nueva = lt.newList('ARRAY_LIST')
    años = mp.keySet(catalogo['years'])
    for c in lt.iterator(años):
        if int(c) >= int(año1) and int(c) <= int(año2):
            valor = mp.get(catalogo['years'],c)
            for i in lt.iterator(me.getValue(valor)['books']):
                lt.addLast(nueva,i)
    orden = sortnacidos(nueva)
    medida = str(lt.size(orden))
    if lt.size(orden) == 0:
        primeros = ''
        ultimos = ''
    elif lt.size(orden) < 6:
        primeros = orden
        ultimos = orden
    elif lt.size(orden) >= 6:
        primeros = lt.subList(orden, 1, 3)
        ultimos = lt.subList(orden, int(lt.size(orden)-2), 3)
    return primeros,ultimos,orden,medida

#----------------------------------------

def segundo_req(catalog,fecha_inicial,fecha_final):

    """

        Responde al segundo requerimiento.
        
    """

    fecha1 = int((date.fromisoformat(fecha_inicial.replace('/','-'))).strftime("%Y%m%d%H%M%S"))
    fecha2 = int((date.fromisoformat(fecha_final.replace('/','-'))).strftime("%Y%m%d%H%M%S"))
    llaves = (mp.keySet(catalog['AdquisicionFecha']))
    nueva = lt.newList('ARRAY_LIST')
    for c in lt.iterator(llaves):
        if c >= fecha1 and c <= fecha2:
            valor = mp.get(catalog['AdquisicionFecha'],c)
            lista = me.getValue(valor)['books']
            for j in lt.iterator(lista):
                lt.addLast(nueva,j)
    orden = sortobras(nueva)
    if lt.size(orden) == 0:
        primeros = ''
        ultimos = ''
    elif lt.size(orden) < 6:
        primeros = orden
        ultimos = orden
    elif lt.size(orden) >= 6:
        primeros = lt.subList(orden, 1, 3)
        ultimos = lt.subList(orden, int(lt.size(orden)-2), 3)
    conteo = 0
    for k in lt.iterator(orden):
        if 'purchase' in k['CreditLine'].lower():
            conteo += 1
    return primeros,ultimos,lt.size(orden),conteo

#----------------------------------------

def tercer_req(catalog,Artista):

    """

        Responde al tercer requerimiento.
        
    """

    valores = mp.get(catalog['Nombres_Artistas'],Artista)
    valores_especificos = mp.get(catalog['Codigos_Artistas'],me.getValue(valores))
    tecnicas = cantidad_tecnicas(me.getValue(valores_especificos))
    tecnicas_orden = sortCantidades(tecnicas[1])
    obras = lt.newList('ARRAY_LIST')
    for obra in lt.iterator(me.getValue(valores_especificos)['obras']):
        if obra['Medium'] == tecnicas[0]:
            lt.addLast(obras,obra)

    if lt.size(tecnicas_orden) <= 10:
        tecnicas_orden = tecnicas_orden
    elif lt.size(tecnicas_orden) > 10:
        primeros = lt.subList(tecnicas_orden, 1, 10)
        tecnicas_orden = primeros

    if lt.size(obras) <= 10:
        obras = obras
    elif lt.size(obras) > 10:
        primeros = lt.subList(obras, 1, 10)
        obras = primeros
    return obras,tecnicas_orden,lt.size(me.getValue(valores_especificos)['obras']),tecnicas[2],tecnicas[0]

#----------------------------------------

def cuarto_req(catalogo):

    """

        Responde al cuarto requerimiento.
        
    """

    artistas = catalogo['Artistas_nacion']

    libros = catalogo['books']
    lt_naciones = lt.newList('ARRAY_LIST')
    

    for obra in lt.iterator(libros):
        codigo_obra = obra["ObjectID"]
        lt_codigos = lt.newList('ARRAY_LIST')

        obras = obra['ConstituentID'].replace("[","")
        obras = obras.replace("]","")
        obras = obras.split(",")
        for c in obras:
            codigo = c.strip()
            nacionalidad = me.getValue(mp.get(artistas, codigo))
            if nacionalidad == "" or nacionalidad == "Nationality unknown":
                nacionalidad = "Unknown"

            estado = mp.contains(catalogo["Orden_naciones"], nacionalidad)
            
            if estado:
                llave_valor = mp.get(catalogo["Orden_naciones"], nacionalidad)
                suma = (me.getValue(llave_valor) + 1)
                me.setValue(llave_valor, suma)

                llave_valor2 = mp.get(catalogo["Codigos_orden"], nacionalidad)
                lista = me.getValue(llave_valor2)
                lt.addLast(lista, codigo_obra)
                me.setValue(llave_valor2, lista)

            else:
                lt.addLast(lt_codigos, codigo_obra)
                mp.put(catalogo["Orden_naciones"], nacionalidad, 1)
                mp.put(catalogo["Codigos_orden"], nacionalidad, lt_codigos)
                lt.addLast(lt_naciones, nacionalidad)


    for pais in lt.iterator(lt_naciones):
        llave_valor1 = mp.get(catalogo["Orden_naciones"], pais)
        cantidad = me.getValue(llave_valor1)
        mp.put(catalogo["Naciones_cantidad"], cantidad, pais)

    llaves = mp.keySet(catalogo["Naciones_cantidad"])
    orden = sortnaciones(llaves)
    
    return orden,catalogo["Codigos_orden"]

#----------------------------------------

def quinto_req(catalog,departamento):

    """

        Responde al quinto requerimiento.
        
    """

    total_departamento = mp.get(catalog['Departamento'],departamento)
    obras_artista = me.getValue(total_departamento)['books']
    obras = calculo_de_transporte(obras_artista)
    costo = suma_costo(obras)
    peso = suma_peso(obras)
    ordenadas_costo = sortcostos(obras)
    primerascostosas = lt.subList(ordenadas_costo,1,5)
    orden_antiguas = sortantiguasobras(obras)
    ultimas_antiguas = obtener_antiguas(orden_antiguas)
    return primerascostosas,ultimas_antiguas,costo,peso,lt.size(obras)