# a_estrella.py

import heapq
from nodo import Nodo

def existe_en_lista_interior(lista_interior, casilla):
    """
    Verifica si una casilla ya existe en lista_interior basada en sus coordenadas.

    :param lista_interior: Lista de objetos Casilla explorados.
    :param casilla: Objeto Casilla a verificar.
    :return: True si existe, False en caso contrario.
    """
    fila = casilla.getFila()
    columna = casilla.getCol()
    for c in lista_interior:
        if c.getFila() == fila and c.getCol() == columna:
            return True
    return False

def existe_en_lista_frontera(lista_frontera, casilla):
    """
    Verifica si una casilla ya existe en lista_frontera basada en sus coordenadas.

    :param lista_frontera: Lista de objetos Nodo en la frontera.
    :param casilla: Objeto Casilla a verificar.
    :return: True si existe, False en caso contrario.
    """
    fila = casilla.getFila()
    columna = casilla.getCol()
    for nodo in lista_frontera:
        estado = nodo.getEstado()
        if estado.getFila() == fila and estado.getCol() == columna:
            return True
    return False

# Heurísticas
def manhattan_heuristica(nodo_actual, nodo_meta):
    """Calcula la distancia Manhattan entre dos nodos (usando Casilla)."""
    resultado = abs(nodo_actual.getFila() - nodo_meta.getFila()) + abs(nodo_actual.getCol() - nodo_meta.getCol())
    return resultado

def trivial_heuristica(nodo_actual, nodo_meta):
    return 0

def euclidea_heuristica(nodo_actual, nodo_meta):
    return ((nodo_actual.getFila() - nodo_meta.getFila())**2 + (nodo_actual.getCol() - nodo_meta.getCol())**2)**0.5

def chebyshev_heuristica(nodo_actual, nodo_meta):
    return max(abs(nodo_actual.getFila() - nodo_meta.getFila()), abs(nodo_actual.getCol() - nodo_meta.getCol()))

