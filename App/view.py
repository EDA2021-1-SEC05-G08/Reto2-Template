"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

#•••••••••••••••••••••••••••••••••••••••••
# Importaciones
#•••••••••••••••••••••••••••••••••••••••••

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT import map as mp
from prettytable import PrettyTable
from DISClib.DataStructures import mapentry as me
from datetime import date
import time

#•••••••••••••••••••••••••••••••••••••••••
# Funciones auxiliares de impresion
#•••••••••••••••••••••••••••••••••••••••••

#----------------------------------------

def print_obras_tecnica(author):

    if author:
        print("\n")
        for book in lt.iterator(author):
            print('Titulo: ' + book['Title'] + '  Medio: ' + book['Medium'] + '  Año: ' + book['Date'])
        print("\n")
    else:
        print('No se encontro el autor.\n')

#----------------------------------------

def print_artistas(author):

    if author == '':
        print('No se encontraron artistas nacidos en el rango dado')
    elif author:
        print("\n")
        x = PrettyTable(["Nombre", "Nacio", 'Murio','Nacionalidad','Genero'])
        x._max_width = {"Nombre" : 20, "Nacio" : 20,"Murio" : 20, "Nacionalidad" : 20,"Genero" : 20}
        for artistas in lt.iterator(author):
            x.add_row([artistas['DisplayName']+'\n', artistas['BeginDate'], artistas['EndDate'],artistas['Nationality'],artistas['Gender']])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

#----------------------------------------

def print_obras(author):

    if author:
        print("\n")
        x = PrettyTable(["Titulo", "Fecha", 'Medio','Dimensiones'])
        x._max_width = {"Titulo" : 30, "Fecha" : 30,"Medio" : 30, "Dimensiones" : 30}
        for artistas in lt.iterator(author):
            if artistas['Medium'] == '':
                tecnica = 'Unknown'
            else: 
                tecnica = artistas['Medium']
            x.add_row([artistas['Title']+'\n', artistas['Date'],tecnica,artistas['Dimensions']])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

#----------------------------------------

def print_obrasyartistas(author):

    if author:
        print("\n")
        x = PrettyTable(["Titulo", 'Artistas',"Fecha", 'Medio','Dimensiones'])
        x._max_width = {"Titulo" : 20, "Artistas" : 30,"Fecha" : 20,"Medio" : 20, "Dimensiones" : 20}
        for artistas in lt.iterator(author):
            codigosautores = artistas['ConstituentID'].replace("[","")
            codigosautores = codigosautores.replace("]","")
            codigosautores = codigosautores.split(",")
            nombres = ''
            for artista in codigosautores:
                codigos = mp.get(cont['Artistas'],artista.strip())
                nombres += me.getValue(codigos)['Nombre']
            if artistas['Medium'] == '':
                tecnica = 'Unknown'
            else: 
                tecnica = artistas['Medium']
            x.add_row([artistas['Title']+'\n',nombres,artistas['DateAcquired'],tecnica,artistas['Dimensions']])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

#----------------------------------------

def print_tecnicas(author):

    if author:
        print("\n")
        x = PrettyTable(["Tecnica", "Cantidad"])
        x._max_width = {"Tecnica" : 40, "Cantidad" : 40}
        for artistas in lt.iterator(author):
            if artistas['Tecnica'] == '':
                tecnica = 'Unknown'
            else: 
                tecnica = artistas['Tecnica']
            x.add_row([tecnica+'\n', artistas['Cantidad']])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

#----------------------------------------

