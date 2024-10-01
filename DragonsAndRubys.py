import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
import sys
import ctypes

# Set the default border thickness
border_thickness = 10

# Class representing each segment of the dragon or the ruby
class cube():
    def __init__(self, start, dirnx=1, dirny=0, color=(86, 248, 91), grid_size_x=20, grid_size_y=20, border_thickness=10):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y
        self.border_thickness = border_thickness

    # Move the cube by updating its direction and position
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    # Draw the cube on the surface, optionally with eyes for the dragon's head
    def draw(self, surface, eyes=False, shape='square'):
        dis_x = self.grid_size_x
        dis_y = self.grid_size_y
        i = self.pos[0]
        j = self.pos[1]

        x = i * dis_x + 1 + self.border_thickness
        y = j * dis_y + 1 + self.border_thickness
        width = dis_x - 2
        height = dis_y - 2

        if shape == 'square':
            pygame.draw.rect(surface, self.color, (x, y, width, height))
            if eyes:  # Draw blue eyes on the dragon's head
                centre_x = x + width // 2
                centre_y = y + height // 2
                radius = 3
                circleMiddle = (centre_x - radius, y + 8)
                circleMiddle2 = (x + width - radius * 2, y + 8)
                pygame.draw.circle(surface, (0, 0, 255), circleMiddle, radius)
                pygame.draw.circle(surface, (0, 0, 255), circleMiddle2, radius)
        elif shape == 'diamond':  # Draw the ruby as a diamond
            center_x = x + width // 2
            center_y = y + height // 2
            point_top = (center_x, y)
            point_right = (x + width, center_y)
            point_bottom = (center_x, y + height)
            point_left = (x, center_y)
            pygame.draw.polygon(surface, self.color, [point_top, point_right, point_bottom, point_left])

# Class representing the dragon
class dragon():
    body = []
    turns = {}

    def __init__(self, color, pos, grid_size_x, grid_size_y, border_thickness):
        self.head = cube(pos, grid_size_x=grid_size_x, grid_size_y=grid_size_y, border_thickness=border_thickness, color=color)
        self.body = []
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        self.previous_move = (self.dirnx, self.dirny)
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y
        self.border_thickness = border_thickness

    # Move the dragon based on user input and update its position
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if len(self.body) >= 3:
            # Prevent 180-degree turns if the dragon's size is 3 or more
            if keys[pygame.K_LEFT] and self.previous_move != (1, 0):
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_RIGHT] and self.previous_move != (-1, 0):
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_UP] and self.previous_move != (0, 1):
                self.dirny = -1
                self.dirnx = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_DOWN] and self.previous_move != (0, -1):
                self.dirny = 1
                self.dirnx = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        else:
            # No movement restriction if the dragon has less than 3 cubes
            if keys[pygame.K_LEFT]:
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_RIGHT]:
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_UP]:
                self.dirny = -1
                self.dirnx = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_DOWN]:
                self.dirny = 1
                self.dirnx = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        if keys[pygame.K_q]:  # Pause the game and ask the user if they want to quit
            self.pause_game()

        self.previous_move = (self.dirnx, self.dirny)

        # Update the position of each cube in the dragon's body
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx, c.dirny)

    # Reset the dragon's position and body length
    def reset(self, pos):
        self.head = cube(pos, grid_size_x=self.grid_size_x, grid_size_y=self.grid_size_y, border_thickness=self.border_thickness, color=self.head.color)
        self.body = [self.head]
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        self.previous_move = (self.dirnx, self.dirny)

    # Add a new cube to the dragon's body
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            new_pos = (tail.pos[0] - 1, tail.pos[1])
        elif dx == -1 and dy == 0:
            new_pos = (tail.pos[0] + 1, tail.pos[1])
        elif dx == 0 and dy == 1:
            new_pos = (tail.pos[0], tail.pos[1] - 1)
        elif dx == 0 and dy == -1:
            new_pos = (tail.pos[0], tail.pos[1] + 1)
        else:
            new_pos = tail.pos

        new_color = self.get_cube_color(len(self.body))
        new_cube = cube(new_pos, dirnx=dx, dirny=dy, grid_size_x=self.grid_size_x, grid_size_y=self.grid_size_y, border_thickness=self.border_thickness, color=new_color)
        self.body.append(new_cube)

    # Calculate the color for each new cube based on its position in the dragon's body
    def get_cube_color(self, index):
        color_stops = [
            (86, 248, 91),  # #56f85b
            (29, 213, 38),  # #1dd526
            (8, 219, 15),   # #08db0f
            (2, 70, 4)      # #024604
        ]
        transition_steps_list = [5, 10, 15]
        total_transitions = len(transition_steps_list)
        cumulative_steps = [0]

        for steps in transition_steps_list:
            cumulative_steps.append(cumulative_steps[-1] + steps)

        if index <= cumulative_steps[-1]:
            for i in range(total_transitions):
                if cumulative_steps[i] < index <= cumulative_steps[i + 1]:
                    start_color = color_stops[i]
                    end_color = color_stops[i + 1]
                    steps_in_transition = transition_steps_list[i]
                    position_in_transition = index - cumulative_steps[i]
                    fraction = position_in_transition / steps_in_transition
                    r = int(start_color[0] + fraction * (end_color[0] - start_color[0]))
                    g = int(start_color[1] + fraction * (end_color[1] - start_color[1]))
                    b = int(start_color[2] + fraction * (end_color[2] - start_color[2]))
                    return (r, g, b)
        else:
            final_color_index = cumulative_steps[-1]
            keep_final_color_until = final_color_index + 7
            if index <= keep_final_color_until:
                return color_stops[-1]
            else:
                transition_to_white_index = index - keep_final_color_until
                transition_to_white_steps = 30
                if transition_to_white_index <= transition_to_white_steps:
                    fraction = transition_to_white_index / transition_to_white_steps
                    start_color = color_stops[-1]
                    end_color = (255, 255, 255)
                    r = int(start_color[0] + fraction * (end_color[0] - start_color[0]))
                    g = int(start_color[1] + fraction * (end_color[1] - start_color[1]))
                    b = int(start_color[2] + fraction * (end_color[2] - start_color[2]))
                    return (r, g, b)
                else:
                    return (255, 255, 255)

    # Draw the entire dragon on the screen
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

    # Pause the game and ask the user if they want to quit
    def pause_game(self):
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askyesno("Pause", "Do you want to quit?")
        if result:
            pygame.quit()
            sys.exit()
        root.destroy()

