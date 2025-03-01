import pygame
import random
import os

# Инициализация pygame
pygame.init()

# Размеры окна
WIDTH = 300
HEIGHT = 420
BLOCK_SIZE = 30

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (0, 0, 255),  # Blue
    (0, 255, 0),  # Green
    (255, 0, 0),  # Red
    (128, 0, 128)  # Purple
]

# Фигуры
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]  # J
]

# Создание окна
screen = pygame.display.set_mode((WIDTH + 180, HEIGHT))
pygame.display.set_caption("Тетрис")

# Часы
clock = pygame.time.Clock()

# Шрифт
font = pygame.font.SysFont("Impact", 30)

# Загрузка фонового изображения
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH + 180, HEIGHT))

# Имя файла для сохранения
SAVE_FILE = "tetris_save.txt"


# Класс фигуры
class Piece:
    def __init__(self, shape):
        self.shape = shape
        self.color = random.choice(COLORS)
        self.x = WIDTH // BLOCK_SIZE // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


# Игровое поле
grid = [[BLACK for _ in range(WIDTH // BLOCK_SIZE)] for _ in range(HEIGHT // BLOCK_SIZE)]


# Функция отрисовки сетки
def draw_grid():
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    for y in range(len(grid)):
        pygame.draw.line(screen, WHITE, (0, y * BLOCK_SIZE), (WIDTH, y * BLOCK_SIZE))
    for x in range(len(grid[0]) + 1):
        pygame.draw.line(screen, WHITE, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, HEIGHT))


# Функция проверки столкновений
def is_collision(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                if (piece.y + y >= len(grid)) or (piece.x + x < 0 or piece.x + x >= len(grid[0])) or grid[piece.y + y][
                    piece.x + x] != BLACK:
                    return True
    return False


# Функция добавления фигуры на поле
def add_to_grid(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[piece.y + y][piece.x + x] = piece.color


# Функция очистки заполненных линий
def clear_lines():
    lines_cleared = 0
    for y in range(len(grid) - 1, -1, -1):
        if BLACK not in grid[y]:
            # Подсветка линии перед удалением
            for x in range(len(grid[y])):
                grid[y][x] = WHITE
            draw_grid()
            pygame.display.update()
            pygame.time.delay(300)  # Задержка для мигания
            lines_cleared += 1
            del grid[y]
            grid.insert(0, [BLACK for _ in range(WIDTH // BLOCK_SIZE)])
    return lines_cleared


# Функция отрисовки текста
def draw_text(text, x, y, color=WHITE, background=None):
    text_surface = font.render(text, True, color, background)
    screen.blit(text_surface, (x, y))


# Функция сохранения прогресса
def save_game(score, level, grid, current_piece, next_piece):
    with open(SAVE_FILE, "w") as file:
        file.write(f"{score}\n")
        file.write(f"{level}\n")
        for row in grid:
            file.write(" ".join([f"{cell[0]},{cell[1]},{cell[2]}" for cell in row]) + "\n")
        file.write(f"{current_piece.x} {current_piece.y}\n")
        file.write(";".join([",".join(map(str, row)) for row in current_piece.shape]) + "\n")
        file.write(";".join([",".join(map(str, row)) for row in next_piece.shape]) + "\n")
        file.write(f"{current_piece.color[0]},{current_piece.color[1]},{current_piece.color[2]}" + '\n')
        file.write(f"{next_piece.color[0]},{next_piece.color[1]},{next_piece.color[2]}" + '\n')


# Функция загрузки прогресса
def load_game():
    if not os.path.exists(SAVE_FILE):
        return None

    with open(SAVE_FILE, "r") as file:
        lines = file.readlines()
        score = int(lines[0].strip())
        level = int(lines[1].strip())
        grid = [[tuple(map(int, cell.split(','))) for cell in row.strip().split()] for row in lines[2:-5]]
        current_piece_data = lines[-5].strip().split()
        current_piece_x = int(current_piece_data[0])
        current_piece_y = int(current_piece_data[1])
        current_piece_shape = [list(map(int, row.split(','))) for row in lines[-4].strip().split(';')]
        next_piece_shape = [list(map(int, row.split(','))) for row in lines[-3].strip().split(';')]
        current_piece_color = tuple(map(int, lines[-2].strip().split(',')))
        next_piece_color = tuple(map(int, lines[-1].strip().split(',')))
        current_piece = Piece(current_piece_shape)
        current_piece.x = current_piece_x
        current_piece.y = current_piece_y
        current_piece.color = current_piece_color
        next_piece = Piece(next_piece_shape)
        next_piece.color = next_piece_color

        return score, level, grid, current_piece, next_piece


# Функция начального экрана
def start_screen():
    screen.blit(background_image, (0, 0))
    draw_text("Тетрис", WIDTH // 2 - 40, HEIGHT // 2 - 150, BLACK)
    draw_text("Начать игру", WIDTH // 2 - 70, HEIGHT // 2 - 100, BLACK)
    if os.path.exists(SAVE_FILE):
        draw_text("Продолжить игру", WIDTH // 2 - 70, HEIGHT // 2 - 50, BLACK)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False, False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 2 - 70 <= mouse_pos[0] <= WIDTH // 2 + 70 and HEIGHT // 2 - 100 <= mouse_pos[
                    1] <= HEIGHT // 2 - 100 + 40:
                    return True, False
                if os.path.exists(SAVE_FILE) and WIDTH // 2 - 70 <= mouse_pos[
                    0] <= WIDTH // 2 + 70 and HEIGHT // 2 - 50 <= \
                        mouse_pos[1] <= HEIGHT // 2 - 50 + 40:
                    return True, True


# Основная функция игры
def game(load_saved_game=False):
    if load_saved_game:
        saved_data = load_game()
        if saved_data:
            score, level, saved_grid, current_piece, next_piece = saved_data
            for y in range(len(grid)):
                for x in range(len(grid[y])):
                    grid[y][x] = saved_grid[y][x]
        else:
            draw_text("Сохранение не найдено", WIDTH // 2 - 90, HEIGHT // 2 - 50, WHITE, BLACK)
            pygame.display.update()
            pygame.time.delay(2000)
            load_saved_game = False
    if not load_saved_game:
        current_piece = Piece(random.choice(SHAPES))
        next_piece = Piece(random.choice(SHAPES))
        score = 0
        level = 1
    fall_time = 0
    fall_speed = 0.3
    running = True
    game_over = False
    paused = False

    while running:
        clock.tick(60)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Спрашиваем пользователя, хочет ли он сохранить прогресс
                screen.blit(background_image, (0, 0))
                draw_text("Сохранить игру?", WIDTH // 2 - 70, HEIGHT // 2 - 50, WHITE, BLACK)
                draw_text("Да", WIDTH // 2 - 70, HEIGHT // 2, WHITE, BLACK)
                draw_text("Нет", WIDTH // 2, HEIGHT // 2, WHITE, BLACK)
                pygame.display.update()
                save_choice = None
                while save_choice is None:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            if (WIDTH // 2 - 70 <= mouse_pos[0] <= WIDTH // 2 - 35 and HEIGHT // 2 <= mouse_pos[1]
                                    <= HEIGHT // 2 + 40):
                                save_game(score, level, grid, current_piece, next_piece)
                                save_choice = True
                            elif (WIDTH // 2 <= mouse_pos[0] <= WIDTH // 2 + 40 and HEIGHT // 2 <= mouse_pos[1]
                                  <= HEIGHT // 2 + 40):
                                save_choice = False
                running = False
            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if is_collision(current_piece):
                            current_piece.x += 1
                    if event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if is_collision(current_piece):
                            current_piece.x -= 1
                    if event.key == pygame.K_DOWN:
                        current_piece.y += 1
                        if is_collision(current_piece):
                            current_piece.y -= 1
                    if event.key == pygame.K_UP:
                        current_piece.rotate()
                        if is_collision(current_piece):
                            for _ in range(3):
                                current_piece.rotate()
                    if event.key == pygame.K_SPACE:
                        while not is_collision(current_piece):
                            current_piece.y += 1
                        current_piece.y -= 1
                    if event.key == pygame.K_p:
                        paused = not paused
                else:
                    if event.key == pygame.K_r:
                        # Перезапуск игры
                        for y in range(len(grid)):
                            for x in range(len(grid[y])):
                                grid[y][x] = BLACK
                        current_piece = Piece(random.choice(SHAPES))
                        next_piece = Piece(random.choice(SHAPES))
                        score = 0
                        level = 1
                        game_over = False

        if not game_over and not paused:
            fall_time += clock.get_rawtime()
            if fall_time / 1000 >= fall_speed:
                fall_time = 0
                current_piece.y += 1
                if is_collision(current_piece):
                    current_piece.y -= 1
                    add_to_grid(current_piece)
                    lines_cleared = clear_lines()
                    if lines_cleared > 0:
                        lines_cleared += clear_lines()
                        lines_cleared += clear_lines()
                        lines_cleared += clear_lines()
                    score += lines_cleared * 100
                    level = 1 + score // 100
                    fall_speed = 0.3 - (level - 1) * 0.02
                    current_piece = next_piece
                    next_piece = Piece(random.choice(SHAPES))
                    if is_collision(current_piece):
                        game_over = True

        draw_grid()

        # Отрисовка текущей фигуры
        for y, row in enumerate(current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, current_piece.color, (
                        (current_piece.x + x) * BLOCK_SIZE, (current_piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                                     0)

        # Отрисовка следующей фигуры
        draw_text("Следующая:", WIDTH + 10, 10)
        for y, row in enumerate(next_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, next_piece.color,
                                     (WIDTH + 10 + x * BLOCK_SIZE, 50 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        # Отрисовка счета и уровня
        draw_text(f"Очки: {score}", WIDTH + 10, 200)
        draw_text(f"Уровень: {level}", WIDTH + 10, 250)

        if paused:
            draw_text("Пауза", WIDTH // 2 - 40, HEIGHT // 2 - 50, WHITE, BLACK)

        if game_over:
            draw_text("Игра окончена!", WIDTH // 2 - 70, HEIGHT // 2 - 50, WHITE, BLACK)
            draw_text("Нажми R, чтобы начать заново", WIDTH // 2 - 90, HEIGHT // 2, WHITE, BLACK)

        pygame.display.update()

    pygame.quit()


# Запуск игры
start, load_saved = start_screen()
if start:
    game(load_saved)
