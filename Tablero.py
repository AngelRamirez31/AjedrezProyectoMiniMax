from PiezaAjedrez import Rey, Reina, Torre, Alfil, Caballo, Peon, PiezaAjedrez
from copy import deepcopy

# TABLAS DE POSICIÓN (Perspectiva Blancas) 
# Valores positivos premian buenas posiciones (centro, avance)
PEON_TABLA = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [0,  0,  0, 20, 20,  0,  0,  0],
    [5, -5,-10,  0,  0,-10, -5,  5],
    [5, 10, 10,-20,-20, 10, 10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]
]

CABALLO_TABLA = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

ALFIL_TABLA = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

TORRE_TABLA = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [0,  0,  0,  5,  5,  0,  0,  0]
]

REINA_TABLA = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [-5,  0,  5,  5,  5,  5,  0, -5],
    [0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

REY_TABLA = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [20, 20,  0,  0,  0,  0, 20, 20],
    [20, 30, 10,  0,  0, 10, 30, 20]
]

TABLAS_DE_POSICION = {
    "Peon": PEON_TABLA,
    "Caballo": CABALLO_TABLA,
    "Alfil": ALFIL_TABLA,
    "Torre": TORRE_TABLA,
    "Reina": REINA_TABLA,
    "Rey": REY_TABLA
}


