import pygame as pg
from wave_function_collapse import wfc
from a_star_algorithm import build_graph, dijkstra

# Отрисовка карты местности
def fill_screen(surface, col, row, tile_width, tile_height, grid, color):
    for r in range(row):
        for c in range(col):
            pg.draw.rect(surface, pg.Color(color[grid[r][c]]), (c * tile_width, r * tile_height, tile_width, tile_height))

# Рисует круг
def draw_circle(surface ,x, y, color, TILE_HEIGHT, TILE_WIDTH):
    pg.draw.circle(surface, pg.Color(color), (x * TILE_WIDTH + TILE_WIDTH // 2, y * TILE_HEIGHT + TILE_HEIGHT // 2), (TILE_WIDTH if TILE_WIDTH < TILE_HEIGHT else TILE_HEIGHT) // 4)

# Возвращает координаты клетки по каторой кликнул пользователь иначе False
def get_click_mouse_pos(TILE_WIDTH, TILE_HEIGHT, HEIGHT, surface):
    x, y = pg.mouse.get_pos()
    if y >= HEIGHT - 50: return False

    grid_x, grid_y = x // TILE_WIDTH, y // TILE_HEIGHT
    draw_circle(surface, grid_x, grid_y, 'red', TILE_HEIGHT, TILE_WIDTH)
    click = pg.mouse.get_pressed()

    return (grid_x, grid_y) if click[0] else False

# Функция отрисовки текста на экране
def text_on_screen(screen, font, font_size, text, color, width, height):
    myfont = pg.font.SysFont(font, font_size)
    textsurface = myfont.render(str(text), False, color)
    screen.blit(textsurface,(width, height))
    pg.display.flip()

# Функция отрисовки карты
def draw_best_way(cols, rows, self):
    WIDTH, HEIGHT = 1000, 600
    TILE_WIDTH = WIDTH // cols
    TILE_HEIGHT = HEIGHT // rows
    RES = WIDTH, HEIGHT = TILE_WIDTH * cols, TILE_HEIGHT * rows + 50

    colors = {1 : '#b5a858', 2 : '#cedf88', 4 : '#90af0a', 7 : '#09af83', 9 : '#ab9494'}
    grid_exampl = [[2, 2, 2, 2, 2, 2], [1, 1, 1, 2, 2, 4], [2, 9, 1, 1, 4, 4], [7, 7, 7, 1, 4, 4], [7, 7, 7, 1, 2, 4], [7, 7, 9, 1, 1, 9]]
    grid = []

    start = (0, int(rows / 2))          # Начальная точка
    goal = start                        # Точка назначения
    visited = {start: None}             # Список посещенных клеток

    pg.init()                           # Инициируем окно
    sc = pg.display.set_mode(RES)       # Устанавливаем разрешение окна
    pg.display.set_caption("Поиск кротчайшего пути на сгенерированной карте местности")     # Устанавливаем заголовок
    clock = pg.time.Clock()             # Инициируем таймер

    while True:
        if grid == []:
            text_on_screen(sc, 'Times New Roman', 30, 'Loading...', (255, 255, 255), WIDTH // 2 - 50, HEIGHT // 2 - 50)

            grid = wfc(grid_exampl, cols, rows)
            graph = build_graph(grid)
        else:
            sc.fill((0, 0, 0))
            # Отрисовывыем поле
            fill_screen(sc, cols, rows, TILE_WIDTH, TILE_HEIGHT, grid, colors)

            # Получаем кординату точки и находим кратчайший путь
            mouse_pos = get_click_mouse_pos(TILE_WIDTH, TILE_HEIGHT, HEIGHT, sc)
            if mouse_pos and mouse_pos != goal:        
                visited = dijkstra(start, mouse_pos, graph)
                goal = mouse_pos
                
            # Отрисовываем кратчайший путь
            path_head, path_segment = goal, visited[goal]
            x, y = path_head
            path_time = 0 if path_segment is None else grid[y][x]
            path_step = 0 if path_segment is None else 1

            while path_segment != start and path_segment:
                draw_circle(sc, *path_segment, 'blue', TILE_HEIGHT, TILE_WIDTH)
                
                # Подсчет количества необходимых шагов и времени на путь
                x, y = path_segment
                path_time += grid[y][x]
                path_step += 1
                path_segment = visited[path_segment]

            # Отрисовываем начало и конец пути
            draw_circle(sc, *start, 'green', TILE_HEIGHT, TILE_WIDTH)
            draw_circle(sc, *path_head, 'magenta', TILE_HEIGHT, TILE_WIDTH)


            text_on_screen(sc, 'Times New Roman', 25, 'Кратчайший путь состоит из ' + str(path_step) + ' шаг(-а/-ов) и занимает ' +
                           str(path_time) + ' единиц времени.', (255, 255, 255), 20, HEIGHT - 40)

        # pygame necessary lines
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.startButton.setEnabled(True)
                self.startButton.setText('Начать генерацию карты')
                pg.display.quit()
                return

        pg.display.flip()
        clock.tick(60)
