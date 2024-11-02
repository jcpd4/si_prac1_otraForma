from casilla import Casilla

class Mapa:
    def __init__(self, archivo):        
        self.mapa = leer(archivo)         
        self.alto = len(self.mapa)
        self.ancho = len(self.mapa[0])

    def __str__(self):
        salida = ""
        for f in range(self.alto):
            for c in range(self.ancho):
                if self.mapa[f][c] == 0:
                    salida += "  "
                if self.mapa[f][c] == 1:
                    salida += "# "
                if self.mapa[f][c] == 3:
                    salida += "D "
                if self.mapa[f][c] == 4:
                    salida += "~ "
                if self.mapa[f][c] == 5:
                    salida += "* "
            salida += "\n"
        return salida

    def getAlto(self):
        return self.alto

    def getAncho(self):
        return self.ancho

    def getCelda(self, y, x):
        return self.mapa[y][x]

    def setCelda(self, y, x, valor):
        self.mapa[y][x] = valor

    def getVecinos(self, casilla):
        """
        Devuelve una lista de casillas vecinas a una casilla dada.
        :param casilla: Instancia de la clase Casilla.
        :return: Lista de casillas vecinas accesibles.
        """
        vecinos = []
        filas = self.getAlto()
        columnas = self.getAncho()
        fila, col = casilla.getFila(), casilla.getCol()

        # Movimientos posibles (vertical, horizontal y diagonal)
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1),
                       (-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Comprobar cada posible movimiento
        for movimiento in movimientos:
            nueva_fila = fila + movimiento[0]
            nueva_col = col + movimiento[1]
            
            # Comprobar que esté dentro de los límites del mapa
            if 0 <= nueva_fila < filas and 0 <= nueva_col < columnas:
                if self.getCelda(nueva_fila, nueva_col) != 1:  # Suponiendo que '1' es intransitable
                    vecinos.append(Casilla(nueva_fila, nueva_col))

        return vecinos

    def costo_movimiento(self,casilla1, casilla2):
        # Movimientos horizontales o verticales (costo 1)
        if casilla1.getFila() == casilla2.getFila() or casilla1.getCol() == casilla2.getCol():
            return 1
        # Movimientos diagonales (costo 1.5)
        else:
            return 1.5
    
    def obtener_tipo_terreno(self, casilla):
        """Devuelve el tipo de terreno en una casilla específica."""
        # Suponiendo que tienes un atributo 'mapa' que guarda el tipo de cada casilla
        fila = casilla.getFila()
        columna = casilla.getCol()
        
        tipo = self.mapa[fila][columna]  # Obtenemos el valor del mapa para esa casilla        
        if tipo == 0:
            return "hierba"
        elif tipo == 4:
            return "agua"
        elif tipo == 5:
            return "roca"
        else:
            return "no_transitable"  # Por ejemplo, para celda no transitable



def leer(archivo):
    mapa = []
    try:
        fich = open(archivo, "r")
        fila = -1
        for cadena in fich:
            fila = fila + 1
            mapa.append([])
            for i in range(len(cadena)):
                if cadena[i] == ".":
                    mapa[fila].append(0)
                if cadena[i] == "#":
                    mapa[fila].append(1)
                if cadena[i] == "~":
                    mapa[fila].append(4)
                if cadena[i] == "*":
                    mapa[fila].append(5)
    except:
        print("Error de fichero")
        fich.close()

    fich.close()
    return mapa
