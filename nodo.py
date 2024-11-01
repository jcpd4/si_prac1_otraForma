# nodo.py

class Nodo:
    def __init__(self, estado, padre=None, g=0, h=0, cal=0):
        """
        Clase Nodo para el algoritmo A* Subε.
        :param estado: Objeto Casilla que representa la posición en el mapa.
        :param padre: Nodo padre desde el cual se llegó a este nodo.
        :param g: Costo acumulado desde el inicio hasta este nodo.
        :param h: Heurística estimada desde este nodo hasta el destino.
        :param cal: Calorías acumuladas hasta este nodo.
        """
        self.estado = estado      # Representa el estado (posición en la cuadrícula)
        self.padre = padre        # Nodo padre
        self.g = g                # Coste desde el nodo inicial hasta este nodo
        self.h = h                # Heurística (estimación de la distancia a la meta)
        self.f = g + h            # f = g + h
        self.cal = cal            # Calorías acumuladas

    def getEstado(self):
        return self.estado

    def getCalorias(self):
        """Devuelve las calorías acumuladas hasta este nodo."""
        return self.cal

    def __eq__(self, otro):
        return self.estado == otro.estado

    def __lt__(self, otro):
        """Comparación basada en el valor de f para utilizar heapq."""
        return self.f < otro.f

    def __hash__(self):
        """Hacer que el Nodo sea hashable para usar en conjuntos y diccionarios."""
        return hash(self.estado)

    def __str__(self):
        return f"Nodo(Estado={self.estado}, G={self.g}, H={self.h}, F={self.f}, Cal={self.cal})"
