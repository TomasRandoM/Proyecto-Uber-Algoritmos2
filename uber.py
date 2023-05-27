import graph
"""
Función para ingresar las calles y esquinas, contenidas como String y pasarlas a lista de esquinas y lista de tuplas, en el caso de las calles.
En las listas resultantes quedan las esquinas y distancias (distancias como float)
Salida: Lista corner que contiene a las esquinas de la forma [e0, e1, e2, e3, e4] y lista street que contiene a las calles de la forma
[(esquina1, esquina2, distancia)] por ejemplo [(e0, e1, 2.0), (e0, e4, 22.0)]
"""
def start():
    fileDir = str(input("Ingrese ruta del archivo: "))
    try:
        f = open(fileDir, "r")
    except:
        start()
    corner = f.readline()
    streets = f.readline()
    corner = corner.strip("[]\n")
    corner = corner.split(", ")
    street = []
    cond = False
    cont = 0
    e1 = ""
    e2 = ""
    p = ""
    for i in range(0, len(streets)):
        if cond == True:
            if (streets[i] != ",") and (streets[i] != ")"):
                if streets[i] != " ":
                    if cont == 1:
                        e1 = e1 + streets[i]
                    elif cont == 2:
                        e2 = e2 + streets[i]
                    else:
                        p = p + streets[i]
            else:
                cont += 1
        if streets[i] == "(":
            cond = True
            cont = 1
        if streets[i] == ")":
            cond = False
            street.append((e1, e2, float(p)))
            e1 = ""
            e2 = ""
            p = ""
    f.close()
    return corner, street

"""
Función que inicia el funcionamiento del programa. Llama a la función start para reunir las dos listas que contienen esquinas y calles. Luego, llama
a createGraph (del módulo graph.py) y guarda el mapa en "theMap", representado como un grafo conexo y dirigido mediante listas de adyacencia.
"""
def createMap():
    corner, street = start()
    theMap, hashTable = graph.createGraph(corner, street)
    #Prueba theMap (Luego borrar)
    for i in range(0, len(theMap)):
        auxList = theMap[i]
        for j in range(0, len(auxList)):
            print((auxList[j].value, auxList[j].dist), end= " ")
        print(" ")
    #Prueba dijkstra (Luego borrar)
    vector = graph.dijkstra(theMap, 0)
    for i in range(0, len(vector)):
        print((vector[i].value, vector[i].d), end=" ")
createMap()