from validaciones import validar_longitud, validar_columna, validar_fila

from posiciones import fila_piezas_negras, fila_piezas_blancas

def crear_tablero():
    matriz = []
    for i in range(8):
        matriz.append([])
        for j in range(8):
            matriz[i].append(".")
    return matriz

def posicion_inicial(tablero):
    tablero[0] = list(fila_piezas_negras)
    tablero[1] = ["pN"] * 8
    tablero[6] = ["pB"] * 8
    tablero[7] = list(fila_piezas_blancas)
    return tablero


def mostrar_tablero(tablero):
    letras = ["A", "B", "C", "D", "E", "F", "G", "H"]

    print("    ", end="")  # Espacio inicial para alinear las letras
    for columna in letras:
        print(f"{columna:4}", end="")  # Imprime las letras de las columnas
    print()

    for i, fila in enumerate(tablero):
        print(f"{8 - i}  ", end="")  # Imprime el número de fila (8 a 1)
        for casilla in fila:
            print(f"{casilla:4}", end="")
        print()
    print()


def pieza_a_mover():    # Solicita y valida si la pieza a mover está dentro de los parametros del tablero,
    piezas_posibles = ("T", "C", "A", "D", "R", "P")                        # y el formato.
    while True:
        pos_pieza = input("Ingrese la inicial de la pieza que quiere mover (letra), la columna en donde está (letra) y la fila (número) (ejemplo: Pe2): ")
        if len(pos_pieza) != 3:
            print("Error: La longitud de la entrada debe ser 3.")
        elif pos_pieza[0].upper() not in piezas_posibles:
            print("Error: Inicial de pieza inválida.")
        elif pos_pieza[1].lower() not in letra:
            print("Error: Columna inválida.")
        elif not pos_pieza[2].isdigit() or int(pos_pieza[2]) < 1 or int(pos_pieza[2]) > 8:
            print("Error: Fila inválida.")
        else:
            return pos_pieza                     # Sale de la función únicamente cuando se validan los valores ingresados. 


def corroborrar_pos_pieza_a_mover(turno, posicion_pieza, tablero):
    pieza = posicion_pieza[:1].lower() + turno[:1].upper()
    columna = posicion_pieza[1:2].lower()
    fila = int(posicion_pieza[2:])
    if pieza == tablero[8 - fila][letra[columna]]:
        return
    else:
        print("La pieza ingresada no se encuentra en esa posición")      
        pieza_a_mover()                                           # Vuelve a la función pieza a mover en este caso.
        

def coordenadas_a_mover():
    while True:
        movimiento = input("Ingrese la casilla a la que quiere mover (ejemplo: e4): ")
        print()
        if not validar_longitud(movimiento):
            print("Error: La longitud de la entrada debe ser 2.")
        elif not validar_columna(movimiento):
            print("Error: Columna inválida.")
        elif not validar_fila(movimiento):
            print("Error: Fila inválida.")
        else:                                                      # Sale de la función únicamente cuando se validan los valores ingresados.
            return letra.get(movimiento[0]), 8 - int(movimiento[1])   


def posibles_movimientos(tablero, posicion_pieza, pos_final, turno): # Deriva a la función de movimiento de pieza correspondiente (según la pieza a mover).
    if posicion_pieza[0].upper() == "P":
        return mover_peon(tablero, posicion_pieza, pos_final, turno)  # Las funciones a las que derivan devuelven True o False
    elif posicion_pieza[0].upper() == "C":                              # dependiendo de si fue posible o no el movimiento.
        return mover_caballo(tablero, posicion_pieza, pos_final, turno)    
    elif posicion_pieza[0].upper() == "A":                              # En caso de ser False, en la función principal se volverá a ejecutar el bloque while.
        return mover_alfil(tablero, posicion_pieza, pos_final, turno) # De ser True, continua con normalidad, y el tablero ya fue actualzido
    elif posicion_pieza[0].upper() == "D":                              # en la función de los movimientos de la pieza.
        return mover_dama(tablero, posicion_pieza, pos_final, turno)
    elif posicion_pieza[0].upper() == "T":
        return mover_torre(tablero, posicion_pieza, pos_final, turno)
    else:
        return mover_rey(tablero, posicion_pieza, pos_final, turno)