def print_obras_especificos(author):

    if author:
        print("\n")
        x = PrettyTable(["Titulo", 'Artistas','clasificacion',"Fecha", 'Medio','Dimensiones','costo'])
        x._max_width = {"Titulo" : 20, "Artistas" : 30,"clasificacion" : 20,"Fecha" : 20,"Medio" : 20, "Dimensiones" : 20,"costo" : 20}
        for artistas in lt.iterator(author):
            codigosautores = artistas['artistas'].replace("[","")
            codigosautores = codigosautores.replace("]","")
            codigosautores = codigosautores.split(",")
            nombres = ''
            for artista in codigosautores:
                codigos = mp.get(cont['Artistas'],artista.strip())
                nombres += me.getValue(codigos)['Nombre']
            if artistas['tecnica'] == '':
                tecnica = 'Unknown'
            else: 
                tecnica = artistas['tecnica']
            x.add_row([artistas['titulo']+'\n',nombres,artistas['clasificacion'],artistas['fecha'],tecnica,artistas['dimensiones'],str(round(artistas['costo'],3))])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

#----------------------------------------

def print_obrasyartistas2(author):

    if author:
        print("\n")
        x = PrettyTable(["Titulo", 'Artistas',"Fecha", 'Medio','Dimensiones'])
        x._max_width = {"Titulo" : 20, "Artistas" : 30,"Fecha" : 20,"Medio" : 20, "Dimensiones" : 20}
        for artistas in lt.iterator(author):
            codigosautores = artistas['ConstituentID'].replace("[","")
            codigosautores = codigosautores.replace("]","")
            codigosautores = codigosautores.split(",")
            nombres = ''
            for artista in codigosautores:
                codigos = mp.get(cont['Artistas'],artista.strip())
                nombres += me.getValue(codigos)['Nombre']
            if artistas['Medium'] == '':
                tecnica = 'Unknown'
            else: 
                tecnica = artistas['Medium']
            x.add_row([artistas['Title']+'\n',nombres,artistas['Date'],tecnica,artistas['Dimensions']])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

#----------------------------------------

def print_top (author):

    if author:
        print("\n")
        x = PrettyTable(["Nacionalidad", "Cantidad"])
        x._max_width = {"Nacionalidad" : 40, "Cantidad" : 40}
        for artistas, cantidad in zip(lt.iterator(author[0]), lt.iterator(author[1])):
            
            x.add_row([artistas+'\n', cantidad])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

#----------------------------------------

#•••••••••••••••••••••••••••••••••••••••••
# Menu de opciones
#•••••••••••••••••••••••••••••••••••••••••

#----------------------------------------

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Mostrar los tres primeros y los tres ultimos artistas, segun el orden cronologico de un rango de años")
    print("3- Mostrar las tres primeras y las tres ultimas obras de arte, segun el orden cronologico de un rango de fechas")
    print("4- Clasificacion de obras por tecnica, y algunso datos sobre la tecnica mas usada de un artista dado")
    print("5- Clasificar las obras por la nacionalidad de los creadores")
    print("6- Calculo del costo total de trasnporte de obras, segun departamento")
    print("0- Salir")

#----------------------------------------

#•••••••••••••••••••••••••••••••••••••••••
# Incializacion de catalogo y cargue de datos
#•••••••••••••••••••••••••••••••••••••••••

#----------------------------------------

def initCatalog():
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog()

#----------------------------------------

def loadData(catalog):
    """
    Carga los libros en el catalogo
    """
    controller.loadData(catalog)

