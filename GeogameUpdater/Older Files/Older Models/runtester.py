import pygame
import sys

# Sample dictionary data
Q2 = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10,
      'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20}

# Initialize Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Scrollable Dictionary Demo")

# Font and text color
font = pygame.font.Font(None, 22)
text_color = (255, 0, 0)

def draw_scrollable_dictionary(Q2, font, screen, text_color):
    # Constants for scroll bar
    SCROLLBAR_WIDTH = 10
    SCROLLBAR_COLOR = (100, 100, 100)
    scroll_position = 0

    # Determine the number of columns to arrange the keys
    num_columns = min(len(Q2), 1)

    while True:
        screen.fill((0, 0, 0))  # Clear the screen

        # Render the dictionary content within the visible portion
        visible_items = list(Q2.items())[scroll_position:scroll_position + 12]  # Display 10 items at a time
        for idx, (key, value) in enumerate(visible_items):
            column = idx % num_columns
            row = idx // num_columns

            # Draw a blue rectangle before rendering text
            rect_x = 625 + column * 90
            rect_y = 345 + row * 30
            rect_width = 130
            rect_height = 305
            pygame.draw.rect(screen, (0, 0, 255), (rect_x, rect_y, rect_width, rect_height))

            text_surface = font.render(f"{key}: {value}", True, text_color)
            screen.blit(text_surface, (650 + column * 90, 350 + row * 30))

        # Draw scroll bar
        scroll_bar_height = 300
        scroll_button_height = scroll_bar_height / len(Q2)
        pygame.draw.rect(screen, SCROLLBAR_COLOR, (980, 350, SCROLLBAR_WIDTH, scroll_bar_height))
        scroll_button_y = 350 + (scroll_position / len(Q2)) * scroll_bar_height
        pygame.draw.rect(screen, (255, 255, 255), (980, scroll_button_y, SCROLLBAR_WIDTH, scroll_button_height))

        pygame.display.update()

        # Event handling for scrolling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    scroll_position = max(0, scroll_position - 1)
                elif event.button == 5:  # Scroll down
                    scroll_position = min(len(Q2) - 10, scroll_position + 1)

# Usage
draw_scrollable_dictionary(Q2, font, screen, text_color)
