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
    letras = ["a", "b", "c", "d", "e", "f", "g", "h"]

    print("    ", end="")  # Espacio inicial para alinear las letras
    for letra in letras:
        print(f"{letra:4}", end="")  # Imprime las letras de columna
    print()

    for i, fila in enumerate(tablero):
        print(f"{8 - i}  ", end="")  # Imprime el número de fila (8 a 1)
        for casilla in fila:
            print(f"{casilla:4}", end="")
        print()
    print()


def pieza_a_mover(letra):                      # Valida si la pieza a mover está dentro de los parametros del tablero y el formato,
    piezas_posibles = ("T", "C", "A", "D", "R", "P")
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

def mover_rey(tablero, letra, pos_inicial, pos_final, turno):
    col_inicial = letra[pos_inicial[1].lower()]
    fila_inicial = 8 - int(pos_inicial[2])

    col_final = pos_final[0]
    fila_final = pos_final[1]

    pieza = tablero[fila_inicial][col_inicial]

    # Verificar que sea un rey del turno correcto
    if turno == "blancas" and pieza != "rB":
        print("No hay un rey blanco en la posición inicial.")
        return False
    if turno == "negras" and pieza != "rN":
        print("No hay un rey negro en la posición inicial.")
        return False

    # Verificar que el movimiento sea de una sola casilla en cualquier dirección
    delta_fila = abs(fila_final - fila_inicial)
    delta_col = abs(col_final - col_inicial)

    if delta_fila <= 1 and delta_col <= 1 and (delta_fila != 0 or delta_col != 0):
        # Movimiento válido: actualizar el tablero
        tablero[fila_final][col_final] = pieza
        tablero[fila_inicial][col_inicial] = "."
        return True
    else:
        print("Movimiento inválido para el rey (sólo una casilla).")
        return False


def mover_peon(tablero, letra, pos_inicial, pos_final, turno):
    col_inicial = letra[pos_inicial[1].lower()]  # CAMBIO AQUÍ
    fila_inicial = 8 - int(pos_inicial[2])       # CAMBIO AQUÍ

    col_final = letra[pos_final[0].lower()]
    fila_final = 8 - int(pos_final[1])

    pieza = tablero[fila_inicial][col_inicial]

    # Verificamos que la pieza sea un peón del turno correcto
    if turno == "blancas" and pieza != "pB":
        print("No hay un peón blanco en la posición inicial.")
        return False
    if turno == "negras" and pieza != "pN":
        print("No hay un peón negro en la posición inicial.")
        return False

    # Movimiento permitido para peones blancos (suben filas)
    if turno == "blancas":
        if col_inicial == col_final:
            if fila_final == fila_inicial - 1 and tablero[fila_final][col_final] == ".":
                tablero[fila_final][col_final] = "pB"
                tablero[fila_inicial][col_inicial] = "."
                return True
            elif fila_inicial == 6 and fila_final == fila_inicial - 2 and tablero[fila_inicial-1][col_inicial] == "." and tablero[fila_final][col_final] == ".":
                tablero[fila_final][col_final] = "pB"
                tablero[fila_inicial][col_inicial] = "."
                return True
            else:
                print("Movimiento inválido para el peón blanco.")
                return False
        else:
            print("El peón blanco no puede moverse en diagonal sin capturar (todavía no implementado).")
            return False

    # Movimiento permitido para peones negros (bajan filas)
    if turno == "negras":
        if col_inicial == col_final:
            if fila_final == fila_inicial + 1 and tablero[fila_final][col_final] == ".":
                tablero[fila_final][col_final] = "pN"
                tablero[fila_inicial][col_inicial] = "."
                return True
            elif fila_inicial == 1 and fila_final == fila_inicial + 2 and tablero[fila_inicial+1][col_inicial] == "." and tablero[fila_final][col_final] == ".":
                tablero[fila_final][col_final] = "pN"
                tablero[fila_inicial][col_inicial] = "."
                return True
            else:
                print("Movimiento inválido para el peón negro.")
                return False
        else:
            print("El peón negro no puede moverse en diagonal sin capturar (todavía no implementado).")
            return False



def mover_torre(tablero, letra, pos_inicial, pos_final, turno):
    col_inicial = letra[pos_inicial[1].lower()]
    fila_inicial = 8 - int(pos_inicial[2])

    col_final = letra[pos_final[0].lower()]
    fila_final = 8 - int(pos_final[1])

    pieza = tablero[fila_inicial][col_inicial]

    # Verificamos que la pieza sea una torre del turno correcto
    if turno == "blancas" and pieza != "tB":
        print("No hay una torre blanca en la posición inicial.")
        return False
    if turno == "negras" and pieza != "tN":
        print("No hay una torre negra en la posición inicial.")
        return False

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

    # Movimiento permitido: actualizamos el tablero
    tablero[fila_final][col_final] = pieza
    tablero[fila_inicial][col_inicial] = "."
    return True


