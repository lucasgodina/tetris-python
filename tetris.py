import pygame
import random

"""
10 x 20 grilla
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


# DIFERENTES FORMAS, IGNORAR AUTOPEP8

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
    grid = [[(0, 0, 0) for x in range(10)] for y in range(20)]

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                color = locked_positions[(x, y)]
                grid[y][x] = color
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


# Funcion para obtener una nueva pieza
def get_shape():
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))


# Funcion para dibujar el texto en el centro
def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(
        label,
        (
            top_left_x + play_width / 2 - (label.get_width() / 2),
            top_left_y + play_height / 2 - label.get_height() / 2,
        ),
    )


# Funcion para dibujar la grilla
def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(
            surface,
            (128, 128, 128),
            (sx, sy + i * block_size),
            (sx + play_width, sy + i * block_size),
        )
        for j in range(col):
            pygame.draw.line(
                surface,
                (128, 128, 128),
                (sx + j * block_size, sy),
                (sx + j * block_size, sy + play_height),
            )


# Funcion para limpiar las filas completas
def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
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


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Proxima forma", 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i in range(len(format)):
        row = list(format[i])
        for j in range(len(row)):
            if row[j] == "0":
                pygame.draw.rect(
                    surface,
                    shape.color,
                    (sx + j * block_size, sy + i * block_size, block_size, block_size),
                    0,
                )

    surface.blit(label, (sx + 10, sy - 30))


def draw_window(surface):
    surface.fill((0, 0, 0))
    # Titulo Tetris
    font = pygame.font.SysFont("comicsans", 60)
    label = font.render("Tetris CRUI", 1, (255, 255, 255))


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

    while run:
        fall_speed = 0.27

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

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

            # LLAMAR A LA FUNCION 4 VECES PARA LIMPIAR FILA COMPLETA
            clear_rows(grid, locked_positions)

        draw_window(win)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        # VERIFICAR SI EL JUGADOR PERDIO
        if check_lost(locked_positions):
            run = False

    draw_text_middle("Has perdido", 40, (255, 255, 255), win)
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle(
            "Presiona cualquier tecla para jugar", 60, (255, 255, 255), win
        )
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
