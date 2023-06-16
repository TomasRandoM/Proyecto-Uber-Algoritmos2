import dictionary
import graph

"""
Inserta el auto en una hashtable (carHashTable) donde van las personas y los autos. Luego, hace un dijkstra desde las esquinas
cercanas (si la calle es de doble mano) o solo desde donde puede ir. Luego, ubica las distancias en una lista
auxiliar (priorityCorners) en la que cada posición representa una esquina (su vértice asociado). Y cada posición
contiene una priorityQueue con las distancias de los autos hasta esa esquina de la forma (p, C) en la que p es el
precio total (sacado con la fórmula la cual incluye distancia y precio) y C el auto en cuestión. Además, la función
recibe el parámetro "esquinas" que es la lista de esquinas.
El parámetro auto viene dado de la forma (nombre, (e1, p1, e2, p2), coste)
"""

def insertCar(Graph, carHashTable, priorityCorners, cornerHashTable, auto, esquinas):
    dictionary.insert(carHashTable, auto, auto[0])
    e1 = dictionary.search(cornerHashTable, auto[1][0])
    e2 = dictionary.search(cornerHashTable, auto[1][2])
    status = graph.sentidoCalle(Graph, e1, e2)
    if status == 1:
        esquinas[e1].append((e2, auto))
        distancias, antecesores = graph.dijkstra(Graph, e2)
        car = (auto[0], auto[1][3], auto[2])
        insertPriortyCorners(car, priorityCorners, distancias, None, esquinas, auto, cornerHashTable)
    elif status == 2:
        esquinas[e2].append((e1, auto))
        distancias, antecesores = graph.dijkstra(Graph, e1)
        car = (auto[0], auto[1][1], auto[2])
        insertPriortyCorners(car, priorityCorners, distancias, None, esquinas, auto, cornerHashTable)
    else:
        esquinas[e1].append((e2, auto))
        esquinas[e2].append((e1, auto))
        distancias, antecesores = graph.dijkstra(Graph, e2)
        distancias2, antecesores2 = graph.dijkstra(Graph, e1)
        car = (auto[0], auto[1][3], auto[1][1], auto[2])
        insertPriortyCorners(car, priorityCorners, distancias, distancias2, esquinas, auto, cornerHashTable)
    return carHashTable

"""
Función auxiliar que inserta las distancias calculadas por dijkstra del auto a cada esquina en la estructura
auxiliar "priorityCorners". Utiliza una priorityQueue e inserta en cada espacio el elemento de la forma
(precio, nombreAuto) siendo precio el precio calculado utilizando distancia y coste del auto y nombreAuto el nombre del vehículo.
"""
def insertPriortyCorners(auto, priorityCorners, distancias1, distancias2, esquinas, car, esquinasHash):
    if car[1][1] == 0:
        e1 = dictionary.search(esquinasHash, car[1][0])
    elif car[1][3] == 0:
        e1 = dictionary.search(esquinasHash, car[1][2])
    else:
        e1 = None
    if distancias2 == None:
        for i in range(0, len(esquinas)):
            if e1 != None:
                if e1 == i:
                    price = auto[2] / 4
                    priorityCorners[i] = insertWithPriority(priorityCorners[i], (price, auto[0]))
                    e1 = None
                    continue
            if priorityCorners[i] == None:
                priorityCorners[i] = []
            price = (distancias1[i] + auto[1] + auto[2]) / 4
            priorityCorners[i] = insertWithPriority(priorityCorners[i], (price, auto[0]))
    else:
        for i in range(0, len(esquinas)):
            if priorityCorners[i] == None:
                priorityCorners[i] = []
            if e1 != None:
                if e1 == i:
                    price = auto[3] / 4
                    priorityCorners[i] = insertWithPriority(priorityCorners[i], (price, auto[0]))
                    e1 = None
                    continue
            if distancias1[i] <= distancias2[i]:
                price = (distancias1[i] + auto[1] + auto[3]) / 4
                priorityCorners[i] = insertWithPriority(priorityCorners[i], (price, auto[0]))
            else:
                price = (distancias2[i] + auto[2] + auto[3]) / 4
                priorityCorners[i] = insertWithPriority(priorityCorners[i], (price, auto[0]))
    return priorityCorners

def insertWithPriority(list1, element):
    if list1 == []:
        list1.append(element)
        return list1
    for i in range(0, len(list1)):
        if list1[i][0] >= element[0]:
            list1.insert(i, element)
            break
        if i == len(list1) - 1:
            list1.append(element)
    return list1

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
def rankingAutos(Graph, cornerHash, priorityCorners, people, corners):
    e1 = dictionary.search(cornerHash, people[1][0])
    e2 = dictionary.search(cornerHash, people[1][2])
    status = graph.sentidoCalle(Graph, e1, e2)
    if status == 1:
        person = (people[2], people[1][1])
        cars = extractCars(priorityCorners, person, e1, None, corners, e2)
    elif status == 2:
        person = (people[2], people[1][3])
        cars = extractCars(priorityCorners, person, e2, None, corners, e1)
    else:
        person = (people[2], people[1][1], people[1][3])
        cars = extractCars(priorityCorners, person, e1, e2, corners, None)
    return cars

