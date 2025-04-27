def crear_tablero():
    matriz = []
    for i in range(8):
        matriz.append([])
        for j in range(8):
            matriz[i].append(".")
    return matriz

def posicion_inicial(tablero):
    for i in range(8):
        for j in range(8):
            if i == 0:
                if j == 0 or j == 7:
                    tablero[i][j] = "tN"
                elif j == 1 or j == 6:
                    tablero[i][j] = "cN"
                elif j == 2 or j == 5:
                    tablero[i][j] = "aN"
                elif j == 3:
                    tablero[i][j] = "dN"
                else:
                    tablero[i][j] = "rN"
                    
            elif i == 1:
                tablero[i][j] = "pN"
                
            elif i == 6:
                tablero[i][j] = "pB"
            
            elif i == 7:
                if j == 0 or j == 7:
                    tablero[i][j] = "tB"
                elif j == 1 or j == 6:
                    tablero[i][j] = "cB"
                elif j == 2 or j == 5:
                    tablero[i][j] = "aB"
                elif j == 3:
                    tablero[i][j] = "dB"
                else:
                    tablero[i][j] = "rB"
    return tablero

def mostrar_tablero(tablero):
    for filas in tablero:
        for ubicaciones in filas:
            print(f"{ubicaciones:4}", end="")
        print()
    print()
        
def pieza_a_mover(letra):                      # Valida si la pieza a mover está dentro de los parametros del tablero y el formato,
    piezas_posibles = ["T", "C", "A", "D", "R", "P"]    # pero no corroborra si realmente está en esa posición.
    while True:
        pos_pieza = input("Ingrese la inicial y la posición de la pieza que quiere mover (ejemplo: Cb1): ")
        if len(pos_pieza) != 3:
            print("Error: La longitud de la entrada debe ser 3.")
        elif pos_pieza[0].upper() not in piezas_posibles:
            print("Error: Inicial de pieza inválida.")
        elif pos_pieza[1].lower() not in letra:
            print("Error: Columna inválida.")
        elif not pos_pieza[2].isdigit() or int(pos_pieza[2]) < 1 or int(pos_pieza[2]) > 8:
            print("Error: Fila inválida.")
        else:
            return pos_pieza

def corroborrar_pos_pieza_a_mover(letra, turno, posicion_pieza, tablero):
    pieza = posicion_pieza[:1].lower() + turno[:1].upper()        
    columna = posicion_pieza[1:2].lower()                         
    fila = int(posicion_pieza[2:])                                 
    if pieza == tablero[8 - fila][letra[columna]]:
        return
    else:
        print("La pieza ingresada no se encuentra en esa posición")
        pieza_a_mover(letra)
        
def como_mueve_rey():
    pass

def como_mueve_peon():
    pass

def como_mueve_torre():
    pass

def como_mueve_alfil():
    pass

def como_mueve_dama():
    pass

def como_mueve_caballo():
    pass

def posibles_movimientos(posicion_pieza, tablero):     # Deriva a la función correspondiente según la pieza a mover.
    if posicion_pieza[0].upper() == "P":
        return mov_peon(posicion_pieza, tablero)
    elif posicion_pieza[0].upper() == "C":
        return mov_caballo(posicion_pieza, tablero)
    elif posicion_pieza[0].upper() == "A":
        return mov_alfil(posicion_pieza, tablero)
    elif posicion_pieza[0].upper() == "D":
        return mov_dama(posicion_pieza, tablero)
    elif posicion_pieza[0].upper() == "T":
        return mov_torre(posicion_pieza, tablero)
    else:
        return mov_rey(posicion_pieza, tablero)

def coordenadas_a_mover(letra):
    while True:
        movimiento = input("Ingrese la casilla a la que quiere mover (ejemplo: e5): ")
        if len(movimiento) != 2:                        
            print("Error: La longitud de la entrada debe ser 2.")       # Valida si el movimiento está dentro de los parametros del tablero y el formato,
        elif movimiento[0].lower() not in letra:                                 # pero no corroborra si realmente puede mover ahí.
            print("Error: Columna inválida.")
        elif not movimiento[1].isdigit or movimiento[1] < 1 or movimiento[1] > 8 :
            print("Error: Fila inválida.")
        
    return letra.get(movimiento[0]), movimiento[1]
    # El número va a ser lo que le falta para llegar a 8, ejemplo: a5 --> tomaría la columna 0 por "a" y la fila 3 (8 - 5).
    

tablero = crear_tablero()
posicion_inicial(tablero)
mostrar_tablero(tablero)
letra = {
    "a" : 0,
    "b" : 1,
    "c" : 2,
    "d" : 3,
    "e" : 4,
    "f" : 5,
    "g" : 6,
    "h" : 7
}

contador = 0
seguir_jugando = True

while seguir_jugando:
    if contador % 2 == 0:
        turno = "blancas"
    else:
        turno = "negras"
    print(f"Juegan las {turno}")
    contador += 1
    posicion_pieza = pieza_a_mover(letra)
    corroborrar_pos_pieza_a_mover(letra, turno, posicion_pieza, tablero)