def mover_peon(tablero, pos_inicial, pos_final, turno):
    col_inicial = letra[pos_inicial[1].lower()]  
    fila_inicial = 8 - int(pos_inicial[2])       

    col_final = pos_final[0]
    fila_final = pos_final[1]

    pieza = tablero[fila_inicial][col_inicial]
    destino = tablero[fila_final][col_final]

    # Movimiento permitido para peones blancos (suben filas)
    if turno == "blancas":
        if col_inicial == col_final:
            if fila_final == fila_inicial - 1 and tablero[fila_final][col_final] == ".":
                tablero[fila_final][col_final] = "pB"
                tablero[fila_inicial][col_inicial] = "."
                return True

            # En el primer movimiento del peon puede avanzar 2 casillas
            elif fila_inicial == 6 and fila_final == fila_inicial - 2 and tablero[fila_inicial-1][col_inicial] == "." and tablero[fila_final][col_final] == ".":
                tablero[fila_final][col_final] = "pB"
                tablero[fila_inicial][col_inicial] = "."
                return True
            else:
                print("Movimiento inválido para el peón blanco.")
                return False
        elif abs(col_inicial - col_final) == 1 and fila_final == fila_inicial - 1:
            if destino != "." and not puede_comer(destino, turno, pieza):
                return False
            elif destino != ".":
                tablero[fila_final][col_final] = pieza
                tablero[fila_inicial][col_inicial] = "."
                return True
            else:
                print("Movimiento diagonal inválido para el peón blanco.")
                return False
        else:
            print("Movimiento diagonal inválido para el peón blanco.")
            return False

    # Movimiento permitido para peones negros (bajan filas)
    elif turno == "negras":
        if col_inicial == col_final:
            if fila_final == fila_inicial + 1 and tablero[fila_final][col_final] == ".":
                tablero[fila_final][col_final] = "pN"
                tablero[fila_inicial][col_inicial] = "."
                return True

            # En el primer movimiento del peon puede avanzar 2 casillas
            elif fila_inicial == 1 and fila_final == fila_inicial + 2 and tablero[fila_inicial+1][col_inicial] == "." and tablero[fila_final][col_final] == ".":
                tablero[fila_final][col_final] = "pN"
                tablero[fila_inicial][col_inicial] = "."
                return True
            else:
                print("Movimiento inválido para el peón negro.")
                return False
        elif abs(col_inicial - col_final) == 1 and fila_final == fila_inicial + 1:
            if destino != "." and not puede_comer(destino, turno, pieza):
                return False
            elif destino != ".":
                tablero[fila_final][col_final] = pieza
                tablero[fila_inicial][col_inicial] = "."
                return True
            else:
                print("Movimiento diagonal inválido para el peón negro.")
                return False
        else:
            print("Movimiento diagonal inválido para el peón negro.")
            return False


def mover_caballo(tablero, pos_inicial, pos_final, turno):
    col_inicial = letra[pos_inicial[1].lower()]
    fila_inicial = 8 - int(pos_inicial[2])

    col_final = pos_final[0]
    fila_final = pos_final[1]

    pieza = tablero[fila_inicial][col_inicial]
    destino = tablero[fila_final][col_final]

    # Movimientos válidos en L
    delta_fila = abs(fila_final - fila_inicial)
    delta_col = abs(col_final - col_inicial)

    if (delta_fila, delta_col) in ((2, 1), (1, 2)):
        if destino != ".":
            if not puede_comer(destino, turno, pieza):
                return False
        # Movimiento válido: actualizar el tablero
        tablero[fila_final][col_final] = pieza
        tablero[fila_inicial][col_inicial] = "."
        return True
    else:
        print("Movimiento inválido para el caballo.")
        return False


