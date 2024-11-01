class Casilla:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def getFila(self):
        return self.fila

    def getCol(self):
        return self.columna

    def __str__(self):
        return f"({self.fila}, {self.columna})"
