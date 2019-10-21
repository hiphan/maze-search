import pygame
from PIL import Image, ImageDraw
import heapq
import math
from random import randint


class Node(object):

    def __init__(self, xy, g=9999, f=9999):
        self.xy = xy
        self.g = g  # ~inf
        self.f = f  # ~inf
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.xy == other.xy


class PacMan(object):

    def __init__(self, maze, x, y):
        self.maze = maze
        self.surface = maze.surface
        self.pacman_x = x
        self.pacman_y = y
        self.direction = 1  # Direction pacman is facing: 0 - Top; 1 - Right; 2 - Bottom; 3 - Left
        self.mouth_closed = False
        self.goal = False
        self.goal_x = -1
        self.goal_y = -1
        self.path = []

    def run(self):
        if self.goal:
            if self.path:
                self.follow_path()
                if (self.pacman_x, self.pacman_y) == (self.goal_x, self.goal_y):
                    print('Reached goal.')
                    self.goal = False
            else:
                self.a_star_search(self.heuristic)
        else:
            new_goal_x = randint(0, self.maze.height - 1)
            new_goal_y = randint(0, self.maze.width - 1)
            self.set_goal(new_goal_x, new_goal_y)

        self.mouth_closed = not self.mouth_closed

    def draw(self):
        # PIL pieslice example at https://github.com/furas/python-examples/tree/master/pygame/pillow-image-pieslice
        pygame.time.wait(100)
        # Mouth opening [start, end] angles which depend on the current facing direction
        open_angles = {
            0: [315, 225],
            1: [45, 315],
            2: [135, 45],
            3: [225, 135]
        }
        close_angles = {
            0: [-90, 270],
            1: [0, 360],
            2: [90, 450],
            3: [-180, 180]
        }
        if self.mouth_closed:
            pil_size = self.maze.cell_size
            pil_image = Image.new("RGBA", (pil_size, pil_size))
            pil_draw = ImageDraw.Draw(pil_image)
            pil_draw.pieslice((5, 5, pil_size - 5, pil_size - 5), close_angles[self.direction][0],
                              close_angles[self.direction][1], fill=(255, 255, 0), outline=(0, 0, 0))
        else:
            pil_size = self.maze.cell_size
            pil_image = Image.new("RGBA", (pil_size, pil_size))
            pil_draw = ImageDraw.Draw(pil_image)
            pil_draw.pieslice((5, 5, pil_size - 5, pil_size - 5), open_angles[self.direction][0],
                              open_angles[self.direction][1], fill=(255, 255, 0), outline=(0, 0, 0))

        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()
        pacman_image = pygame.image.fromstring(data, size, mode)
        self.surface.blit(pacman_image, (self.pacman_y, self.pacman_x))

        # draw goal (cherry)
        if self.goal:
            cherry = pygame.image.load('cherry.jpg')
            color = cherry.get_at((0, 0))
            cherry.set_colorkey(color)
            cherry = cherry.convert()
            cherry = pygame.transform.scale(cherry, (pil_size, pil_size))
            self.surface.blit(cherry, (self.goal_y, self.goal_x))

        pygame.display.update()

    def set_goal(self, x, y):
        self.goal_x = x // self.maze.cell_size * self.maze.cell_size
        self.goal_y = y // self.maze.cell_size * self.maze.cell_size
        self.goal = True

    def heuristic(self, node, dist='euclidean'):
        if dist == 'manhattan':
            return self.manhattan_dist(node)
        elif dist == 'diagonal':
            return self.diagonal_dist(node)
        else:
            return self.euclidean_dist(node)

    def manhattan_dist(self, node, D=1):
        node_x, node_y = node
        dx = abs(node_x - self.goal_x)
        dy = abs(node_y - self.goal_y)
        return D * (dx + dy)

    def diagonal_dist(self, node, D1=1, D2=2):
        node_x, node_y = node
        dx = abs(node_x - self.goal_x)
        dy = abs(node_y - self.goal_y)
        return D1 * (dx + dy) + (D2 - 2 * D1) * min(dx, dy)

    def euclidean_dist(self, node, D=1):
        node_x, node_y = node
        dx = abs(node_x - self.goal_x)
        dy = abs(node_y - self.goal_y)
        return D * math.sqrt(dx ** 2 + dy ** 2)

    def a_star_search(self, h):
        if not self.goal:
            return "NO GOAL"
        open_list = []
        closed_list = []

        start = Node((self.pacman_x, self.pacman_y))
        start.g = 0
        start.f = h(start.xy)
        heapq.heappush(open_list, start)

        while open_list:
            current_node = heapq.heappop(open_list)
            current_xy = current_node.xy

            # Check goal
            if current_xy == (self.goal_x, self.goal_y):
                return self.backtrack_path(current_node)

            closed_list.append(current_node)

            successors = self.get_successors(current_node)
            for successor in successors:
                if successor in closed_list:
                    continue
                tentative_g = current_node.g
                if tentative_g < successor.g:
                    successor.parent = current_node
                    successor.g = tentative_g
                    successor.f = successor.g + h(successor.xy)
                    if successor not in open_list:
                        heapq.heappush(open_list, successor)
        return "FAILURE"

    def get_successors(self, node):
        curr_x, curr_y = node.xy
        successors = []
        cell_size = self.maze.cell_size
        if curr_x - cell_size >= 0 and not self.maze.grid[curr_x // cell_size][curr_y // cell_size].wall_top:
            successors.append((curr_x - cell_size, curr_y))
        if curr_x + cell_size < self.maze.height and not self.maze.grid[curr_x // cell_size][curr_y // cell_size].wall_bottom:
            successors.append((curr_x + cell_size, curr_y))
        if curr_y - cell_size >= 0 and not self.maze.grid[curr_x // cell_size][curr_y // cell_size].wall_left:
            successors.append((curr_x, curr_y - cell_size))
        if curr_y + cell_size < self.maze.width and not self.maze.grid[curr_x // cell_size][curr_y // cell_size].wall_right:
            successors.append((curr_x, curr_y + cell_size))
        return [Node((s[0], s[1])) for s in successors]

    def backtrack_path(self, goal):
        path = [goal.xy]
        curr_node = goal
        while curr_node.xy != (self.pacman_x, self.pacman_y):
            curr_node = curr_node.parent
            path.append(curr_node.xy)
        self.path = path
        return path

    def follow_path(self):
        next_step = self.path.pop()
        next_x, next_y = next_step
        if next_x == self.pacman_x + self.maze.cell_size:
            self.direction = 2
        elif next_x == self.pacman_x - self.maze.cell_size:
            self.direction = 0
        elif next_y == self.pacman_y + self.maze.cell_size:
            self.direction = 1
        elif next_y == self.pacman_y - self.maze.cell_size:
            self.direction = 3
        else:
            return
        self.pacman_x = next_x
        self.pacman_y = next_y
