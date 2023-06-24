# pygame_app.py

import pygame
import sys

# Initialize Pygame
pygame.init()

# Grid dimensions
grid_size = (10, 10)
tile_size = 50

# Window size
window_size = (grid_size[0]*tile_size, grid_size[1]*tile_size)

# Create the window
screen = pygame.display.set_mode(window_size)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Current position
pos = [0, 0]

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                pos[1] = max(0, pos[1] - 1)
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                pos[0] = max(0, pos[0] - 1)
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                pos[1] = min(grid_size[1] - 1, pos[1] + 1)
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                pos[0] = min(grid_size[0] - 1, pos[0] + 1)

    # Draw the grid
    screen.fill(black)
    for y in range(grid_size[1]):
        for x in range(grid_size[0]):
            rect = pygame.Rect(x*tile_size, y*tile_size, tile_size, tile_size)
            if (x, y) == (pos[0], pos[1]):
                pygame.draw.rect(screen, white, rect)
            pygame.draw.rect(screen, white, rect, 1)

    pygame.display.flip()

pygame.quit()
sys.exit()
