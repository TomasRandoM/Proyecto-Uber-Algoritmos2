import math
class vertex:
    value = None
    dist = None

#Crea grafo dirigido y ponderado representado por lista de adyacencia
"""
Se utiliza listas de Python para crear las listas de adyacencia. Cada elemento de la lista es una tupla (v, d) en el que v es el vértice y
d es la distancia hasta ese vértice (O el valor de la arista)
"""
def createGraph(list1, list2):
    Graph = []
    n = len(list1)
    for i in range(0, n):
        Graph.append([])

    for i in list2:
        newVertex = vertex()
        newVertex.value = i[1]
        newVertex.dist = i[2]
        Graph[i[0]].append(newVertex)
    return Graph

"""
dijkstra(Graph, v) recibe el Grafo y un vértice inicial. Devuelve una lista del tamaño de los vértices de la forma:
[v1, v2, v3, v4, v5, v6, ..., m] donde cada vX tiene atributos "value", "d" y "pi".
value contiene el número de vértice, d la menor distancia hasta el vértice inicial y pi el ancestro de cada vértice. 
"""
#Clase para contener el ancestro, la menor distancia y el valor de cada vértice
class dijVertex:
    value = None
    d = math.inf
    pi = None

#Inicializa la lista "vertices" con todos los vértices. Coloca distancia del primer vértice en 0
def initRelax(G, vertices, s):
    for i in range(len(G)):
        v = dijVertex()
        v.value = i
        vertices.append(v)
    vertices[s].d = 0
    vertices[s].pi = s
    return vertices

#Función que "relaja" cada vértice. Si la distancia del vértice objetivo es
#mayor a la suma de la distancia del vértice actual + el valor de la arista, entonces
#cambia el valor de la distancia del vértice objetivo por el nuevo valor.
def relax(Graph, Q, vertices, u, vertice):
    if vertices[vertice.value].d > vertices[u].d + vertice.dist:
        vertices[vertice.value].d = vertices[u].d + vertice.dist
        aux = vertices[u].d + vertice.dist
        vertices[vertice.value].pi = u
        for i in range(len(Q)):
            if Q[i][0] == vertice.value:
                aux2 = i
        #Elimina de Q el vértice objetivo
        Q.pop(aux2)
        #Lo vuelve a agregar, pero con distancia actualizada y en la posición correcta (en términos de distancia)
        if len(Q) == 0:
            Q.insert(0, (vertice.value, vertices[u].d + vertice.dist))
        else:
            for i in range(len(Q)):
                if aux <= Q[i][1]:
                    Q.insert(i, (vertice.value, vertices[u].d + vertice.dist))
                    break
    return vertices, Q

def dijkstra(Graph, s):
    vertices = []
    vertices = initRelax(Graph, vertices, s)
    S = []
    Q = []
    #Inicializa una lista PriorityQueue con todos los vértices y su distancia.
    #Todas las distancias inicializadas en infinito, excepto el vértice inicial, que es 0.
    Q.append((s, 0))
    for i in range(1, len(Graph)):
        if i != s:
            Q.append((i, math.inf))
    while len(Q) > 0:
        u = Q.pop(0)
        S.append(u)
        #Extrae el primer vértice en la lista de prioridad y "relaja" todos sus vértices vecinos.
        for i in range(0, len(Graph[u[0]])):
            condition = False
            if Graph[u[0]][i].value not in S:
                condition = True
            if condition == True:
                vertices, Q = relax(Graph, Q, vertices, u[0], Graph[u[0]][i])
    return vertices



"""
FUNCIONES DE REPUESTO
def createGraph(list1, list2):
    Graph = []
    n = len(list1)
    for i in range(0, n):
        Graph.append([])

    for i in list2:
        element = (i[1], i[2])
        Graph[i[0]].append(element)
    return Graph

def createGraph(list1, list2):
    Graph = []
    n = len(list1)
    for i in range(0, n):
        Graph.append([])

    for i in list2:
        newVertex = vertex()
        newVertex.value = i[1]
        newVertex.dist = i[2]
        Graph[i[0]].append(newVertex)
    return Graph


def createGraph(list1, list2):
    Graph = Array(len(list1), [])

    for i in range (0, len(list1)):
        Graph[i] = []

    for i in list2:
        newVertex = vertex()
        newVertex.value = i[1]
        newVertex.dist = i[2]
        Graph[i[0]].append(newVertex)
    return Graph
"""