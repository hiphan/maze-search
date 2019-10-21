from random import choice
import pygame


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (128, 128, 128)


class MazeCell(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wall_left = True
        self.wall_right = True
        self.wall_top = True
        self.wall_bottom = True
        self.color = white


class Maze(object):

    def __init__(self, surface, width, height):
        self.surface = surface
        self.width = width
        self.height = height
        self.cell_size = 40
        self.grid = []

    # Initialize maze cells with 4 walls each
    def initialize_maze(self):
        for row in range(0, self.height, self.cell_size):
            curr_row = []
            for col in range(0, self.width, self.cell_size):
                curr_row.append(MazeCell(row // self.cell_size, col // self.cell_size))
            self.grid.append(curr_row)

    def draw(self):
        pygame.time.wait(50)

        # Fill color
        for row in range(0, self.height, self.cell_size):
            for col in range(0, self.width, self.cell_size):
                row_idx = row // self.cell_size
                col_idx = col // self.cell_size
                pygame.draw.rect(self.surface, self.grid[row_idx][col_idx].color, (col, row, self.cell_size, self.cell_size))

        # Draw cell walls if any
        for row in range(0, self.height, self.cell_size):
            for col in range(0, self.width, self.cell_size):
                row_idx = row // self.cell_size
                col_idx = col // self.cell_size
                if self.grid[row_idx][col_idx].wall_left:
                    pygame.draw.line(self.surface, black, (col, row), (col, row + self.cell_size), 2)
                if self.grid[row_idx][col_idx].wall_right:
                    pygame.draw.line(self.surface, black, (col + self.cell_size, row), (col + self.cell_size, row + self.cell_size), 2)
                if self.grid[row_idx][col_idx].wall_top:
                    pygame.draw.line(self.surface, black, (col, row), (col + self.cell_size, row), 2)
                if self.grid[row_idx][col_idx].wall_bottom:
                    pygame.draw.line(self.surface, black, (col, row + self.cell_size), (col + self.cell_size, row + self.cell_size), 2)
        pygame.display.update()

    # Recursive backtracker
    def generate_maze(self):
        def get_unvisited_neighbors(curr_cell, visited):
            x, y = curr_cell
            unvisited_neighbors = []
            if x - 1 >= 0 and (x - 1, y) not in visited:
                unvisited_neighbors.append((x - 1, y))
            if x + 1 < (self.height // self.cell_size) and (x + 1, y) not in visited:
                unvisited_neighbors.append((x + 1, y))
            if y - 1 >= 0 and (x, y - 1) not in visited:
                unvisited_neighbors.append((x, y - 1))
            if y + 1 < (self.width // self.cell_size) and (x, y + 1) not in visited:
                unvisited_neighbors.append((x, y + 1))
            return unvisited_neighbors

        def update_visited_cell(cell):
            x, y = cell
            self.grid[x][y].color = gray
            self.draw()

        visited_cells = []
        unvisited_cells = []
        for row in self.grid:
            for cell in row:
                unvisited_cells.append((cell.x, cell.y))
        stack = []

        current_cell = (0, 0)
        visited_cells.append(current_cell)
        unvisited_cells.remove(current_cell)
        update_visited_cell(current_cell)

        while unvisited_cells:
            curr_unvisited_neighbors = get_unvisited_neighbors(current_cell, visited_cells)
            if len(curr_unvisited_neighbors) > 0:
                rand_neighbor = choice(curr_unvisited_neighbors)
                if len(curr_unvisited_neighbors) > 1:
                    stack.append(current_cell)
                self.remove_walls(current_cell, rand_neighbor)

                current_cell = rand_neighbor
                visited_cells.append(current_cell)
                unvisited_cells.remove(current_cell)
                update_visited_cell(current_cell)
            else:
                if stack:
                    while stack:
                        popped_cell = stack.pop()
                        if len(get_unvisited_neighbors(popped_cell, visited_cells)) > 0:
                            break
                        else:
                            continue
                    current_cell = popped_cell

    def remove_walls(self, curr_cell, neighbor):
        x1, y1 = curr_cell
        x2, y2 = neighbor
        if x1 == x2:
            if y2 == y1 + 1:
                self.grid[x1][y1].wall_right = False
                self.grid[x2][y2].wall_left = False
            elif y1 == y2 + 1:
                self.grid[x1][y1].wall_left = False
                self.grid[x2][y2].wall_right = False
        elif y1 == y2:
            if x2 == x1 + 1:
                self.grid[x1][y1].wall_bottom = False
                self.grid[x2][y2].wall_top = False
            elif x1 == x2 + 1:
                self.grid[x1][y1].wall_top = False
                self.grid[x2][y2].wall_bottom = False