def mover_alfil(tablero, letra, pos_inicial, pos_final, turno):
    col_inicial = letra[pos_inicial[1].lower()]
    fila_inicial = 8 - int(pos_inicial[2])

    col_final = letra[pos_final[0].lower()]
    fila_final = 8 - int(pos_final[1])

    pieza = tablero[fila_inicial][col_inicial]

    # Verificamos que la pieza sea un alfil del turno correcto
    if turno == "blancas" and pieza != "aB":
        print("No hay un alfil blanco en la posición inicial.")
        return False
    if turno == "negras" and pieza != "aN":
        print("No hay un alfil negro en la posición inicial.")
        return False

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

    # Movimiento permitido: actualizamos el tablero
    tablero[fila_final][col_final] = pieza
    tablero[fila_inicial][col_inicial] = "."
    return True


def mover_dama(tablero, letra, pos_inicial, pos_final, turno):
    col_inicial = letra[pos_inicial[1].lower()]
    fila_inicial = 8 - int(pos_inicial[2])

    col_final = letra[pos_final[0].lower()]
    fila_final = 8 - int(pos_final[1])

    pieza = tablero[fila_inicial][col_inicial]

    # Verificamos que la pieza sea una dama del turno correcto
    if turno == "blancas" and pieza != "dB":
        print("No hay una dama blanca en la posición inicial.")
        return False
    if turno == "negras" and pieza != "dN":
        print("No hay una dama negra en la posición inicial.")
        return False

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

        # Movimiento permitido: actualizamos el tablero
        tablero[fila_final][col_final] = pieza
        tablero[fila_inicial][col_inicial] = "."
        return True

    else:
        print("La dama sólo se mueve en línea recta o en diagonal.")
        return False


def mover_caballo(tablero, letra, pos_inicial, pos_final, turno):
    col_inicial = letra[pos_inicial[1].lower()]
    fila_inicial = 8 - int(pos_inicial[2])

    col_final = letra[pos_final[0].lower()]
    fila_final = 8 - int(pos_final[1])

    pieza = tablero[fila_inicial][col_inicial]

    # Verificamos que la pieza sea un caballo del turno correcto
    if turno == "blancas" and pieza != "cB":
        print("No hay un caballo blanco en la posición inicial.")
        return False
    if turno == "negras" and pieza != "cN":
        print("No hay un caballo negro en la posición inicial.")
        return False

    # Movimientos válidos en L
    delta_fila = abs(fila_final - fila_inicial)
    delta_col = abs(col_final - col_inicial)

    if (delta_fila, delta_col) in ((2, 1), (1, 2)):
        # Movimiento válido: actualizar el tablero
        tablero[fila_final][col_final] = pieza
        tablero[fila_inicial][col_inicial] = "."
        return True
    else:
        print("Movimiento inválido para el caballo.")
        return False


def posibles_movimientos(posicion_pieza, tablero):     # Deriva a la función correspondiente según la pieza a mover.
    if posicion_pieza[0].upper() == "P":
        return mover_peon(posicion_pieza, tablero)
    elif posicion_pieza[0].upper() == "C":
        return mover_torre(posicion_pieza, tablero)
    elif posicion_pieza[0].upper() == "A":
        return mov_alfil(posicion_pieza, tablero)
    elif posicion_pieza[0].upper() == "D":
        return mov_dama(posicion_pieza, tablero)
    elif posicion_pieza[0].upper() == "T":
        return mover(posicion_pieza, tablero)
    else:
        return mov_rey(posicion_pieza, tablero)

def coordenadas_a_mover(letra):
    while True:
        movimiento = input("Ingrese la casilla a la que quiere mover (ejemplo: e5): ")
        if not validar_longitud(movimiento):
            print("Error: La longitud de la entrada debe ser 2.")
        elif not validar_columna(movimiento, letra):
            print("Error: Columna inválida.")
        elif not validar_fila(movimiento):
            print("Error: Fila inválida.")
        else:
            return letra.get(movimiento[0]), 8 - int(movimiento[1])



    return letra.get(movimiento[0]), movimiento[1]
    # El número va a ser lo que le falta para llegar a 8, ejemplo: a5 --> tomaría la columna 0 por "a" y la fila 3 (8 - 5).


def init():
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

    turno = "blancas"  # Asignamos turno porque lo usa mover_peon

    # Pedimos movimientos
    pieza_inicial = pieza_a_mover(letra)      # <<< CAMBIÉ NOMBRE
    coordenada_destino = coordenadas_a_mover(letra)
    tablero[6][3]='.'
    mover_rey(tablero, letra, pieza_inicial, coordenada_destino, turno)
    mostrar_tablero(tablero)

    # contador = 0
    # seguir_jugando = True
    #
    # while seguir_jugando:
    #     if contador % 2 == 0:
    #         turno = "blancas"
    #     else:
    #         turno = "negras"
    #     print(f"Juegan las {turno}")
    #     contador += 1
    #     posicion_pieza = pieza_a_mover(letra)
    #     corroborrar_pos_pieza_a_mover(letra, turno, posicion_pieza, tablero)




init()