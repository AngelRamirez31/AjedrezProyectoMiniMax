# Tablero.py
from PiezaAjedrez import Rey, Reina, Torre, Alfil, Caballo, Peon, PiezaAjedrez
from copy import deepcopy


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

        # --- LÓGICA DE TABLERO CORREGIDA ---
        # Fila 0 y 1 son NEGRAS
        # Fila 6 y 7 son BLANCAS

        # Negras
        self.rey_negro = Rey("negro", 0, 3, "♚") 
        self.matriz[0][0] = Torre("negro", 0, 0, "♜")
        self.matriz[0][7] = Torre("negro", 0, 7, "♜")
        self.matriz[0][1] = Caballo("negro", 0, 1, "♞")
        self.matriz[0][6] = Caballo("negro", 0, 6, "♞")
        self.matriz[0][2] = Alfil("negro", 0, 2, "♝")
        self.matriz[0][5] = Alfil("negro", 0, 5, "♝")
        self.matriz[0][4] = Reina("negro", 0, 4, "♛")
        self.matriz[0][3] = self.rey_negro
        for col in range(8):
            self.matriz[1][col] = Peon("negro", 1, col, "♟")

        # Blancas
        self.rey_blanco = Rey("blanco", 7, 3, "♔")
        self.matriz[7][0] = Torre("blanco", 7, 0, "♖")
        self.matriz[7][7] = Torre("blanco", 7, 7, "♖")
        self.matriz[7][1] = Caballo("blanco", 7, 1, "♘")
        self.matriz[7][6] = Caballo("blanco", 7, 6, "♘")
        self.matriz[7][2] = Alfil("blanco", 7, 2, "♗")
        self.matriz[7][5] = Alfil("blanco", 7, 5, "♗")
        self.matriz[7][4] = Reina("blanco", 7, 4, "♕")
        self.matriz[7][3] = self.rey_blanco
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

    def realizar_movimiento(
        self, pieza, nueva_fila, nueva_columna, registrar_historial=False
    ):
        fila_antigua, col_antigua = pieza.fila, pieza.columna

        if registrar_historial:
            pieza.historial_posicion.append((fila_antigua, col_antigua))
            pieza.historial_capturas.append(self.matriz[nueva_fila][nueva_columna])
            pieza.historial_movimiento.append(pieza.se_ha_movido) # <-- CORRECCIÓN BUG PEÓN

        pieza_capturada = self.matriz[nueva_fila][nueva_columna]
        if isinstance(pieza_capturada, PiezaAjedrez):
            if pieza_capturada.equipo == "blanco":
                self.piezas_blancas.remove(pieza_capturada)
            else:
                self.piezas_negras.remove(pieza_capturada)

        self.matriz[nueva_fila][nueva_columna] = pieza
        self.matriz[fila_antigua][col_antigua] = "vacio"
        pieza.actualizar_posicion(nueva_fila, nueva_columna) # Llama a la versión por defecto
        
        # --- LÓGICA DE ENROQUE: MOVER TORRE ---
        if isinstance(pieza, Rey) and abs(nueva_columna - col_antigua) == 2:
            if nueva_columna == 6: # Enroque corto
                torre = self.matriz[fila_antigua][7]
                self.matriz[fila_antigua][5] = torre
                self.matriz[fila_antigua][7] = "vacio"
                torre.actualizar_posicion(fila_antigua, 5)
            elif nueva_columna == 2: # Enroque largo
                torre = self.matriz[fila_antigua][0]
                self.matriz[fila_antigua][3] = torre
                self.matriz[fila_antigua][0] = "vacio"
                torre.actualizar_posicion(fila_antigua, 3)

    def deshacer_movimiento(self, pieza):
        fila_actual, col_actual = pieza.fila, pieza.columna
        fila_antigua, col_antigua = pieza.historial_posicion.pop()
        pieza_capturada = pieza.historial_capturas.pop()
        estado_movido_anterior = pieza.historial_movimiento.pop() # <-- CORRECCIÓN BUG PEÓN

        # --- LÓGICA DE ENROQUE: DESHACER MOVIMIENTO DE TORRE ---
        if isinstance(pieza, Rey) and abs(col_actual - col_antigua) == 2:
            if col_actual == 6: # Deshacer enroque corto
                torre = self.matriz[fila_antigua][5]
                self.matriz[fila_antigua][7] = torre
                self.matriz[fila_antigua][5] = "vacio"
                torre.actualizar_posicion(fila_antigua, 7, se_ha_movido_estado=False)
            elif col_actual == 2: # Deshacer enroque largo
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

    def rey_en_jaque(self, equipo_rey):
        rey = self.rey_blanco if equipo_rey == "blanco" else self.rey_negro
        # --- LÓGICA DE OPONENTES CORREGIDA ---
        oponentes = self.piezas_negras if equipo_rey == "blanco" else self.piezas_blancas

        for oponente in oponentes:
            # --- CORRECCIÓN BUG DE RECURSIÓN ---
            # Si el oponente es un Rey, solo revisa sus movimientos básicos.
            if isinstance(oponente, Rey):
                if (rey.fila, rey.columna) in oponente.obtener_movimientos_basicos(self):
                    return True
            else:
                if (rey.fila, rey.columna) in oponente.obtener_movimientos(self):
                    return True
        return False

    def es_casilla_atacada(self, fila, col, equipo_atacado):
        """Comprueba si una casilla está siendo atacada por el equipo oponente."""
        oponentes = self.piezas_negras if equipo_atacado == "blanco" else self.piezas_blancas
        for oponente in oponentes:
            # --- CORRECCIÓN BUG DE RECURSIÓN ---
            if isinstance(oponente, Rey):
                if (fila, col) in oponente.obtener_movimientos_basicos(self):
                    return True
            else:
                if (fila, col) in oponente.obtener_movimientos(self):
                    return True
        return False

    @staticmethod
    def es_valido(fila, col):
        return 0 <= fila < 8 and 0 <= col < 8

    def hay_oponente(self, pieza, fila, col):
        if not self.es_valido(fila, col) or not isinstance(
            self.matriz[fila][col], PiezaAjedrez
        ):
            return False
        # --- CORRECCIÓN BUG "ALFIL COME REY" ---
        # No se puede capturar al rey
        if isinstance(self.matriz[fila][col], Rey):
            return False
        return pieza.equipo != self.matriz[fila][col].equipo

    def hay_aliado(self, pieza, fila, col):
        if not self.es_valido(fila, col) or not isinstance(
            self.matriz[fila][col], PiezaAjedrez
        ):
            return False
        return pieza.equipo == self.matriz[fila][col].equipo

    def es_casilla_vacia(self, fila, col):
        return self.es_valido(fila, col) and not isinstance(
            self.matriz[fila][col], PiezaAjedrez
        )

    def tiene_movimientos_legales(self, equipo):
        piezas = self.piezas_blancas if equipo == "blanco" else self.piezas_negras
        for pieza in piezas:
            if (
                len(
                    pieza.filtrar_movimientos_legales(
                        pieza.obtener_movimientos(self), self
                    )
                )
                > 0
            ):
                return True
        return False

    def es_jaque_mate(self, equipo):
        return self.rey_en_jaque(equipo) and not self.tiene_movimientos_legales(equipo)

    def es_ahogado(self, equipo):
        return not self.rey_en_jaque(equipo) and not self.tiene_movimientos_legales(
            equipo
        )

    def clonar(self):
        return deepcopy(self)

    def evaluar_puntaje(self):
        # --- LÓGICA DE PUNTAJE CORREGIDA ---
        puntaje_blanco = sum([p.valor for p in self.piezas_blancas])
        puntaje_negro = sum([p.valor for p in self.piezas_negras])
        # Positivo = Ganan Blancas (MAX), Negativo = Ganan Negras (MIN)
        return puntaje_blanco - puntaje_negro

    def es_terminal(self):
        return (
            self.es_jaque_mate("negro")
            or self.es_jaque_mate("blanco")
            or self.es_ahogado("negro")
            or self.es_ahogado("blanco")
        )

    def obtener_equipo_jugador(self):
        # --- LÓGICA CORREGIDA ---
        # modo_juego=0 es Humano Blanco, modo_juego=1 es Humano Negro
        return "blanco" if self.modo_juego == 0 else "negro"

    def obtener_representacion_unicode(self):
        rep = []
        for fila_datos in self.matriz:
            fila_simbolos = [
                p.simbolo if isinstance(p, PiezaAjedrez) else "·" for p in fila_datos
            ]
            rep.append(fila_simbolos)
        return rep