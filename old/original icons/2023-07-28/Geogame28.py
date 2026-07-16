import pygame
import os
import numpy as np  # Numeric functions and arrays
import pandas as pd
# IMPORTANT NOTE The game can be made into an HTML5 and have it run online by utilizing pygbad which already supports pygame
root_dir = os.path.dirname(os.path.abspath(__file__))

# game_data
# totalQ = 2000
pipe_section = 0
# Initialize Pygame
pygame.init()

'read input data'
#idata = pd.read_excel(r"C:\\Diplomatikh\diplomatikh\2023-07-09(UPDATED)\geodata.xlsx", sheet_name="na_icons")  # kostas pc
#idata = pd.read_excel(r"C:\Users\User\.spyder-py3\geodata.xlsx",  sheet_name="na_icons") #yiannis pc
idata = pd.read_excel(root_dir + "\geodata.xlsx",  sheet_name="na_icons")
na_icons_L = idata['left'].to_numpy()
na_icons_R = idata['right'].to_numpy()
na_icons_U = idata['up'].to_numpy()
na_icons_D = idata['down'].to_numpy()
na_icons0 = np.concatenate((na_icons_L, na_icons_R, na_icons_U, na_icons_D))
na_icons = np.reshape(na_icons0, (4, 13))
idata = pd.read_excel(root_dir + "\geodata.xlsx",  sheet_name="pipe_connections")
conn_L = idata['left'].to_numpy()
conn_U = idata['up'].to_numpy()
conn_R = idata['right'].to_numpy()
conn_D = idata['down'].to_numpy()
conn0 = np.concatenate((conn_L, conn_U, conn_R, conn_D))
conn = np.reshape(conn0, (4, 13))
#conn[x][y] simainei x=0,1,2,3 left, up, right, down kai y = icon index

# Screen dimensions
screen_width = 1000
screen_height = 800

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
# Load the sounds
#click_sound = pygame.mixer.Sound("C:\Diplomatikh\diplomatikh\\2023-07-09(UPDATED)\SoundEffects\MouseClick.wav")
#enter_input_sound = pygame.mixer.Sound("C:\Diplomatikh\diplomatikh\\2023-07-09(UPDATED)\SoundEffects\EnterInputSound.wav") #kostas
#enter_input_sound = pygame.mixer.Sound("C:\Diplomatikh\diplomatikh\\2023-07-09(UPDATED)\SoundEffects\EnterInputSound.wav") #yiannis
enter_input_sound = pygame.mixer.Sound(root_dir + "\SoundEffects\EnterInputSound.wav")
# Volume Management
#click_sound.set_volume(0.3)
enter_input_sound.set_volume(0.5)
# Load the icons
icon_dir = "icons"
icons = []
icon_pw_path = os.path.join(icon_dir, "icon11.png")
icon_pw = pygame.image.load(icon_pw_path).convert_alpha()
icon_building1_path = os.path.join(icon_dir, "icon12.png")
icon_building1 = pygame.image.load(icon_building1_path).convert_alpha()
icon_building2_path = os.path.join(icon_dir, "icon13.png")
icon_building2 = pygame.image.load(icon_building2_path).convert_alpha()
icon_greenhouse_path = os.path.join(icon_dir, "icon14.png")
icon_greenhouse = pygame.image.load(icon_greenhouse_path).convert_alpha()
icon_rw_path = os.path.join(icon_dir, "icon15.png")
icon_rw = pygame.image.load(icon_rw_path).convert_alpha()
icon_starting_spot_path = os.path.join(icon_dir, "icon16.png")
icon_starting_spot = pygame.image.load(icon_starting_spot_path).convert_alpha()
icon_left_arrow_path = os.path.join(icon_dir, "left_arrow.png")
icon_left_arrow = pygame.image.load(icon_left_arrow_path).convert_alpha()
icon_right_arrow_path = os.path.join(icon_dir, "right_arrow.png")
icon_right_arrow = pygame.image.load(icon_right_arrow_path).convert_alpha()
icon_up_arrow_path = os.path.join(icon_dir, "up_arrow.png")
icon_up_arrow = pygame.image.load(icon_up_arrow_path).convert_alpha()
icon_down_arrow_path = os.path.join(icon_dir,"down_arrow.png")
icon_down_arrow = pygame.image.load(icon_down_arrow_path).convert_alpha()
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
# Initialize the Q_grid state
Q_grid = [[-2] * grid_size for _ in range(grid_size)]
# Initialize the T_grid state
T_grid = [[-3] * grid_size for _ in range(grid_size)]
# Initialize the pipe_section_grid state
pipe_section_grid = [[0] * grid_size for _ in range(grid_size)]
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

