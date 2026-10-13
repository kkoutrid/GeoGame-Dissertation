import pygame
import os
import numpy as np              # Numeric functions and arrays
import pandas as pd

# Initialize Pygame
pygame.init()

'read input data'
idata = pd.read_excel(r"C:\\Diplomatikh\diplomatikh\2023-07-05\GeoData.xlsx",  sheet_name="na_icons")
na_icons_L  = idata['left'].to_numpy()
na_icons_R  = idata['right'].to_numpy()
na_icons_U  = idata['up'].to_numpy()
na_icons_D  = idata['down'].to_numpy()
na_icons0 = np.concatenate((na_icons_L, na_icons_R, na_icons_U, na_icons_D))
na_icons = np.reshape(na_icons0, (4,11))

# Screen dimensions
screen_width = 700
screen_height = 700

# Grid dimensions
grid_size = 17
square_size = 32

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Grid")

# Load the icons
icon_dir = "icons"
icons = []
icon_pw_path = os.path.join(icon_dir, "icon11.png")
icon_pw = pygame.image.load(icon_pw_path).convert_alpha()
for i in range(1, 11):
    icon_path = os.path.join(icon_dir, f"icon{i}.png")
    icon_image = pygame.image.load(icon_path).convert_alpha()
    icons.append(icon_image)

# Define the square properties
square_x = 64
square_y = 64

# Initialize the grid state
grid = [[None] * grid_size for _ in range(grid_size)]
# Initialize the placement grid state
placement_grid = [[-1] * grid_size for _ in range(grid_size)]
# Initialize the dropdown menu state
dropdown_open = False
dropdown_x = 0
dropdown_y = 0
dropdown_width = square_size
dropdown_height = square_size * len(icons)
dropdown_rect = pygame.Rect(0, 0, 0, 0)

# Button dimensions
button_width = 100
button_height = 50

# Button position
button_x = (screen_width - button_width) // 2
button_y = screen_height - square_size - button_height - 10

# Undo button position
undo_button_x = button_x - button_width - 10
undo_button_y = button_y

# Undo stack
undo_stack = []

def initialize_grid():
    """Initialize the two center cells of the grid as icon_pw."""
    center_row = (grid_size - 6) // 2
    center_col = grid_size // 2
    grid[center_row][center_col] = icon_pw
    placement_grid[center_row][center_col] = 10

def reset_grid():
    """Reset the grid by clearing all icons except for icon_pw."""
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] is not None and grid[i][j] != icon_pw:
                grid[i][j] = None
                placement_grid[i][j] = -1

def undo():
    """Undo the last placed icon on the grid."""
    if undo_stack:
        row, col = undo_stack.pop()
        grid[row][col] = None
        placement_grid[row][col] = -1

def get_available_icons(row, col):
    """Get the available icons based on the placement grid values."""
    available_icons = icons.copy()
    # Check the surrounding cells
    i = -1
    icons2rem = []
    for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        i = i + 1
        neighbor_row = row + dr
        neighbor_col = col + dc
        if (
            0 <= neighbor_row < grid_size
            and 0 <= neighbor_col < grid_size
            and placement_grid[neighbor_row][neighbor_col] >-1
        ):
            #= [int(num) for num in my_string.split(',')]
            icons2rem.append(na_icons[i][placement_grid[neighbor_row][neighbor_col]])

    if len(icons2rem) != 0:
        icons2rem = [int(j) for j in ",".join(icons2rem).split(',')]
        icons2rem = list(set(icons2rem))
        #print('in', icons2rem)
        for j in icons2rem:
            available_icons.remove(icons[j-1])
    return available_icons


# Initialize the grid
initialize_grid()

