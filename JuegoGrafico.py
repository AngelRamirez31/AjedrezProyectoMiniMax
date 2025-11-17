import pygame
import sys
from PiezaAjedrez import *
from InteligenciaArtificial import obtener_movimiento_ia
from Tablero import Tablero

# Assets
try:
    dark_block = pygame.image.load('assets/black square.png')
    light_block = pygame.image.load('assets/white square.png')
    dark_block = pygame.transform.scale(dark_block, (75, 75))
    light_block = pygame.transform.scale(light_block, (75, 75))

    whitePawn = pygame.image.load('assets/W_Pawn.png')
    whitePawn = pygame.transform.scale(whitePawn, (75, 75))
    whiteRook = pygame.image.load('assets/W_Rook.png')
    whiteRook = pygame.transform.scale(whiteRook, (75, 75))
    whiteBishop = pygame.image.load('assets/W_Bishop.png')
    whiteBishop = pygame.transform.scale(whiteBishop, (75, 75))
    whiteKnight = pygame.image.load('assets/W_Knight.png')
    whiteKnight = pygame.transform.scale(whiteKnight, (75, 75))
    whiteKing = pygame.image.load('assets/W_King.png')
    whiteKing = pygame.transform.scale(whiteKing, (75, 75))
    whiteQueen = pygame.image.load('assets/W_Queen.png')
    whiteQueen = pygame.transform.scale(whiteQueen, (75, 75))

    blackPawn = pygame.image.load('assets/B_Pawn.png')
    blackPawn = pygame.transform.scale(blackPawn, (75, 75))
    blackRook = pygame.image.load('assets/B_Rook.png')
    blackRook = pygame.transform.scale(blackRook, (75, 75))
    blackBishop = pygame.image.load('assets/B_Bishop.png')
    blackBishop = pygame.transform.scale(blackBishop, (75, 75))
    blackKnight = pygame.image.load('assets/B_Knight.png')
    blackKnight = pygame.transform.scale(blackKnight, (75, 75))
    blackKing = pygame.image.load('assets/B_King.png')
    blackKing = pygame.transform.scale(blackKing, (75, 75))
    blackQueen = pygame.image.load('assets/B_Queen.png')
    blackQueen = pygame.transform.scale(blackQueen, (75, 75))

    highlight_block = pygame.image.load('assets/highlight.png')
    highlight_block = pygame.transform.scale(highlight_block, (75, 75))
    
    try:
        icon = pygame.image.load('assets/icon.png')
        pygame.display.set_icon(icon)
    except:
        pass

except pygame.error as e:
    print(f"Error cargando imagenes: {e}")
    sys.exit()

screen = None
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 24)

MAPEO_PIEZAS = {
    'blanco': {'Peon': whitePawn, 'Torre': whiteRook, 'Caballo': whiteKnight, 'Alfil': whiteBishop, 'Reina': whiteQueen, 'Rey': whiteKing},
    'negro': {'Peon': blackPawn, 'Torre': blackRook, 'Caballo': blackKnight, 'Alfil': blackBishop, 'Reina': blackQueen, 'Rey': blackKing}
}

def initialize():
    global screen
    pygame.init()
    pygame.display.set_caption('Ajedrez con IA')
    screen = pygame.display.set_mode((600, 600))
    screen.fill((0, 0, 0))

def draw_background(board, equipo_jugador):

    block_x = 0
    for i in range(4):
        block_y = 0
        for j in range(4):
            screen.blit(light_block, (block_x, block_y))
            screen.blit(dark_block, (block_x + 75, block_y))
            screen.blit(light_block, (block_x + 75, block_y + 75))
            screen.blit(dark_block, (block_x, block_y + 75))
            block_y += 150
        block_x += 150

    soy_blanco = (equipo_jugador == 'blanco')

    for i in range(8):
        for j in range(8):
            pieza = board[i][j]
            if isinstance(pieza, PiezaAjedrez):
                obj = MAPEO_PIEZAS[pieza.equipo][pieza.tipo]

                if soy_blanco:

                    screen_y = i * 75
                    screen_x = j * 75
                else:

                    screen_y = (7 - i) * 75
                    screen_x = (7 - j) * 75
                
                screen.blit(obj, (screen_x, screen_y))
    pygame.display.update()

def seleccionar_promocion(equipo):
    seleccionando = True
    opciones = ['Reina', 'Torre', 'Alfil', 'Caballo']
    imagenes = [
        MAPEO_PIEZAS[equipo]['Reina'],
        MAPEO_PIEZAS[equipo]['Torre'],
        MAPEO_PIEZAS[equipo]['Alfil'],
        MAPEO_PIEZAS[equipo]['Caballo']
    ]

    s = pygame.Surface((600, 600))
    s.set_alpha(150)
    s.fill((0,0,0))
    screen.blit(s, (0,0))
    
    base_x = 140
    base_y = 250

    pygame.draw.rect(screen, (220, 220, 220), (120, 200, 360, 150))
    
    texto = font.render("Selecciona Pieza:", True, (0, 0, 0))
    screen.blit(texto, (200, 210))
    
    for idx, img in enumerate(imagenes):
        screen.blit(img, (base_x + idx * 85, base_y))
    
    pygame.display.update()
    
    while seleccionando:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = pygame.mouse.get_pos()
                if 250 <= pos_y <= 325:
                    for idx in range(4):
                        x_min = base_x + idx * 85
                        if x_min <= pos_x <= x_min + 75:
                            return opciones[idx]
    return 'Reina'