class Tablero:
    def __init__(self, modo_juego=0, es_ia=False, profundidad_ia=2, registrar=False):
        self.matriz = []
        self.piezas_blancas = []
        self.piezas_negras = []
        self.modo_juego = modo_juego
        self.es_ia = es_ia
        self.profundidad = profundidad_ia
        self.registrar = registrar
        self.rey_negro = None
        self.rey_blanco = None
        self.colocar_piezas_iniciales()

    def __getitem__(self, indice):
        return self.matriz[indice]

    def colocar_piezas_iniciales(self):
        self.matriz = [["vacio" for _ in range(8)] for _ in range(8)]

        # Negras
        self.rey_negro = Rey("negro", 0, 4, "♚")
        self.matriz[0][0] = Torre("negro", 0, 0, "♜")
        self.matriz[0][7] = Torre("negro", 0, 7, "♜")
        self.matriz[0][1] = Caballo("negro", 0, 1, "♞")
        self.matriz[0][6] = Caballo("negro", 0, 6, "♞")
        self.matriz[0][2] = Alfil("negro", 0, 2, "♝")
        self.matriz[0][5] = Alfil("negro", 0, 5, "♝")
        self.matriz[0][3] = Reina("negro", 0, 3, "♛") 
        self.matriz[0][4] = self.rey_negro           
        for col in range(8):
            self.matriz[1][col] = Peon("negro", 1, col, "♟")

        # Blancas
        self.rey_blanco = Rey("blanco", 7, 4, "♔")
        self.matriz[7][0] = Torre("blanco", 7, 0, "♖")
        self.matriz[7][7] = Torre("blanco", 7, 7, "♖")
        self.matriz[7][1] = Caballo("blanco", 7, 1, "♘")
        self.matriz[7][6] = Caballo("blanco", 7, 6, "♘")
        self.matriz[7][2] = Alfil("blanco", 7, 2, "♗")
        self.matriz[7][5] = Alfil("blanco", 7, 5, "♗")
        self.matriz[7][3] = Reina("blanco", 7, 3, "♕") 
        self.matriz[7][4] = self.rey_blanco            
        for col in range(8):
            self.matriz[6][col] = Peon("blanco", 6, col, "♙")

        self._actualizar_listas_piezas()

    def _actualizar_listas_piezas(self):
        self.piezas_blancas.clear()
        self.piezas_negras.clear()
        for fila in self.matriz:
            for pieza in fila:
                if isinstance(pieza, PiezaAjedrez):
                    if pieza.equipo == "blanco":
                        self.piezas_blancas.append(pieza)
                    else:
                        self.piezas_negras.append(pieza)

    def realizar_movimiento(self, pieza, nueva_fila, nueva_columna, registrar_historial=False):
        fila_antigua, col_antigua = pieza.fila, pieza.columna

        if registrar_historial:
            pieza.historial_posicion.append((fila_antigua, col_antigua))
            pieza.historial_capturas.append(self.matriz[nueva_fila][nueva_columna])
            pieza.historial_movimiento.append(pieza.se_ha_movido)

        pieza_capturada = self.matriz[nueva_fila][nueva_columna]
        if isinstance(pieza_capturada, PiezaAjedrez):
            if pieza_capturada.equipo == "blanco":
                self.piezas_blancas.remove(pieza_capturada)
            else:
                self.piezas_negras.remove(pieza_capturada)

        self.matriz[nueva_fila][nueva_columna] = pieza
        self.matriz[fila_antigua][col_antigua] = "vacio"
        pieza.actualizar_posicion(nueva_fila, nueva_columna)
        
        # Enroque
        if isinstance(pieza, Rey) and abs(nueva_columna - col_antigua) == 2:
            if nueva_columna == 6: # Corto
                torre = self.matriz[fila_antigua][7]
                self.matriz[fila_antigua][5] = torre
                self.matriz[fila_antigua][7] = "vacio"
                torre.actualizar_posicion(fila_antigua, 5)
            elif nueva_columna == 2: # Largo
                torre = self.matriz[fila_antigua][0]
                self.matriz[fila_antigua][3] = torre
                self.matriz[fila_antigua][0] = "vacio"
                torre.actualizar_posicion(fila_antigua, 3)

    def deshacer_movimiento(self, pieza):
        fila_actual, col_actual = pieza.fila, pieza.columna
        fila_antigua, col_antigua = pieza.historial_posicion.pop()
        pieza_capturada = pieza.historial_capturas.pop()
        estado_movido_anterior = pieza.historial_movimiento.pop()

        # Deshacer Enroque
        if isinstance(pieza, Rey) and abs(col_actual - col_antigua) == 2:
            if col_actual == 6:
                torre = self.matriz[fila_antigua][5]
                self.matriz[fila_antigua][7] = torre
                self.matriz[fila_antigua][5] = "vacio"
                torre.actualizar_posicion(fila_antigua, 7, se_ha_movido_estado=False)
            elif col_actual == 2:
                torre = self.matriz[fila_antigua][3]
                self.matriz[fila_antigua][0] = torre
                self.matriz[fila_antigua][3] = "vacio"
                torre.actualizar_posicion(fila_antigua, 0, se_ha_movido_estado=False)

        self.matriz[fila_antigua][col_antigua] = pieza
        pieza.actualizar_posicion(fila_antigua, col_antigua, se_ha_movido_estado=estado_movido_anterior)

        self.matriz[fila_actual][col_actual] = pieza_capturada
        if isinstance(pieza_capturada, PiezaAjedrez):
            if pieza_capturada.equipo == "blanco":
                self.piezas_blancas.append(pieza_capturada)
            else:
                self.piezas_negras.append(pieza_capturada)

    def promocionar_peon(self, fila, col, tipo_pieza):
        pieza_actual = self.matriz[fila][col]
        equipo = pieza_actual.equipo
        
        nueva_pieza = None
        if tipo_pieza == 'Reina':
            nueva_pieza = Reina(equipo, fila, col, "♕" if equipo == "blanco" else "♛")
        elif tipo_pieza == 'Torre':
            nueva_pieza = Torre(equipo, fila, col, "♖" if equipo == "blanco" else "♜")
        elif tipo_pieza == 'Alfil':
            nueva_pieza = Alfil(equipo, fila, col, "♗" if equipo == "blanco" else "♝")
        elif tipo_pieza == 'Caballo':
            nueva_pieza = Caballo(equipo, fila, col, "♘" if equipo == "blanco" else "♞")
            
        if nueva_pieza:
            self.matriz[fila][col] = nueva_pieza
            lista_aliada = self.piezas_blancas if equipo == "blanco" else self.piezas_negras
            if pieza_actual in lista_aliada:
                lista_aliada.remove(pieza_actual)
            lista_aliada.append(nueva_pieza)

    def es_casilla_atacada(self, fila, col, equipo_atacado):
        oponentes = self.piezas_negras if equipo_atacado == "blanco" else self.piezas_blancas
        for oponente in oponentes:
            if isinstance(oponente, Peon):
                direccion = -1 if oponente.equipo == "blanco" else 1
                fila_ataque = oponente.fila + direccion
                if fila == fila_ataque and abs(oponente.columna - col) == 1:
                    return True
            elif isinstance(oponente, Rey):
                # Usamos movimientos basicos para evitar recursión infinita.
                if hasattr(oponente, 'obtener_movimientos_basicos'):
                    if (fila, col) in oponente.obtener_movimientos_basicos(self):
                        return True
                else:
                     if (fila, col) in oponente.obtener_movimientos(self):
                        return True
            else:
                if (fila, col) in oponente.obtener_movimientos(self):
                    return True
        return False

    def rey_en_jaque(self, equipo_rey):
        rey = self.rey_blanco if equipo_rey == "blanco" else self.rey_negro
        if not rey: return False # Seguridad
        return self.es_casilla_atacada(rey.fila, rey.columna, equipo_rey)

    # Validaciones estandar
    @staticmethod
    def es_valido(fila, col):
        return 0 <= fila < 8 and 0 <= col < 8

    def hay_oponente(self, pieza, fila, col):
        if not self.es_valido(fila, col) or not isinstance(self.matriz[fila][col], PiezaAjedrez):
            return False
        if isinstance(self.matriz[fila][col], Rey):
            return False 
        return pieza.equipo != self.matriz[fila][col].equipo

    def hay_aliado(self, pieza, fila, col):
        if not self.es_valido(fila, col) or not isinstance(self.matriz[fila][col], PiezaAjedrez):
            return False
        return pieza.equipo == self.matriz[fila][col].equipo

    def es_casilla_vacia(self, fila, col):
        return self.es_valido(fila, col) and not isinstance(self.matriz[fila][col], PiezaAjedrez)

    def tiene_movimientos_legales(self, equipo):
        piezas = self.piezas_blancas if equipo == "blanco" else self.piezas_negras
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

    def evaluar_puntaje(self):
        puntaje_blanco = 0
        puntaje_negro = 0

        for pieza in self.piezas_blancas:
            puntaje_blanco += pieza.valor
            if TABLAS_DE_POSICION and pieza.tipo in TABLAS_DE_POSICION:

                puntaje_blanco += TABLAS_DE_POSICION[pieza.tipo][pieza.fila][pieza.columna]

        for pieza in self.piezas_negras:
            puntaje_negro += pieza.valor
            if TABLAS_DE_POSICION and pieza.tipo in TABLAS_DE_POSICION:

                puntaje_negro += TABLAS_DE_POSICION[pieza.tipo][7 - pieza.fila][pieza.columna]

        return puntaje_blanco - puntaje_negro

    def es_terminal(self):
        return (self.es_jaque_mate("negro") or self.es_jaque_mate("blanco") or 
                self.es_ahogado("negro") or self.es_ahogado("blanco"))

    def obtener_equipo_jugador(self):
        return "blanco" if self.modo_juego == 0 else "negro"

    def obtener_representacion_unicode(self):
        rep = []
        for fila_datos in self.matriz:
            fila_simbolos = [p.simbolo if isinstance(p, PiezaAjedrez) else "·" for p in fila_datos]
            rep.append(fila_simbolos)
        return rep