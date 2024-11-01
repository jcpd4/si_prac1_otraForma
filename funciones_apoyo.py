# funciones_apoyo.py

from casilla import Casilla

def obtener_vecinos(estado, mapa):
    """Obtiene los vecinos de una casilla en 8 direcciones."""
    vecinos = []
    fila, columna = estado.getFila(), estado.getCol()
    movimientos = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]  # 8 direcciones
    for df, dc in movimientos:
        nueva_fila = fila + df
        nueva_columna = columna + dc
        vecino = Casilla(nueva_fila, nueva_columna)
        if mapa.es_valido(vecino):
            vecinos.append(vecino)
    return vecinos

def costo_movimiento(estado_actual, vecino, mapa):
    """Calcula el costo de moverse de una casilla a otra basado en el tipo de movimiento."""
    fila_actual, col_actual = estado_actual.getFila(), estado_actual.getCol()
    fila_vecino, col_vecino = vecino.getFila(), vecino.getCol()
    # Determinar si el movimiento es diagonal
    if abs(fila_vecino - fila_actual) == 1 and abs(col_vecino - col_actual) == 1:
        return 1.5  # Diagonal
    else:
        return 1  # Horizontal o Vertical

def manhattan_heuristica(estado, meta):
    """Heurística de distancia Manhattan."""
    return abs(estado.getFila() - meta.getFila()) + abs(estado.getCol() - meta.getCol())
