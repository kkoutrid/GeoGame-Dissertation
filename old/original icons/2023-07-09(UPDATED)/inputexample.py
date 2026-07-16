import pygame
import sys

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 24
INPUT_BOX_WIDTH = 200
INPUT_BOX_HEIGHT = 40

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Player Input Box")

# Function to handle player input
def get_player_input():
    input_box_text = ""
    font = pygame.font.Font(None, FONT_SIZE)
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_box_text = input_box_text[:-1]
                else:
                    input_box_text += event.unicode

        # Draw the input box and the text
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - INPUT_BOX_WIDTH // 2, SCREEN_HEIGHT // 2 - INPUT_BOX_HEIGHT // 2, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT))
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - INPUT_BOX_WIDTH // 2, SCREEN_HEIGHT // 2 - INPUT_BOX_HEIGHT // 2, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT), 2)

        input_text_surface = font.render(input_box_text, True, BLACK)
        screen.blit(input_text_surface, (SCREEN_WIDTH // 2 - input_text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - input_text_surface.get_height() // 2))

        pygame.display.update()

    return input_box_text

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                player_input = get_player_input()
                print("Player input:", player_input)

    # Clear the screen
    screen.fill(WHITE)
    pygame.display.flip()

pygame.quit()