def mover_torre(tablero, pos_inicial, pos_final, turno):
    col_inicial = letra[pos_inicial[1].lower()]
    fila_inicial = 8 - int(pos_inicial[2])

    col_final = pos_final[0]
    fila_final = pos_final[1]

    pieza = tablero[fila_inicial][col_inicial]
    destino = tablero[fila_final][col_final]

    # Validamos movimiento: recto en filas o columnas
    if fila_inicial != fila_final and col_inicial != col_final:
        print("La torre sólo se mueve en línea recta.")
        return False

    # Comprobamos que el camino esté libre
    if fila_inicial == fila_final:  # Movimiento horizontal
        paso = 1 if col_final > col_inicial else -1
        for c in range(col_inicial + paso, col_final, paso):
            if tablero[fila_inicial][c] != ".":
                print("Movimiento bloqueado: hay una pieza en el camino.")
                return False

    elif col_inicial == col_final:  # Movimiento vertical
        paso = 1 if fila_final > fila_inicial else -1
        for f in range(fila_inicial + paso, fila_final, paso):
            if tablero[f][col_inicial] != ".":
                print("Movimiento bloqueado: hay una pieza en el camino.")
                return False

    # Verificamos si puede comer una pieza
    if destino != ".":
        if not puede_comer(destino, turno, pieza):
            return False

    # Movimiento permitido: actualizamos el tablero
    tablero[fila_final][col_final] = pieza
    tablero[fila_inicial][col_inicial] = "."
    return True


def mover_alfil(tablero, pos_inicial, pos_final, turno):
    col_inicial = letra[pos_inicial[1].lower()]
    fila_inicial = 8 - int(pos_inicial[2])

    col_final = pos_final[0]
    fila_final = pos_final[1]

    pieza = tablero[fila_inicial][col_inicial]
    destino = tablero[fila_final][col_final]

    # Validar que el movimiento sea en diagonal
    if abs(fila_final - fila_inicial) != abs(col_final - col_inicial):
        print("El alfil sólo se mueve en diagonal.")
        return False

    # Comprobar que el camino esté libre
    paso_fila = 1 if fila_final > fila_inicial else -1
    paso_col = 1 if col_final > col_inicial else -1

    f, c = fila_inicial + paso_fila, col_inicial + paso_col
    while f != fila_final and c != col_final:
        if tablero[f][c] != ".":
            print("Movimiento bloqueado: hay una pieza en el camino.")
            return False
        f += paso_fila
        c += paso_col
    
    # Verificamos si puede comer una pieza
    if destino != ".":
        if not puede_comer(destino, turno, pieza):
            return False

    # Movimiento permitido: actualizamos el tablero
    tablero[fila_final][col_final] = pieza
    tablero[fila_inicial][col_inicial] = "."
    return True


def mover_dama(tablero, pos_inicial, pos_final, turno):
    col_inicial = letra[pos_inicial[1].lower()]
    fila_inicial = 8 - int(pos_inicial[2])

    col_final = pos_final[0]
    fila_final = pos_final[1]

    pieza = tablero[fila_inicial][col_inicial]
    destino = tablero[fila_final][col_final]

    # Movimiento tipo torre
    if fila_inicial == fila_final or col_inicial == col_final:
        # Comprobamos que el camino esté libre
        if fila_inicial == fila_final:  # Movimiento horizontal
            paso = 1 if col_final > col_inicial else -1
            for c in range(col_inicial + paso, col_final, paso):
                if tablero[fila_inicial][c] != ".":
                    print("Movimiento bloqueado: hay una pieza en el camino.")
                    return False

        elif col_inicial == col_final:  # Movimiento vertical
            paso = 1 if fila_final > fila_inicial else -1
            for f in range(fila_inicial + paso, fila_final, paso):
                if tablero[f][col_inicial] != ".":
                    print("Movimiento bloqueado: hay una pieza en el camino.")
                    return False

        if destino != ".":
            if not puede_comer(destino, turno, pieza):
                return False

        # Movimiento permitido: actualizamos el tablero
        tablero[fila_final][col_final] = pieza
        tablero[fila_inicial][col_inicial] = "."
        return True

    # Movimiento tipo alfil
    elif abs(fila_final - fila_inicial) == abs(col_final - col_inicial):
        paso_fila = 1 if fila_final > fila_inicial else -1
        paso_col = 1 if col_final > col_inicial else -1

        f, c = fila_inicial + paso_fila, col_inicial + paso_col
        while f != fila_final and c != col_final:
            if tablero[f][c] != ".":
                print("Movimiento bloqueado: hay una pieza en el camino.")
                return False
            f += paso_fila
            c += paso_col

        if destino != ".":
            if not puede_comer(destino, turno, pieza):
                return False

        # Movimiento permitido: actualizamos el tablero
        tablero[fila_final][col_final] = pieza
        tablero[fila_inicial][col_inicial] = "."
        return True

    else:
        print("La dama sólo se mueve en línea recta o en diagonal.")
        return False


