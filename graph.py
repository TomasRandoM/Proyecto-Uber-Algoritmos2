from algo1 import * 

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
        element = (i[1], i[2])
        Graph[i[0]].append(element)
    return Graph

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