"""
Función auxiliar que devuelve la lista con los 3 autos más cercanos.
"""
def extractCars(priorityCorners, people, vertice, vertice2, corners, enext):
    newList = []
    if vertice2 == None:
        if priorityCorners[vertice] == None:
            return newList
        m = len(priorityCorners[vertice])
        if m >= 3:
            m = 3
        for i in range(0, m):
            car = priorityCorners[vertice][i]
            carAux = (car[1], car[0] + (people[1] / 4))
            price = car[0] + (people[1] / 4)
            if price > people[0]:
                break
            newList.append(carAux)
        m = len(corners[vertice])
        if m > 1:
            for i in range(1, m):
                if (corners[vertice][i][0] == enext):
                    aux = corners[vertice][i][1]
                    if corners[vertice][0] == aux[1][0]:
                        dist = aux[1][1]
                    else:
                        dist = aux[1][3]
                    if dist <= people[1]:
                        price = ((people[1] - dist) + aux[2]) / 4
                    n = len(newList)
                    if n == 0:
                        if (people[0] >= price):
                            newList.append((aux[0], price))
                    else:
                        if price <= newList[n-1][1]:
                            insertWithPriorityAux(newList, (aux[0], price))
        return newList
    else:
        auxList = []
        cont = 0
        while cont != 3:
            if priorityCorners[vertice] == [] and priorityCorners[vertice2] == []:
                break
            elif priorityCorners[vertice] == [] and priorityCorners[vertice2] != []:
                car2 = priorityCorners[vertice2].pop(0)
                dist2 = car2[0] +  (people[2] / 4)
                if dist2 > people[0]:
                    break
                carAux = (car2[1], car2[0] +  (people[2] / 4))
                auxList.append((vertice2, car2))
                condition = checkReplace(newList, carAux)
                if condition == True:
                    cont += 1
            elif priorityCorners[vertice] != [] and priorityCorners[vertice2] == []:
                car1 = priorityCorners[vertice].pop(0)
                dist1 = car1[0] +  (people[1] / 4)
                if dist2 > people[0]:
                    break
                carAux = (car1[1], car1[0] +  (people[1] / 4))
                auxList.append((vertice, car1))
                condition = checkReplace(newList, carAux)
                if condition == True:
                    cont += 1
            else:
                car1 = priorityCorners[vertice].pop(0)
                car2 = priorityCorners[vertice2].pop(0)
                dist1 = car1[0] +  (people[1] / 4)
                dist2 = car2[0] +  (people[2] / 4)
                check1 = checkExists(newList, car1)
                check2 = checkExists(newList, car2)
                if (check1 == True) and (check2 == True):
                    auxList.append((vertice, car1))
                    auxList.append((vertice2, car2))
                elif (check1 == True) and (check2 == False):
                    if dist2 > people[0]:
                        break
                    carAux = (car2[1], car2[0] +  (people[2] / 4))
                    auxList.append((vertice2, car2))
                    condition = checkReplace(newList, carAux)
                    if condition == True:
                        cont += 1
                    if car1[1] != car2[1]:
                        priorityCorners[vertice] = insertWithPriority(priorityCorners[vertice], car1)
                    else:
                        auxList.append((vertice, car1))
                elif (check1 == False) and (check2 == True):
                    if dist1 > people[0]:
                        break
                    carAux = (car1[1], car1[0] +  (people[1] / 4))
                    auxList.append((vertice, car1))
                    condition = checkReplace(newList, carAux)
                    if car1[1] != car2[1]:
                        priorityCorners[vertice2] = insertWithPriority(priorityCorners[vertice2], car2)
                    else:
                        auxList.append((vertice2, car2))
                    if condition == True:
                        cont += 1
                else:
                    if dist1 <= dist2:
                        if dist1 > people[0]:
                            break
                        carAux = (car1[1], car1[0] +  (people[1] / 4))
                        auxList.append((vertice, car1))
                        condition = checkReplace(newList, carAux)
                        if car1[1] != car2[1]:
                            priorityCorners[vertice2] = insertWithPriority(priorityCorners[vertice2], car2)
                        else:
                            auxList.append((vertice2, car2))
                        if condition == True:
                            cont += 1
                    else:
                        if dist2 > people[0]:
                            break
                        carAux = (car2[1], car2[0] +  (people[2] / 4))
                        auxList.append((vertice2, car2))
                        condition = checkReplace(newList, carAux)
                        if car1[1] != car2[1]:
                            priorityCorners[vertice] = insertWithPriority(priorityCorners[vertice], car1)
                        else:
                            auxList.append((vertice, car1))
                        if condition == True:
                            cont += 1
        for i in range(0, len(auxList)):
            priorityCorners[auxList[i][0]] = insertWithPriority(priorityCorners[auxList[i][0]], auxList[i][1])
        m = len(corners[vertice])
        for i in range(1, m):
            if (corners[vertice][i][0] == vertice2):
                aux = corners[vertice][i][1]
                if corners[vertice][0] == aux[1][0]:
                    dist = aux[1][1]
                else:
                    dist = aux[1][3]
                price = (abs((people[1] - dist)) + aux[2]) / 4
                n = len(newList)
                if n == 0:
                    if (people[0] >= price):
                        newList.append((aux[0], price))
                else:
                    if price <= newList[n-1][1]:
                        insertWithPriorityAux(newList, (aux[0], price))
    return newList

