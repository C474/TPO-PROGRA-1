validar_longitud = lambda movimiento: len(movimiento) == 2
validar_columna = lambda movimiento, letra: movimiento[0].lower() in letra
validar_fila = lambda movimiento: movimiento[1].isdigit() and 1 <= int(movimiento[1]) <= 8