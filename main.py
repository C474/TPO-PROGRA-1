import copy

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
    tablero[1] = ["Pn"] * 8
    tablero[6] = ["Pb"] * 8
    tablero[7] = list(fila_piezas_blancas)
    return tablero


def mostrar_tablero(tablero, marcadas=None):
    if marcadas is None:
        marcadas = []

    letras = ["A", "B", "C", "D", "E", "F", "G", "H"]

    print("    ", end="")
    for columna in letras:
        print(f"{columna:4}", end="")
    print()

    for i, fila in enumerate(tablero):
        print(f"{8 - i}  ", end="")
        for j, casilla in enumerate(fila):
            if (i, j) in marcadas and casilla == ".":
                print(f"{'*':4}", end="")
            else:
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
    pieza = posicion_pieza[:1].upper() + turno[:1].lower()
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
        elif not validar_columna(movimiento, letra):
            print("Error: Columna inválida.")
        elif not validar_fila(movimiento):
            print("Error: Fila inválida.")
        else:                                                      # Sale de la función únicamente cuando se validan los valores ingresados.
            return letra.get(movimiento[0]), 8 - int(movimiento[1])


# Deriva a la función de movimiento de pieza correspondiente (según la pieza a mover).
def posibles_movimientos(tablero, posicion_pieza, pos_final, turno, silencioso=False):
    if posicion_pieza[0].upper() == "P":
        return mover_peon(tablero, posicion_pieza, pos_final, turno, silencioso)
    elif posicion_pieza[0].upper() == "C":
        return mover_caballo(tablero, posicion_pieza, pos_final, turno, silencioso)
    elif posicion_pieza[0].upper() == "A":
        return mover_alfil(tablero, posicion_pieza, pos_final, turno, silencioso)
    elif posicion_pieza[0].upper() == "D":
        return mover_dama(tablero, posicion_pieza, pos_final, turno, silencioso)
    elif posicion_pieza[0].upper() == "T":
        return mover_torre(tablero, posicion_pieza, pos_final, turno, silencioso)
    else:
        return mover_rey(tablero, posicion_pieza, pos_final, turno, silencioso)


def mover_peon(tablero, pos_inicial, pos_final, turno, silencioso=False):
    col_inicial = letra[pos_inicial[1].lower()]
    fila_inicial = 8 - int(pos_inicial[2])

    col_final = pos_final[0]
    fila_final = pos_final[1]

    pieza = tablero[fila_inicial][col_inicial]
    destino = tablero[fila_final][col_final]

    if turno == "blancas":
        if col_inicial == col_final:
            if fila_final == fila_inicial - 1 and tablero[fila_final][col_final] == ".":
                tablero[fila_final][col_final] = "Pb"
                tablero[fila_inicial][col_inicial] = "."
                return True
            elif fila_inicial == 6 and fila_final == fila_inicial - 2 and tablero[fila_inicial-1][col_inicial] == "." and tablero[fila_final][col_final] == ".":
                tablero[fila_final][col_final] = "Pb"
                tablero[fila_inicial][col_inicial] = "."
                return True
            else:
                if not silencioso:
                    print("Movimiento inválido para el peón blanco.")
                return False
        elif abs(col_inicial - col_final) == 1 and fila_final == fila_inicial - 1:
            if destino != "." and not puede_comer(destino, turno, pieza, silencioso):
                return False
            elif destino != ".":
                tablero[fila_final][col_final] = pieza
                tablero[fila_inicial][col_inicial] = "."
                return True
            else:
                if not silencioso:
                    print("Movimiento diagonal inválido para el peón blanco.")
                return False
        else:
            if not silencioso:
                print("Movimiento diagonal inválido para el peón blanco.")
            return False

    elif turno == "negras":
        if col_inicial == col_final:
            if fila_final == fila_inicial + 1 and tablero[fila_final][col_final] == ".":
                tablero[fila_final][col_final] = "Pn"
                tablero[fila_inicial][col_inicial] = "."
                return True
            elif fila_inicial == 1 and fila_final == fila_inicial + 2 and tablero[fila_inicial+1][col_inicial] == "." and tablero[fila_final][col_final] == ".":
                tablero[fila_final][col_final] = "Pn"
                tablero[fila_inicial][col_inicial] = "."
                return True
            else:
                if not silencioso:
                    print("Movimiento inválido para el peón negro.")
                return False
        elif abs(col_inicial - col_final) == 1 and fila_final == fila_inicial + 1:
            if destino != "." and not puede_comer(destino, turno, pieza, silencioso):
                return False
            elif destino != ".":
                tablero[fila_final][col_final] = pieza
                tablero[fila_inicial][col_inicial] = "."
                return True
            else:
                if not silencioso:
                    print("Movimiento diagonal inválido para el peón negro.")
                return False
        else:
            if not silencioso:
                print("Movimiento diagonal inválido para el peón negro.")
            return False



