# a_estrella_subepsilon.py

import heapq
from nodo import Nodo

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
        return nodo_padre.getCalorias() + cal_terreno
    else:
        return cal_terreno

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

def a_estrella_subepsilon(camino, inicio, meta, obtener_vecinos, costo_movimiento_func, tipo_heuristica, epsilon, mapi):
    """
    Algoritmo A* Subε que relaja la restricción de optimalidad.
    Imprime una traza detallada de cada iteración.

    :param camino: Matriz para marcar el camino encontrado.
    :param inicio: Casilla de inicio.
    :param meta: Casilla de destino.
    :param obtener_vecinos: Función para obtener vecinos de una casilla.
    :param costo_movimiento_func: Función para calcular el costo de movimiento entre casillas.
    :param tipo_heuristica: Función heurística a utilizar.
    :param epsilon: Factor de relajación.
    :param mapi: Objeto Mapa.
    :return: Tupla (coste, calorías) del camino encontrado.
    """
    lista_frontera = []
    lista_interior = []  # Lista de objetos Casilla explorados

    # Nodo inicial con la heurística seleccionada y calorías iniciales
    cal_inicial = calcular_caloria(None, inicio, mapi)
    nodo_inicial = Nodo(inicio, None, 0, tipo_heuristica(inicio, meta), cal=cal_inicial)
    heapq.heappush(lista_frontera, nodo_inicial)

    iteracion = 1

    while lista_frontera:
        # Obtener el nodo con el menor f(n) de lista_frontera para definir la lista focal
        nodo_minimo = lista_frontera[0]  # El nodo con el menor f(n) en lista_frontera
        min_f = nodo_minimo.f
        lista_focal = [nodo for nodo in lista_frontera if nodo.f <= (1 + epsilon) * min_f]

        # Seleccionar el nodo de lista_focal con menor valor de calorías, y si hay empate, menor f(n)
        nodo_actual = min(lista_focal, key=lambda nodo: (nodo.cal, nodo.f))
        lista_frontera.remove(nodo_actual)
        heapq.heapify(lista_frontera)  # Reordenar la lista_frontera después de la eliminación

        # Añadir el nodo actual a la lista interior (nodos ya explorados) si no está ya presente
        if not existe_en_lista_interior(lista_interior, nodo_actual.getEstado()):
            lista_interior.append(nodo_actual.getEstado())

        # Mostrar Iteración
        print(f"\nIteración : {iteracion}")
        print(f"Posición actual: ({nodo_actual.getEstado().getFila()},{nodo_actual.getEstado().getCol()})")

        # Obtener vecinos
        vecinos = obtener_vecinos(nodo_actual.getEstado())
        nodos_vecinos = []
        for vecino in vecinos:
            # Solo consideramos vecinos que no están en lista_interior ni en lista_frontera
            if not existe_en_lista_interior(lista_interior, vecino) and not existe_en_lista_frontera(lista_frontera, vecino):
                nodos_vecinos.append(f"({vecino.getFila()},{vecino.getCol()})")
        print(f"Nodos_vecinos: {' '.join(nodos_vecinos)}")

        # Mostrar lista_interior
        lista_interior_str = ', '.join([f"({casilla.getFila()},{casilla.getCol()})" for casilla in lista_interior])
        print(f"Lista_interior: {lista_interior_str}")

        # Mostrar lista_frontera
        lista_frontera_str = ' '.join([f"({nodo.getEstado().getFila()},{nodo.getEstado().getCol()})" for nodo in lista_frontera])
        print(f"Lista_frontera: {lista_frontera_str}")

        # Verificar si hemos llegado al destino
        if (nodo_actual.getEstado().getFila() == meta.getFila() and
            nodo_actual.getEstado().getCol() == meta.getCol()):
            print("\nCamino encontrado:")
            camino_reconstruido, cal = reconstruir_camino(nodo_actual, mapi, camino)
            mostrar_camino(camino_reconstruido, mapi)
            return nodo_actual.f, cal  # Devolver el coste final y las calorías

        # Expandir los vecinos del nodo actual
        for vecino in vecinos:
            # Verificar si el vecino ya está en lista_interior
            if existe_en_lista_interior(lista_interior, vecino):
                continue

            # Calcular el nuevo coste g
            g_nuevo = nodo_actual.g + costo_movimiento_func(nodo_actual.getEstado(), vecino)

            # Calcular las nuevas calorías acumuladas utilizando la función calcular_caloria
            cal_nueva = calcular_caloria(nodo_actual, vecino, mapi)

            # Crear el nodo vecino con las calorías actualizadas
            nodo_vecino = Nodo(
                estado=vecino,
                padre=nodo_actual,
                g=g_nuevo,
                h=tipo_heuristica(vecino, meta),
                cal=cal_nueva
            )

            # Verificar si el vecino ya está en lista_frontera
            if not existe_en_lista_frontera(lista_frontera, vecino):
                heapq.heappush(lista_frontera, nodo_vecino)

        iteracion +=1

    return -1, -1  # Devuelve -1 para el coste y calorías si no se encuentra un camino válido

def reconstruir_camino(nodo, mapi, camino):
    """
    Reconstruye el camino desde el nodo final hasta el inicial y lo marca en 'camino'.

    :param nodo: Nodo final (destino).
    :param mapi: Objeto Mapa.
    :param camino: Matriz para marcar el camino.
    :return: Lista de casillas que forman el camino y las calorías totales.
    """
    camino_reconstruido = []
    calorias_totales = nodo.getCalorias()
    while nodo is not None:
        camino_reconstruido.append(nodo.getEstado())
        # Marcar el camino en 'camino' con un asterisco '*'
        fila = nodo.getEstado().getFila()
        columna = nodo.getEstado().getCol()
        camino[fila][columna] = '*'  # Puedes cambiar el símbolo si lo prefieres
        nodo = nodo.padre
    camino_reconstruido = camino_reconstruido[::-1]  # Invertir para que vaya desde inicio hasta destino
    return camino_reconstruido, calorias_totales

def mostrar_camino(camino, mapi):
    """
    Imprime el camino encontrado y visualiza el mapa con el camino marcado.

    :param camino: Lista de objetos Casilla que forman el camino.
    :param mapi: Objeto Mapa.
    """
    # Imprimir el camino en formato (fila,columna),(fila,columna),...
    camino_str = ','.join([f"({casilla.getFila()},{casilla.getCol()})" for casilla in camino])
    print(camino_str)

    # Visualización del mapa con el camino marcado ('*')
    print("\nVisualización del Camino en el Mapa:")
    mapa_visual = [
        [mapi.getCelda(fila, columna) for columna in range(mapi.getAncho())]
        for fila in range(mapi.getAlto())
    ]
    for casilla in camino:
        fila = casilla.getFila()
        columna = casilla.getCol()
        mapa_visual[fila][columna] = '*'  # Marca el camino con '*'

    for fila in mapa_visual:
        fila_mostrar = ' '.join([
            '*' if celda == '*' else '.' if celda == 0 else '#' if celda ==1 else '~' if celda==4 else '*' if celda==5 else '.' 
            for celda in fila
        ])
        print(fila_mostrar)

