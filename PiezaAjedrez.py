import operator
from itertools import product

class PiezaAjedrez:
    def __init__(self, equipo, fila, columna, simbolo):
        self.se_ha_movido = False
        self.equipo = equipo
        self.fila = fila
        self.columna = columna
        self.tipo = self.__class__.__name__
        self.simbolo = simbolo
        self.valor = {'Peon': 10, 'Caballo': 30, 'Alfil': 30, 'Torre': 50, 'Reina': 90, 'Rey': 900}.get(self.tipo, 0)
        self.historial_posicion = []
        self.historial_capturas = []

    def filtrar_movimientos_legales(self, posibles_movimientos, tablero):
        movimientos_finales = []
        for mov in posibles_movimientos:
            tablero_simulado = tablero.clonar()
            pieza_a_mover = tablero_simulado.matriz[self.fila][self.columna]
            tablero_simulado.realizar_movimiento(pieza_a_mover, mov[0], mov[1])

            if not tablero_simulado.rey_en_jaque(self.equipo):
                movimientos_finales.append(mov)
        return movimientos_finales

    def obtener_movimientos(self, tablero):
        pass

    def actualizar_posicion(self, nueva_fila, nueva_columna):
        self.fila = nueva_fila
        self.columna = nueva_columna
        self.se_ha_movido = True

    def __repr__(self):
        return f'{self.tipo}: {self.equipo}|({self.fila},{self.columna})'

class Peon(PiezaAjedrez):
    def obtener_movimientos(self, tablero):
        movimientos = []
        direccion = 1 if self.equipo == 'blanco' else -1
        nueva_fila = self.fila + direccion
        if tablero.es_casilla_vacia(nueva_fila, self.columna):
            movimientos.append((nueva_fila, self.columna))
            if not self.se_ha_movido and tablero.es_casilla_vacia(nueva_fila + direccion, self.columna):
                movimientos.append((nueva_fila + direccion, self.columna))
        for d_col in [-1, 1]:
            if tablero.es_valido(nueva_fila, self.columna + d_col) and tablero.hay_oponente(self, nueva_fila, self.columna + d_col):
                movimientos.append((nueva_fila, self.columna + d_col))
        return movimientos

class Caballo(PiezaAjedrez):
    def obtener_movimientos(self, tablero):
        movimientos = []
        saltos_posibles = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for salto in saltos_posibles:
            nueva_fila, nueva_columna = self.fila + salto[0], self.columna + salto[1]
            if tablero.es_valido(nueva_fila, nueva_columna) and not tablero.hay_aliado(self, nueva_fila, nueva_columna):
                movimientos.append((nueva_fila, nueva_columna))
        return movimientos

class Alfil(PiezaAjedrez):
    def obtener_movimientos(self, tablero):
        movimientos = []
        direcciones = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for d in direcciones:
            for i in range(1, 8):
                nueva_fila, nueva_columna = self.fila + d[0] * i, self.columna + d[1] * i
                if not tablero.es_valido(nueva_fila, nueva_columna) or tablero.hay_aliado(self, nueva_fila, nueva_columna): break
                movimientos.append((nueva_fila, nueva_columna))
                if tablero.hay_oponente(self, nueva_fila, nueva_columna): break
        return movimientos

class Torre(PiezaAjedrez):
    def obtener_movimientos(self, tablero):
        movimientos = []
        direcciones = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for d in direcciones:
            for i in range(1, 8):
                nueva_fila, nueva_columna = self.fila + d[0] * i, self.columna + d[1] * i
                if not tablero.es_valido(nueva_fila, nueva_columna) or tablero.hay_aliado(self, nueva_fila, nueva_columna): break
                movimientos.append((nueva_fila, nueva_columna))
                if tablero.hay_oponente(self, nueva_fila, nueva_columna): break
        return movimientos

class Reina(PiezaAjedrez):
    def obtener_movimientos(self, tablero):
        movimientos = []
        movimientos.extend(Torre(self.equipo, self.fila, self.columna, self.simbolo).obtener_movimientos(tablero))
        movimientos.extend(Alfil(self.equipo, self.fila, self.columna, self.simbolo).obtener_movimientos(tablero))
        return movimientos

class Rey(PiezaAjedrez):
    def obtener_movimientos(self, tablero):
        movimientos = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0: continue
                nueva_fila, nueva_columna = self.fila + i, self.columna + j
                if tablero.es_valido(nueva_fila, nueva_columna) and not tablero.hay_aliado(self, nueva_fila, nueva_columna):
                    movimientos.append((nueva_fila, nueva_columna))
        return movimientos