def mover_caballo(tablero, pos_inicial, pos_final, turno, silencioso=False):
    col_inicial = letra[pos_inicial[1].lower()]
    fila_inicial = 8 - int(pos_inicial[2])

    col_final = pos_final[0]
    fila_final = pos_final[1]

    pieza = tablero[fila_inicial][col_inicial]
    destino = tablero[fila_final][col_final]

    delta_fila = abs(fila_final - fila_inicial)
    delta_col = abs(col_final - col_inicial)

    if (delta_fila, delta_col) in ((2, 1), (1, 2)):
        if destino != "." and not puede_comer(destino, turno, pieza, silencioso):
            return False
        tablero[fila_final][col_final] = pieza
        tablero[fila_inicial][col_inicial] = "."
        return True
    else:
        if not silencioso:
            print("Movimiento inválido para el caballo.")
        return False


def mover_torre(tablero, pos_inicial, pos_final, turno, silencioso=False):
    col_inicial = letra[pos_inicial[1].lower()]
    fila_inicial = 8 - int(pos_inicial[2])

    col_final = pos_final[0]
    fila_final = pos_final[1]

    pieza = tablero[fila_inicial][col_inicial]
    destino = tablero[fila_final][col_final]

    if fila_inicial != fila_final and col_inicial != col_final:
        if not silencioso:
            print("La torre sólo se mueve en línea recta.")
        return False

    if fila_inicial == fila_final:
        paso = 1 if col_final > col_inicial else -1
        for c in range(col_inicial + paso, col_final, paso):
            if tablero[fila_inicial][c] != ".":
                if not silencioso:
                    print("Movimiento bloqueado: hay una pieza en el camino.")
                return False

    elif col_inicial == col_final:
        paso = 1 if fila_final > fila_inicial else -1
        for f in range(fila_inicial + paso, fila_final, paso):
            if tablero[f][col_inicial] != ".":
                if not silencioso:
                    print("Movimiento bloqueado: hay una pieza en el camino.")
                return False

    if destino != "." and not puede_comer(destino, turno, pieza, silencioso):
        return False

    tablero[fila_final][col_final] = pieza
    tablero[fila_inicial][col_inicial] = "."
    return True


def mover_alfil(tablero, pos_inicial, pos_final, turno, silencioso=False):
    col_inicial = letra[pos_inicial[1].lower()]
    fila_inicial = 8 - int(pos_inicial[2])

    col_final = pos_final[0]
    fila_final = pos_final[1]

    pieza = tablero[fila_inicial][col_inicial]
    destino = tablero[fila_final][col_final]

    if abs(fila_final - fila_inicial) != abs(col_final - col_inicial):
        if not silencioso:
            print("El alfil sólo se mueve en diagonal.")
        return False

    paso_fila = 1 if fila_final > fila_inicial else -1
    paso_col = 1 if col_final > col_inicial else -1

    f, c = fila_inicial + paso_fila, col_inicial + paso_col
    while f != fila_final and c != col_final:
        if tablero[f][c] != ".":
            if not silencioso:
                print("Movimiento bloqueado: hay una pieza en el camino.")
            return False
        f += paso_fila
        c += paso_col

    if destino != "." and not puede_comer(destino, turno, pieza, silencioso):
        return False

    tablero[fila_final][col_final] = pieza
    tablero[fila_inicial][col_inicial] = "."
    return True


