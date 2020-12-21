import sys
import random
import pygame
pygame.init()


WIDTH, HEIGHT = 600, 600
num_cell = 20

cols, rows = WIDTH // num_cell, HEIGHT // num_cell
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(
    "maze generator menggunakan algoritma backtracking".title())
fps_clock = pygame.time.Clock()



class Cell(object):
    def __init__(self, i, j, n):
        self.i = int(i)
        self.j = int(j)
        self.n = n
        self.visited = False

        self.color = (255, 255, 255)
        self.bgcolor = (0, 0, 0)

        # top, right, bottom, right
        self.walls = [True, True, True, True]

    def __repr__(self):
        return f"<cell (i={self.i}, j={self.j}, n={self.n})>"

    def cell_index(self, i, j):
        if i < 0 or j < 0 or i > num_cell - 1 or j > num_cell - 1:
            return None
        else:
            index = i + j * num_cell
            return grid[index]

    def checkNeighbors(self, check=True):
        neighbors = []

        for i, n in enumerate([
            self.cell_index(self.i, self.j - 1),
            self.cell_index(self.i + 1, self.j),
            self.cell_index(self.i, self.j + 1),
            self.cell_index(self.i - 1, self.j)
        ]):
            if n is not None and (not check or n.visited is False):
                neighbors.append((i, n))

        if not check:
            return neighbors
        elif len(neighbors) > 0:
            return random.choice(neighbors)

    def getRect(self):
        x = self.i * cols
        y = self.j * rows
        if cols - 10 > 0:
            rect = pygame.Rect(x + 5, y + 5, cols - 10, rows - 10)
        else:
            rect = pygame.Rect(x, y, cols, rows)
        return rect

    def highlight(self):
        pygame.draw.rect(surface, (0, 200, 0), self.getRect())

    def set_finish(self):
        self.bgcolor = (200, 0, 0)
        self.visited = self.getRect()

    def show(self):
        x = self.i * cols
        y = self.j * rows

        if self.visited:
            if isinstance(self.visited, pygame.Rect):
                rect = self.visited
            else:
                rect = (x, y, cols, rows)
            pygame.draw.rect(surface, self.bgcolor,
                             rect)
            if self.walls[0]:
                pygame.draw.line(surface, self.color, (x, y), (x + cols, y))
            if self.walls[1]:
                pygame.draw.line(surface, self.color, (x + cols, y),
                                 (x + cols, y + rows))
            if self.walls[2]:
                pygame.draw.line(
                    surface, self.color, (x + cols, y + rows), (x, y + rows))
            if self.walls[3]:
                pygame.draw.line(surface, self.color, (x, y + rows), (x, y))


grid = []
playable = False
stack = []
current = None
last_index = ()

def initialize():
    global grid, playable, stack, current, last_index
    grid = []
    playable = False
    stack = []

    for j in range(num_cell):
        for i in range(num_cell):
            cell = Cell(i, j, len(grid))
            grid.append(cell)

    current = grid[0]
    last_index = (-1, None)

initialize()
while True:
    surface.fill(0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == 768 and event.key == ord("r"):
            initialize()
        elif playable is True and event.type == 768:
            walls = current.walls
            move = -1
            if event.key == ord("w") and not walls[0]:
                move = 0
            elif event.key == ord("d") and not walls[1]:
                move = 1
            elif event.key == ord("s") and not walls[2]:
                move = 2
            elif event.key == ord("a") and not walls[3]:
                move = 3

            for n, cell in current.checkNeighbors(False):
                if n == move:
                    current = cell
                    break
            if current == last_index[1]:
                playable = None

    if playable is False:
        current.visited = True
        next_ = current.checkNeighbors()
        if next_ is not None:
            index, next_ = next_
            current.walls[index] = False
            next_.walls[{0: 2, 1: 3, 2: 0, 3: 1}[index]] = False
            stack.append(current)
            current = next_
        else:
            if stack:
                current = stack.pop()

                lstack = len(stack)
                if lstack > last_index[0]:
                    last_index = (lstack, current)
            else:
                last = last_index[1]
                for _, n in last.checkNeighbors(False):
                    if len(list(filter(lambda x: x, n.walls))) == 3:
                        last_index = (last_index[0] + 1, n)
                        break
                last_index[1].set_finish()
                playable = True

    # draw every single cell
    for cell in grid:
        cell.show()
    current.highlight()
    pygame.draw.rect(surface, (255, 255, 255), (0, 0, WIDTH, HEIGHT), 1)

    pygame.display.update()
    fps_clock.tick(20)
