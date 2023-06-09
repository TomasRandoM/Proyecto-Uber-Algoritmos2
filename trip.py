import dictionary
import graph
import queue
"""
Inserta el auto en una hashtable (carHashTable) donde van las personas y los autos. Luego, hace un dijkstra desde las esquinas
cercanas (si la calle es de doble mano) o solo desde donde puede ir. Luego, ubica las distancias en una lista
auxiliar (priorityCorners) en la que cada posición representa una esquina (su vértice asociado). Y cada posición
contiene una priorityQueue con las distancias de los autos hasta esa esquina de la forma (p, C) en la que p es el
precio total (sacado con la fórmula la cual incluye distancia y precio) y C el auto en cuestión.

El parámetro auto viene dado de la forma (nombre, (e1, p1, e2, p2), coste)
"""

def insertCar(Graph, carHashTable, priorityCorners, cornerHashTable, auto):
    dictionary.insert(carHashTable, auto, auto[0])
    e1 = dictionary.search(cornerHashTable, auto[1][0])
    e2 = dictionary.search(cornerHashTable, auto[1][2])
    status = graph.sentidoCalle(e1, e2)
    if status == 1:
        distancias, antecesores = graph.dijkstra(Graph, e2)
        car = (auto[0], auto[1][3], auto[2])
        insertPriortyCorners(car, priorityCorners, distancias, None)
    elif status == 2:
        distancias, antecesores = graph.dijkstra(Graph, e1)
        car = (auto[0], auto[1][1], auto[2])
        insertPriortyCorners(car, priorityCorners, distancias, None)
    else:
        distancias, antecesores = graph.dijkstra(Graph, e2)
        distancias2, antecesores2 = graph.dijkstra(Graph, e1)
        car = (auto[0], auto[1][3], auto[1][1], auto[2])
        insertPriortyCorners(car, priorityCorners, distancias, distancias2)
    return carHashTable

"""
Función auxiliar que inserta las distancias calculadas por dijkstra del auto a cada esquina en la estructura
auxiliar "priorityCorners". Utiliza una priorityQueue e inserta en cada espacio el elemento de la forma
(precio, nombreAuto) siendo precio el precio calculado utilizando distancia y coste del auto y nombreAuto el nombre del vehículo.
"""
def insertPriortyCorners(auto, priorityCorners, distancias1, distancias2):
    if distancias2 == None:
        for i in range(0, distancias1):
            if priorityCorners[i] == None:
                newQueue = queue.PriorityQueue()
                priorityCorners[i] = newQueue
            price = (distancias1[i] + auto[1] + auto[2]) / 4
            priorityCorners[i].put((price, auto[0]))
    else:
        for i in range(0, distancias1):
            if priorityCorners[i] == None:
                newQueue = queue.PriorityQueue()
                priorityCorners[i] = newQueue
            if distancias1[i] <= distancias2[i]:
                price = (distancias1[i] + auto[1] + auto[3]) / 4
                priorityCorners[i].put((price, auto[0]))
            else:
                price = (distancias2[i] + auto[2] + auto[3]) / 4
                priorityCorners[i].put((price, auto[0]))
    return priorityCorners

"""
Inserta una persona en el hash de personas y autos (peopleHashTable), people viene dado de la forma
(nombre, (e1, p1, e2, p2), monto). Siendo la posición 0 el nombre, la posición 1 la dirección y la 2 el monto
disponible para viajar
"""
def insertPeople(peopleHashTable, people):
    peopleHashTable = dictionary.insert(peopleHashTable, people, people[0])
    return peopleHashTable

"""
Función que crea el ranking de los 3 autos más cercanos a la persona. Se recibe la hash de las esquinas (cornerHash), 
la lista (priorityCorners) con las priorityQueue de cada esquina y la persona (people) que es de la forma
(nombre, (e1, p1, e2, p2), monto). 
Devuelve una lista con los 3 autos más cercanos de la forma:
[(c1, precio), (c2, precio), (c3, precio)] siedo ci cada auto y precio el valor total a ser abonado.
"""
def rankingAutos(cornerHash, priorityCorners, people):
    e1 = dictionary.search(cornerHash, people[1][0])
    e2 = dictionary.search(cornerHash, people[1][2])
    status = graph.sentidoCalle(e1, e2)
    if status == 1:
        person = (people[1][1])
        cars = extractCars(priorityCorners, person, e1, None)
    elif status == 2:
        person = (people[1][3])
        cars = extractCars(priorityCorners, person, e2, None)
    else:
        person = (people[1][1], people[1][3])
        cars = extractCars(priorityCorners, person, e1, e2)
    return cars

"""
Función auxiliar que devuelve la lista con los 3 autos más cercanos.
"""
def extractCars(priorityCorners, people, vertice, vertice2):
    newList = []
    if vertice2 == None:
        for i in range(0, 3):
            car = priorityCorners[vertice].get()
            carAux = (car[1], car[0] + (people[0] / 4))
            newList.append()
    else:
        for i in range(0, 3):
            car1 = priorityCorners[vertice].get()
            car2 = priorityCorners[vertice2].get()
            if car1 <= car2:
                carAux = (car[1], car[0] +  (people[0] / 4))
                newList.append(carAux)
                priorityCorners[vertice2].put(car2)
            else:
                carAux = (car[1], car[0] +  (people[1] / 4))
                newList.append(carAux)
                priorityCorners[vertice].put(car1)
    return newList
