from Tablero import Tablero
from PiezaAjedrez import PiezaAjedrez 
from InteligenciaArtificial import obtener_movimiento_ia

def imprimir_tablero_consola(tablero):
    print("\n   y: 0  1  2  3  4  5  6  7")
    print("x: --------------------------")
    representacion = tablero.obtener_representacion_unicode()
    
    # Imprime el tablero desde la fila 7 hasta la 0 para que las blancaSs queden abajo
    for i in range(7, -1, -1):
        fila_texto = ' '.join(representacion[i])
        print(f"{i}|   {fila_texto}")

def iniciar_partida():

    # Si eliges 1 eres blancas, sino eres negras, profundidad 3.
    tablero = Tablero(modo_juego=1, es_ia=True, profundidad_ia= 3)
    
    equipo_humano = tablero.obtener_equipo_jugador()
    turno_actual = 'blanco'

    # Bucle principal del juego
    while True:
        imprimir_tablero_consola(tablero)

        # Se revisa si el juego ha terminado
        if tablero.es_jaque_mate(turno_actual):
            ganador = 'Negras' if turno_actual == 'blanco' else 'Blancas'
            print(f"\n¡¡JAQUE MATE!! Ganan las {ganador}")
            break
        if tablero.es_ahogado(turno_actual):
            print("\n¡PARTIDA EN TABLAS! El resultado es un empate por ahogado.")
            break

        # Determina si es turno del jugador o de la IA
        if turno_actual == equipo_humano:
            print(f"\n- Tu turno ({equipo_humano}) -")
            
            jugada_valida = False
            while not jugada_valida:
                try:
                    entrada = input("Ingresa tu jugada (fila_inicial col_inicial fila_final col_final): ")
                    
                    # Procesa y valida la entrada 
                    partes = entrada.split()
                    if len(partes) != 4:
                        print(" ERROR: Debes introducir exactamente 4 números. ")
                        continue # Vuelve a pedir la jugada
                    
                    coords = list(map(int, partes))
                    fila_i, col_i, fila_f, col_f = coords

                    # Valida la logica del movimiento 
                    if not (0 <= fila_i <= 7 and 0 <= col_i <= 7 and 0 <= fila_f <= 7 and 0 <= col_f <= 7):
                        print(" ERROR: Las coordenadas deben estar entre 0 y 7. ")
                        continue

                    pieza = tablero[fila_i][col_i]
                    if not isinstance(pieza, PiezaAjedrez):
                        print(" ERROR: No hay ninguna pieza en la casilla de inicio. ")
                        continue
                    if pieza.equipo != equipo_humano:
                        print(f"ERROR: La pieza en ({fila_i},{col_i}) es del equipo contrario.")
                        continue

                    movimientos_legales = pieza.filtrar_movimientos_legales(pieza.obtener_movimientos(tablero), tablero)
                    
                    if (fila_f, col_f) in movimientos_legales:
                        tablero.realizar_movimiento(pieza, fila_f, col_f)
                        jugada_valida = True
                        print("Movimiento realizado con exito!!")
                    else:
                        print("ERROR: Movimiento no permitido para esa pieza o te deja en jaque.")
                        # Ayuda para el jugador: muestra los movimientos validos para la pieza elegida
                        print(f"Movimientos válidos para el {pieza.tipo} en ({fila_i},{col_i}): {movimientos_legales}")

                except ValueError:
                    # Este error solo ocurre si la entrada no son numeros (ej: "1 a 3 4")
                    print(" ERROR: Asegúrate de introducir solo números enteros.")

                except Exception as e:
                    # Este error atrapa cualquier otro problema inesperado y nos dice que es
                    print(f" ¡ERROR INESPERADO! Ha ocurrido un problema: {e} ")
            
        else: # Turno de la IA
            print("\nTurno de la IA, calculando jugada...")
            obtener_movimiento_ia(tablero)

        # Cambia de turno para la siguiente iteración
        turno_actual = 'negro' if turno_actual == 'blanco' else 'blanco'

    print("\n- Fin de la partida -")

if __name__ == '__main__':
    iniciar_partida()