def mover_rey(tablero, pos_inicial, pos_final, turno):
    col_inicial = letra[pos_inicial[1].lower()]
    fila_inicial = 8 - int(pos_inicial[2])

    col_final = pos_final[0]
    fila_final = pos_final[1]

    pieza = tablero[fila_inicial][col_inicial]
    destino = tablero[fila_final][col_final]

    # Verificar que el movimiento sea de una sola casilla en cualquier dirección
    delta_fila = abs(fila_final - fila_inicial)
    delta_col = abs(col_final - col_inicial)

    if delta_fila <= 1 and delta_col <= 1 and (delta_fila != 0 or delta_col != 0):
        if destino != ".":
            if not puede_comer(destino, turno, pieza):
                return False
        # Movimiento válido: actualizar el tablero
        tablero[fila_final][col_final] = pieza
        tablero[fila_inicial][col_inicial] = "."
        return True
    else:
        print("Movimiento inválido para el rey (sólo una casilla).")
        return False


def puede_comer(destino, turno, pieza):
    if turno == "blancas" and destino.endswith("B"):
        print("No podés capturar tus propias piezas.")
        return False
    elif turno == "negras" and destino.endswith("N"):
        print("No podés capturar tus propias piezas.")
        return False
    print(f"¡{pieza} capturó a {destino}!")   # Se capturó una pieza
    return True


def finalizacion_juego(tablero, turno):       # Finaliza el juego si no se encuentra el rey enemigo en el tablero.
    if turno == "blancas":                    # Fue caputrado.
        color_oponente = "N"
    else:
        color_oponente = "B"
    rey = "r" + color_oponente
    for fila in range(8):
        for columna in range(8):
            if tablero[fila][columna] == rey:
                return False
    return True


def inicializacion():
    print("Acá va un archivo explicando muchas cosas")
    print()
    print()
    tablero = crear_tablero()
    posicion_inicial(tablero)
    

    contador = 0
    while True:
        mostrar_tablero(tablero)
        if contador % 2 == 0:
            turno = "blancas"
        else:
            turno = "negras"
        
    
        print(f"Juegan las {turno}\n")
        
        pos_inical_pieza = pieza_a_mover()       # Solicitamos que ingrese la pieza a mover junto con la posición en la que se encuentra.
        corroborrar_pos_pieza_a_mover(turno, pos_inical_pieza, tablero)  # Verificamos que efectivamente este en esa posición.
        posicion_final = coordenadas_a_mover()                      # Solicitamos la casilla a donde se va a mover la pieza elegida.
        if not posibles_movimientos(tablero, pos_inical_pieza, posicion_final, turno):
            print("Vamos de vuelta\n")    # Funcionón que identifica la pieza a mover y deriva a la función de los movimientos de esa pieza.
            continue                    # De no poderse realizar el movimiento devuelve False y se vuelve a ejecutar el bloque (sin sumar contador).
        if finalizacion_juego(tablero, turno):
            mostrar_tablero(tablero)
            print(f"Finalizo el juego, ganaron las {turno}")
            break                                # Finaliza el juego si no se encuentra el rey enemigo en el tablero.
        contador += 1


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

inicializacion()