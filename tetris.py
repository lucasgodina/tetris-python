import pygame
import random

"""
Grilla de 10 x 20
formas: S, Z, I, O, J, L, T
representadas en orden del 0 - 6
"""

pygame.font.init()

# VARIABLES GLOBALES
s_width = 800
s_height = 700
play_width = 300  # 300 // 10 = 30 width x block
play_height = 600  # 600 // 20 = 20 height x block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

high_score = 10


# TETROMINOS

S = [
    [".....", "......", "..00..", ".00...", "....."],
    [".....", "..0..", "..00.", "...0.", "....."],
]

Z = [
    [".....", ".....", ".00..", "..00.", "....."],
    [".....", "..0..", ".00..", ".0...", "....."],
]

I = [
    ["..0..", "..0..", "..0..", "..0..", "....."],
    [".....", "0000.", ".....", ".....", "....."],
]

O = [[".....", ".....", ".00..", ".00..", "....."]]

J = [
    [".....", ".0...", ".000.", ".....", "....."],
    [".....", "..00.", "..0..", "..0..", "....."],
    [".....", ".....", ".000.", "...0.", "....."],
    [".....", "..0..", "..0..", ".00..", "....."],
]

L = [
    [".....", "...0.", ".000.", ".....", "....."],
    [".....", "..0..", "..0..", "..00.", "....."],
    [".....", ".....", ".000.", ".0...", "....."],
    [".....", ".00..", "..0..", "..0..", "....."],
]

T = [
    [".....", "..0..", ".000.", ".....", "....."],
    [".....", "..0..", "..00.", "..0..", "....."],
    [".....", ".....", ".000.", "..0..", "....."],
    [".....", "..0..", ".00..", "..0..", "....."],
]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [
    (0, 255, 0),
    (255, 0, 0),
    (0, 255, 255),
    (255, 255, 0),
    (255, 165, 0),
    (0, 0, 255),
    (128, 0, 128),
]
# index del 0 - 6 corresponde a las formas


# CLASE QUE DEFINE LAS PIEZAS
class Piece(object):
    rows = 20  # Y
    columns = 10  # X

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # numero de rotaciones desde el 0 al 3


# Funcion para crear la grilla y las posiciones bloqueadas
def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


# Funcion para convertir la forma de la pieza en posiciones
def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


# Funcion para verificar si la posicion es valida
def valid_space(shape, grid):
    accepted_positions = [
        [(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)
    ]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


# Funcion para verificar si el jugador perdio
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


# Funcion para actualizar nuevo puntaje alto
def update_high_score(new_score):
    global high_score
    if new_score > high_score:
        high_score = new_score
        return True
    return False


# Funcion para mostrar el puntaje alto a la izquierda de la pantalla
def draw_high_score():
    font = pygame.font.SysFont("arial", 30)
    label = font.render(f"MEJOR: {high_score}", 1, (255, 255, 255))

    sx = top_left_x - 200
    sy = top_left_y + play_height / 2 - 100

    win.blit(label, (sx + 20, sy + 160))


# Funcion para obtener una nueva pieza
def get_shape():
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))


# Funcion para dibujar el texto en el centro
def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)

    # Calcular la posición del rectángulo y del texto
    rect_width = label.get_width() + 20
    rect_height = label.get_height() + 20
    rect_x = top_left_x + play_width / 2 - rect_width / 2
    rect_y = top_left_y + play_height / 2 - rect_height / 2

    # Dibujar el rectángulo negro
    pygame.draw.rect(surface, (0, 0, 0), (rect_x, rect_y, rect_width, rect_height))

    # Dibujar el texto
    surface.blit(label, (rect_x + 10, rect_y + 10))


# Funcion para dibujar la grilla
def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(
            surface, (128, 128, 128), (sx, sy + i * 30), (sx + play_width, sy + i * 30)
        )  # Lineas horizontales
        for j in range(col):
            pygame.draw.line(
                surface,
                (128, 128, 128),
                (sx + j * 30, sy),
                (sx + j * 30, sy + play_height),
            )  # Lineas verticales


# Funcion para limpiar las filas completas
def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # Agregar posiciones a remover
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    if inc == 4:
        return 5  # Tetris
    return inc  # 1 punto por línea


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont("arial", 30)
    label = font.render("Proxima", 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                pygame.draw.rect(
                    surface, shape.color, (sx + j * 30, sy + i * 30, 30, 30), 0
                )

    surface.blit(label, (sx + 10, sy - 30))


def draw_window(surface, score):
    surface.fill((0, 0, 0))
    # TITULO TETRIS CRUI
    font = pygame.font.SysFont("arial", 60)
    label = font.render("TETRIS CRUI", 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # MOSTRAR PUNTAJE
    font = pygame.font.SysFont("arial", 30)
    label = font.render(f"Puntaje: {score}", 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    surface.blit(label, (sx + 20, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(
                surface,
                grid[i][j],
                (top_left_x + j * 30, top_left_y + i * 30, 30, 30),
                0,
            )

    # DIBUJAR GRILLA Y BORDE
    draw_grid(surface, 20, 10)
    pygame.draw.rect(
        surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5
    )


def main():
    global grid
    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    score = 0  # INICIALIZAR PUNTAJE
    fall_speed = 0.30  # VELOCIDAD INICIAL DE CAIDA

    while run:
        grid = create_grid(locked_positions)

        fall_time += clock.get_rawtime()
        clock.tick()

        # AUMENTAR LA VELOCIDAD DE CAIDA CADA 5 PUNTOS
        fall_speed = 0.30 - (score // 5) * 0.02

        #  CAIDA DE PIEZA
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                # MOVER PIEZA HACIA LA IZQUIERDA
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                # MOVER PIEZA HACIA LA DERECHA
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                # MOVER PIEZA HACIA ABAJO
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                # ROTAR PIEZA
                elif event.key == pygame.K_UP:
                    current_piece.rotation = current_piece.rotation + 1 % len(
                        current_piece.shape
                    )
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(
                            current_piece.shape
                        )

        shape_pos = convert_shape_format(current_piece)

        # DIBUJAR PIEZA ACTUAL
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # SI LA PIEZA LLEGA AL FONDO
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            # INCREMENTAR PUNTAJE
            score += clear_rows(grid, locked_positions)

        draw_window(win, score)
        draw_next_shape(next_piece, win)  # Dibujar la siguiente pieza
        draw_high_score()  # Dibujar puntaje alto
        pygame.display.update()

        # VERIFICAR SI EL JUGADOR PERDIO
        if check_lost(locked_positions):
            if update_high_score(score) == True:
                draw_text_middle(
                    f"Nuevo puntaje alto! {high_score}", 40, (255, 255, 255), win
                )
            else:
                draw_text_middle("Has perdido", 40, (255, 255, 255), win)
            run = False
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle("Presiona cualquier tecla", 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Tetris CRUI")
main_menu()  # EMPEZAR EL JUEGO