def mover_dama(tablero, pos_inicial, pos_final, turno, silencioso=False):
    col_inicial = letra[pos_inicial[1].lower()]
    fila_inicial = 8 - int(pos_inicial[2])

    col_final = pos_final[0]
    fila_final = pos_final[1]

    pieza = tablero[fila_inicial][col_inicial]
    destino = tablero[fila_final][col_final]

    if fila_inicial == fila_final or col_inicial == col_final:
        if fila_inicial == fila_final:
            paso = 1 if col_final > col_inicial else -1
            for c in range(col_inicial + paso, col_final, paso):
                if tablero[fila_inicial][c] != ".":
                    if not silencioso:
                        print("Movimiento bloqueado: hay una pieza en el camino.")
                    return False
        elif col_inicial == col_final:
            paso = 1 if fila_final > fila_inicial else -1
            for f in range(fila_inicial + paso, fila_final, paso):
                if tablero[f][col_inicial] != ".":
                    if not silencioso:
                        print("Movimiento bloqueado: hay una pieza en el camino.")
                    return False

        if destino != "." and not puede_comer(destino, turno, pieza, silencioso):
            return False

        tablero[fila_final][col_final] = pieza
        tablero[fila_inicial][col_inicial] = "."
        return True

    elif abs(fila_final - fila_inicial) == abs(col_final - col_inicial):
        paso_fila = 1 if fila_final > fila_inicial else -1
        paso_col = 1 if col_final > col_inicial else -1

        f, c = fila_inicial + paso_fila, col_inicial + paso_col
        while f != fila_final and c != col_final:
            if tablero[f][c] != ".":
                if not silencioso:
                    print("Movimiento bloqueado: hay una pieza en el camino.")
                return False
            f += paso_fila
            c += paso_col

        if destino != "." and not puede_comer(destino, turno, pieza, silencioso):
            return False

        tablero[fila_final][col_final] = pieza
        tablero[fila_inicial][col_inicial] = "."
        return True

    else:
        if not silencioso:
            print("La dama sólo se mueve en línea recta o en diagonal.")
        return False


def mover_rey(tablero, pos_inicial, pos_final, turno, silencioso=False):
    col_inicial = letra[pos_inicial[1].lower()]
    fila_inicial = 8 - int(pos_inicial[2])

    col_final = pos_final[0]
    fila_final = pos_final[1]

    pieza = tablero[fila_inicial][col_inicial]
    destino = tablero[fila_final][col_final]

    delta_fila = abs(fila_final - fila_inicial)
    delta_col = abs(col_final - col_inicial)

    if delta_fila <= 1 and delta_col <= 1 and (delta_fila != 0 or delta_col != 0):
        if destino != "." and not puede_comer(destino, turno, pieza, silencioso):
            return False
        tablero[fila_final][col_final] = pieza
        tablero[fila_inicial][col_inicial] = "."
        return True
    else:
        if not silencioso:
            print("Movimiento inválido para el rey (sólo una casilla).")
        return False



def puede_comer(destino, turno, pieza, silencioso=False):
    if turno == "blancas" and destino.endswith("b"):
        if not silencioso:
            print("No podés capturar tus propias piezas.")
        return False
    elif turno == "negras" and destino.endswith("n"):
        if not silencioso:
            print("No podés capturar tus propias piezas.")
        return False
    if not silencioso:
        print(f"¡{pieza} capturó a {destino}!")
    return True


def finalizacion_juego(tablero, turno):       # Finaliza el juego si no se encuentra el rey enemigo en el tablero.
    if turno == "blancas":                    # Fue caputrado.
        color_oponente = "n"
    else:
        color_oponente = "b"
    rey = "R" + color_oponente
    for fila in range(8):
        for columna in range(8):
            if tablero[fila][columna] == rey:
                return False
    return True



def obtener_movimientos_validos(tablero, pos_inicial, turno):
    movimientos = []
    col_inicial = letra[pos_inicial[1].lower()]
    fila_inicial = 8 - int(pos_inicial[2])

    for fila in range(8):
        for col in range(8):
            tablero_temp = copy.deepcopy(tablero)
            try:
                # PASA silencioso=True aquí:
                if posibles_movimientos(tablero_temp, pos_inicial, (col, fila), turno, silencioso=True):
                    movimientos.append((fila, col))
            except:
                continue
    return movimientos


def convertir_a_notacion(posiciones):
    letra_inv = {v: k for k, v in letra.items()}
    return [f"{letra_inv[col]}{8 - fila}" for fila, col in posiciones]

def inicializacion():
    print("¿Desea jugar con ayudas para ver los movimientos posibles?")
    print("1. Sí")
    print("2. No")
    eleccion = input("Seleccione una opción (1 o 2): ")
    ayuda = eleccion == "1"
    # print("Acá va un archivo explicando muchas cosas")
    # print()
    # print()
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
        if ayuda:
            movimientos_validos = obtener_movimientos_validos(tablero, pos_inical_pieza, turno)
            if movimientos_validos:
                print("Movimientos posibles:")
                mostrar_tablero(tablero, marcadas=movimientos_validos)
                print("Opciones:", ", ".join(convertir_a_notacion(movimientos_validos)))
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