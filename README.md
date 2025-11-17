# Chess AI Agent with Minimax & GUI

This project is a complete implementation of a Chess Engine with Artificial Intelligence, capable of playing against a human opponent through a graphical interface.

The core of the agent is based on the **Minimax** algorithm with **Alpha-Beta pruning** optimizations. Unlike basic engines, this agent utilizes **positional evaluation** (Piece-Square Tables), allowing it to understand strategies—such as controlling the center or developing pieces—beyond simple material value.



---

# Key Features

* **Graphical User Interface (GUI):** Built with `Pygame`, offering a visual and interactive experience with event handling (clicks, window management) without freezing during AI calculation.
* **Strategic AI:**
    * **Minimax Algorithm:** Adjustable depth to balance difficulty and calculation time.
    * **Alpha-Beta Pruning:** Massive optimization that discards irrelevant game trees, allowing for deeper search.
    * **Piece-Square Tables:** The AI evaluates how "good" a square is for a specific piece (e.g., Knights in the center, Rooks on open files).
* **Dynamic Gameplay:**
    * **Board Flipping:** The board automatically orients itself depending on whether you play as White or Black.
    * **Pawn Promotion:** Interactive menu to choose your promotion piece (Queen, Rook, Bishop, Knight).
* **Complete Chess Rules:** Implementation of legal moves, captures, check, checkmate, stalemate, and special moves like **Castling** (Kingside and Queenside).

---

##  The Algorithm: Minimax

Our project uses an advanced version of Minimax that operates on the following principles:

1.  **Tree Search:** The AI simulates all possible move sequences up to a defined depth (e.g., 3 or 4 moves ahead).
2.  **Two Players, Opposite Goals:**
    * **MAX (White):** Aims to maximize the board score.
    * **MIN (Black):** Aims to minimize the board score.
3.  **Heuristic Evaluation:** To determine if a position is advantageous, the evaluation function calculates:
    * **Material:** The sum of piece values (Pawn=10, Queen=90, etc.).
    * **Position:** Bonuses or penalties based on where the piece is located on the board.
4.  **Recursion:** The algorithm explores the tree recursively, assuming the opponent will always make the optimal move. This allows the agent to choose the path that guarantees the best possible result in the worst-case scenario.

---

##  Project Architecture

The code follows Object-Oriented Programming (OOP) principles for a clear separation of responsibilities:

* `JuegoGrafico.py` (Main): The entry point. Manages the `Pygame` window, graphics, user events (clicks), and the main game loop.
* `InteligenciaArtificial.py`: Contains the opponent's "brain." Implements `minimax_algorithm`, pruning logic, and the `get_ai_move` function.
* `Tablero.py` (Board): Represents the environment. Manages the 8x8 matrix, validates game state (check/mate), handles castling/promotion, and stores the **Positional Tables**.
* `PiezaAjedrez.py`: Defines classes for each piece (`Pawn`, `King`, etc.) and their specific movement and attack rules.
* `assets/`: Folder containing the `.png` images for pieces and board elements.

---

##  Installation and Usage

### Requirements
You need Python 3 installed and the `pygame` library.

```bash
pip install pygame
```
---

##  How to run
*Clone the repository or download the files.
*Ensure the assets folder is in the same directory as the scripts.
*Run the main file: `JuegoGrafico.py`

---

## Credits 
*Assets: The visual assets (pieces and board sprites) were created by DANI MACCARI.