def checkExists(list1, element):
    if list1 == []:
        return False
    for i in range(0, len(list1)):
        if list1[i][0] == element[1]:
            return True
    return False
"""
Función auxiliar para verificar que un elemento esté en la lista o no. En el caso de estar, verificar que sea posible su
reemplazo. Se devuelve la lista modificada.
"""
def checkReplace(list1, element):
    if len(list1) == 0:
        list1.append(element)
        return True
    else:
        m = len(list1)
        for i in range(0, m):
            if list1[i][0] == element[0]:
                if list1[i][1] > element[1]:
                    list1.pop(i)
                    list1.insert(i, element)
                    return True
                return False
        list1.append(element)
    return False

"""
Función que elimina un auto dado de la lista de prioridad de distancias a cada esquina desde cada auto.
Luego, calcula la nueva distancia más corta y las vuelve a insertar en la lista de prioridad.
"""
def deleteCars(Graph, priorityCorners, car, oldcar, cornerHashTable, esquinas):
    n = len(priorityCorners)
    for i in range (0, n):
        m = len(priorityCorners[i])
        for j in range(0, m):
            if priorityCorners[i][j][1] == car[0]:
                priorityCorners[i].pop(j)
                break
    e1 = dictionary.search(cornerHashTable, car[1][0])
    e2 = dictionary.search(cornerHashTable, car[1][2])
    status = graph.sentidoCalle(Graph, e1, e2)
    
    if status == 1:
        vertice = e1
        carAux = (e2, (car))
        esquinas[e1].append(carAux)
        distancias, antecesores = graph.dijkstra(Graph, e2)
        carNew = (car[0], car[1][3], car[2])
        insertPriortyCorners(carNew, priorityCorners, distancias, None, esquinas, car, cornerHashTable)
    elif status == 2:
        vertice = e2
        carAux = (e1, (car))
        esquinas[e2].append(carAux)
        distancias, antecesores = graph.dijkstra(Graph, e1)
        carNew = (car[0], car[1][1], car[2])
        insertPriortyCorners(carNew, priorityCorners, distancias, None, esquinas, car, cornerHashTable)
    else:
        carAux = (e2, (car))
        esquinas[e1].append(carAux)
        carAux = (e1, (car))
        esquinas[e2].append(carAux)
        distancias, antecesores = graph.dijkstra(Graph, e2)
        distancias2, antecesores2 = graph.dijkstra(Graph, e1)
        carNew = (car[0], car[1][3], car[1][1], car[2])
        insertPriortyCorners(carNew, priorityCorners, distancias, distancias2, esquinas, car, cornerHashTable)
        antecesores2.clear()
    antecesores.clear()
    e3 = dictionary.search(cornerHashTable, oldcar[1][0])
    e4 = dictionary.search(cornerHashTable, oldcar[1][2])
    status = graph.sentidoCalle(Graph, e3, e4)
    if status == 1:
        vertice = e3
    elif status == 2:
        vertice = e4
    if status != 3:
        for i in range(1, len(esquinas[vertice])):
            if esquinas[vertice][i][1][0] == oldcar[0]:
                esquinas[vertice].pop(i)
                break
    else:
        for i in range(1, len(esquinas[e3])):
                if esquinas[e3][i][1][0] == oldcar[0]:
                    esquinas[e3].pop(i)
                    break
        for i in range(1, len(esquinas[e4])):
                if esquinas[e4][i][1][0] == oldcar[0]:
                    esquinas[e4].pop(i)
                    break
    return priorityCorners

"""Función auxiliar para extractCars. Inserta con prioridad en la lista resultante. Element viene dado
de la forma (car, precio)"""
def insertWithPriorityAux(list1, element):
    for i in range(0, len(list1)):
        if list1[i][0] == element[0]:
            if list1[i][1] > element[1]:
                list1.pop(i)
                break
            else:
                return list1
    if len(list1) == 3:
        complete = True
    else:
        complete = False
    for i in range(0, len(list1)):
        if list1[i][1] > element[1]:
            if complete == True:
                list1.pop(len(list1) - 1)
            list1.insert(i, element)
            return list1
    if len(list1) < 3:
        list1.append(element)
    return list1