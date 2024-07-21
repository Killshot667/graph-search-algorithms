import pygame
import math
from queue import PriorityQueue, Queue
import sys

# pylint: disable=no-member
pygame.init()


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('Breadth first search visuliser')

RED = (255, 0, 0)
SKY_BLUE = (135, 206, 235)
GREEN = (0, 255, 0)
NAVY = (0, 0, 139)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == NAVY
    
    def is_open(self):
        return self.color == SKY_BLUE
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == GREEN
    
    def is_end(self):
        return self.color == RED

    def reset(self):
        self.color = WHITE
    
    def make_closed(self):
        self.color = NAVY 

    def make_open(self):
        self.color = SKY_BLUE
    
    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = GREEN
    
    def make_end(self):
        self.color = RED
    
    def make_path(self):
        self.color = YELLOW
    
    def draw(self,win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self,other):
        return False
    
def h(a, b):
    row1, col1 = a
    row2, col2 = b
    return abs(row1-row2) + abs(col1-col2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = Queue()
    open_set.put(start)
    open_set_hash = {start}
    came_from = {}
    visited=set()
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()
        open_set_hash.remove(current)
        visited.add(current)
        # open_set_hash.remove(current)
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        
        for neighbor in current.neighbors:
            if neighbor not in visited and neighbor not in open_set_hash:
                came_from[neighbor] = current
                open_set.put(neighbor)
                open_set_hash.add(neighbor)
                neighbor.make_open()
        
        draw()
        if current != start:
            current.make_closed()
        draw()
    
    return False


        

def make_grid(rows, span):
    gap = span // rows
    grid = []

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    
    return grid

def draw_grid(win, rows, span):
    gap = span // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (span, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, span))

def draw(win, grid, rows, span):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    
    draw_grid(win, rows, span)
    pygame.display.update()

def get_clicked(pos, rows, span):
    gap = span // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main(win, span):
    ROWS = 50
    grid = make_grid(ROWS, span)

    start = None
    end = None
    
    run = True
    started = False

    while run:
        draw(win, grid, ROWS, span) 
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT: 
                run = False
            
            if started:
                continue
            
            if pygame.mouse.get_pressed()[0]: # left mouse click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked(pos, ROWS, span)
                spot = grid[row][col]
                
                if not start:
                    start = spot
                    start.make_start()
                
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                
                elif spot != start and spot != end:
                    spot.make_barrier()

            
            elif pygame.mouse.get_pressed()[2]: # right mouse click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked(pos, ROWS, span)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    
                    algorithm(lambda: draw(win, grid, ROWS, span), grid, start, end)
                
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, WIDTH)
   
    pygame.quit()       
    sys.exit()

main(WIN, WIDTH)