# Reset button position
button_x = (((screen_width - 300) - button_width) // 2)
button_y = screen_height - square_size - button_height - 110

# Undo button position
undo_button_x = button_x - button_width - 10
undo_button_y = button_y

# Undo stack
undo_stack = []

def render_textrect(text, font, rect, text_color, background_color, wrap=True):
    # Internal function to render a surface with wrapped text
    def render_text(surface, text, font, rect, text_color, background_color):
        words = text.split()
        space_width, _ = font.size(" ")

        x, y = rect.topleft
        line_spacing = 2
        space_width = font.size(" ")[0]

        for word in words:
            word_width, word_height = font.size(word)
            if x + word_width >= rect.right:
                x = rect.left  # Reset x to the left side of the rectangle
                y += word_height + line_spacing  # Move to the next line
            surface.blit(font.render(word, True, text_color), (x, y))
            x += word_width + space_width

    rendered_text = pygame.Surface(rect.size)
    rendered_text.fill(background_color)
    if wrap:
        render_text(rendered_text, text, font, rendered_text.get_rect(), text_color, background_color)
    else:
        rendered_text.blit(font.render(text, True, text_color), (0, 0))
    return rendered_text


def exercise_info():
    """Display all the information that is necessary for the player to solve the problem"""
    # Calculate the position for the info_text_rect (above the grid)
    info_text_width = 850 # Change this if you want a different width for the text box
    info_text_height = 80  # Change this if you want a different height for the text box
    info_text_x = 10
    info_text_y = 10

    # Create the text rectangle and render the wrapped text
    info_text_rect = pygame.Rect(info_text_x, info_text_y, info_text_width, info_text_height)
    font = pygame.font.Font(None, 15)
    info_text = ("Η θερμοκρασία του γεωθερμικού νερού είναι 75οC. Η ποιότητά του είναι καλή."
                 "Η απαιτούμενη παροχή θερμού νερού είναι ίση με Q1 για τα συγκροτήματα Α και Β, 1.4∙Q1 για το συγκρότημα Γ και 2.0∙Q1 για το θερμοκήπιο Δ. "
                 "Δεν υπάρχει κίνδυνος εξάντλησης του υδροφορέα, αν η συνολικά αντλούμενη παροχή QΣ<2.5·Q1, προκαλείται όμως σημαντική πτώση στάθμης του πιεζομετρικού φορτίου, αν QΣ>1.7·Q1. "
                 "Οι απαιτούμενες θερμοκρασίες εισόδου και εξόδου στα Α, Β, Γ, Δ φαίνονται στο σχήμα. Κάθε αγωγός πρέπει να έχει στην αρχή και στο τέλος του (χρήστης ή γεώτρηση ή κόμβος) θερμοκρασία και παροχή ρευστού.")

    # Adjust the wrapping width here (600 in this case, you can change it)
    wrapped_info_text = render_textrect(info_text, font, info_text_rect, (255, 255, 255), (0, 0, 255), wrap=True)

    pygame.draw.rect(screen, (255, 0, 0), info_text_rect)
    screen.blit(wrapped_info_text, (info_text_x, info_text_y))

def display_start_menu():
    """Display the start menu and wait for the player to click "Play" or "Instructions"."""
    play_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 50, 200, 50)
    instructions_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 50, 200, 50)
    font = pygame.font.Font(None, 36)
    play_text = font.render("Play", True, (255, 255, 255))
    instructions_text = font.render("Instructions", True, (255, 255, 255))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(pygame.mouse.get_pos()):
                    return  # Exit the function to start the game

        screen.fill(BLUE)
        pygame.draw.rect(screen, (255, 0, 0), play_button_rect)
        screen.blit(play_text, (screen_width // 2 - play_text.get_width() // 2, screen_height // 2 - 40))
        pygame.draw.rect(screen, (255, 0, 0), instructions_button_rect)
        screen.blit(instructions_text,(screen_width // 2 - instructions_text.get_width() // 2, screen_height // 2 + 60))

        pygame.display.flip()

def initialize_grid():
    """Initialize everything in all the grids(grid, placement_grid, etc)"""
    # What is happening in the grid
    center_row = (grid_size - 6) // 2
    center_col = grid_size // 2
    grid[center_row][center_col] = icon_pw
    building1_row = (grid_size - 2) // 2
    building1_col = (grid_size - 10) // 2
    grid[building1_row][building1_col] = icon_building1
    building2_row = (grid_size - 2) // 2
    building2_col = (grid_size + 10) // 2
    grid[building2_row][building2_col] = icon_building2
    greenhouse_row = (grid_size + 8) // 2
    greenhouse_col = grid_size // 2
    grid[greenhouse_row][greenhouse_col] = icon_greenhouse
    rw_row = (grid_size + 11) // 2
    rw_col = (grid_size + 9) // 2
    grid[rw_row][rw_col] = icon_rw
    # What is happening in the placement_grid
    placement_grid[center_row][center_col] = 10
    placement_grid[building1_row][building1_col] = 11
    placement_grid[building2_row][building2_col] = 11
    placement_grid[greenhouse_row][greenhouse_col] = 11
    placement_grid[rw_row][rw_col] = 12

def pipe_section_grid_for_icon_building1():
    global pipe_section
    building1_row = (grid_size - 2) // 2
    building1_col = (grid_size - 10) // 2
    pipe_section_grid[building1_row][building1_col] = pipe_section
    if pipe_section_grid[building1_row-1][building1_col] != 0 and pipe_section_grid[building1_row+1][building1_col] == 0:
        pipe_section += 1
        Q[pipe_section] = Q_grid[building1_row][building1_col]
        pipe_section_grid[building1_row + 1][building1_col] = pipe_section
        Q_grid[building1_row][building1_col] = Q_grid[building1_row-1][building1_col]
        Q[pipe_section] = Q_grid[building1_row][building1_col]
def pipe_section_grid_for_icon_building2():
    global pipe_section
    building2_row = (grid_size - 2) // 2
    building2_col = (grid_size + 10) // 2
    pipe_section_grid[building2_row][building2_col] = pipe_section
    if pipe_section_grid[building2_row-1][building2_col] != 0 and pipe_section_grid[building2_row+1][building2_col] == 0:
        pipe_section += 1
        Q[pipe_section] = Q_grid[building2_row][building2_col]
        pipe_section_grid[building2_row + 1][building2_col] = pipe_section
        Q_grid[building2_row][building2_col] = Q_grid[building2_row-1][building2_col]

def pipe_section_grid_for_icon_greenhouse():
    global pipe_section
    greenhouse_row = (grid_size + 8) // 2
    greenhouse_col = grid_size // 2
    pipe_section_grid[greenhouse_row][greenhouse_col] = pipe_section
    if pipe_section_grid[greenhouse_row-1][greenhouse_col] != 0 and pipe_section_grid[greenhouse_row+1][greenhouse_col] == 0:
        pipe_section += 1
        Q[pipe_section] = Q_grid[greenhouse_row][greenhouse_col]
        pipe_section_grid[greenhouse_row + 1][greenhouse_col] = pipe_section
        Q_grid[greenhouse_row][greenhouse_col] = Q_grid[greenhouse_row-1][greenhouse_col]

def reset_grid():
    """Reset the grid by clearing all icons except for icon_pw."""
    global Starting_Q, pipe_section

    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] is not None : #and grid[i][j] != icon_pw and grid[i][j] != icon_building1 and grid[i][j] != icon_building2 and grid[i][j] != icon_greenhouse and grid[i][j] != icon_rw:
                grid[i][j] = None
                placement_grid[i][j] = -1
                Q_grid[i][j] = -2
                T_grid[i][j] = -3
                pipe_section_grid[i][j] = 0
    Q.clear()
    pipe_section = 0
    Starting_Q = 0
def undo():
    """Undo the last placed icon on the grid."""
    if undo_stack:
        row, col = undo_stack.pop()
        grid[row][col] = None
        placement_grid[row][col] = -1
        Q_grid[row][col] = -2
        T_grid[row][col] = -3
        pipe_section_grid[row][col] = 0


def show_input_box(x, y, screen_width, screen_height, text=""):
    """Show an input box on the screen and return the player's input as an integer."""
    global pipe_section
    input_box_font = pygame.font.Font(None, 30)
    active = True
    enter_input_sound.play(0)
    input_label_font = pygame.font.Font(None, 40)  # New font for the input label
    submitted = False  # Initialize the variable here

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    active = False
                    submitted = True  # Set submitted to True when Enter key is pressed
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        input_box_x = 700
        input_box_y = 150
        input_box_width = 100
        input_box_height = 25

        # Draw the input box
        pygame.draw.rect(screen, WHITE, (input_box_x, input_box_y, input_box_width, input_box_height))
        pygame.draw.rect(screen, BLACK, (input_box_x, input_box_y, input_box_width, input_box_height), 1)

        # Draw the input text
        input_text = input_box_font.render(text, True, BLACK)
        input_text_rect = input_text.get_rect(center=(input_box_x + input_box_width // 2, input_box_y + input_box_height // 2))
        screen.blit(input_text, input_text_rect)

        # Draw the input label
        input_label_text = input_label_font.render(f"Q{pipe_section}:", True, BLACK)
        input_label_text_rect = input_label_text.get_rect(x=input_box_x - 50, y=input_box_y)
        screen.blit(input_label_text, input_label_text_rect)

        pygame.display.update()

    # Draw the blue square after the event handling loop
    if submitted:
        pygame.draw.rect(screen, BLUE,(input_box_x - 50, input_box_y , 200, 40))  # Adjust the rectangle size as needed
        pygame.display.update()

    # Validate the input and ask the player to redo the input if it's not a valid integer
    while True:
        try:
            return int(text)
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            text = show_input_box(x, y, screen_width, screen_height)  # Recursively call the function to redo the input
def left_arrow_appears():
    """Display all the information that is necessary for the player to solve the problem"""
    # Change the position of the icon_down_arrow to (x=700, y=50)
    icon_left_arrow_rect = icon_left_arrow.get_rect(x=725, y=90)

    # Scale the size of the icon_down_arrow
    scaled_width = 50  # Change this to the desired width
    scaled_height = 50  # Change this to the desired height
    icon_left_arrow_scaled = pygame.transform.scale(icon_left_arrow, (scaled_width, scaled_height))

    # Draw the scaled icon_down_arrow at the new position
    screen.blit(icon_left_arrow_scaled, icon_left_arrow_rect)

def right_arrow_appears():
    """Display the right arrow icon"""
    # Change the position of the icon_right_arrow to (x=700, y=50) for the right position
    icon_right_arrow_rect = icon_right_arrow.get_rect(x=725, y=90)

    # Scale the size of the icon_right_arrow
    scaled_width = 50  # Change this to the desired width
    scaled_height = 50  # Change this to the desired height
    icon_right_arrow_scaled = pygame.transform.scale(icon_right_arrow, (scaled_width, scaled_height))

    # Draw the scaled icon_right_arrow at the new position
    screen.blit(icon_right_arrow_scaled, icon_right_arrow_rect)


def down_arrow_appears():
    """Display the down arrow icon"""
    # Change the position of the icon_down_arrow to (x=700, y=50) for the down position
    icon_down_arrow_rect = icon_down_arrow.get_rect(x=725, y=90)

    # Scale the size of the icon_down_arrow
    scaled_width = 50  # Change this to the desired width
    scaled_height = 50  # Change this to the desired height
    icon_down_arrow_scaled = pygame.transform.scale(icon_down_arrow, (scaled_width, scaled_height))

    # Draw the scaled icon_down_arrow at the new position
    screen.blit(icon_down_arrow_scaled, icon_down_arrow_rect)


def up_arrow_appears():
    """Display the up arrow icon"""
    # Change the position of the icon_up_arrow to (x=700, y=50) for the up position
    icon_up_arrow_rect = icon_up_arrow.get_rect(x=725, y=90)

    # Scale the size of the icon_up_arrow
    scaled_width = 50  # Change this to the desired width
    scaled_height = 50  # Change this to the desired height
    icon_up_arrow_scaled = pygame.transform.scale(icon_up_arrow, (scaled_width, scaled_height))

    # Draw the scaled icon_up_arrow at the new position
    screen.blit(icon_up_arrow_scaled, icon_up_arrow_rect)

def covering_the_arrow(screen):
    """Draw the cover on the screen at a fixed position."""
    blue_rect_width = 50
    blue_rect_height = 50
    blue_rect_color = (0, 0, 255)  # RGB value for blue

    pygame.draw.rect(screen, blue_rect_color, (725, 90, blue_rect_width, blue_rect_height))
    pygame.display.update()
def get_available_icons(row, col):
    """Get the available icons based on the placement grid values."""
    available_icons = icons.copy()
    connection_type = 0
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
                and placement_grid[neighbor_row][neighbor_col] > -1
        ):
            # = [int(num) for num in my_string.split(',')]
            icons2rem.append(na_icons[i][placement_grid[neighbor_row][neighbor_col]])
            connection_type += 1
    if len(icons2rem) != 0:
        icons2rem = [int(j) for j in ",".join(icons2rem).split(',')]
        icons2rem = list(set(icons2rem))
        # print('in', icons2rem)
        for j in icons2rem:
            available_icons.remove(icons[j - 1])
    return available_icons, connection_type
def render_q2_dictionary(Q2):
    font = pygame.font.Font( None,24)
    text_color = (255, 0, 0)  # Red text color (RGB value)

    # Determine the number of columns to arrange the keys
    num_columns = min(len(Q2), 5)

    # Render the Q2 dictionary on the screen with special positioning
    for idx, (key, value) in enumerate(Q2.items()):
        column = idx % num_columns
        row = idx // num_columns
        text_surface = font.render(f"{key}: {value}", True, text_color)
        screen.blit(text_surface, (10 + column * 90, 680 + row * 30))

    pygame.display.update()


# Initialize the grid
initialize_grid()
# Creating Q Parameters
Q = {}
Q2 = {}
Starting_Q = 0
number_of_items = 0
# Starting_Q= float(input(f"Q{pipe_section}:"))
# print(Q[0])
# wait = input("666")

# Main game loop
display_start_menu()
running = True
placed_new_item = False # Flag to track if a new item is placed
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not dropdown_open:
            # Check if the button to reset the grid is clicked
            if button_x <= event.pos[0] <= button_x + button_width and button_y <= event.pos[1] <= button_y + button_height:
                reset_grid()
                initialize_grid()
            # Check if the button to undo is clicked
            elif undo_button_x <= event.pos[0] <= undo_button_x + button_width and undo_button_y <= event.pos[1] <= undo_button_y + button_height:
                undo()
            else:
                row = (event.pos[1] - square_y) // square_size
                col = (event.pos[0] - square_x) // square_size
                available_icons, connection_type = get_available_icons(row, col)
                print("connection_type", connection_type)
                print('out', available_icons)
                print('out2', len(available_icons))
                if 0 <= row < grid_size and 0 <= col < grid_size and (
                        (row + 1 < grid_size and ((placement_grid[row + 1][col] == 11 and 0 <= placement_grid[row + 2][col] <= 10) or (0 <= placement_grid[row + 1][col] <= 10))) or
                        (row - 1 >= 0 and ((placement_grid[row - 1][col] == 11 and 0 <= placement_grid[row - 2][col] <= 10) or (0 <= placement_grid[row - 1][col] <= 10))) or
                        (col - 1 >= 0 and ((placement_grid[row][col - 1] == 11 and 0 <= placement_grid[row][col - 2] <= 10) or (0 <= placement_grid[row][col - 1] <= 10))) or
                        (col + 1 < grid_size and ((placement_grid[row][col + 1] == 11 and 0 <= placement_grid[row][col + 2] <= 10) or (0 <= placement_grid[row][col + 1] <= 10)))
                ):
                    if -1 <= placement_grid[row][col] <= 9:
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
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and dropdown_open:
            if not dropdown_rect.collidepoint(event.pos):
                dropdown_open = False
                selected_icon = None
            else:
                icon_index = (event.pos[1] - dropdown_y) // square_size
                # selected_icon = icons[icon_index]
                selected_icon = available_icons[icon_index]
                icon_index = icons.index(selected_icon)
                print("icon_index:", icon_index)
                row = (dropdown_y - square_y - square_size) // square_size
                col = (dropdown_x - square_x) // square_size
                grid[row][col] = selected_icon
                placement_grid[row][col] = icon_index
                if dropdown_open == True and placed_new_item == False and 0 <= icon_index <= 5 and Starting_Q==0 :
                    Starting_Q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                    Q_grid[row][col] = Starting_Q
                    Q[pipe_section] = Q_grid[row][col]
                    print(Q[pipe_section])
                if dropdown_open == True and placed_new_item == False and 0 <= icon_index <= 5 and Starting_Q!=0 :
                    if pipe_section_grid[row][col] == 0:
                        things_around = 0
                        #i: 0=;eft, 1=up, 2=right, 3=down
                        for i in range(0,4):
                            tx = (i+2) % 4
                            print(tx)
                            if i == 0: #ti icon type exei to row-1
                                ty = placement_grid[row][col-1]
                                trow = row
                                tcol = col-1
                            elif i == 1:
                                ty = placement_grid[row-1][col]
                                trow = row-1
                                tcol = col
                            elif i == 2:
                                ty = placement_grid[row][col+1]
                                trow = row
                                tcol = col+1
                            elif i == 3:
                                ty = placement_grid[row+1][col]
                                trow = row+1
                                tcol = col
                            if ty == -1:
                                conn[tx][ty] = 0
                            if conn[i][icon_index]*conn[tx][ty] > 0 and things_around <= 1 and placement_grid[row - 1][col] <= 9:
                                pipe_section_grid[row][col] = pipe_section_grid[trow][tcol]
                                things_around += 1
                            if conn[i][icon_index]*conn[tx][ty] > 0 and things_around <= 1 and placement_grid[row - 1][col] > 9:
                                pipe_section_grid[row][col] = pipe_section + 1
                                things_around += 1
                            if conn[i][icon_index] * conn[tx][ty] > 0 and things_around > 1:
                                pipe_section_grid[row][col] = min(element for element in [pipe_section_grid[row][col-1], pipe_section_grid[row-1][col], pipe_section_grid[row][col+1], pipe_section_grid[row+1][col]] if element != 0)
                                Q_grid[row][col] = Q[pipe_section_grid[row][col]]
                                Q_grid[row+1][col] = Q_grid[row][col]
                    Q_grid[row][col] = Q[pipe_section_grid[row][col]]
                elif dropdown_open == True and placed_new_item == False and icon_index == 6 and connection_type == 1:
                    # Ask for player input
                    while True:
                        try:
                            if placement_grid[row + 1][col] != -1:
                                pipe_section += 1
                                left_arrow_appears()  # Left arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row][col - 1] = Q[pipe_section]
                                pipe_section_grid[row][col - 1] = pipe_section

                                pipe_section += 1
                                right_arrow_appears()  # Right arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row][col + 1] = Q[pipe_section]
                                pipe_section_grid[row][col + 1] = pipe_section

                            elif placement_grid[row][col - 1] != -1:
                                pipe_section += 1
                                right_arrow_appears()  # Right arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row + 1][col] = Q[pipe_section]
                                pipe_section_grid[row + 1][col] = pipe_section

                                pipe_section += 1
                                down_arrow_appears()  # Down arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row - 1][col] = Q[pipe_section]
                                pipe_section_grid[row - 1][col] = pipe_section

                            elif placement_grid[row][col + 1] != -1:
                                pipe_section += 1
                                left_arrow_appears()  # Left arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row][col - 1] = Q[pipe_section]
                                pipe_section_grid[row][col - 1] = pipe_section

                                pipe_section += 1
                                down_arrow_appears()  # Down arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row + 1][col] = Q[pipe_section]
                                pipe_section_grid[row + 1][col] = pipe_section

                            Q_grid[row][col] = Q[pipe_section - 2]
                            if Q[pipe_section - 2] != (Q[pipe_section - 1] + Q[pipe_section]):
                                print(f"You have made a mistake. Please enter Q{pipe_section - 1} and Q{pipe_section} properly")
                                pipe_section -= 2
                            else:
                                break
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                elif dropdown_open == True and placed_new_item == False and icon_index == 7 and connection_type == 1:
                    # Ask for player input
                    while True:
                        try:
                            if placement_grid[row - 1][col] != -1:
                                pipe_section += 1
                                left_arrow_appears() # Left arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row][col - 1] = Q[pipe_section]
                                pipe_section_grid[row][col - 1] = pipe_section

                                pipe_section += 1
                                down_arrow_appears() # Down arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row + 1][col] = Q[pipe_section]
                                pipe_section_grid[row + 1][col] = pipe_section
                            elif placement_grid[row][col - 1] != -1:
                                pipe_section += 1
                                up_arrow_appears()  # Up arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row - 1][col] = Q[pipe_section]
                                pipe_section_grid[row - 1][col] = pipe_section

                                pipe_section += 1
                                down_arrow_appears()  # Down arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row + 1][col] = Q[pipe_section]
                                pipe_section_grid[row + 1][col] = pipe_section
                            elif placement_grid[row + 1][col] != -1:
                                pipe_section += 1
                                left_arrow_appears()  # Left arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row - 1][col] = Q[pipe_section]
                                pipe_section_grid[row - 1][col] = pipe_section
                                pipe_section += 1
                                up_arrow_appears()  # Up arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                Q[pipe_section] = q
                                Q_grid[row-1][col] = Q[pipe_section]
                                pipe_section_grid[row - 1][col] = pipe_section
                            Q_grid[row][col] = Q[pipe_section - 2]
                            if Q[pipe_section - 2] != (Q[pipe_section - 1] + Q[pipe_section]):
                                print(
                                    f"You have made a mistake. Please enter Q{pipe_section - 1} and Q{pipe_section} properly")
                                pipe_section -= 2
                            else:
                                break
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                elif dropdown_open == True and placed_new_item == False and icon_index == 8 and connection_type == 1:
                    # Ask for player input
                    while True:
                        try:
                            if placement_grid[row - 1][col] != -1:
                                pipe_section += 1
                                left_arrow_appears()  # Left arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row][col - 1] = Q[pipe_section]
                                pipe_section_grid[row][col - 1] = pipe_section

                                pipe_section += 1
                                right_arrow_appears()  # Right arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row][col + 1] = Q[pipe_section]
                                pipe_section_grid[row][col + 1] = pipe_section
                            elif placement_grid[row][col - 1] != -1:
                                pipe_section += 1
                                up_arrow_appears()  # Up arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row - 1][col] = Q[pipe_section]
                                pipe_section_grid[row - 1][col] = pipe_section

                                pipe_section += 1
                                right_arrow_appears()  # Right arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row][col + 1] = Q[pipe_section]
                                pipe_section_grid[row][col + 1] = pipe_section
                            elif placement_grid[row][col + 1] != -1:
                                pipe_section += 1
                                left_arrow_appears()  # Left arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row][col - 1] = Q[pipe_section]
                                pipe_section_grid[row][col - 1] = pipe_section

                                pipe_section += 1
                                up_arrow_appears()  # Down arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row - 1][col] = Q[pipe_section]
                                pipe_section_grid[row - 1][col] = pipe_section
                            Q_grid[row][col] = Q[pipe_section - 2]
                            if Q[pipe_section - 2] != (Q[pipe_section - 1] + Q[pipe_section]):
                                print(
                                    f"You have made a mistake. Please enter Q{pipe_section - 1} and Q{pipe_section} properly")
                                pipe_section -= 2
                            else:
                                break
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                elif dropdown_open == True and placed_new_item == False and icon_index == 9 and connection_type == 1:
                    # Ask for player input
                    while True:
                        try:
                            if placement_grid[row - 1][col] != -1:
                                pipe_section += 1
                                right_arrow_appears()  # Right arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row][col + 1] = Q[pipe_section]
                                pipe_section_grid[row][col + 1] = pipe_section

                                pipe_section += 1
                                down_arrow_appears()  # Down arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row+1][col] = Q[pipe_section]
                                pipe_section_grid[row+1][col] = pipe_section
                            elif placement_grid[row][col + 1] != -1:
                                pipe_section += 1
                                up_arrow_appears()  # Up arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row - 1][col] = Q[pipe_section]
                                pipe_section_grid[row - 1][col] = pipe_section

                                pipe_section += 1
                                down_arrow_appears()  # Down arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row + 1][col] = Q[pipe_section]
                                pipe_section_grid[row + 1][col] = pipe_section
                            elif placement_grid[row + 1][col] != -1:
                                pipe_section += 1
                                up_arrow_appears()  # Up arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row - 1][col] = Q[pipe_section]
                                pipe_section_grid[row - 1][col] = pipe_section

                                pipe_section += 1
                                right_arrow_appears()  # Right arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row][col + 1] = Q[pipe_section]
                                pipe_section_grid[row][col + 1] = pipe_section
                            Q_grid[row][col] = Q[pipe_section - 2]
                            if Q[pipe_section - 2] != (Q[pipe_section - 1] + Q[pipe_section]):
                                print(
                                    f"You have made a mistake. Please enter Q{pipe_section - 1} and Q{pipe_section} properly")
                                pipe_section -= 2
                            else:
                                break
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                elif dropdown_open == True and placed_new_item == False and icon_index == 6 and connection_type == 2:
                    pipe_section += 1
                    if placement_grid[row + 1][col] != -1 and placement_grid[row][col - 1] != -1:
                        Q_grid[row][col + 1] = Q_grid[row + 1][col] + Q_grid[row][col - 1]
                        pipe_section_grid[row][col + 1] = pipe_section
                        Q[pipe_section] = Q_grid[row][col + 1]
                        Q_grid[row][col] = Q_grid[row + 1][col] + Q_grid[row][col - 1]
                    if placement_grid[row + 1][col] != -1 and placement_grid[row][col + 1] != -1:
                        Q_grid[row][col - 1] = Q_grid[row + 1][col] + Q_grid[row][col + 1]
                        pipe_section_grid[row][col - 1] = pipe_section
                        Q[pipe_section] = Q_grid[row][col - 1]
                        Q_grid[row][col] = Q_grid[row + 1][col] + Q_grid[row][col + 1]
                    if placement_grid[row][col - 1] != -1 and placement_grid[row][col + 1] != -1:
                        Q_grid[row + 1][col] = Q_grid[row][col - 1] + Q_grid[row][col + 1]
                        pipe_section_grid[row + 1][col] = pipe_section
                        Q[pipe_section] = Q_grid[row + 1][col]
                        Q_grid[row][col] = Q_grid[row][col - 1] + Q_grid[row][col + 1]
                elif dropdown_open == True and placed_new_item == False and icon_index == 7 and connection_type == 2:
                    pipe_section += 1
                    if placement_grid[row + 1][col] != -1 and placement_grid[row][col - 1] != -1:
                        Q_grid[row - 1][col] = Q_grid[row + 1][col] + Q_grid[row][col - 1]
                        pipe_section_grid[row - 1][col] = pipe_section
                        Q[pipe_section] = Q_grid[row - 1][col]
                        Q_grid[row][col] = Q_grid[row + 1][col] + Q_grid[row][col - 1]
                    if placement_grid[row + 1][col] != -1 and placement_grid[row + 1][col] != -1:
                        Q_grid[row][col - 1] = Q_grid[row + 1][col] + Q_grid[row + 1][col]
                        pipe_section_grid[row][col - 1] = pipe_section
                        Q[pipe_section] = Q_grid[row][col - 1]
                        Q_grid[row][col] = Q_grid[row + 1][col] + Q_grid[row + 1][col]
                    if placement_grid[row][col - 1] != -1 and placement_grid[row - 1][col] != -1:
                        Q_grid[row + 1][col] = Q_grid[row][col - 1] + Q_grid[row - 1][col]
                        pipe_section_grid[row + 1][col] = pipe_section
                        Q[pipe_section] = Q_grid[row + 1][col]
                        Q_grid[row][col] = Q_grid[row][col - 1] + Q_grid[row - 1][col]
                elif dropdown_open == True and placed_new_item == False and icon_index == 8 and connection_type == 2:
                    pipe_section += 1
                    if placement_grid[row - 1][col] != -1 and placement_grid[row][col - 1] != -1:
                        Q_grid[row][col + 1] = Q_grid[row - 1][col] + Q_grid[row][col - 1]
                        pipe_section_grid[row][col + 1] = pipe_section
                        Q[pipe_section] = Q_grid[row][col + 1]
                        Q_grid[row][col] = Q_grid[row - 1][col] + Q_grid[row][col - 1]
                    if placement_grid[row - 1][col] != -1 and placement_grid[row][col + 1] != -1:
                        Q_grid[row][col - 1] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                        pipe_section_grid[row][col - 1] = pipe_section
                        Q[pipe_section] = Q_grid[row][col - 1]
                        Q_grid[row][col] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                    if placement_grid[row][col - 1] != -1 and placement_grid[row][col + 1] != -1:
                        Q_grid[row - 1][col] = Q_grid[row][col - 1] + placement_grid[row][col + 1]
                        pipe_section_grid[row - 1][col] = pipe_section
                        Q[pipe_section] = Q_grid[row - 1][col]
                        Q_grid[row][col] = Q_grid[row][col - 1] + placement_grid[row][col + 1]
                elif dropdown_open == True and placed_new_item == False and icon_index == 9 and connection_type == 2:
                    pipe_section += 1
                    if placement_grid[row - 1][col] != -1 and placement_grid[row][col + 1] != -1:
                        Q_grid[row + 1][col] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                        pipe_section_grid[row + 1][col] = pipe_section
                        Q[pipe_section] = Q_grid[row + 1][col]
                        Q_grid[row][col] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                    if placement_grid[row - 1][col] != -1 and placement_grid[row][col + 1] != -1:
                        Q_grid[row - 1][col] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                        pipe_section_grid[row - 1][col] = pipe_section
                        Q[pipe_section] = Q_grid[row - 1][col]
                        Q_grid[row][col] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                    if placement_grid[row - 1][col] != -1 and placement_grid[row + 1][col] != -1:
                        Q_grid[row][col + 1] = Q_grid[row - 1][col] + Q_grid[row + 1][col]
                        pipe_section_grid[row][col + 1] = pipe_section
                        Q[pipe_section] = Q_grid[row][col + 1]
                        Q_grid[row][col] = Q_grid[row - 1][col] + Q_grid[row + 1][col]
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
    reset_text_rect = reset_text.get_rect(center=((button_x + button_width // 2), button_y + button_height // 2))
    screen.blit(reset_text, reset_text_rect)

    # Draw the undo button
    pygame.draw.rect(screen, GRAY, (undo_button_x, undo_button_y, button_width, button_height))
    undo_text = reset_font.render("Undo", True, WHITE)
    undo_text_rect = undo_text.get_rect(center=(undo_button_x + button_width // 2, undo_button_y + button_height // 2))
    screen.blit(undo_text, undo_text_rect)
    exercise_info()

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

        for i, icon in enumerate(available_icons):
            icon_scaled = pygame.transform.scale(icon, (square_size, square_size))
            dropdown_icon_rect = pygame.Rect(dropdown_x, dropdown_y + i * square_size, square_size, square_size)
            screen.blit(icon_scaled, dropdown_icon_rect)
    # Arrange the pipe_section_grid properly
    pipe_section_grid_for_icon_building1()
    pipe_section_grid_for_icon_building2()
    pipe_section_grid_for_icon_greenhouse()
    # Print the placement grid if a new item is placed
    if placed_new_item:
        print("Placement Grid:")
        for row in placement_grid:
            print(row)
        print()
        # Print the Q_grid if a new item is placed
        print("Q-Grid:")
        for row in Q_grid:
            print(row)
        print()
        # Print the T_grid if a new item is placed
        print("T-Grid:")
        for row in T_grid:
            print(row)
        print()
        # Print the pipe_section_grid if a new item is placed
        print("pipe_section-Grid:")
        for row in pipe_section_grid:
            print(row)
        print()
        placed_new_item = False
        print(Q)
        Q2 = {'Q' + str(key): value for key, value in Q.items()}
        print(Q2)
    # Render the dictionary with the provided Q
    render_q2_dictionary(Q2)
    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
