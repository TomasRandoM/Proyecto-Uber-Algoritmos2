import math
import dictionary
import queue

class vertex:
    value = None
    dist = None
    nextCorner = None

#Crea grafo dirigido y ponderado representado por lista de adyacencia
"""
Se utiliza listas de Python para crear las listas de adyacencia. Cada elemento de la lista es una tupla (v, d) en el que v es el vértice asignado a cada esquina y
d es la distancia hasta ese vértice (O el valor de la arista). El vértice asignado a cada esquina se guarda en la hashTable, donde se guarda con la key "e1" (ejemplo),
y element = vértice asignado.
Salida = Grafo (Graph) representado mediante lista de adyacencia. Lista hash con las esquinas y sus vértices (hashTable)
"""
def createGraph(list1, list2):
    Graph = []
    m = len(list1)
    if m % 2 == 0:
        m = m + 1
    hashTable = dictionary.dictionary(m)
    n = len(list1)
    for i in range(0, n):
        Graph.append([])
        hashTable = dictionary.insert(hashTable, i, list1[i])

    for i in list2:
        newVertex = vertex()
        newVertex.value = dictionary.search(hashTable, i[1])
        newVertex.dist = i[2]
        newVertex.nextCorner = None
        Graph[dictionary.search(hashTable, i[0])].append(newVertex)
    return Graph, hashTable


#Transforma el valor m a impar en caso de ser par, caso contrario devuelve el mismo número
def sizeModd(m):
    if m % 2 == 0:
        m = m + 1
    return m

"""
dijkstra(Graph, v) recibe el Grafo y un vértice inicial. Devuelve una lista del tamaño de los vértices de la forma:
[p1, p2, p3, p4, p5, p6, ..., pm] donde cada p corresponde a la distancia desde el vértice s hasta el vértice correspondiente a la posición en la lista.
Además devuelve la lista antecesor, la cual tiene el mismo tamaño que la anterior y es de la forma [a1, a2, a3, ..., an] correspondiendo cada a al antecesor
de cada vértice correspondiente a la posición en la lista
"""
def dijkstra(Graph, s):
    visited = []
    distancia = []
    antecesor = []
    for i in range(0, len(Graph)):
        visited.append(0)
        distancia.append(math.inf)
        antecesor.append(None)
    pqueue = queue.PriorityQueue()
    distancia[s] = 0
    pqueue.put((0, s))
    while pqueue.empty() != True:
        element = pqueue.get()
        u = element[1]
        visited[u] = True
        for i in range(0, len(Graph[u])):
            if visited[Graph[u][i].value] == 1:
                continue
            distAux = distancia[u] + Graph[u][i].dist
            if distAux < distancia[Graph[u][i].value]:
                antecesor[Graph[u][i].value] = u
                distancia[Graph[u][i].value] = distAux
                pqueue.put((distAux, Graph[u][i].value))
    return distancia, antecesor

"""
shortestPath utiliza la lista calculada por dijkstra (antecesor) y un vértice s. Devuelve una lista con los vértices que forman
el camino más corto entre s y el vértice utilizado para calcular dijkstra.
"""
def shortestPath(antecesor, s, esquinas):
    shortPath = []
    n = len(esquinas)
    while s != None:
        if s < n:
            shortPath.insert(0, esquinas[s])
        s = antecesor[s]
    return shortPath

"""
Función auxiliar que verifica el sentido de la calle para mostrar correctamente el camino más corto hacia la ubicación objetivo desde la persona.
"""
def shortestPathAux(hashCorners, personNode, directionNode, directiontrip, place):
    e1 = dictionary.search(hashCorners, personNode[1][0])
    e2 = dictionary.search(hashCorners, personNode[1][2])
    status = sentidoCalle(map, e1, e2)
    if status == 1:
        distancia, ancestros = dijkstra(map, e2)
    elif status == 2:
        distancia, ancestros = dijkstra(map, e1)
    else:
        distancia, ancestros = dijkstra(map, e1)
        distancia2, ancestros2 = dijkstra(map, e2)

    print("El camino más corto es:")
    if place == True:
        if status != 3:
            print(shortestPath(ancestros, directionNode[1]))
        else:
            if distancia[directionNode[1]] <= distancia2[directionNode[1]]:
                print(shortestPath(ancestros, directionNode[1]))
            else:
                print(shortestPath(ancestros2, directionNode[1]))
    else:
        e1 = dictionary.search(hashCorners, directiontrip[0])
        e2 = dictionary.search(hashCorners, directiontrip[2])
        status2 = sentidoCalle(map, directiontrip[0], directiontrip[2])
        if status2 != 3:
            if status2 == 2:
                e1 = e2
            if status != 3:
                print(shortestPath(ancestros, e1))
            else:
                if distancia[e1] <= distancia2[e1]:
                    print(shortestPath(ancestros, e1))
                else:
                    print(shortestPath(ancestros2, e1))
        else:
            if status != 3:
                if distancia[e1] <= distancia[e2]:
                    print(shortestPath(ancestros, e1))
                else:
                    print(shortestPath(ancestros, e2))
            else:
                if distancia[e1] <= distancia2[e1]:
                    dist1 = (distancia[e1], 1, e1) 
                else: 
                    dist1 = (distancia2[e1], 2, e1)
                if distancia[e2] <= distancia2[e2]:
                    dist2 = (distancia[e2], 1, e2)
                else:
                    dist2 = (distancia2[e2], 2, e2)
                if dist1[0] <= dist2[0]:
                    definitivo = dist1
                else:
                    definitivo = dist2
                if definitivo[1] == 1:
                    print(shortestPath(ancestros, definitivo[2]))
                else:
                    print(shortestPath(ancestros2, definitivo[2]))
    ancestros.clear()
    distancia.clear()
    return
