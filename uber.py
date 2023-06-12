import sys
import pickle
import graph
import dictionary
import trip
entrada = sys.argv

def imprimirhash(hashf):
    for i in range(0, len(hashf)):
        print(i, end= " ")
        print(hashf[i])
        print(" ")

def imprimirmapa(theMap):
    for i in range(0, len(theMap)):
        auxList = theMap[i]
        print(i, end =" ")
        for j in range(0, len(auxList)):
            print((auxList[j].value, auxList[j].dist, auxList[j].nextCorner), end= " ")
        print(" ")
    return
"""
Función que gestiona la carga de una ubicación fija. Llama a la función getDirection
para que corte la dirección y crea el objeto tupla element de la forma
(nombre, dirección) y ese elemento se guarda en la hash de ubicaciones fijas.
Posteriormente se procede al guardado de las estructuras en sus respectivos
archivos .pickle
"""
def loadFixElement(entrada):
    direction = getDirection(entrada[1])
    element = (entrada[0], direction)
    f = open("hashCorners.pickle", "rb")
    esquinas = pickle.load(f)
    f.close()
    f = open("hashFixedLocations.pickle", "rb")
    hashFixLocs = pickle.load(f)
    f.close()
    f = open("mapa.pickle", "rb")
    mapa = pickle.load(f)
    f.close()
    mapa = graph.insert(mapa, hashFixLocs, esquinas, element)
    f = open("mapa.pickle", "wb")
    pickle.dump(mapa, f)
    f.close()
    f = open("hashFixedLocations.pickle", "wb")
    pickle.dump(hashFixLocs, f)
    f.close()
    return

"""
Función que gestiona la carga de ubicaciones móviles. Se realiza la apertura
de todas las estructuras necesarias. Si es un auto o una persona varía el procedimiento.
Si es un auto, se inserta el auto en la hash con la función insertCar. Se devuelve la 
priorityCorner con las distancias de los autos hasta las esquinas actualizadas. Además, el
hash de ubicaciones móviles se actualiza ya que es pasado por referencia. Si es una persona, solamente
se produce la inserción del elemento en la lista de ubicaciones móviles. 
Finalmente se produce el guardado de todas las estructuras en sus respectivos
archivos.pickle
"""
def loadMobileElement(element):
    f = open("mapa.pickle", "rb")
    mapa = pickle.load(f)
    f.close()
    f = open("hashMobile.pickle", "rb")
    hashMovil = pickle.load(f)
    f.close()
    f = open("cornerDistances.pickle", "rb")
    priorityCorners = pickle.load(f)
    f.close()
    f = open("hashCorners.pickle", "rb")
    hashEsquinas = pickle.load(f)
    f.close()
    f = open("corners.pickle", "rb")
    esquinas = pickle.load(f)
    f.close()
    if element[0][0] == "C":
        hashMovil = trip.insertCar(mapa, hashMovil, priorityCorners, hashEsquinas, element, esquinas)
    elif element[0][0] == "P":
        hashMovil = trip.insertPeople(hashMovil, element)
    else:
        print("Objeto mal ingresado")
        return
    f = open("hashMobile.pickle", "wb")
    pickle.dump(hashMovil, f)
    f.close()
    f = open("cornerDistances.pickle", "wb")
    pickle.dump(priorityCorners, f)
    f.close()
    return



"""
Función para crear el mapa. Recibe la dirección del archivo que contiene
las esquinas y las calles. La función cutMap realiza el corte para trabajarla como
listas. Posteriormente la función createGraph se encarga de crear el mapa mediante
lista de adyacencia. 
Adicionalmente, se crean todos los hash a utilizar y la lista vacía que contiene
las distancias de los autos a las esquinas. Finalmente se guardan en sus archivos .pickle
correspondientes.
"""
def createMap(fileDir):
    corners, streets = cutMap(fileDir)
    theMap, esquinas = graph.createGraph(corners, streets)
    hashDirFijas = dictionary.dictionary(len(theMap))
    hashMobile = dictionary.dictionary(len(theMap))
    cornerDistances = [None] * len(theMap)
    f = open("corners.pickle", "wb")
    pickle.dump(corners, f)
    f.close()
    f = open("cornerDistances.pickle", "wb")
    pickle.dump(cornerDistances, f)
    f.close()
    f = open("hashFixedLocations.pickle", "wb")
    pickle.dump(hashDirFijas, f)
    f.close()
    f = open("mapa.pickle", "wb")
    pickle.dump(theMap, f)
    f.close()
    f = open("hashCorners.pickle", "wb")
    pickle.dump(esquinas, f)
    f.close()
    f = open("hashMobile.pickle", "wb")
    pickle.dump(hashMobile, f)
    f.close()
    print("map created successfully")
    return

"""
Función que corta las esquinas y calles del archivo .txt y las transforma de string
a una lista de esquinas y una lista de tuplas de calles, respectivamente.
Se las devuelve a ambas al final, con el nombre corner, street, respectivamente.
"""
def cutMap(fileDir):
    try:
        f = open(fileDir, "r")
    except:
        print("Dirección no válida")
    corner = f.readline()
    streets = f.readline()
    corner = corner.strip("{E=}\n")
    corner = corner.split(",")
    street = []
    cond = False
    cont = 0
    e1 = ""
    e2 = ""
    p = ""
    for i in range(0, len(streets)):
        if streets[i] == ">":
            cond = False
            street.append((e1, e2, float(p)))
            e1 = ""
            e2 = ""
            p = ""
        if cond == True:
            if (streets[i] != ",") and (streets[i] != "{") and (streets[i] != "}"):
                if streets[i] != " ":
                    if cont == 1:
                        e1 = e1 + streets[i]
                    elif cont == 2:
                        e2 = e2 + streets[i]
                    else:
                        p = p + streets[i]
            else:
                cont += 1
        if streets[i] == "<":
            cond = True
            cont = 1
    
    f.close()
    return corner, street

