import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 400
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Left Arrow")

# Set colors
white = (255, 255, 255)
black = (0, 0, 0)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(white)

    # Draw arrow
    pygame.draw.polygon(screen, black, [(100, 150), (150, 100), (150, 125), (250, 125), (250, 175), (150, 175), (150, 200)])

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
