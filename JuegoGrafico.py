import pygame
import sys
from PiezaAjedrez import *
from InteligenciaArtificial import obtener_movimiento_ia
from Tablero import Tablero

# Carga de Assets
try:
    dark_block = pygame.image.load('assets/square brown dark.png')
    light_block = pygame.image.load('assets/square brown light.png')
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

    highlight_block = pygame.image.load('assets/highlight_128px.png')
    highlight_block = pygame.transform.scale(highlight_block, (75, 75))

except pygame.error as e:
    print(f"Error al cargar las imágenes. Asegúrate de que la carpeta 'assets' exista y contenga todas las imágenes.")
    print(e)
    sys.exit()

# Variables Globales de Pygame 
screen = None
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 24)

MAPEO_PIEZAS = {
    'blanco': {
        'Peon': whitePawn, 'Torre': whiteRook, 'Caballo': whiteKnight,
        'Alfil': whiteBishop, 'Reina': whiteQueen, 'Rey': whiteKing
    },
    'negro': {
        'Peon': blackPawn, 'Torre': blackRook, 'Caballo': blackKnight,
        'Alfil': blackBishop, 'Reina': blackQueen, 'Rey': blackKing
    }
}


# Funciones de Dibujo 

def initialize():
    global screen
    pygame.init()
    pygame.display.set_caption('Ajedrez con IA')
    try:
        icon = pygame.image.load('assets/icon.png') 
        pygame.display.set_icon(icon)
    except:
        print("Icono 'icon.png' no encontrado en 'assets', continuando sin icono.")
        
    screen = pygame.display.set_mode((600, 650))
    screen.fill((0, 0, 0))

def draw_background(board):
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
    
    step_x = 0
    for i in range(7, -1, -1):
        for j in range(8):
            if isinstance(board[i][j], PiezaAjedrez):
                pieza = board[i][j]
                obj = MAPEO_PIEZAS[pieza.equipo][pieza.tipo]
                screen_y = (7 - i) * 75 
                screen.blit(obj, (step_x, screen_y))
            step_x += 75
        step_x = 0
    
    pygame.display.update()

def draw_text(text):
    s = pygame.Surface((600, 50))
    s.fill((0, 0, 0))
    screen.blit(s, (0, 600))
    
    text_surface = font.render(text, False, (237, 237, 237))
    text_rect = text_surface.get_rect(center=(300, 615)) 
    
    text_surface_restart = font.render('Presiona ESPACIO para reiniciar', False, (237, 237, 237))
    text_restart_rect = text_surface_restart.get_rect(center=(300, 635))

    screen.blit(text_surface, text_rect)
    screen.blit(text_surface_restart, text_restart_rect)
    pygame.display.update()


# Bucle Principal del Juego 

def start_game_loop(board):
    global screen
    possible_piece_moves = []
    running = True
    visible_moves = False
    game_over = False
    pieza_seleccionada = None
    
    equipo_humano = board.obtener_equipo_jugador()
    turno_actual = 'blanco'
    
    if equipo_humano == 'negro' and board.es_ia:
        pygame.display.set_caption("IA está pensando...")
        obtener_movimiento_ia(board)
        pygame.display.set_caption("Ajedrez")
        draw_background(board)
        turno_actual = 'negro'

    while running:
        if game_over:
            draw_text(game_over_txt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False 
            
            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True 

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and turno_actual == equipo_humano:
                pos_y, pos_x = pygame.mouse.get_pos()
                
                fila_clic = 7 - (pos_x // 75) 
                col_clic = pos_y // 75
                
                if not (0 <= fila_clic <= 7 and 0 <= col_clic <= 7):
                    continue

                if (fila_clic, col_clic) in possible_piece_moves:
                    board.realizar_movimiento(pieza_seleccionada, fila_clic, col_clic)
                    possible_piece_moves.clear()
                    visible_moves = False
                    draw_background(board)
                    turno_actual = 'negro' if equipo_humano == 'blanco' else 'blanco'
                    
                    if board.es_jaque_mate('negro'):
                        game_over = True
                        game_over_txt = '¡GANAN LAS BLANCAS!'
                    elif board.es_jaque_mate('blanco'):
                        game_over = True
                        game_over_txt = '¡GANAN LAS NEGRAS!'
                    elif board.es_ahogado('blanco') or board.es_ahogado('negro'):
                        game_over = True
                        game_over_txt = '¡EMPATE POR AHOGADO!'
                
                else:
                    pieza = board[fila_clic][col_clic]
                    if isinstance(pieza, PiezaAjedrez) and (equipo_humano == pieza.equipo):
                        pieza_seleccionada = pieza
                        moves = pieza.filtrar_movimientos_legales(pieza.obtener_movimientos(board), board)
                        
                        if visible_moves:
                            draw_background(board)
                            visible_moves = False
                        
                        possible_piece_moves = moves
                        
                        for move in possible_piece_moves:
                            move_fila, move_col = move
                            pixel_x = move_col * 75
                            pixel_y = (7 - move_fila) * 75
                            
                            screen.blit(highlight_block, (pixel_x, pixel_y))
                            visible_moves = True
                        pygame.display.update()
                    else:
                        if visible_moves:
                            draw_background(board)
                            visible_moves = False
                        possible_piece_moves.clear()
                        pieza_seleccionada = None
        
        if turno_actual != equipo_humano and not game_over and board.es_ia:
            pygame.display.set_caption("IA está pensando...")
            pygame.time.wait(100) 
            
            obtener_movimiento_ia(board)
            
            pygame.display.set_caption("Ajedrez con IA")
            draw_background(board)
            turno_actual = equipo_humano
            
            if board.es_jaque_mate('negro'):
                game_over = True
                game_over_txt = '¡GANAN LAS BLANCAS!'
            elif board.es_jaque_mate('blanco'):
                game_over = True
                game_over_txt = '¡GANAN LAS NEGRAS!'
            elif board.es_ahogado('blanco') or board.es_ahogado('negro'):
                game_over = True
                game_over_txt = '¡EMPATE POR AHOGADO!'

    return False 

# Main

def main():
    keep_playing = True
    while keep_playing:
        initialize()
        
        board = Tablero(modo_juego=0, es_ia=True, profundidad_ia=3) 
        
        draw_background(board)
        
        keep_playing = start_game_loop(board)
        
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()