"""
Función que corta una dirección pasada como string. Devuelve una tupla
de la forma (e1, p1, e2, p2). ei son las esquinas y los pi son las distancias
desde el objeto a la esquina ei.
"""
def getDirection(directionStr):
    p1 = ""
    p2 = ""
    e1 = ""
    e2 = ""
    cont = 0
    for i in directionStr:
        if (i != ",") and (i != "<"):
            if (i != " ") and (i != ">"):
                if cont == 1:
                    e1 = e1 + i
                elif cont == 2:
                    p1 = p1 + i
                elif cont == 3:
                    e2 = e2 + i
                else:
                    p2 = p2 + i
        else:
            cont += 1
    return (e1, float(p1), e2, float(p2))

"""
Función que realiza la unión de todas las subfunciones para realizar el viaje en su totalidad.
Recibe el nombre person y la dirección objetivo. Esta última puede estar de la forma "H1" o ser
una dirección normal.
"""
def createTrip(person, direction):  
    f = open("hashFixedLocations.pickle", "rb")
    hashFixed = pickle.load(f)
    f.close()
    
    place = False
    if len(direction) > 9:
        directiontrip = getDirection(direction)
    else:
        place = True
        directionNode = dictionary.search(hashFixed, direction)
        if directionNode == None:
            print("Esta ubicación fija no se encuentra en el mapa.")
            return
        directiontrip = directionNode[2]
        
    f = open("hashMobile.pickle", "rb")
    hashMovil = pickle.load(f)
    f.close()
    
    personNode = dictionary.search(hashMovil, person)
    if personNode == None:
        print("Esta persona no se encuentra en el mapa.")
        return
    
    f = open("mapa.pickle", "rb")
    mapa = pickle.load(f)
    f.close()
    f = open("hashCorners.pickle", "rb")
    hashCorners = pickle.load(f)
    f.close()
    f = open("cornerDistances.pickle", "rb")
    priorityQ = pickle.load(f)
    f.close()
    f = open("corners.pickle", "rb")
    esquinas = pickle.load(f)
    f.close()
    
    graph.shortestPathAux(mapa, hashCorners, personNode, directionNode, directiontrip, place, esquinas)

    ranking = trip.rankingAutos(mapa,hashCorners,priorityQ,personNode)
    
    print("OPCIONES | AUTO | COSTO")
    for i in range(3):
        print(i+1 , ".      |", ranking[i][0], "  |", ranking[i][1])
    print("4 . No realizar viaje")
    print("Monto de dinero de la persona ", personNode[0], ": ", personNode[2])
    print("")
    
    eleccion = int(input("Que opción eliges: "))
    while eleccion not in [1,2,3,4] or eleccion == "":
        eleccion = int(input("Opción invalida, ingrese nuevamente: "))
    
    if eleccion == 1:
        carselected = ranking[0]
    elif eleccion == 2:
        carselected = ranking[1]
    elif eleccion == 3:
        carselected = ranking[2]
    elif eleccion == 4:
        print("Viaje cancelado")
        return
    
    nuevoMonto = personNode[2] - carselected[1]
    newPersonNode = (personNode[0], directiontrip, nuevoMonto)
    hashNewPerson = (personNode[0], newPersonNode)
    
    k = dictionary.hashFunction(hashNewPerson[0], len(hashMovil))
    n = len(hashMovil[k])
    for i in range(0, n):
        if hashNewPerson[0] == hashMovil[k][i][0]:
            hashMovil[k][i] = hashNewPerson
    
    r = dictionary.hashFunction(carselected[0], len(hashMovil))
    n = len(hashMovil[r])
    for j in range(0, n):
        if carselected[0] == hashMovil[r][j][0]:
            carNode = hashMovil[r][j][1]
            newCarNode = (carNode[0], directiontrip, carNode[2])
            hashNewCar = (carNode[0], newCarNode)
            hashMovil[r][j] = hashNewCar
    
    priorityQ = trip.deleteCars(mapa, priorityQ, newCarNode, hashCorners, esquinas)
    print("Viaje realizado.")
    f = open("cornerDistances.pickle", "wb")
    pickle.dump(priorityQ, f)
    f.close()
    f = open("hashMobile.pickle", "wb")
    pickle.dump(hashMovil, f)
    f.close()
    
    return
    
"""
Condicionales para manejar los argumentos pasados por consola.
"""
entrada.pop(0)
if (entrada[0] == "-load_fix_element"):
    entrada.pop(0)
    loadFixElement(entrada)
elif (entrada[0] == "-load_movil_element"):
    entrada.pop(0)
    direction = getDirection(entrada[1])
    element = (entrada[0], direction, float(entrada[2]))
    loadMobileElement(element)
elif (entrada[0] == "-create_trip"):
    entrada.pop(0)
    createTrip(entrada[0], entrada[1])
elif (entrada[0] == "-create_map"):
    entrada.pop(0)
    createMap(entrada[0])
    





