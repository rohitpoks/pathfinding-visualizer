import pygame
import sys
import math
from queue import PriorityQueue

WIDTH = 800
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('Path Finding Algorithm')

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (255, 165, 0)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (128, 0, 128)
grey = (128, 128, 128)
turquoise = (64, 224, 208)

pygame.init()

font = pygame.font.Font('font.ttf', 30)
bg = pygame.image.load('bg.jpg')


class Node:  # keep track of all nodes and know what color they are
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width  # width to determine coordinates from indices
        self.y = col * width
        self.color = white
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == red

    def is_open(self):
        return self.color == green

    def is_barrier(self):
        return self.color == black

    def is_start(self):
        return self.color == orange

    def is_end(self):
        return self.color == turquoise

    def reset(self):
        self.color = white

    def make_start(self):
        self.color = orange

    def make_closed(self):
        self.color = red

    def make_open(self):
        self.color = green

    def make_barrier(self):
        self.color = black

    def make_end(self):
        self.color = turquoise

    def make_path(self):
        self.color = purple

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # left
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):  # heuristic fn to calculate manhattan distance
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def draw_text(text, font, color, surface, x, y):
    pygame.font.init()
    textObj = font.render(text, 1, color)
    text_rect = textObj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(textObj, text_rect)


def a_star(draw, grid, start, end):
    # draw = Lambda: print('hello') - prints hello each time draw is called
    count = 0  # to break ties if two nodes with the same f score, consider the one inserted first
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float('inf') for row in grid for spot in row}  # table to score all g scores
    # list comprehension, for row in grid for spot in row, g_score of spot = infinity
    g_score[start] = 0
    f_score = {spot: float('inf') for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos()) + g_score[start]
    open_set_hash = {start}  # to check what's in the priority queue, the pq data structure doesn't let us check
    while not open_set.empty():  # empty when gone through the entire set
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]  # stores f_score, count and node, just to get node
        open_set_hash.remove(current)
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()  # don't overwrite start and end nodes
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()  # make it green
        draw()
        if current != start:
            current.make_closed()  # make it red once we're done considering
    return False


def algorithm_2(draw, grid, start, end):
    # draw = Lambda: print('hello') - prints hello each time draw is called
    count = 0  # to break ties if two nodes with the same f score, consider the one inserted first
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float('inf') for row in grid for spot in row}  # table to score all g scores
    # list comprehension, for row in grid for spot in row, g_score of spot = infinity
    g_score[start] = 0
    f_score = {spot: float('inf') for row in grid for spot in row}
    f_score[start] = g_score[start]
    open_set_hash = {start}  # to check what's in the priority queue, the pq data structure doesn't let us check
    while not open_set.empty():  # empty when gone through the entire set
        draw_text('-', font, (0, 0, 0), screen, 0, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]  # stores f_score, count and node, just to get node
        open_set_hash.remove(current)
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()  # don't overwrite start and end nodes
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()  # make it green
        draw()
        if current != start:
            current.make_closed()  # make it red once we're done considering
    return False


def make_grid(row, width):
    grid = []
    gap = width // row  # width of each cube
    for i in range(row):
        grid.append([])
        for j in range(row):
            spot = Node(i, j, gap, row)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):  # draw grid lines
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, grey, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(win, grey, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):  # draws the rectangles
    win.fill(white)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    rows = 50
    grid = make_grid(rows, width)

    start = None
    end = None
    run = True
    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:  # lmb
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]
                if not start and spot != end:  # if start isn't there
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()
            elif pygame.mouse.get_pressed()[2]:  # rmb
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                if spot == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    a_star(lambda: draw(win, grid, rows, width), grid, start, end)
                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(rows, width)
                if event.key == pygame.K_ESCAPE:
                    run = False


def main_(win, width):
    rows = 50
    grid = make_grid(rows, width)

    start = None
    end = None
    run = True
    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:  # lmb
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]
                if not start and spot != end:  # if start isn't there
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()
            elif pygame.mouse.get_pressed()[2]:  # rmb
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                if spot == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm_2(lambda: draw(win, grid, rows, width), grid, start, end)
                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(rows, width)
                if event.key == pygame.K_ESCAPE:
                    run = False


def main_menu():
    click = False
    color_1 = (255, 255, 255)
    color_2 = (70, 70, 70)
    while True:
        screen.blit(bg, (0, 0))
        draw_text('Main Menu', font, (255, 255, 255), screen, 20, 20)
        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)
        pygame.draw.rect(screen, color_1, button_1)
        pygame.draw.rect(screen, color_2, button_2)
        mx, my = pygame.mouse.get_pos()
        if button_1.collidepoint(mx, my):
            color_1 = (70, 70, 70)
            if click:
                main(screen, WIDTH)
        else:
            color_1 = (255, 255, 255)
        if button_2.collidepoint(mx, my):
            color_2 = (70, 70, 70)
            if click:
                main_(screen, WIDTH)
        else:
            color_2 = (255, 255, 255)
        draw_text("Dijkstra's", font, (0, 0, 0), screen, 60, 210)
        draw_text('A*', font, (0, 0, 0), screen, 60, 100)
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            pygame.display.update()


main_menu()
