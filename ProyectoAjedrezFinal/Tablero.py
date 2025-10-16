# Tablero.py
from PiezaAjedrez import *
from copy import deepcopy

class Tablero:
    def __init__(self, modo_juego=0, es_ia=False, profundidad_ia=2, registrar=False):
        self.matriz = []
        self.piezas_blancas = []
        self.piezas_negras = []
        self.modo_juego = modo_juego
        
        # Atributos para la minimax
        self.es_ia = es_ia
        self.profundidad = profundidad_ia
        self.registrar = registrar
        
        self.rey_blanco = None
        self.rey_negro = None
        self.colocar_piezas_iniciales()

    def __getitem__(self, indice):
        return self.matriz[indice]

    def colocar_piezas_iniciales(self):
        # Se limpia y reinicia el tablero
        self.matriz = [['vacio' for _ in range(8)] for _ in range(8)]
        
        # Se colocan las piezas en su posición inicial
        self.rey_blanco = Rey('blanco', 0, 4, '♔')
        self.rey_negro = Rey('negro', 7, 4, '♚')
        
        # Peones
        for col in range(8):
            self.matriz[1][col] = Peon('blanco', 1, col, '♙')
            self.matriz[6][col] = Peon('negro', 6, col, '♟')
        
        # Blancas
        self.matriz[0][0] = Torre('blanco', 0, 0, '♖')
        self.matriz[0][7] = Torre('blanco', 0, 7, '♖')
        self.matriz[0][1] = Caballo('blanco', 0, 1, '♘')
        self.matriz[0][6] = Caballo('blanco', 0, 6, '♘')
        self.matriz[0][2] = Alfil('blanco', 0, 2, '♗')
        self.matriz[0][5] = Alfil('blanco', 0, 5, '♗')
        self.matriz[0][3] = Reina('blanco', 0, 3, '♕')
        self.matriz[0][4] = self.rey_blanco
        
        # Negras
        self.matriz[7][0] = Torre('negro', 7, 0, '♜')
        self.matriz[7][7] = Torre('negro', 7, 7, '♜')
        self.matriz[7][1] = Caballo('negro', 7, 1, '♞')
        self.matriz[7][6] = Caballo('negro', 7, 6, '♞')
        self.matriz[7][2] = Alfil('negro', 7, 2, '♝')
        self.matriz[7][5] = Alfil('negro', 7, 5, '♝')
        self.matriz[7][3] = Reina('negro', 7, 3, '♛')
        self.matriz[7][4] = self.rey_negro
        
        self._actualizar_listas_piezas()

    def _actualizar_listas_piezas(self):
        self.piezas_blancas.clear()
        self.piezas_negras.clear()
        for fila in self.matriz:
            for pieza in fila:
                if isinstance(pieza, PiezaAjedrez):
                    if pieza.equipo == 'blanco':
                        self.piezas_blancas.append(pieza)
                    else:
                        self.piezas_negras.append(pieza)

    def realizar_movimiento(self, pieza, nueva_fila, nueva_columna, registrar_historial=False):
        fila_antigua, col_antigua = pieza.fila, pieza.columna
        
        # Lógica para la IA (deshacer movimientos)
        if registrar_historial:
            pieza.historial_posicion.append((fila_antigua, col_antigua))
            pieza.historial_capturas.append(self.matriz[nueva_fila][nueva_columna])
        
        # Elimina pieza capturada de las listas
        pieza_capturada = self.matriz[nueva_fila][nueva_columna]
        if isinstance(pieza_capturada, PiezaAjedrez):
            if pieza_capturada.equipo == 'blanco':
                self.piezas_blancas.remove(pieza_capturada)
            else:
                self.piezas_negras.remove(pieza_capturada)
        
        self.matriz[nueva_fila][nueva_columna] = pieza
        self.matriz[fila_antigua][col_antigua] = 'vacio'
        pieza.actualizar_posicion(nueva_fila, nueva_columna)

    def deshacer_movimiento(self, pieza):
        # Lógica exclusiva para la IA
        fila_actual, col_actual = pieza.fila, pieza.columna
        fila_antigua, col_antigua = pieza.historial_posicion.pop()
        pieza_capturada = pieza.historial_capturas.pop()
        
        # Restaura la pieza a su posición original
        self.matriz[fila_antigua][col_antigua] = pieza
        pieza.actualizar_posicion(fila_antigua, col_antigua)
        
        # Devuelve la pieza capturada al tablero y a la lista
        self.matriz[fila_actual][col_actual] = pieza_capturada
        if isinstance(pieza_capturada, PiezaAjedrez):
            if pieza_capturada.equipo == 'blanco':
                self.piezas_blancas.append(pieza_capturada)
            else:
                self.piezas_negras.append(pieza_capturada)
        
    def rey_en_jaque(self, equipo_rey):
        rey = self.rey_blanco if equipo_rey == 'blanco' else self.rey_negro
        oponentes = self.piezas_negras if equipo_rey == 'blanco' else self.piezas_blancas
        
        for oponente in oponentes:
            if (rey.fila, rey.columna) in oponente.obtener_movimientos(self):
                return True
        return False

    # --- Funciones de ayuda y validación ---
    @staticmethod
    def es_valido(fila, col):
        return 0 <= fila < 8 and 0 <= col < 8

    def hay_oponente(self, pieza, fila, col):
        if not self.es_valido(fila, col) or not isinstance(self.matriz[fila][col], PiezaAjedrez):
            return False
        return pieza.equipo != self.matriz[fila][col].equipo

    def hay_aliado(self, pieza, fila, col):
        if not self.es_valido(fila, col) or not isinstance(self.matriz[fila][col], PiezaAjedrez):
            return False
        return pieza.equipo == self.matriz[fila][col].equipo

    def es_casilla_vacia(self, fila, col):
        return self.es_valido(fila, col) and not isinstance(self.matriz[fila][col], PiezaAjedrez)

    # --- Lógica de fin de juego ---
    def tiene_movimientos_legales(self, equipo):
        piezas = self.piezas_blancas if equipo == 'blanco' else self.piezas_negras
        for pieza in piezas:
            if len(pieza.filtrar_movimientos_legales(pieza.obtener_movimientos(self), self)) > 0:
                return True
        return False

    def es_jaque_mate(self, equipo):
        return self.rey_en_jaque(equipo) and not self.tiene_movimientos_legales(equipo)

    def es_ahogado(self, equipo):
        return not self.rey_en_jaque(equipo) and not self.tiene_movimientos_legales(equipo)
        
    def clonar(self):
        return deepcopy(self)

    # --- Funciones para la IA ---
    def evaluar_puntaje(self):
        puntaje_blanco = sum([p.valor for p in self.piezas_blancas])
        puntaje_negro = sum([p.valor for p in self.piezas_negras])
        # Devuelve la diferencia desde la perspectiva del jugador actual
        return puntaje_blanco - puntaje_negro

    def es_terminal(self):
        return self.es_jaque_mate('blanco') or self.es_jaque_mate('negro') or self.es_ahogado('blanco') or self.es_ahogado('negro')
        
    def obtener_equipo_jugador(self):
        return 'blanco' if self.modo_juego == 0 else 'negro'
        
    def obtener_representacion_unicode(self):
        rep = []
        for fila_datos in self.matriz:
            fila_simbolos = [p.simbolo if isinstance(p, PiezaAjedrez) else '·' for p in fila_datos]
            rep.append(fila_simbolos)
        return rep