# Update and redraw the window
def redrawWindow(win, d, ruby, width, height, grid_size_x, grid_size_y):
    win.fill((0, 0, 0))
    drawBorder(win, width, height)
    drawGrid(win, width, height, grid_size_x, grid_size_y)
    d.draw(win)
    ruby.draw(win, shape='diamond')
    pygame.display.update()

# Draw the grid lines for the game
def drawGrid(surface, width, height, grid_size_x, grid_size_y):
    for x in range(0, width, grid_size_x):
        pygame.draw.line(surface, (255, 255, 255), (x + border_thickness, border_thickness), (x + border_thickness, height + border_thickness))
    for y in range(0, height, grid_size_y):
        pygame.draw.line(surface, (255, 255, 255), (border_thickness, y + border_thickness), (width + border_thickness, y + border_thickness))

# Draw the border around the game window
def drawBorder(surface, width, height):
    pygame.draw.rect(surface, (128, 128, 128), (0, 0, width + 2 * border_thickness, border_thickness))
    pygame.draw.rect(surface, (128, 128, 128), (0, height + border_thickness, width + 2 * border_thickness, border_thickness))
    pygame.draw.rect(surface, (128, 128, 128), (0, 0, border_thickness, height + 2 * border_thickness))
    pygame.draw.rect(surface, (128, 128, 128), (width + border_thickness, 0, border_thickness, height + 2 * border_thickness))

# Randomly place the ruby on the grid
def randomRuby(cols, rows, d):
    positions = d.body
    while True:
        x = random.randrange(1, cols - 1)
        y = random.randrange(1, rows - 1)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return (x, y)

# Set the game size based on user input
def get_game_size():
    size_input = input("Select game size (small/medium/large): ").strip().lower()
    if size_input == "small":
        return 200, 200, 10, 10
    elif size_input == "large":
        return 700, 700, 35, 30
    else:
        return 500, 500, 25, 20

# Bring the game window to the front
def bring_window_to_front():
    hwnd = pygame.display.get_wm_info()['window']
    ctypes.windll.user32.SetForegroundWindow(hwnd)

# Main function to run the game loop
def main():
    global d, ruby, win
    game_started = False
    pygame.init()

    width, height, cols, rows = get_game_size()
    grid_size_x = width // cols
    grid_size_y = height // rows

    win = pygame.display.set_mode((width + 2 * border_thickness, height + 2 * border_thickness))
    pygame.display.set_caption("Dragon and Ruby Game")

    bring_window_to_front()

    if not game_started:
        print("The game has started!")
        game_started = True

    d = dragon((86, 248, 91), (cols // 2, rows // 2), grid_size_x, grid_size_y, border_thickness)
    d.addCube()
    ruby = cube(randomRuby(cols, rows, d), color=(255, 0, 0), grid_size_x=grid_size_x, grid_size_y=grid_size_y, border_thickness=border_thickness)

    flag = True
    clock = pygame.time.Clock()
    max_score = (cols - 2) * (rows - 2)

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        d.move()
        headPos = d.head.pos
        if headPos[0] >= cols or headPos[0] < 0 or headPos[1] >= rows or headPos[1] < 0:
            print("Score:", len(d.body))
            d.reset((cols // 2, rows // 2))

        if d.body[0].pos == ruby.pos:
            d.addCube()
            if len(d.body) - 1 == max_score:
                print("Congratulations! You won the game!")
                root = tk.Tk()
                root.withdraw()
                messagebox.showinfo("You Win!", "Congratulations! You have filled the board and won the game!")
                pygame.quit()
                sys.exit()
            else:
                ruby = cube(randomRuby(cols, rows, d), color=(255, 0, 0), grid_size_x=grid_size_x, grid_size_y=grid_size_y, border_thickness=border_thickness)

        for x in range(len(d.body)):
            if d.body[x].pos in list(map(lambda z: z.pos, d.body[x + 1:])):
                print("Score:", len(d.body))
                d.reset((cols // 2, rows // 2))
                break

        redrawWindow(win, d, ruby, width, height, grid_size_x, grid_size_y)

main()