# Main game loop
running = True
placed_new_item = False  # Flag to track if a new item is placed
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not dropdown_open:
            # Check if the button to reset the grid is clicked
            if button_x <= event.pos[0] <= button_x + button_width and button_y <= event.pos[1] <= button_y + button_height:
                reset_grid()
            # Check if the button to undo is clicked
            elif undo_button_x <= event.pos[0] <= undo_button_x + button_width and undo_button_y <= event.pos[1] <= undo_button_y + button_height:
                undo()
            else:
                row = (event.pos[1] - square_y) // square_size
                col = (event.pos[0] - square_x) // square_size
                available_icons = get_available_icons(row, col)
                print('out', available_icons)
                print('out2', len(available_icons))
                if 0 <= row < grid_size and 0 <= col < grid_size and placement_grid[row+1][col] != -1 or placement_grid[row-1][col]!= -1 or placement_grid[row][col-1]!= -1 or placement_grid[row][col+1]!= -1:
                    if grid[row][col] is None:
                        dropdown_x = square_x + col * square_size
                        dropdown_y = square_y + (row + 1) * square_size
                        dropdown_width = square_size
                        dropdown_height = square_size * len(available_icons)
                        dropdown_rect = pygame.Rect(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                        dropdown_open = True
                        selected_icon = None
                    else:
                        dropdown_open = False
                        selected_icon = grid[row][col]
        elif event.type == pygame.MOUSEBUTTONDOWN and dropdown_open:
            if not dropdown_rect.collidepoint(event.pos):
                dropdown_open = False
                selected_icon = None
            else:
                icon_index = (event.pos[1] - dropdown_y) // square_size
                #selected_icon = icons[icon_index]
                selected_icon = available_icons[icon_index]
                icon_index = icons.index(selected_icon)
                print(icon_index)
                row = (dropdown_y - square_y - square_size) // square_size
                col = (dropdown_x - square_x) // square_size
                grid[row][col] = selected_icon
                placement_grid[row][col] = icon_index
                dropdown_open = False
                # Add the placed icon to the undo stack
                undo_stack.append((row, col))
                placed_new_item = True

    # Clear the screen
    screen.fill(BLUE)

    # Draw the reset grid button
    pygame.draw.rect(screen, GRAY, (button_x, button_y, button_width, button_height))
    reset_font = pygame.font.Font(None, 36)
    reset_text = reset_font.render("Reset", True, WHITE)
    reset_text_rect = reset_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(reset_text, reset_text_rect)

    # Draw the undo button
    pygame.draw.rect(screen, GRAY, (undo_button_x, undo_button_y, button_width, button_height))
    undo_text = reset_font.render("Undo", True, WHITE)
    undo_text_rect = undo_text.get_rect(center=(undo_button_x + button_width // 2, undo_button_y + button_height // 2))
    screen.blit(undo_text, undo_text_rect)

    # Draw the grid
    for i in range(grid_size):
        for j in range(grid_size):
            rect = pygame.Rect(square_x + j * square_size, square_y + i * square_size, square_size, square_size)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

            # Draw the icon in the square if it exists
            icon = grid[i][j]
            if icon is not None:
                if icon == BLACK:
                    pygame.draw.rect(screen, BLACK, rect)
                    pygame.draw.rect(screen, WHITE, rect, 1)
                else:
                    icon_scaled = pygame.transform.scale(icon, (square_size - 2, square_size - 2))
                    screen.blit(icon_scaled, rect.move(1, 1))

    # Draw the dropdown menu
    if dropdown_open:
        pygame.draw.rect(screen, WHITE, dropdown_rect)
        pygame.draw.rect(screen, BLACK, dropdown_rect, 1)

        for i, icon in enumerate(available_icons): #for i, icon in enumerate(icons):
            icon_scaled = pygame.transform.scale(icon, (square_size, square_size))
            dropdown_icon_rect = pygame.Rect(dropdown_x, dropdown_y + i * square_size, square_size, square_size)
            screen.blit(icon_scaled, dropdown_icon_rect)


    # Print the placement grid if a new item is placed
    if placed_new_item:
        print("Placement Grid:")
        for row in placement_grid:
            print(row)
        print()
        placed_new_item = False

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
