import math
import random
import pygame  # <--- AÑADIDO 1: Importamos Pygame
import sys     # <--- AÑADIDO 2: Importamos Sys (para salir)
from Tablero import Tablero 
from PiezaAjedrez import PiezaAjedrez

def algoritmo_minimax(tablero, profundidad, alfa, beta, es_turno_max):
    """
    Esta función no se modifica.
    """
    if profundidad == 0 or tablero.es_terminal():
        return tablero.evaluar_puntaje()

    piezas_a_mover = tablero.piezas_blancas if es_turno_max else tablero.piezas_negras

    if es_turno_max:
        max_puntuacion = -math.inf
        for pieza in random.sample(piezas_a_mover, len(piezas_a_mover)):
            for movimiento in random.sample(
                pieza.filtrar_movimientos_legales(pieza.obtener_movimientos(tablero), tablero),
                len(pieza.filtrar_movimientos_legales(pieza.obtener_movimientos(tablero), tablero))
            ):
                tablero.realizar_movimiento(
                    pieza, movimiento[0], movimiento[1], registrar_historial=True
                )
                puntuacion = algoritmo_minimax(
                    tablero, profundidad - 1, alfa, beta, False
                )
                tablero.deshacer_movimiento(pieza)

                max_puntuacion = max(max_puntuacion, puntuacion)
                alfa = max(alfa, puntuacion)
                if beta <= alfa:
                    break 
            if beta <= alfa:
                break
        return max_puntuacion
    else: # Turno Minimizador
        min_puntuacion = math.inf
        for pieza in random.sample(piezas_a_mover, len(piezas_a_mover)):
            for movimiento in random.sample(
                pieza.filtrar_movimientos_legales(pieza.obtener_movimientos(tablero), tablero),
                len(pieza.filtrar_movimientos_legales(pieza.obtener_movimientos(tablero), tablero))
            ):
                tablero.realizar_movimiento(
                    pieza, movimiento[0], movimiento[1], registrar_historial=True
                )
                puntuacion = algoritmo_minimax(
                    tablero, profundidad - 1, alfa, beta, True
                )
                tablero.deshacer_movimiento(pieza)

                min_puntuacion = min(min_puntuacion, puntuacion)
                beta = min(beta, puntuacion)
                if beta <= alfa:
                    break 
            if beta <= alfa:
                break
        return min_puntuacion


def obtener_movimiento_ia(tablero):
    mejor_movimiento = None
    equipo_humano = tablero.obtener_equipo_jugador()
    equipo_ia = "negro" if equipo_humano == "blanco" else "blanco"
    es_turno_max_ia = equipo_ia == "blanco"

    if es_turno_max_ia:
        mejor_puntuacion = -math.inf
        piezas_ia = tablero.piezas_blancas
    else:
        mejor_puntuacion = math.inf
        piezas_ia = tablero.piezas_negras

    movimientos_posibles = []
    for pieza in piezas_ia:
        for movimiento in pieza.filtrar_movimientos_legales(
            pieza.obtener_movimientos(tablero), tablero
        ):
            movimientos_posibles.append((pieza, movimiento))
    
    random.shuffle(movimientos_posibles) 

    # --- BUCLE DE PENSAMIENTO DE LA IA ---
    for pieza, movimiento in movimientos_posibles:
        
        # --- ¡CORRECCIÓN DE "NO RESPONDE"! ---
        # AÑADIDO 3: Le damos un "respiro" a Pygame en cada iteración
        # para que procese eventos y la ventana no se congele.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Juego cerrado durante el pensamiento de la IA.")
                pygame.quit()
                sys.exit()
        # --- FIN DE LA CORRECCIÓN ---

        tablero.realizar_movimiento(
            pieza, movimiento[0], movimiento[1], registrar_historial=True
        )
        puntuacion = algoritmo_minimax(
            tablero,
            tablero.profundidad - 1,
            -math.inf,
            math.inf,
            not es_turno_max_ia,
        )
        tablero.deshacer_movimiento(pieza)

        if es_turno_max_ia: 
            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_movimiento = (pieza, movimiento)
        else: 
            if puntuacion < mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_movimiento = (pieza, movimiento)

    if mejor_movimiento:
        pieza_a_mover, mov_a_realizar = mejor_movimiento
        print(
            f"IA mueve {pieza_a_mover.tipo} de ({pieza_a_mover.fila},{pieza_a_mover.columna}) a ({mov_a_realizar[0]},{mov_a_realizar[1]})"
        )
        tablero.realizar_movimiento(pieza_a_mover, mov_a_realizar[0], mov_a_realizar[1])
    else:
        print("La IA no encontro movimientos posibles (Jaque Mate o Ahogado).")