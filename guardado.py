import json
import os

NOMBRE_ARCHIVO_PARTIDAS = "partidas.json"

def guardar_partida(nombre_partida, tablero, ayuda, contador):
    partida = {
        "nombre": nombre_partida,
        "tablero": tablero,
        "ayuda": ayuda,
        "contador": contador
    }

    partidas = []

    if os.path.exists(NOMBRE_ARCHIVO_PARTIDAS):
        with open(NOMBRE_ARCHIVO_PARTIDAS, "r") as archivo:
            try:
                partidas = json.load(archivo)
            except json.JSONDecodeError:
                # El archivo existe pero está vacío o corrupto: empieza con lista vacía
                partidas = []

    # Reemplaza si ya existe
    partidas = [p for p in partidas if p["nombre"] != nombre_partida]
    partidas.append(partida)

    with open(NOMBRE_ARCHIVO_PARTIDAS, "w") as archivo:
        json.dump(partidas, archivo, indent=4)

    # print(f"✅ Partida '{nombre_partida}' guardada automáticamente.")

def cargar_partida(nombre_partida):
    if not os.path.exists(NOMBRE_ARCHIVO_PARTIDAS):
        print("No hay partidas guardadas.")
        return None

    with open(NOMBRE_ARCHIVO_PARTIDAS, "r") as archivo:
        partidas = json.load(archivo)

    for partida in partidas:
        if partida["nombre"] == nombre_partida:
            print(f"Partida '{nombre_partida}' cargada con éxito.")
            return partida

    print(f"No se encontró la partida '{nombre_partida}'.")
    return None