#•••••••••••••••••••••••••••••••••••••••••
# Menu principal
#•••••••••••••••••••••••••••••••••••••••••

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    #----------------------------------------

    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        cont = controller.initCatalog()
        controller.loadData(cont)
        print('Obras cargadas: ' + str(lt.size(cont['books'])))
        print('Artistas cargados: ' + str(mp.size(cont['Artistas'])))

    #----------------------------------------

    elif int(inputs[0]) == 2:
        año1 = input("Porfavor escriba el primer año de su rango: ")
        año2 = input("Porfavor escriba el ultimo año de su rango: ")
        start_time = time.process_time()
        respuesta = controller.primer_req(cont,año1,año2)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(('\n') +"El total de artistas nacidos en el rango es de: "+ ' ' + str(respuesta[3])+ '\n')
        print(('-'*5) + "Estos son los 3 primeros artistas del rango dado"+ ('-'*5))
        print_artistas(respuesta[0])
        print(('-'*5) + "Estos son los 3 ultimos artistas del rango dado"+ ('-'*5))
        print_artistas(respuesta[1])
        print(elapsed_time_mseg)

    #----------------------------------------

    elif int(inputs[0]) == 3:
        start_time = time.process_time()
        fecha_inicial = input("Porfavor, dijite la fecha inicial en el formato AAAA/MM/DD del rango que desea buscar: ")
        fecha_final = input("Porfavor, dijite la fecha final en el formato AAAA/MM/DD del rango que desea buscar: ")
        respuesta = controller.segundo_req(cont,fecha_inicial,fecha_final)
        print(('\n') +"El total de obras del rango dado es de: "+ ' ' + str(respuesta[2])+ '\n')
        print(('\n') +"El total de obras que fueron compradas en el rango es de : "+ ' ' + str(respuesta[3])+ '\n')
        print(('-'*5) + "Estos son los 3 primeras obras del rango dado"+ ('-'*5))
        print_obrasyartistas(respuesta[0])
        print(('-'*5) + "Estos son los 3 ultimas obras del rango dado"+ ('-'*5))
        print_obrasyartistas(respuesta[1])
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)

    #----------------------------------------
    
    elif int(inputs[0]) == 4:
        start_time = time.process_time()
        Artista = input("Porfavor, dijite el nombre del artista que desea buscar")
        respuesta = controller.tercer_req(cont,Artista)
        print(('\n') +"El total de obras de arte del artista es de: "+ ' ' + str(respuesta[2])+ '\n')
        print(('\n') +"El total de tecnicas utilzadas por el artista es de: "+ ' ' + str(respuesta[3])+ '\n')
        print_tecnicas(respuesta[1])
        print(('\n') +"La tecnica mas utilizada por el artista fue : "+ ' ' + str(respuesta[4])+ '\n')
        print(('\n') +"Esta es una muestra de las obras de la tecnica mas utilizada : "+ ' ' + '\n')
        print_obras(respuesta[0])
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)

    #----------------------------------------

    elif int(inputs[0]) == 5:
        start_time = time.process_time()
        respuesta = controller.cuarto_req(cont)
        top_10 = controller.cuarto_req_10Primeros(respuesta[0],cont)
        primeros_ultimos = controller.primeros_ultimos(top_10[0], cont)
        pais = lt.getElement(top_10[0], 1)
        print(('\n') +"Top 10 nacionalidades: "+ '\n')
        print_top(top_10)
        print(('\n') +"3 primeras obras de "+ str(pais) +": "+ '\n')
        print_obrasyartistas2(primeros_ultimos[0])
        print(('\n') +"3 últimas obras de "+ str(pais) +": "+ '\n')
        print_obrasyartistas2(primeros_ultimos[1])
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)

    #----------------------------------------

    elif int(inputs[0]) == 6:
        start_time = time.process_time()
        Departamento = input("Porfavor, dijite el departamento que desea conocer el costo del tramsporte")
        respuesta = controller.quinto_req(cont,Departamento)
        stop_time = time.process_time()
        print(('\n') +"El total de obras a transportar es de: "+ ' ' + str(respuesta[4])+ '\n')
        print((('\n') +"El total de costo de transporte es de : "+ ' ' + str(round(respuesta[2],2))+ '\n'))
        print((('\n') +"El total de peso de las obras es de : "+ ' ' + str(round(respuesta[3],2))+ '\n'))
        print(('-'*5) + "Estos son las 5 obras mas caras del departmento"+ ('-'*5))
        print_obras_especificos(respuesta[0])
        print(('-'*5) + "Estos son las 5 obras mas antiguas del departmento"+ ('-'*5))
        print_obras_especificos(respuesta[1])
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)
        
    else:
        sys.exit(0)
sys.exit(0)