def start_game_loop(board):
    global screen
    possible_piece_moves = []
    running = True
    visible_moves = False
    game_over = False
    pieza_seleccionada = None
    
    equipo_humano = board.obtener_equipo_jugador()
    soy_blanco = (equipo_humano == 'blanco')
    turno_actual = 'blanco'

    if equipo_humano == 'negro' and board.es_ia:
        pygame.display.set_caption("IA está pensando...")
        obtener_movimiento_ia(board)
        pygame.display.set_caption("Ajedrez")
        draw_background(board, equipo_humano)
        turno_actual = 'negro' 

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False 
            
            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True 

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and turno_actual == equipo_humano:
                pos_x_pixel, pos_y_pixel = pygame.mouse.get_pos()
                
                
                col_click = pos_x_pixel // 75
                fila_click = pos_y_pixel // 75
                
                if soy_blanco:
                    fila_logica = fila_click
                    col_logica = col_click
                else:
                    fila_logica = 7 - fila_click
                    col_logica = 7 - col_click
                
                if not (0 <= fila_logica <= 7 and 0 <= col_logica <= 7):
                    continue

                if (fila_logica, col_logica) in possible_piece_moves:

                    board.realizar_movimiento(pieza_seleccionada, fila_logica, col_logica)

                    pieza_movida = board[fila_logica][col_logica]
                    if isinstance(pieza_movida, Peon):

                        if pieza_movida.equipo == 'blanco' and fila_logica == 0:
                            eleccion = seleccionar_promocion('blanco')
                            board.promocionar_peon(fila_logica, col_logica, eleccion)
                        elif pieza_movida.equipo == 'negro' and fila_logica == 7:
                            eleccion = seleccionar_promocion('negro')
                            board.promocionar_peon(fila_logica, col_logica, eleccion)

                    possible_piece_moves.clear()
                    visible_moves = False
                    draw_background(board, equipo_humano)
                    turno_actual = 'negro' if equipo_humano == 'blanco' else 'blanco'
                    
                    # Checa estado
                    if board.es_jaque_mate('negro') or board.es_jaque_mate('blanco') or board.es_ahogado('blanco') or board.es_ahogado('negro'):
                        game_over = True
                
                else:
                    # SELECCIONA PIEZA 
                    pieza = board[fila_logica][col_logica]
                    if isinstance(pieza, PiezaAjedrez) and (equipo_humano == pieza.equipo):
                        pieza_seleccionada = pieza
                        moves = pieza.filtrar_movimientos_legales(pieza.obtener_movimientos(board), board)
                        
                        if visible_moves:
                            draw_background(board, equipo_humano)
                            visible_moves = False
                        
                        possible_piece_moves = moves

                        for move in possible_piece_moves:
                            mf, mc = move
                            if soy_blanco:
                                py = mf * 75
                                px = mc * 75
                            else:
                                py = (7 - mf) * 75
                                px = (7 - mc) * 75
                            screen.blit(highlight_block, (px, py))
                            
                        pygame.display.update()
                        visible_moves = True
                    else:
                        if visible_moves:
                            draw_background(board, equipo_humano)
                            visible_moves = False
                        possible_piece_moves.clear()
                        pieza_seleccionada = None
        
        # Turno IA
        if turno_actual != equipo_humano and not game_over and board.es_ia:
            pygame.display.set_caption("IA está pensando...")
            pygame.display.update()
            pygame.time.wait(50)
            
            obtener_movimiento_ia(board)

            fila_meta = 0 if turno_actual == 'blanco' else 7
            for c in range(8):
                p = board[fila_meta][c]
                if isinstance(p, Peon) and p.equipo == turno_actual:
                    board.promocionar_peon(fila_meta, c, 'Reina')
            
            pygame.display.set_caption("Ajedrez")
            draw_background(board, equipo_humano)
            turno_actual = equipo_humano
            
            if board.es_jaque_mate('negro') or board.es_jaque_mate('blanco') or board.es_ahogado('blanco') or board.es_ahogado('negro'):
                game_over = True

    return False 

def main():
    keep_playing = True
    while keep_playing:
        initialize()
        # CONFIGURACIÓN: modo_juego=0 (Blancas), modo_juego=1 (Negras)
        board = Tablero(modo_juego=0, es_ia=True, profundidad_ia=3) 
        
        equipo = board.obtener_equipo_jugador()
        draw_background(board, equipo)
        
        keep_playing = start_game_loop(board)
        
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()