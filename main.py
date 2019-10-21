import pygame
import sys
from maze import *
from pacman import *


pygame.init()

window_width = 800
window_height = 400
window = pygame.display.set_mode((window_width, window_height))

clock = pygame.time.Clock()

maze = Maze(window, window_width, window_height)
maze.initialize_maze()
maze.generate_maze()

pac = PacMan(maze, 0, 0)

running = True

while running:
    clock.tick(60)
    pygame.time.wait(100)
    maze.draw()
    pac.run()
    pac.draw()
    if pygame.event.get(pygame.QUIT):
        running = False

pygame.quit()
sys.exit()