"""
Función que inserta una ubicación FIJA en el grafo. Recibe el Grafo, la hashTable correspondiente a las ubicaciones fijas, la hashtable correspondiente
a las esquinas y la variable ad que es la dirección de la ubicación fija que viene dada de la forma <nombre, {<e1, p>, <e2, p2>}. Devuelve el grafo
con el vértice insertado.
"""
def insert(Graph, hashTable, esquinas, ad):
    direc = (ad[0], len(Graph), ad[1])
    e1 = ad[1][0]
    e2 = ad[1][2]
    dictionary.insert(hashTable, direc, direc[0])
    e1 = dictionary.search(esquinas, e1)
    e2 = dictionary.search(esquinas, e2)
    newVertex = vertex()
    newVertex.value = direc[1]
    list1 = Graph[e1]
    Graph.append([])
    status = 0
    for i in list1:
        if (i.value == e2) or (i.nextCorner == e2):
            status = 1
            newVertex.nextCorner = e2
            break
    list1 = Graph[e2]
    for i in list1:
        if (i.value == e1) or (i.nextCorner == e1):
            if status == 1:
                status = 2
                newVertex2 = vertex()
                newVertex2.value = newVertex.value
                newVertex2.nextCorner = e1
            else:
                status = 4
                newVertex.nextCorner = e1
            break
    if status == 1:
        Graph = recorrerArista(Graph, direc, newVertex, e1, e2, e1, 1, 1)
    elif status == 4:
        Graph = recorrerArista(Graph, direc, newVertex, e2, e1, e2, 2, 1)
    elif status == 2:
        Graph = recorrerArista(Graph, direc, newVertex, e1, e2, e1, 1, 1)
        Graph = recorrerArista(Graph, direc, newVertex2, e2, e1, e2, 2, 1)
    return Graph

#Función recursiva auxiliar de insert
def recorrerArista(Graph, direc, newVertex, e1, e2, nextVertex, status, first):
    list1 = Graph[nextVertex]
    k = len(Graph) - 1
    if first != 0:
        if status == 1:
            newVertex.dist = direc[2][1]
        elif status == 2:
            newVertex.dist = direc[2][3]
    for i in range (len(list1)):
        if list1[i].value == e2:
            vertex = Graph[nextVertex].pop(i)
            if status == 2:
                vertex.dist = direc[2][1]
            else:
                vertex.dist = direc[2][3]
            Graph[nextVertex].insert(0, newVertex)
            Graph[k].append(vertex)
            return Graph
        if list1[i].nextCorner == e2:
            if list1[i].dist < newVertex.dist:
                newVertex.dist = newVertex.dist - list1[i].dist
                return recorrerArista(Graph, direc, newVertex, e1, e2, list1[i].value, status, 0)
            else:
                vertex = Graph[nextVertex].pop(i)
                if status == 2:
                    vertex.dist = abs(vertex.dist - direc[2][1])
                else:
                    vertex.dist = abs(vertex.dist - direc[2][3])
                Graph[nextVertex].insert(0, newVertex)
                Graph[k].append(vertex)
                return Graph
            

"""
Función que verifica el sentido de la calle. Devuelve 1 si la calle es del sentido (e1, e2), devuelve 2 si es
(e2, e1) y devuelve 3 si es de doble sentido
"""
def sentidoCalle(Graph, e1, e2):
    list1 = Graph[e1]
    status = 0
    for i in list1:
        if (i.value == e2) or (i.nextCorner == e2):
            status = 1
            break
    list1 = Graph[e2]
    for i in list1:
        if (i.value == e1) or (i.nextCorner == e1):
            if status == 1:
                status = 3
            else:
                status = 2
            break
    return status