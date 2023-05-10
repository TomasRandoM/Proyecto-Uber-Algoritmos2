#Función para ingresar las calles y esquinas, contenidas como String y pasarlas a lista de esquinas y lista de tuplas, en el caso de las calles.
def start():
    fileDir = str(input(" Ingrese ruta del archivo: "))
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
            if (streets[i] != ",") and (streets[i] != " ") and (streets[i] != ")"):
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
            street.append((e1, e2, int(p)))
            e1 = ""
            e2 = ""
            p = ""
    f.close()
    return corner, street
start()