def a_estrella(camino, inicio, meta, obtener_vecinos, costo_movimiento, tipo_heuristica, mapi):
    """Algoritmo A* que encuentra el camino óptimo entre 'inicio' y 'meta'."""
    lista_frontera = []
    lista_interior = []  # Mantener como lista según restricción del usuario

    # Verificar si el inicio o el meta están bloqueados
    if mapi.obtener_tipo_terreno(inicio) == 'obstaculo' or mapi.obtener_tipo_terreno(meta) == 'obstaculo':
        print("EL CONEJO NO PUEDE ALCANZAR LA ZANAHORIA")
        return -1, 0

    # Nodo inicial con la heurística seleccionada y calorías iniciales
    cal_inicial = calcular_caloria(None, inicio, mapi)
    nodo_inicial = Nodo(inicio, None, 0, tipo_heuristica(inicio, meta), cal=cal_inicial)
    heapq.heappush(lista_frontera, nodo_inicial)
    
    f_final = -1  # Coste final, inicialmente -1
    iteracion = 1

    while lista_frontera:
        nodo_actual = heapq.heappop(lista_frontera)

        # Si el nodo actual ya ha sido expandido, lo ignoramos
        if existe_en_lista_interior(lista_interior, nodo_actual.getEstado()):
            continue

        # Añadir el nodo actual a la lista interior (nodos ya explorados)
        lista_interior.append(nodo_actual.getEstado())

        # Mostrar Iteración
        print(f"\nIteración : {iteracion}")
        print(f"Posición actual: ({nodo_actual.getEstado().getFila()},{nodo_actual.getEstado().getCol()})")

        # Mostrar lista_interior
        lista_interior_str = ', '.join([f"({casilla.getFila()},{casilla.getCol()})" for casilla in lista_interior])
        print(f"Lista_interior: {lista_interior_str}")

        # Mostrar lista_frontera
        lista_frontera_str = ' '.join([f"({nodo.getEstado().getFila()},{nodo.getEstado().getCol()})" for nodo in lista_frontera])
        print(f"Lista_frontera: {lista_frontera_str}")

        # Si hemos llegado al nodo destino, reconstruir el camino
        if nodo_actual.getEstado().getFila() == meta.getFila() and nodo_actual.getEstado().getCol() == meta.getCol():
            # Reconstruir el camino desde el nodo final al inicial
            camino_reconstruido, cal = reconstruir_camino(nodo_actual, mapi)
            print("LAS CALORIAS SON", cal)
            
            # Marcar el camino en el mapa cambiando '.' por '*'
            for casilla in camino_reconstruido:
                fila = casilla.getFila()
                columna = casilla.getCol()
                camino[fila][columna] = '*'  # Marcar el camino en el mapa
            
            f_final = nodo_actual.f  # El coste final es el valor de 'f' del nodo meta
            return f_final, cal  # Devolver el coste final y las calorías

        # Inicializar lista_vecinos para esta iteración
        nodos_vecinos = []

        # Expandir los vecinos del nodo actual
        for vecino in obtener_vecinos(nodo_actual.getEstado()):
            if existe_en_lista_interior(lista_interior, vecino):
                continue  # Saltar los nodos que ya fueron expandidos

            # Calcular nuevo g (coste desde el inicio)
            g_nuevo = nodo_actual.g + costo_movimiento(nodo_actual.getEstado(), vecino)
            
            # Calcular las nuevas calorías acumuladas utilizando la función calcular_caloria
            cal_nueva = calcular_caloria(nodo_actual, vecino, mapi)
            
            # Crear un nodo vecino con la heurística seleccionada
            nodo_vecino = Nodo(vecino, nodo_actual, g_nuevo, tipo_heuristica(vecino, meta), cal=cal_nueva)

            # Solo consideramos vecinos que no están en lista_interior ni en lista_frontera
            if not existe_en_lista_frontera(lista_frontera, vecino):
                heapq.heappush(lista_frontera, nodo_vecino)
                nodos_vecinos.append(f"({vecino.getFila()},{vecino.getCol()})")

        # Mostrar vecinos accesibles en esta iteración
        print(f"Nodos_vecinos: {' '.join(nodos_vecinos)}")

        iteracion +=1

    # Si no se encuentra un camino válido
    print("EL CONEJO NO PUEDE ALCANZAR LA ZANAHORIA")
    return -1, -1  # Devuelve -1 para el coste y las calorías si no se encuentra un camino válido

def reconstruir_camino(nodo, mapi):
    """Reconstruir el camino desde el nodo final hasta el inicial."""
    camino = []
    cal = 0
    es_origen = True
    while nodo is not None:
        camino.append(nodo.getEstado())  # Agregar el estado del nodo actual
        # Ignora el nodo de origen en el cálculo de calorías
        if not es_origen:
            # Obtener el tipo de terreno y calcular calorías solo para el camino final
            tipo_terreno = mapi.obtener_tipo_terreno(nodo.getEstado())
            if tipo_terreno == "hierba":
                cal += 2
            elif tipo_terreno == "agua":
                cal += 4
            elif tipo_terreno == "roca":
                cal += 6
            # Imprimir las calorías acumuladas después de cada movimiento
            print(f"Calorías acumuladas tras mover a {tipo_terreno}: {cal}")
        else:
            es_origen = False
        
        nodo = nodo.padre
    return camino[::-1], cal  # Invertir el camino para que vaya desde inicio hasta destino

def calcular_caloria(nodo_padre, estado, mapi):
    """
    Calcula las calorías acumuladas para un nodo.
    :param nodo_padre: El nodo padre.
    :param estado: El estado (Casilla) del nodo actual.
    :param mapi: El mapa que contiene la información de terrenos.
    :return: Calorías acumuladas para el nodo actual.
    """
    tipo_terreno = mapi.obtener_tipo_terreno(estado)
    if tipo_terreno == "hierba":
        cal_terreno = 2
    elif tipo_terreno == "agua":
        cal_terreno = 6
    elif tipo_terreno == "roca":
        cal_terreno = 6
    else:
        cal_terreno = 0  # Por si acaso

    if nodo_padre is not None:
        return nodo_padre.cal + cal_terreno
    else:
        return cal_terreno

