import pygame

def draw_blue_square(screen):
    blue_square_size = 100
    blue_square_color = (0, 0, 255)  # RGB value for blue

    pygame.draw.rect(screen, blue_square_color, (700, 100, blue_square_size, blue_square_size))
    pygame.display.update()

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Test Draw Blue Square")
running = True

screen.fill((255, 255, 255))  # Fill the screen with white once at the beginning

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Your existing code for other operations within the loop
    # ...

    # Call the draw_blue_square function to draw the blue square
    draw_blue_square(screen)

    pygame.display.update()

pygame.quit()