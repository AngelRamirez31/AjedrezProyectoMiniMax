import math
<<<<<<< HEAD

=======
import random
from Tablero import Tablero 
>>>>>>> 7f3292b4b672311f6396c2145ba8e647fc8d90c4

def algoritmo_minimax(tablero, profundidad, alfa, beta, es_turno_max):

    if profundidad == 0 or tablero.es_terminal():
        return tablero.evaluar_puntaje()

    # Determina que piezas se deben mover en este nivel del arbol
    piezas_a_mover = tablero.piezas_blancas if es_turno_max else tablero.piezas_negras

    if es_turno_max:
        max_puntuacion = -math.inf
        for pieza in piezas_a_mover:
<<<<<<< HEAD
            for movimiento in pieza.filtrar_movimientos_legales(
                pieza.obtener_movimientos(tablero), tablero
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
                    break  # Poda Alfa
            if beta <= alfa:
                break
        return max_puntuacion
    else:  # Turno Minimizador
        min_puntuacion = math.inf
        for pieza in piezas_a_mover:
            for movimiento in pieza.filtrar_movimientos_legales(
                pieza.obtener_movimientos(tablero), tablero
            ):
                tablero.realizar_movimiento(
                    pieza, movimiento[0], movimiento[1], registrar_historial=True
                )
                puntuacion = algoritmo_minimax(
                    tablero, profundidad - 1, alfa, beta, True
                )
=======
            for movimiento in pieza.filtrar_movimientos_legales(pieza.obtener_movimientos(tablero), tablero):
                tablero.realizar_movimiento(pieza, movimiento[0], movimiento[1], registrar_historial=True)
                puntuacion = algoritmo_minimax(tablero, profundidad - 1, alfa, beta, False)
                tablero.deshacer_movimiento(pieza)
                
                max_puntuacion = max(max_puntuacion, puntuacion)
                alfa = max(alfa, puntuacion)
                if beta <= alfa:
                    break # Poda Alfa
            if beta <= alfa:
                break
        return max_puntuacion
    else: # Turno Minimizador
        min_puntuacion = math.inf
        for pieza in piezas_a_mover:
            for movimiento in pieza.filtrar_movimientos_legales(pieza.obtener_movimientos(tablero), tablero):
                tablero.realizar_movimiento(pieza, movimiento[0], movimiento[1], registrar_historial=True)
                puntuacion = algoritmo_minimax(tablero, profundidad - 1, alfa, beta, True)
>>>>>>> 7f3292b4b672311f6396c2145ba8e647fc8d90c4
                tablero.deshacer_movimiento(pieza)

                min_puntuacion = min(min_puntuacion, puntuacion)
                beta = min(beta, puntuacion)
                if beta <= alfa:
<<<<<<< HEAD
                    break  # Poda Beta
=======
                    break # Poda Beta
>>>>>>> 7f3292b4b672311f6396c2145ba8e647fc8d90c4
            if beta <= alfa:
                break
        return min_puntuacion

<<<<<<< HEAD

def obtener_movimiento_ia(tablero):
    mejor_movimiento = None

    # Determina el rol de la IA
    equipo_humano = tablero.obtener_equipo_jugador()
    equipo_ia = "negro" if equipo_humano == "blanco" else "blanco"

    es_turno_max_ia = equipo_ia == "blanco"
=======
def obtener_movimiento_ia(tablero):
    mejor_movimiento = None
    
    # Determina el rol de la IA
    equipo_humano = tablero.obtener_equipo_jugador()
    equipo_ia = 'negro' if equipo_humano == 'blanco' else 'blanco'
    
    es_turno_max_ia = (equipo_ia == 'blanco')
>>>>>>> 7f3292b4b672311f6396c2145ba8e647fc8d90c4

    if es_turno_max_ia:
        mejor_puntuacion = -math.inf
        piezas_ia = tablero.piezas_blancas
    else:
        mejor_puntuacion = math.inf
        piezas_ia = tablero.piezas_negras

    # Itera sobre todos los movimientos posibles para la IA
    for pieza in piezas_ia:
<<<<<<< HEAD
        for movimiento in pieza.filtrar_movimientos_legales(
            pieza.obtener_movimientos(tablero), tablero
        ):
            # Simula el movimiento
            tablero.realizar_movimiento(
                pieza, movimiento[0], movimiento[1], registrar_historial=True
            )
            # Evalua la posicion resultante con Minimax
            puntuacion = algoritmo_minimax(
                tablero,
                tablero.profundidad - 1,
                -math.inf,
                math.inf,
                not es_turno_max_ia,
            )
=======
        for movimiento in pieza.filtrar_movimientos_legales(pieza.obtener_movimientos(tablero), tablero):
            # Simula el movimiento
            tablero.realizar_movimiento(pieza, movimiento[0], movimiento[1], registrar_historial=True)
            # Evalua la posicion resultante con Minimax
            puntuacion = algoritmo_minimax(tablero, tablero.profundidad - 1, -math.inf, math.inf, not es_turno_max_ia)
>>>>>>> 7f3292b4b672311f6396c2145ba8e647fc8d90c4
            # Deshace el movimiento para probar el siguiente
            tablero.deshacer_movimiento(pieza)

            # Actualiza el mejor movimiento encontrado hasta ahora
<<<<<<< HEAD
            if es_turno_max_ia:  # La IA es blanca y busca maximizar
                if puntuacion > mejor_puntuacion:
                    mejor_puntuacion = puntuacion
                    mejor_movimiento = (pieza, movimiento)
            else:  # La IA es negra y busca minimizar
=======
            if es_turno_max_ia: # La IA es blanca y busca maximizar
                if puntuacion > mejor_puntuacion:
                    mejor_puntuacion = puntuacion
                    mejor_movimiento = (pieza, movimiento)
            else: # La IA es negra y busca minimizar
>>>>>>> 7f3292b4b672311f6396c2145ba8e647fc8d90c4
                if puntuacion < mejor_puntuacion:
                    mejor_puntuacion = puntuacion
                    mejor_movimiento = (pieza, movimiento)

    # Realiza el mejor movimiento en el tablero real
    if mejor_movimiento:
        pieza_a_mover, mov_a_realizar = mejor_movimiento
<<<<<<< HEAD
        print(
            f"IA mueve {pieza_a_mover.tipo} de ({pieza_a_mover.fila},{pieza_a_mover.columna}) a ({mov_a_realizar[0]},{mov_a_realizar[1]})"
        )
        tablero.realizar_movimiento(pieza_a_mover, mov_a_realizar[0], mov_a_realizar[1])
    else:
        print("La IA no encontro movimientos posibles (Jaque Mate o Ahogado).")
=======
        print(f"IA mueve {pieza_a_mover.tipo} de ({pieza_a_mover.fila},{pieza_a_mover.columna}) a ({mov_a_realizar[0]},{mov_a_realizar[1]})")
        tablero.realizar_movimiento(pieza_a_mover, mov_a_realizar[0], mov_a_realizar[1])
    else:
        print("La IA no encontro movimientos posibles (Jaque Mate o Ahogado).")
>>>>>>> 7f3292b4b672311f6396c2145ba8e647fc8d90c4
