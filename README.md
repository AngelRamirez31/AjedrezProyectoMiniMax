# Agente de Ajedrez con IA - Algoritmo Minimax

Este proyecto es una implementación de un agente de Inteligencia Artificial capaz de jugar una partida completa de ajedrez contra un oponente humano. El núcleo del agente se basa en el algoritmo **Minimax** con optimizaciones de **poda Alfa-Beta**, lo que le permite tomar decisiones estratégicas explorando un árbol de jugadas futuras.

El programa se ejecuta completamente en la terminal y no requiere dependencias externas.



---

## Características

* **Motor de Ajedrez Completo:** Implementa todas las reglas del ajedrez, incluyendo el movimiento de cada pieza y las condiciones de fin de partida.
* **Agente Inteligente:** La IA utiliza el algoritmo Minimax para analizar las posibles jugadas y elegir la más óptima.
* **Poda Alfa-Beta:** El algoritmo está optimizado para "podar" ramas inútiles del árbol de búsqueda, lo que le permite pensar más rápido y a mayor profundidad.
* **Dificultad Ajustable:** La "inteligencia" del agente se puede modificar fácilmente cambiando la variable `profundidad_ia`, que controla cuántos movimientos hacia el futuro analiza.
* **Interfaz de Consola:** Juega directamente en tu terminal, con una representación visual del tablero que se actualiza en cada turno.
* **Juega como Blancas o Negras:** Puedes configurar el programa para jugar con el color de piezas que prefieras.

---

## Algoritmo: Minimax

Nuestro proyecto utiliza el algoritmo Minimax. Funciona bajo los siguientes principios:

1.  **Búsqueda en Árbol:** La IA construye un árbol de todas las posibles secuencias de movimientos hasta una profundidad definida.
2.  **Dos Jugadores, Objetivos Opuestos:** Asigna roles a los jugadores:
    * **MAX (Blancas):** Su objetivo es maximizar la puntuación del tablero.
    * **MIN (Negras):** Su objetivo es minimizar la puntuación del tablero.
3.  **Función de Evaluación:** Para saber qué tan "buena" es una posición, se utiliza una función de evaluación heurística que asigna un valor numérico al tablero basado en el material (la suma del valor de las piezas de cada bando).
4.  **Recursividad:** El algoritmo explora el árbol de forma recursiva, asumiendo que en cada turno el oponente elegirá la jugada que es peor para la IA. Esto permite al agente elegir el camino que le garantiza el mejor resultado posible en el peor de los casos.

---

## Arquitectura del Proyecto

El código está estructurado en cuatro archivos principales, siguiendo los principios de la Programación Orientada a Objetos para una clara separación de responsabilidades.

* `PiezaAjedrez.py`: Define las clases para cada pieza del ajedrez (`Peon`, `Torre`, `Rey`, etc.). Cada clase contiene la lógica de sus movimientos y características como su equipo y valor.
* `Tablero.py`: Representa el entorno del juego. Gestiona el estado de la partida, contiene la matriz 8x8, aplica las reglas, ejecuta los movimientos y determina las condiciones de fin de juego (jaque mate, ahogado).
* `InteligenciaArtificial.py`: Contiene la implementación del agente. Aquí residen las funciones `algoritmo_minimax` y `obtener_movimiento_ia`, que constituyen el cerebro estratégico del oponente.
* `Juego.py`: Es el archivo principal que orquesta la partida. Contiene el bucle de juego, gestiona los turnos, imprime el tablero en la consola y maneja las entradas del jugador humano.

---

## Futuras Mejoras

* **Mejorar la Función de Evaluación:** Añadir más heurísticas además del valor material, como la posición de las piezas, el control del centro o la seguridad del rey.
* **Implementar una Interfaz Gráfica:** Utilizar librerías como `Pygame` o `Tkinter` para crear una experiencia de juego visual.
* **Tabla de Transposición:** Guardar posiciones ya evaluadas para evitar recalcularlas y acelerar el rendimiento de la IA.
