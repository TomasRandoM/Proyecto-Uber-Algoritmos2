import math

"""
Función que retorna el valor de la key al ser pasada por la función hash aquí definida. Se multiplica cada valor por 10 elevado a un entero.
En el caso de las letras, se multiplica su código ASCII. Luego, se pasa el resultado por el método de la multiplicación y se devuelve el módulo de
ese valor.
O(1) al ser constante la longitud de las key pasadas.
Salida: Nueva key
"""
def hashFunction(x, m):
    n = len(x)
    hashValue = 0
    for i in range(0, n):
        if i == 0:
            hashValue = hashValue + ord(x[i]) * (10**n)
        else:
            hashValue = hashValue + int(x[i]) * (10 ** (n-i))
    A = (math.sqrt(5) - 1) / 2
    return int((m * ((hashValue * A) % 1))) % m

"""
Función que crea una hash table y la devuelve. La longitud de la hash será de n.
Salida: Hash table de tamaño (len(x) * 2) + 1
"""
def dictionary(n):
    hashTable = []
    for i in range(0, n):
        hashTable.append([])
        hashTable[i] = []
    return hashTable

"""
Inserta en la hash (Dictionary) un elemento junto a su key. La key se pasa por la función hash para obtener "k". Luego, en la hash table, en la posición
k se coloca una tupla con el formato (key, element).
Salida: La hash table (Dictionary) con el elemento y la key agregados.
"""
def insert(Dictionary, element, key):
    k = hashFunction(key, len(Dictionary))
    Dictionary[k].append((key, element))
    return Dictionary

"""
Busca en una hash table (Dictionary) una key específica, la cual es pasada por la función hash. En el caso de haber coincidencias, se retorna el campo [1] de la tupla,
la cual corresponde a "element". Caso contrario se retorna None.
Salida: Si existe, el campo "element" de la tupla agregada. Si no, "None".
"""
def search(Dictionary, key):
    k = hashFunction(key, len(Dictionary))
    n = len(Dictionary[k])
    for i in range(0, n):
        if key == Dictionary[k][i][0]:
            return Dictionary[k][i][1]
    return None