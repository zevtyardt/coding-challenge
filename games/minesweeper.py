import pygame
import sys
import random
pygame.init()


WIDTH, HEIGHT = 600, 600
num_cell = 10
total_mines = 10

cols, rows = WIDTH // num_cell, HEIGHT // num_cell
surface = pygame.display.set_mode((WIDTH, HEIGHT))

# ukuran font sesuaikan sama ukuran layar
font_obj = pygame.font.Font("freesansbold.ttf", 32)

pygame.display.set_caption("Minesweeper".title())
fps_clock = pygame.time.Clock()


class Cell(object):
    def __init__(self, i, j, n):
        self.i = i
        self.j = j
        self.n = n

        self.mine = False
        self.revealed = False
        self.color = (255, 255, 255)
        self.total_mine = 0
        self.is_checked = False

    def __repr__(self):
        return f"<cell (i={self.i}, j={self.j}, n={self.n})>"

    def show(self):
        x = self.i * cols
        y = self.j * rows
        rect1 = pygame.Rect(x, y, cols, rows)
        if self.revealed:
            pygame.draw.rect(surface, (15, 15, 15), rect1)
            if not self.mine:
                total_mine = self.checkNeighbors()
                if total_mine > 0:
                    msg = font_obj.render(f"{total_mine}", True, self.color)
                    msg_rect = msg.get_rect()
                    msg_rect.topleft = (x + msg_rect[2], y + msg_rect[3] * 0.5)
                    surface.blit(msg, msg_rect)
            else:
                rect = pygame.Rect(x + cols // 4, y + rows // 4, cols * 0.5, rows * 0.5)
                pygame.draw.ellipse(surface, (200, 0, 0), rect)
        pygame.draw.rect(surface, self.color, rect1, 1)

    def yield_neighbors(self):
        for x, y in [
            (-1, -1), (0, -1), (1, -1),
            (-1, 0), (1, 0),
            (-1, 1), (0, 1), (1, 1)
        ]:
            yield cell_index(self.i + x, self.j + y)

    def checkNeighbors(self):
        if not self.is_checked:
            for cell in self.yield_neighbors():
                if cell and cell.mine:
                    self.total_mine += 1
            self.is_checked = True
        return self.total_mine

    def reveal(self):
        self.revealed = True
        if self.checkNeighbors() == 0:
            self.floodFill()

    def floodFill(self):
        for cell in self.yield_neighbors():
            if cell and not cell.revealed and not cell.mine:
                cell.reveal()

grid = []
gameOver = False
mines = total_mines

def initialize():
    global grid, gameOver
    grid = []
    gameOver = False
    mines = total_mines
    for j in range(num_cell):
        for i in range(num_cell):
            cell = Cell(i, j, len(grid))
            grid.append(cell)

    while mines > 0:
        cell = random.choice(grid)
        if not cell.mine:
            cell.mine = True
            mines -= 1

def cell_index(i, j):
    if i < 0 or j < 0 or i > num_cell - 1 or j > num_cell - 1:
        return None
    else:
        index = i + j * num_cell
        return grid[index]

initialize()
while True:
    surface.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == 768 and event.key == ord("r"):
            initialize()

        # left click
        if not gameOver and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            i, j = x // cols, y // rows

            cell = cell_index(i, j)
            if cell.mine:
                    gameOver = True
            cell.reveal()        

    for cell in grid:
        if gameOver and cell.mine:
            cell.revealed = True
        cell.show()

    pygame.display.update()
