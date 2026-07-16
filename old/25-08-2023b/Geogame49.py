import pygame
import os
import numpy as np  # Numeric functions and arrays
import pandas as pd
import time

# IMPORTANT part of the code that need fixing are found using the search "lines for correction"
root_dir = os.path.dirname(os.path.abspath(__file__))

house0_executed = False
house1_executed = False
house2_executed = False
ghouse0_executed = False
ghouse1_executed = False

# game_data
dataset = 0
# totalQ = 2000
pipe_section = 0
icon_index = 100
rw_existence = True
cell_info = False
username = ""
# Initialize Pygame
pygame.init()

'read input data'
# idata = pd.read_excel(r"C:\\Diplomatikh\diplomatikh\2023-07-09(UPDATED)\geodata.xlsx", sheet_name="na_icons")  # kostas pc
# idata = pd.read_excel(r"C:\Users\User\.spyder-py3\geodata.xlsx",  sheet_name="na_icons") #yiannis pc
idata = pd.read_excel(root_dir + "\geodata.xlsx", sheet_name="na_icons")
na_icons_L = idata['left'].to_numpy()
na_icons_R = idata['right'].to_numpy()
na_icons_U = idata['up'].to_numpy()
na_icons_D = idata['down'].to_numpy()
na_icons0 = np.concatenate((na_icons_L, na_icons_R, na_icons_U, na_icons_D))
na_icons = np.reshape(na_icons0, (4, 13))
idata = pd.read_excel(root_dir + "\geodata.xlsx", sheet_name="pipe_connections")
conn_L = idata['left'].to_numpy()
conn_U = idata['up'].to_numpy()
conn_R = idata['right'].to_numpy()
conn_D = idata['down'].to_numpy()
conn0 = np.concatenate((conn_L, conn_U, conn_R, conn_D))
conn = np.reshape(conn0, (4, 13))
# conn[x][y] simainei x=0,1,2,3 left, up, right, down kai y = icon index
idata = pd.read_excel(root_dir + "\geodata.xlsx", sheet_name="info")
Qtot_depl = idata['Qtot_depl'].to_numpy()
Qtot_head = idata['Qtot_head'].to_numpy()
quality = idata['quality'].to_numpy()
T0 = idata['T0'].to_numpy(float)
pw_row = idata['pw_row'].to_numpy().astype(int)
pw_col = idata['pw_col'].to_numpy().astype(int)
house0_row = idata['house0_row'].to_numpy().astype(int)
house0_col = idata['house0_col'].to_numpy().astype(int)
Thouse0_in = idata['Thouse0_in'].to_numpy().astype(float)
Thouse0_out = idata['Thouse0_out'].to_numpy().astype(float)
Qhouse0_in = idata['Qhouse0_in'].to_numpy().astype(float)
Qhouse0_out = idata['Qhouse0_out'].to_numpy().astype(float)
house1_row = idata['house1_row'].to_numpy().astype(int)
house1_col = idata['house1_col'].to_numpy().astype(int)
Thouse1_in = idata['Thouse1_in'].to_numpy().astype(float)
Thouse1_out = idata['Thouse1_out'].to_numpy().astype(float)
Qhouse1_in = idata['Qhouse1_in'].to_numpy().astype(float)
Qhouse1_out = idata['Qhouse1_out'].to_numpy().astype(float)
house2_row = idata['house2_row'].to_numpy().astype(int)
house2_col = idata['house2_col'].to_numpy().astype(int)
Thouse2_in = idata['Thouse2_in'].to_numpy().astype(float)
Thouse2_out = idata['Thouse2_out'].to_numpy().astype(float)
Qhouse2_in = idata['Qhouse2_in'].to_numpy().astype(float)
Qhouse2_out = idata['Qhouse2_out'].to_numpy().astype(float)
greenhouse0_row = idata['greenhouse0_row'].to_numpy().astype(int)
greenhouse0_col = idata['greenhouse0_col'].to_numpy().astype(int)
Tgreenhouse0_in = idata['Tghouse0_in'].to_numpy().astype(float)
Tgreenhouse0_out = idata['Tghouse0_out'].to_numpy().astype(float)
Qghouse0_in = idata['Qghouse0_in'].to_numpy().astype(float)
Qghouse0_out = idata['Qghouse0_out'].to_numpy().astype(float)
greenhouse1_row = idata['greenhouse1_row'].to_numpy().astype(int)
greenhouse1_col = idata['greenhouse1_col'].to_numpy().astype(int)
Tgreenhouse1_in = idata['Tghouse1_in'].to_numpy().astype(float)
Tgreenhouse1_out = idata['Tghouse1_out'].to_numpy().astype(float)
Qghouse1_in = idata['Qghouse1_in'].to_numpy().astype(float)
Qghouse1_out = idata['Qghouse1_out'].to_numpy().astype(float)
rw_row = idata['rw_row'].to_numpy().astype(int)
rw_col = idata['rw_col'].to_numpy().astype(int)
outflow_row = idata['outflow_row'].to_numpy().astype(int)
outflow_col = idata['outflow_col'].to_numpy().astype(int)
Tloss_pipe = idata['Tloss_pipe'].to_numpy().astype(float)
simple_pipe_cost = idata['simple_pipe_cost'].to_numpy().astype(float)
corner_pipe_cost = idata['corner_pipe_cost'].to_numpy().astype(float)
triplet_pipe_cost = idata['triplet_pipe_cost'].to_numpy().astype(float)

# Screen dimensions
screen_width = 1005
screen_height = 750

# Grid dimensions
grid_size = 17
square_size = 32

"""" Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (35, 75, 225)  # (0,128,128) #(152,251,152) #(0,128,128)
BLUE2 = (0, 0, 170)
BLUE3 = (0, 0, 205)
RED = (222, 49, 99)
RED2 = (255, 49, 49)
GREEN = (0, 205, 0)"""

# Coolors
WHITE = (239, 242, 241)
BLACK = (19, 18, 0)
GRAY = (76, 76, 76)
BLUE = (3, 37, 108)
BLUE2 = (37, 65, 178)
BLUE3 = (58, 80, 107)
RED = (218, 65, 103)
RED2 = (245, 100, 118)
GOLD = (231, 187, 65)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Grid")
# Load the sounds
# click_sound = pygame.mixer.Sound("C:\Diplomatikh\diplomatikh\\2023-07-09(UPDATED)\SoundEffects\MouseClick.wav")
# enter_input_sound = pygame.mixer.Sound("C:\Diplomatikh\diplomatikh\\2023-07-09(UPDATED)\SoundEffects\EnterInputSound.wav") #kostas
# enter_input_sound = pygame.mixer.Sound("C:\Diplomatikh\diplomatikh\\2023-07-09(UPDATED)\SoundEffects\EnterInputSound.wav") #yiannis
enter_input_sound = pygame.mixer.Sound(root_dir + "\SoundEffects\EnterInputSound.wav")
# Volume Management
# click_sound.set_volume(0.3)
enter_input_sound.set_volume(0.0)  # volume
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
icon_starting_spot_path = os.path.join(icon_dir, "icongreen.png")
icon_starting_spot = pygame.image.load(icon_starting_spot_path).convert_alpha()
icon_ending_spot_path = os.path.join(icon_dir, "iconred.png")
icon_ending_spot = pygame.image.load(icon_ending_spot_path).convert_alpha()
icon_left_arrow_path = os.path.join(icon_dir, "left_arrow.png")
icon_left_arrow = pygame.image.load(icon_left_arrow_path).convert_alpha()
icon_right_arrow_path = os.path.join(icon_dir, "right_arrow.png")
icon_right_arrow = pygame.image.load(icon_right_arrow_path).convert_alpha()
icon_up_arrow_path = os.path.join(icon_dir, "up_arrow.png")
icon_up_arrow = pygame.image.load(icon_up_arrow_path).convert_alpha()
icon_down_arrow_path = os.path.join(icon_dir, "down_arrow.png")
icon_down_arrow = pygame.image.load(icon_down_arrow_path).convert_alpha()
icon_dollar_sign_path = os.path.join(icon_dir, "icon17.png")
icon_dollar_sign = pygame.image.load(icon_dollar_sign_path).convert_alpha()
instructions_budget_path = os.path.join(icon_dir, "instructionsbudget.png")
instructions_budget = pygame.image.load(instructions_budget_path).convert_alpha()
instructions_dropdown_path = os.path.join(icon_dir, "instructionsdropdown.png")
instructions_dropdown = pygame.image.load(instructions_dropdown_path).convert_alpha()
instructions_input_path = os.path.join(icon_dir, "instructionsinput.png")
instructions_input = pygame.image.load(instructions_input_path).convert_alpha()
instructions_right_click_path = os.path.join(icon_dir, "instructionsrightclick.png")
instructions_right_click = pygame.image.load(instructions_right_click_path).convert_alpha()

# Load the fonts
title_font = root_dir + "\Fonts\Handjet\static\Handjet-Light.ttf"
info_font = root_dir + "\Fonts\Roboto\Roboto-Medium.ttf"
info_font2 = root_dir + "\Fonts\PtSerif\PTSerif-Bold.ttf"

for i in range(1, 11):
    icon_path = os.path.join(icon_dir, f"icon{i}.png")
    icon_image = pygame.image.load(icon_path).convert_alpha()
    icons.append(icon_image)
# Define the square properties
square_x = 64  # Grid top left x coordinate start
square_y = 64  # Grid top left y coordinate start

# Initialize the grid state
grid = [[None] * grid_size for _ in range(grid_size)]
# Initialize the placement grid state
placement_grid = [[-1] * grid_size for _ in range(grid_size)]
# Initialize the Q_grid state
Q_grid = [[-2] * grid_size for _ in range(grid_size)]
# Initialize the T_grid state
T_grid = [[0] * grid_size for _ in range(grid_size)]
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
button_y = 800 - square_size - button_height - 110

# Undo button position
undo_button_x = button_x - button_width - 10
undo_button_y = button_y

# Pipe Section Button
pipe_section_button_width = 184
pipe_section_button_height = 50
pipe_section_button_x = button_x + button_width + 10
# Undo stack
undo_stack = []


def render_text_rect(text, font, rect, text_color, background_color, wrap=True):
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
    info_text_width = 200  # Change this if you want a different width for the text box
    info_text_height = 80  # Change this if you want a different height for the text box
    info_text_x = 10
    info_text_y = 10

    # Create the text rectangle and render the wrapped text
    info_text_rect = pygame.Rect(info_text_x, info_text_y, info_text_width, info_text_height)
    font = pygame.font.Font(info_font, 13)
    info_text = (
        f"simple pipe cost = {int(simple_pipe_cost[dataset])}")
    "lines for correction"  # Να τοποθετηθεί το σωστό κείμενο
    info_text2 = (f"corner pipe cost = {int(corner_pipe_cost[dataset])}")
    info_text3 = (f"triplet pipe cost = {int(triplet_pipe_cost[dataset])}")

    icon0 = pygame.transform.scale(icons[0], (20, 20))
    icon0_rect = icon0.get_rect(center=(50, 40))  # Adjust position as needed

    icon1 = pygame.transform.scale(icons[1], (20, 20))
    icon1_rect = icon1.get_rect(center=(50 + 20, 40))  # Adjust position as needed

    icon2 = pygame.transform.scale(icons[2], (20, 20))
    icon2_rect = icon2.get_rect(center=(170 + 20, 40))  # Adjust position as needed

    icon3 = pygame.transform.scale(icons[3], (20, 20))
    icon3_rect = icon3.get_rect(center=(170 + 40, 40))  # Adjust position as needed

    icon4 = pygame.transform.scale(icons[4], (20, 20))
    icon4_rect = icon4.get_rect(center=(170 + 60, 40))  # Adjust position as needed

    icon5 = pygame.transform.scale(icons[5], (20, 20))
    icon5_rect = icon5.get_rect(center=(170 + 80, 40))  # Adjust position as needed

    icon6 = pygame.transform.scale(icons[6], (20, 20))
    icon6_rect = icon6.get_rect(center=(320 + 20, 40))  # Adjust position as needed

    icon7 = pygame.transform.scale(icons[7], (20, 20))
    icon7_rect = icon7.get_rect(center=(320 + 40, 40))  # Adjust position as needed

    icon8 = pygame.transform.scale(icons[8], (20, 20))
    icon8_rect = icon8.get_rect(center=(320 + 60, 40))  # Adjust position as needed

    icon9 = pygame.transform.scale(icons[9], (20, 20))
    icon9_rect = icon9.get_rect(center=(320 + 80, 40))  # Adjust position as needed

    # Adjust the wrapping width here (600 in this case, you can change it)
    wrapped_info_text = render_text_rect(info_text, font, info_text_rect, (255, 255, 255), (BLUE), wrap=True)
    wrapped_info_text2 = render_text_rect(info_text2, font, info_text_rect, (255, 255, 255), (BLUE), wrap=True)
    wrapped_info_text3 = render_text_rect(info_text3, font, info_text_rect, (255, 255, 255), (BLUE), wrap=True)

    pygame.draw.rect(screen, (RED), info_text_rect)
    screen.blit(wrapped_info_text, (info_text_x, info_text_y))
    screen.blit(wrapped_info_text2, (info_text_x + 150, info_text_y))
    screen.blit(wrapped_info_text3, (info_text_x + 300, info_text_y))
    screen.blit(icon0, icon0_rect)
    screen.blit(icon1, icon1_rect)
    screen.blit(icon2, icon2_rect)
    screen.blit(icon3, icon3_rect)
    screen.blit(icon4, icon4_rect)
    screen.blit(icon5, icon5_rect)
    screen.blit(icon6, icon6_rect)
    screen.blit(icon7, icon7_rect)
    screen.blit(icon8, icon8_rect)
    screen.blit(icon9, icon9_rect)


def display_start_menu():
    """Display the start menu and wait for the player to click "Play" or "Instructions"."""
    play_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 50, 200, 50)
    instructions_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 50, 200, 50)
    font = pygame.font.Font(None, 36)
    font_title = pygame.font.Font(title_font, 200)
    play_text = font.render("Play", True, (255, 255, 255))
    instructions_text = font.render("Instructions", True, (255, 255, 255))
    title_rect = pygame.Rect(screen_width // 2 - 350, screen_height // 2 - 275, 700, 200)
    title_text = font_title.render("GeoGame", True, (0, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button_rect.collidepoint(pygame.mouse.get_pos()):
                    return  # Exit the function to start the game
                elif instructions_button_rect.collidepoint(pygame.mouse.get_pos()):
                    instructions()

        screen.fill(BLUE)
        pygame.draw.rect(screen, (RED), play_button_rect)
        screen.blit(play_text, (screen_width // 2 - play_text.get_width() // 2, screen_height // 2 - 40))
        pygame.draw.rect(screen, (RED), instructions_button_rect)
        screen.blit(instructions_text,
                    (screen_width // 2 - instructions_text.get_width() // 2, screen_height // 2 + 60))
        pygame.draw.rect(screen, (BLUE), title_rect)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 2 - 300))

        pygame.display.flip()


def instructions():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill(BLUE2)
        instructions_text = "Welcome to GeoGame!"
        instructions_text2 = "Your solution will be graded primarily based on how much money you have spent."
        instructions_text3 = "Money gets spend from choosing pipes(different price per pipe type) and doing Q and T corrections"
        instructions_text4 = "Always start above the pumping well. - - - To place a pipe click on an empty square next to an already existing pipe."
        instructions_text5 = "When you click on a square a dropdown list with pipes will appear. Choose your pipe and place it on the square."
        instructions_text6 = "When it's needed type the Q of the pipeline on the white pop-up square"
        instructions_text7 = "Mistakes on T and Q cost a lot. If you go broke it's GAME OVER!."
        instructions_text8 = "Watch on the top right of the game screen to get your information about houses."
        instructions_text9 = "Tips"
        instructions_text10 = "In case you forget you can always RIGHT CLICK on a placed pipe to see its pipeline and T."
        instructions_text11 = "All your info about Q, T about each pipeline is displayed to the right of the grid"
        instructions_text12 = "Grading"
        instructions_text13 = "Gameplay"

        font = pygame.font.Font(info_font, 16)
        font1 = pygame.font.Font(info_font, 30)
        font2 = pygame.font.Font(info_font, 20)

        text_surface = font1.render(instructions_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(screen_width // 2, 60))

        text_surface2 = font.render(instructions_text2, True, WHITE)
        text_rect2 = text_surface2.get_rect(topleft=(50, 140))

        text_surface3 = font.render(instructions_text3, True, WHITE)
        text_rect3 = text_surface3.get_rect(topleft=(50, 170))

        text_surface4 = font.render(instructions_text4, True, WHITE)
        text_rect4 = text_surface4.get_rect(topleft=(50, 260))

        text_surface5 = font.render(instructions_text5, True, WHITE)
        text_rect5 = text_surface5.get_rect(topleft=(50, 310))

        text_surface6 = font.render(instructions_text6, True, WHITE)
        text_rect6 = text_surface6.get_rect(topleft=(50, 360))

        text_surface7 = font.render(instructions_text7, True, WHITE)
        text_rect7 = text_surface7.get_rect(topleft=(50, 410))

        text_surface8 = font.render(instructions_text8, True, WHITE)
        text_rect8 = text_surface8.get_rect(topleft=(50, 460))

        text_surface9 = font2.render(instructions_text9, True, WHITE)
        text_rect9 = text_surface9.get_rect(topleft=(50, 520))

        text_surface10 = font.render(instructions_text10, True, WHITE)
        text_rect10 = text_surface10.get_rect(topleft=(50, 560))

        text_surface11 = font.render(instructions_text11, True, WHITE)
        text_rect11 = text_surface11.get_rect(topleft=(50, 600))

        text_surface12 = font2.render(instructions_text12, True, WHITE)
        text_rect12 = text_surface12.get_rect(topleft=(50, 100))

        text_surface13 = font2.render(instructions_text13, True, WHITE)
        text_rect13 = text_surface13.get_rect(topleft=(50, 220))

        icon1 = pygame.transform.scale(instructions_budget, (200, 50))
        icon1_rect = icon1.get_rect(topright=(screen_width - 10, 130))  # Adjust position as needed

        icon2 = pygame.transform.scale(icon_pw, (25, 25))
        icon2_rect = icon2.get_rect(topright=(screen_width - 655, 250))  # Adjust position as needed

        icon3 = pygame.transform.scale(instructions_dropdown, (80, 120))
        icon3_rect = icon3.get_rect(topright=(screen_width - 50, 290))  # Adjust position as needed

        icon4 = pygame.transform.scale(instructions_input, (150, 50))
        icon4_rect = icon4.get_rect(topright=(screen_width - 285, 340))  # Adjust position as needed

        icon5 = pygame.transform.scale(instructions_right_click, (150, 100))
        icon5_rect = icon4.get_rect(topright=(screen_width - 140, 550))  # Adjust position as needed

        # Draw the text onto the screen
        screen.blit(text_surface, text_rect)
        screen.blit(text_surface2, text_rect2)
        screen.blit(text_surface3, text_rect3)
        screen.blit(text_surface4, text_rect4)
        screen.blit(text_surface5, text_rect5)
        screen.blit(text_surface6, text_rect6)
        screen.blit(text_surface7, text_rect7)
        screen.blit(text_surface8, text_rect8)
        screen.blit(text_surface9, text_rect9)
        screen.blit(text_surface10, text_rect10)
        screen.blit(text_surface11, text_rect11)
        screen.blit(text_surface12, text_rect12)
        screen.blit(text_surface13, text_rect13)
        screen.blit(icon1, icon1_rect)
        screen.blit(icon2, icon2_rect)
        screen.blit(icon3, icon3_rect)
        screen.blit(icon4, icon4_rect)
        screen.blit(icon5, icon5_rect)

        # Draw the "Back" button
        back_button_rect = pygame.Rect(0, 0, 200, 50)
        pygame.draw.rect(screen, RED, back_button_rect)

        # Render the "Back" button text
        back_font = pygame.font.Font(None, 24)
        back_text = back_font.render("Back", True, WHITE)
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        screen.blit(back_text, back_text_rect)

        pygame.display.flip()

        # Check for button click
        mouse_pos = pygame.mouse.get_pos()
        if back_button_rect.collidepoint(mouse_pos):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return


def username_to_info_and_start():
    global Starting_Q, username, rw_existence

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            else:
                if username == "":
                    screen.fill(BLUE)
                    username = show_input_box2(50, 50, 50, 50, "")
                screen.fill(BLUE2)
                choose_the_starting_Q()
                choose_the_use_of_rw_well()
                game_over()
                return

        pygame.display.update()


def choose_the_starting_Q():
    global Starting_Q, rw_existence

    screen.fill(BLUE3)
    font = pygame.font.Font(info_font, 20)
    font2 = pygame.font.Font(info_font, 24)
    icon1 = pygame.transform.scale(icon_pw, (100, 100))
    icon1_rect = icon1.get_rect(center=(500, 600))  # Adjust position as needed
    info_text_width = 900  # Change this if you want a different width for the text box
    info_text_height = 500  # Change this if you want a different height for the text box
    info_text_x = 50
    info_text_y = 80

    # Create the text rectangle and render the wrapped text
    font = pygame.font.Font(info_font, 18)
    info_text1 = "Συμπληρώστε το σκαρίφημα του συστήματος θέρμανσης των συγκροτημάτων κατοικιών Α, Β και θερμοκηπίων Γ του σχήματος. Δίνεται ότι:"
    info_text2 = "1-Η θερμοκρασία του γεωθερμικού νερού είναι 85 οC."
    info_text3 = "2-Η ποιότητά του είναι καλή."
    info_text4 = "3-Η απαιτούμενη παροχή θερμού νερού είναι ίση με Q1 για τα συγκροτήματα κατοικιών Α και Β και 1.9Q1 για το θερμοκήπιο Γ."
    info_text5 = "4-Δεν υπάρχει κίνδυνος εξάντλησης του υδροφορέα, αν η συνολικά αντλούμενη παροχή QΣ είναι μικρότερη από 2.1Q1"
    info_text6 = "5-Προκαλείται όμως σημαντική πτώση στάθμης του πιεζομετρικού φορτίου, αν η QΣ είναι μεγαλύτερη από 1.5Q1."
    info_text7 = "6-Οι απαιτούμενες θερμοκρασίες εισόδου και εξόδου φαίνονται στο σχήμα."

    step_h = 50
    text_rect1 = pygame.Rect(info_text_x, info_text_y + 0 * step_h, info_text_width, info_text_height)
    text_rect2 = pygame.Rect(30 + info_text_x, info_text_y + 1 * step_h, info_text_width, info_text_height)
    text_rect3 = pygame.Rect(30 + info_text_x, info_text_y + 2 * step_h, info_text_width, info_text_height)
    text_rect4 = pygame.Rect(30 + info_text_x, info_text_y + 3 * step_h, info_text_width, info_text_height)
    text_rect5 = pygame.Rect(30 + info_text_x, info_text_y + 4 * step_h, info_text_width, info_text_height)
    text_rect6 = pygame.Rect(30 + info_text_x, info_text_y + 5 * step_h, info_text_width, info_text_height)
    text_rect7 = pygame.Rect(30 + info_text_x, info_text_y + 6 * step_h, info_text_width, info_text_height)

    wrapped_info_text1 = render_text_rect(info_text1, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text2 = render_text_rect(info_text2, font, text_rect2, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text3 = render_text_rect(info_text3, font, text_rect3, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text4 = render_text_rect(info_text4, font, text_rect4, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text5 = render_text_rect(info_text5, font, text_rect5, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text6 = render_text_rect(info_text6, font, text_rect6, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text7 = render_text_rect(info_text7, font, text_rect7, (255, 255, 255), (BLUE3), wrap=True)

    screen.blit(wrapped_info_text1, text_rect1)
    screen.blit(wrapped_info_text2, text_rect2)
    screen.blit(wrapped_info_text3, text_rect3)
    screen.blit(wrapped_info_text4, text_rect4)
    screen.blit(wrapped_info_text5, text_rect5)
    screen.blit(wrapped_info_text6, text_rect6)
    screen.blit(wrapped_info_text7, text_rect7)

    screen.blit(icon1, icon1_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            else:
                Starting_Q = show_input_box3(10, 10, screen_width, screen_height)
                rw_existence = True
                # game_over()
                fill_area_rect = pygame.Rect(280, 420, 450, 300)
                pygame.draw.rect(screen, BLUE3, fill_area_rect)
                return Starting_Q  # Exit the function to start the game

        screen.blit(wrapped_info_text1, text_rect1)
        screen.blit(wrapped_info_text2, text_rect2)
        screen.blit(wrapped_info_text3, text_rect3)
        screen.blit(wrapped_info_text4, text_rect4)
        screen.blit(wrapped_info_text5, text_rect5)
        screen.blit(wrapped_info_text6, text_rect6)
        screen.blit(wrapped_info_text7, text_rect7)

        screen.blit(icon1, icon1_rect)
        pygame.display.update()


def choose_the_use_of_rw_well():
    global rw_existence
    yes_button = pygame.Rect(screen_width // 2 - 150, screen_height // 2 + 270, 100, 50)
    no_button = pygame.Rect(screen_width // 2 + 50, screen_height // 2 + 270, 100, 50)

    font = pygame.font.Font(info_font, 20)
    font2 = pygame.font.Font(info_font, 22)

    yes_text = font.render("Yes", True, (255, 255, 255))
    no_text = font.render("No", True, (255, 255, 255))

    rw_text = "Are you using a recharging well?"
    text_surface = font2.render(rw_text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(500, 450))

    icon1 = pygame.transform.scale(icon_rw, (100, 100))
    icon1_rect = icon1.get_rect(topright=(screen_width // 2 + 50, 500))  # Adjust position as needed

    screen.fill(BLUE3)
    font = pygame.font.Font(info_font, 20)
    font2 = pygame.font.Font(info_font, 24)
    info_text_width = 900  # Change this if you want a different width for the text box
    info_text_height = 500  # Change this if you want a different height for the text box
    info_text_x = 50
    info_text_y = 80

    # Create the text rectangle and render the wrapped text
    font = pygame.font.Font(info_font, 18)
    info_text1 = "Συμπληρώστε το σκαρίφημα του συστήματος θέρμανσης των συγκροτημάτων κατοικιών Α, Β και θερμοκηπίων Γ του σχήματος. Δίνεται ότι:"
    info_text2 = "1-Η θερμοκρασία του γεωθερμικού νερού είναι 85 οC."
    info_text3 = "2-Η ποιότητά του είναι καλή."
    info_text4 = "3-Η απαιτούμενη παροχή θερμού νερού είναι ίση με Q1 για τα συγκροτήματα κατοικιών Α και Β και 1.9Q1 για το θερμοκήπιο Γ."
    info_text5 = "4-Δεν υπάρχει κίνδυνος εξάντλησης του υδροφορέα, αν η συνολικά αντλούμενη παροχή QΣ είναι μικρότερη από 2.1∙Q1"
    info_text6 = "5-Προκαλείται όμως σημαντική πτώση στάθμης του πιεζομετρικού φορτίου, αν η QΣ είναι μεγαλύτερη από 1.5∙Q1."
    info_text7 = "6-Οι απαιτούμενες θερμοκρασίες εισόδου και εξόδου φαίνονται στο σχήμα."

    step_h = 50
    text_rect1 = pygame.Rect(info_text_x, info_text_y + 0 * step_h, info_text_width, info_text_height)
    text_rect2 = pygame.Rect(30 + info_text_x, info_text_y + 1 * step_h, info_text_width, info_text_height)
    text_rect3 = pygame.Rect(30 + info_text_x, info_text_y + 2 * step_h, info_text_width, info_text_height)
    text_rect4 = pygame.Rect(30 + info_text_x, info_text_y + 3 * step_h, info_text_width, info_text_height)
    text_rect5 = pygame.Rect(30 + info_text_x, info_text_y + 4 * step_h, info_text_width, info_text_height)
    text_rect6 = pygame.Rect(30 + info_text_x, info_text_y + 5 * step_h, info_text_width, info_text_height)
    text_rect7 = pygame.Rect(30 + info_text_x, info_text_y + 6 * step_h, info_text_width, info_text_height)

    wrapped_info_text1 = render_text_rect(info_text1, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text2 = render_text_rect(info_text2, font, text_rect2, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text3 = render_text_rect(info_text3, font, text_rect3, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text4 = render_text_rect(info_text4, font, text_rect4, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text5 = render_text_rect(info_text5, font, text_rect5, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text6 = render_text_rect(info_text6, font, text_rect6, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text7 = render_text_rect(info_text7, font, text_rect7, (255, 255, 255), (BLUE3), wrap=True)

    screen.blit(wrapped_info_text1, text_rect1)
    screen.blit(wrapped_info_text2, text_rect2)
    screen.blit(wrapped_info_text3, text_rect3)
    screen.blit(wrapped_info_text4, text_rect4)
    screen.blit(wrapped_info_text5, text_rect5)
    screen.blit(wrapped_info_text6, text_rect6)
    screen.blit(wrapped_info_text7, text_rect7)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(pygame.mouse.get_pos()):
                    rw_existence = True  # Use single '=' for assignment
                    return  # Exit the function to start the game
                elif no_button.collidepoint(pygame.mouse.get_pos()):
                    rw_existence = False  # Use single '=' for assignment
                    return  # Exit the function to start the game

        pygame.draw.rect(screen, (RED), yes_button)
        screen.blit(yes_text, (screen_width // 2 - yes_text.get_width() // 2 - 100, screen_height // 2 + 280))
        pygame.draw.rect(screen, (RED), no_button)
        screen.blit(no_text, (screen_width // 2 - no_text.get_width() // 2 + 100, screen_height // 2 + 280))
        screen.blit(text_surface, text_rect)
        screen.blit(icon1, icon1_rect)

        pygame.display.flip()


def combined_start_function():
    global rw_existence, player_budget
    player_budget = 3000
    display_start_menu()
    username_to_info_and_start()
    screen.fill(BLUE)
    initialize_grid()


def initialize_grid():
    """Initialize everything in all the grids(grid, placement_grid, etc)"""
    # Clear the grid
    reset_grid()
    # What is happening in the grid
    if pw_row[dataset] > 0:
        grid[pw_row[dataset]][pw_col[dataset]] = icon_pw
        grid[pw_row[dataset] - 1][pw_col[dataset]] = icon_starting_spot
    if house0_row[dataset] > 0: grid[house0_row[dataset]][house0_col[dataset]] = icon_building1
    if house1_row[dataset] > 0: grid[house1_row[dataset]][house1_col[dataset]] = icon_building2
    if house2_row[dataset] > 0: grid[house2_row[dataset]][house2_col[dataset]] = icon_building1
    if greenhouse0_row[dataset] > 0: grid[greenhouse0_row[dataset]][greenhouse0_col[dataset]] = icon_greenhouse
    if greenhouse1_row[dataset] > 0: grid[greenhouse1_row[dataset]][greenhouse1_col[dataset]] = icon_greenhouse
    if rw_row[dataset] > 0 and rw_existence == True:
        grid[rw_row[dataset]][rw_col[dataset]] = icon_rw
        grid[rw_row[dataset] - 1][rw_col[dataset]] = icon_ending_spot
    else:
        grid[outflow_row[dataset]][outflow_col[dataset]] = icon_rw  # na valoume eikonidio outflow
        grid[outflow_row[dataset] - 1][outflow_col[dataset]] = icon_ending_spot
    # What is happening in the placement_grid
    if pw_row[dataset] > 0: placement_grid[pw_row[dataset]][pw_col[dataset]] = 10
    if house0_row[dataset] > 0: placement_grid[house0_row[dataset]][house0_col[dataset]] = 11
    if house1_row[dataset] > 0: placement_grid[house1_row[dataset]][house1_col[dataset]] = 11
    if house2_row[dataset] > 0: placement_grid[house2_row[dataset]][house2_col[dataset]] = 11
    if greenhouse0_row[dataset] > 0: placement_grid[greenhouse0_row[dataset]][greenhouse0_col[dataset]] = 11
    if greenhouse1_row[dataset] > 0: placement_grid[greenhouse1_row[dataset]][greenhouse1_col[dataset]] = 11
    if rw_row[dataset] > 0 and rw_existence == True: placement_grid[rw_row[dataset]][rw_col[dataset]] = 12
    if outflow_row[dataset] > 0 and rw_existence == False: placement_grid[outflow_row[dataset]][
        outflow_col[dataset]] = 12


def pipe_section_grid_for_icon_house0():
    global pipe_section
    pipe_section_grid[house0_row[dataset]][house0_col[dataset]] = -11
    T_grid[house0_row[dataset]][house0_col[dataset]] = Thouse0_in[dataset], Thouse0_out[dataset]
    Q_grid[house0_row[dataset]][house0_col[dataset]] = float(Qhouse0_in[dataset])
    # Q_grid[house0_row[dataset]][house0_col[dataset]] =
    font = pygame.font.Font(info_font, 15)
    text_content1 = f"T_εισόδου = {int(Thouse0_in[dataset])}"
    text_content2 = f"T_εξόδου = {int(Thouse0_out[dataset])}"
    text_content3 = f"Q_εισόδου = {int(Qhouse0_in[dataset])}"
    text_surface1 = font.render(text_content1, True, (255, 255, 255))  # White text color
    text_position1 = (675, 25)  # Position to render the text
    text_surface2 = font.render(text_content2, True, (255, 255, 255))  # White text color
    text_position2 = (675, 50)  # Position to render the text
    text_surface3 = font.render(text_content3, True, (255, 255, 255))  # White text color
    text_position3 = (675, 75)  # Position to render the text
    new_width = 40
    new_height = 40
    icon_building1_resized = pygame.transform.scale(icon_building1, (new_width, new_height))
    screen.blit(icon_building1_resized, (625, 38))
    screen.blit(text_surface1, text_position1)
    screen.blit(text_surface2, text_position2)
    screen.blit(text_surface3, text_position3)


def budget_calculator_for_icon_house0():
    global house0_executed, player_budget
    if max(T_grid[house0_row[dataset]][house0_col[dataset]]) > T_grid[house0_row[dataset] - 1][house0_col[dataset]] and \
            T_grid[house0_row[dataset] - 1][house0_col[dataset]] != 0 and house0_executed == False:
        player_budget -= float((max(T_grid[house0_row[dataset]][house0_col[dataset]]) - T_grid[house0_row[dataset] - 1][
            house0_col[dataset]]) * 500)
        house0_executed = True


def pipe_section_grid_for_icon_house1():
    global pipe_section
    pipe_section_grid[house1_row[dataset]][house1_col[dataset]] = -11
    T_grid[house1_row[dataset]][house1_col[dataset]] = Thouse1_in[dataset], Thouse1_out[dataset]
    Q_grid[house1_row[dataset]][house1_col[dataset]] = float(Qhouse1_in[dataset])
    font = pygame.font.Font(info_font, 15)
    text_content1 = f"T_εισόδου = {int(Thouse1_in[dataset])}"
    text_content2 = f"T_εξόδου = {int(Thouse1_out[dataset])}"
    text_content3 = f"Q_εισόδου = {int(Qhouse1_in[dataset])}"
    text_surface1 = font.render(text_content1, True, (255, 255, 255))  # White text color
    text_position1 = (875, 25)  # Position to render the text
    text_surface2 = font.render(text_content2, True, (255, 255, 255))  # White text color
    text_position2 = (875, 50)  # Position to render the text
    text_surface3 = font.render(text_content3, True, (255, 255, 255))  # White text color
    text_position3 = (875, 75)  # Position to render the text
    new_width = 40
    new_height = 40
    icon_building2_resized = pygame.transform.scale(icon_building2, (new_width, new_height))
    screen.blit(icon_building2_resized, (825, 38))
    screen.blit(text_surface1, text_position1)
    screen.blit(text_surface2, text_position2)
    screen.blit(text_surface3, text_position3)


def budget_calculator_for_icon_house1():
    global house1_executed, player_budget
    if max(T_grid[house1_row[dataset]][house1_col[dataset]]) > T_grid[house1_row[dataset] - 1][house1_col[dataset]] and \
            T_grid[house1_row[dataset] - 1][house1_col[dataset]] != 0 and house1_executed == False:
        player_budget -= float((max(T_grid[house1_row[dataset]][house1_col[dataset]]) - T_grid[house1_row[dataset] - 1][
            house1_col[dataset]]) * 500)
        house1_executed = True


def pipe_section_grid_for_icon_house2():
    global pipe_section
    pipe_section_grid[house2_row[dataset]][house2_col[dataset]] = -11
    T_grid[house2_row[dataset]][house2_col[dataset]] = Thouse2_in[dataset], Thouse2_out[dataset]
    Q_grid[house2_row[dataset]][house2_col[dataset]] = float(Qhouse2_in[dataset])
    font = pygame.font.Font(info_font, 15)
    text_content1 = f"T_εισόδου = {int(Thouse2_in[dataset])}"
    text_content2 = f"T_εξόδου = {int(Thouse2_out[dataset])}"
    text_content3 = f"Q_εισόδου = {int(Qhouse2_in[dataset])}"
    text_surface1 = font.render(text_content1, True, (255, 255, 255))  # White text color
    text_position1 = (875, 125)  # Position to render the text
    text_surface2 = font.render(text_content2, True, (255, 255, 255))  # White text color
    text_position2 = (875, 150)  # Position to render the text
    text_surface3 = font.render(text_content3, True, (255, 255, 255))  # White text color
    text_position3 = (875, 175)  # Position to render the text
    new_width = 40
    new_height = 40
    icon_building2_resized = pygame.transform.scale(icon_building2, (new_width, new_height))  # "To icon 3 θεωριτικά"
    screen.blit(icon_building2_resized, (825, 150 + 13))
    screen.blit(text_surface1, text_position1)
    screen.blit(text_surface2, text_position2)
    screen.blit(text_surface3, text_position3)


def budget_calculator_for_icon_house2():
    global house2_executed, player_budget
    if max(T_grid[house2_row[dataset]][house2_col[dataset]]) > T_grid[house2_row[dataset] - 1][house2_col[dataset]] and \
            T_grid[house2_row[dataset] - 1][house2_col[dataset]] != 0 and house2_executed == False:
        player_budget -= float((max(T_grid[house2_row[dataset]][house2_col[dataset]]) - T_grid[house2_row[dataset] - 1][
            house2_col[dataset]]) * 500)
        house2_executed = True


def pipe_section_grid_for_icon_greenhouse0():
    global pipe_section
    pipe_section_grid[greenhouse0_row[dataset]][greenhouse0_col[dataset]] = -12
    T_grid[greenhouse0_row[dataset]][greenhouse0_col[dataset]] = Tgreenhouse0_in[dataset], Tgreenhouse0_out[dataset]
    Q_grid[greenhouse0_row[dataset]][greenhouse0_col[dataset]] = float(Qghouse0_in[dataset])
    font = pygame.font.Font(info_font, 15)
    text_content1 = f"T_εισόδου = {int(Tgreenhouse0_in[dataset])}"
    text_content2 = f"T_εξόδου = {int(Tgreenhouse0_out[dataset])}"
    text_content3 = f"Q_εισόδου = {int(Qghouse0_in[dataset])}"
    text_surface1 = font.render(text_content1, True, (255, 255, 255))  # White text color
    text_position1 = (675, 125 + 25)  # Position to render the text
    text_surface2 = font.render(text_content2, True, (255, 255, 255))  # White text color
    text_position2 = (675, 150 + 25)  # Position to render the text
    text_surface3 = font.render(text_content3, True, (255, 255, 255))  # White text color
    text_position3 = (675, 175 + 25)  # Position to render the text
    new_width = 40
    new_height = 40
    icon_greenhouse_resized = pygame.transform.scale(icon_greenhouse, (new_width, new_height))
    screen.blit(icon_greenhouse_resized, (625, 150 + 13))
    screen.blit(text_surface1, text_position1)
    screen.blit(text_surface2, text_position2)
    screen.blit(text_surface3, text_position3)


def budget_calculator_for_icon_greenhouse0():
    global ghouse0_executed, player_budget
    if max(T_grid[greenhouse0_row[dataset]][greenhouse0_col[dataset]]) > T_grid[greenhouse0_row[dataset] - 1][
        greenhouse0_col[dataset]] and \
            T_grid[greenhouse0_row[dataset] - 1][greenhouse0_col[dataset]] != 0 and ghouse0_executed == False:
        player_budget -= float(
            (max(T_grid[greenhouse0_row[dataset]][greenhouse0_col[dataset]]) - T_grid[greenhouse0_row[dataset] - 1][
                greenhouse0_col[dataset]]) * 500)
        ghouse0_executed = True


def pipe_section_grid_for_icon_greenhouse1():
    global pipe_section
    pipe_section_grid[greenhouse1_row[dataset]][greenhouse1_col[dataset]] = -12
    T_grid[greenhouse1_row[dataset]][greenhouse1_col[dataset]] = Tgreenhouse1_in[dataset], Tgreenhouse1_out[dataset]
    Q_grid[greenhouse1_row[dataset]][greenhouse1_col[dataset]] = float(Qghouse1_in[dataset])
    "lines for corrections"  # Λογικά η θέση δεν είναι ακριβώς σωστή
    font = pygame.font.Font(info_font, 15)
    text_content1 = f"T_εισόδου = {int(Tgreenhouse1_in[dataset])}"
    text_content2 = f"T_εξόδου = {int(Tgreenhouse1_out[dataset])}"
    text_content3 = f"Q_εισόδου = {int(Qghouse1_in[dataset])}"
    text_surface1 = font.render(text_content1, True, (255, 255, 255))  # White text color
    text_position1 = (675, 125 + 50)  # Position to render the text
    text_surface2 = font.render(text_content2, True, (255, 255, 255))  # White text color
    text_position2 = (675, 150 + 50)  # Position to render the text
    text_surface3 = font.render(text_content3, True, (255, 255, 255))  # White text color
    text_position3 = (675, 175 + 50)  # Position to render the text
    new_width = 40
    new_height = 40
    icon_greenhouse_resized = pygame.transform.scale(icon_greenhouse, (new_width, new_height))
    screen.blit(icon_greenhouse_resized, (625, 150 + 13))
    screen.blit(text_surface1, text_position1)
    screen.blit(text_surface2, text_position2)
    screen.blit(text_surface3, text_position3)


def budget_calculator_for_icon_greenhouse1():
    global ghouse1_executed, player_budget
    if max(T_grid[greenhouse1_row[dataset]][greenhouse1_col[dataset]]) > T_grid[greenhouse1_row[dataset] - 1][
        greenhouse1_col[dataset]] and \
            T_grid[greenhouse1_row[dataset] - 1][greenhouse1_col[dataset]] != 0 and ghouse1_executed == False:
        player_budget -= float(
            (max(T_grid[greenhouse1_row[dataset]][greenhouse1_col[dataset]]) - T_grid[greenhouse1_row[dataset] - 1][
                greenhouse1_col[dataset]]) * 500)
        ghouse1_executed = True


def info_ghouse_blue_square():
    # Draw a blue rectangle background
    rect_x = 610
    rect_y = 10
    rect_width = 390  # Adding a little extra for padding
    rect_height = 230
    pygame.draw.rect(screen, BLUE, (rect_x, rect_y, rect_width, rect_height))


def budget_calculator():
    global icon_index, player_budget, house0_executed, house1_executed, house2_executed, ghouse0_executed, ghouse1_executed

    new_width = 40
    new_height = 40
    font = pygame.font.Font(None, 30)

    # simple_pipe_cost = 50
    # corner_pipe_cost = 60
    # triplet_pipe_cost = 70

    if 0 <= icon_index <= 1:
        player_budget -= simple_pipe_cost[dataset]
    elif 2 <= icon_index <= 5:
        player_budget -= corner_pipe_cost[dataset]
    elif 6 <= icon_index <= 9:
        player_budget -= triplet_pipe_cost[dataset]
    "lines for correction"

    if house0_row[dataset] > 0: budget_calculator_for_icon_house0()
    if house1_row[dataset] > 0: budget_calculator_for_icon_house1()
    if house2_row[dataset] > 0: budget_calculator_for_icon_house2()
    if greenhouse0_row[dataset] > 0: budget_calculator_for_icon_greenhouse0()
    if greenhouse1_row[dataset] > 0: budget_calculator_for_icon_greenhouse1()

    text_content = f"Budget = {int(player_budget)} "
    text_surface = font.render(text_content, True, WHITE)  # White text color

    # Get dimensions of the text surface
    text_width, text_height = text_surface.get_size()

    # Draw a blue rectangle background
    rect_x = 0
    rect_y = 660
    rect_width = text_width + 460  # Adding a little extra for padding
    rect_height = 150
    pygame.draw.rect(screen, BLUE, (rect_x, rect_y, rect_width, rect_height))

    # Position to render the text and icon
    text_position = (80, 680)
    icon_dollar_sign_resized = pygame.transform.scale(icon_dollar_sign, (new_width, new_height))

    screen.blit(icon_dollar_sign_resized, (40, 668))
    screen.blit(text_surface, text_position)

    pygame.display.update()


def draw_buttons(screen, button_x, button_y, button_width, button_height, undo_button_x, undo_button_y):
    # Blue rect for no flickering
    pygame.draw.rect(screen, BLUE, (0, 608, 544 + 63, 52))
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

    # Draw the Tip button
    pygame.draw.rect(screen, GRAY, (button_x + 110, button_y, button_width, button_height))
    tip_text = reset_font.render("Tips", True, WHITE)
    tip_text_rect = tip_text.get_rect(center=((button_x + button_width // 2 + 110), button_y + button_height // 2))
    screen.blit(tip_text, tip_text_rect)


def right_click_grid_cell_info(event, row, col):
    if 64 <= event.pos[0] <= 544 + 64 and 64 <= event.pos[1] <= 544 + 64 and placement_grid[row][col] != -1:
        transparent_surface = pygame.Surface((100, 50), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())

        font = pygame.font.Font(None, 15)
        text1 = font.render(f" Pipe_Section:{pipe_section_grid[row][col] + 1}", True, WHITE)
        text2 = font.render(f" T: {T_grid[row][col]}", True, WHITE)
        transparent_surface.blit(text1, (0, 10))
        transparent_surface.blit(text2, (0, 30))

        screen.blit(transparent_surface, (event.pos[0], event.pos[1] - 80))

        pygame.display.update()

        start_time = pygame.time.get_ticks()
        elapsed_time = 0
        while elapsed_time < 3000:  # Wait for 3 seconds
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        return

    else:
        return


def reset_grid():
    """Reset the grid by clearing all icons except for icon_pw."""
    global Starting_Q, pipe_section, row, col, Starting_T, player_budget

    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][
                j] is not None:  # and grid[i][j] != icon_pw and grid[i][j] != icon_building1 and grid[i][j] != icon_building2 and grid[i][j] != icon_greenhouse and grid[i][j] != icon_rw:
                grid[i][j] = None
                placement_grid[i][j] = -1
                Q_grid[i][j] = -2
                T_grid[i][j] = 0
                pipe_section_grid[i][j] = 0

    Q.clear()
    T.clear()
    Q2.clear()
    T2.clear()
    T[pipe_section] = []
    pipe_section = 0
    Q_grid[pw_row[dataset] - 1][pw_col[dataset]] = int(Starting_Q)
    T_grid[pw_row[dataset]][pw_col[dataset]] = Starting_T
    T[pipe_section] = [T_grid[pw_row[dataset] - 1][pw_col[dataset]]]
    Q[pipe_section] = [Q_grid[pw_row[dataset] - 1][pw_col[dataset]]]
    player_budget = 3000
    pygame.draw.rect(screen, BLUE, (610, 350, 400, 400))


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
        input_box_y = 300
        input_box_width = 100
        input_box_height = 25

        # Draw the input box
        pygame.draw.rect(screen, WHITE, (input_box_x, input_box_y, input_box_width, input_box_height))
        pygame.draw.rect(screen, BLACK, (input_box_x, input_box_y, input_box_width, input_box_height), 1)

        # Draw the input text
        input_text = input_box_font.render(text, True, BLACK)
        input_text_rect = input_text.get_rect(
            center=(input_box_x + input_box_width // 2, input_box_y + input_box_height // 2))
        screen.blit(input_text, input_text_rect)

        # Draw the input label
        input_label_text = input_label_font.render(f"Q{pipe_section + 1}:", True, BLACK)
        input_label_text_rect = input_label_text.get_rect(x=input_box_x - 50, y=input_box_y)
        screen.blit(input_label_text, input_label_text_rect)

        pygame.display.update()

    # Draw the blue square after the event handling loop
    if submitted:
        pygame.draw.rect(screen, BLUE,
                         (input_box_x - 50, input_box_y - 60, 200, 90))  # Adjust the rectangle size as needed
        pygame.display.update()

    # Validate the input and ask the player to redo the input if it's not a valid integer
    while True:
        try:
            return int(text)
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            text = show_input_box(x, y, screen_width, screen_height)  # Recursively call the function to redo the input


def show_input_box2(x, y, screen_width, screen_height, text=""):
    """Show an input box on the screen and return the player's input as an integer."""
    global pipe_section
    input_box_font = pygame.font.Font(info_font, 30)
    active = True
    enter_input_sound.play(0)
    input_label_font = pygame.font.Font(info_font2, 34)  # New font for the input label
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

        input_box_x = 360
        input_box_y = 750 // 2
        input_box_width = 300
        input_box_height = 30

        # Draw the input box
        pygame.draw.rect(screen, WHITE, (input_box_x, input_box_y, input_box_width, input_box_height))
        pygame.draw.rect(screen, BLACK, (input_box_x, input_box_y, input_box_width, input_box_height), 1)

        # Draw the input text
        input_text = input_box_font.render(text, True, BLACK)
        input_text_rect = input_text.get_rect(
            center=(input_box_x + input_box_width // 2, input_box_y + input_box_height // 2))
        screen.blit(input_text, input_text_rect)

        # Draw the input label
        input_label_text = input_label_font.render(f"Please enter your username", True, WHITE)
        input_label_text_rect = input_label_text.get_rect(x=300, y=input_box_y - 75)
        screen.blit(input_label_text, input_label_text_rect)

        pygame.display.update()

    # Draw the blue square after the event handling loop
    if submitted:
        pygame.draw.rect(screen, BLUE,
                         (input_box_x - 50, input_box_y - 55, 200, 40))  # Adjust the rectangle size as needed
        pygame.display.update()

    # Validate the input and ask the player to redo the input if it's not a valid integer
    while True:
        try:
            return str(text)
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            text = show_input_box2(x, y, screen_width, screen_height)  # Recursively call the function to redo the input


def show_input_box3(x, y, screen_width, screen_height, text=""):
    """Show an input box on the screen and return the player's input as an integer."""
    global pipe_section
    input_box_font = pygame.font.Font(info_font, 22)
    active = True
    enter_input_sound.play(0)
    input_label_font = pygame.font.Font(info_font, 30)  # New font for the input label
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

        input_box_x = 500
        input_box_y = 475
        input_box_width = 150
        input_box_height = 25

        # Draw the input box
        pygame.draw.rect(screen, WHITE, (input_box_x, input_box_y, input_box_width, input_box_height))
        pygame.draw.rect(screen, BLACK, (input_box_x, input_box_y, input_box_width, input_box_height), 1)

        # Draw the input text
        input_text = input_box_font.render(text, True, BLACK)
        input_text_rect = input_text.get_rect(
            center=(input_box_x + input_box_width // 2, input_box_y + input_box_height // 2))
        screen.blit(input_text, input_text_rect)

        # Draw the input label
        input_label_text = input_label_font.render(f"Starting Q(Q{pipe_section + 1}):", True, WHITE)
        input_label_text_rect = input_label_text.get_rect(x=input_box_x - 205, y=input_box_y - 7.5)
        screen.blit(input_label_text, input_label_text_rect)

        pygame.display.update()

    # Validate the input and ask the player to redo the input if it's not a valid integer
    while True:
        try:
            return int(text)
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            text = show_input_box3(x, y, screen_width, screen_height)  # Recursively call the function to redo the input


def left_arrow_appears():
    """Display all the information that is necessary for the player to solve the problem"""
    # Change the position of the icon_down_arrow to (x=700, y=50)
    icon_left_arrow_rect = icon_left_arrow.get_rect(x=725, y=240)

    # Scale the size of the icon_down_arrow
    scaled_width = 50  # Change this to the desired width
    scaled_height = 50  # Change this to the desired height
    icon_left_arrow_scaled = pygame.transform.scale(icon_left_arrow, (scaled_width, scaled_height))

    # Draw the scaled icon_down_arrow at the new position
    screen.blit(icon_left_arrow_scaled, icon_left_arrow_rect)


def right_arrow_appears():
    """Display the right arrow icon"""
    # Change the position of the icon_right_arrow to (x=700, y=50) for the right position
    icon_right_arrow_rect = icon_right_arrow.get_rect(x=725, y=240)

    # Scale the size of the icon_right_arrow
    scaled_width = 50  # Change this to the desired width
    scaled_height = 50  # Change this to the desired height
    icon_right_arrow_scaled = pygame.transform.scale(icon_right_arrow, (scaled_width, scaled_height))

    # Draw the scaled icon_right_arrow at the new position
    screen.blit(icon_right_arrow_scaled, icon_right_arrow_rect)


def down_arrow_appears():
    """Display the down arrow icon"""
    # Change the position of the icon_down_arrow to (x=700, y=50) for the down position
    icon_down_arrow_rect = icon_down_arrow.get_rect(x=725, y=240)

    # Scale the size of the icon_down_arrow
    scaled_width = 50  # Change this to the desired width
    scaled_height = 50  # Change this to the desired height
    icon_down_arrow_scaled = pygame.transform.scale(icon_down_arrow, (scaled_width, scaled_height))

    # Draw the scaled icon_down_arrow at the new position
    screen.blit(icon_down_arrow_scaled, icon_down_arrow_rect)


def up_arrow_appears():
    """Display the up arrow icon"""
    # Change the position of the icon_up_arrow to (x=700, y=50) for the up position
    icon_up_arrow_rect = icon_up_arrow.get_rect(x=725, y=240)

    # Scale the size of the icon_up_arrow
    scaled_width = 50  # Change this to the desired width
    scaled_height = 50  # Change this to the desired height
    icon_up_arrow_scaled = pygame.transform.scale(icon_up_arrow, (scaled_width, scaled_height))

    # Draw the scaled icon_up_arrow at the new position
    screen.blit(icon_up_arrow_scaled, icon_up_arrow_rect)


def covering_the_arrow(screen):
    """Draw the cover on the screen at a fixed position."""
    blue_rect_width = 50
    blue_rect_height = 40
    blue_rect_color = (BLUE)  # RGB value for blue

    pygame.draw.rect(screen, blue_rect_color, (650, 300, blue_rect_width, blue_rect_height))
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
    font = pygame.font.Font(None, 22)
    text_color = RED2
    num_columns = min(len(Q2), 1)

    for idx, (key, value) in enumerate(Q2.items()):
        column = idx % num_columns
        row = idx // num_columns

        # Draw a blue rectangle before rendering text
        rect_x = 625 + column * 90
        rect_y = 345 + row * 30
        rect_width = 130
        rect_height = 305
        pygame.draw.rect(screen, BLUE, (rect_x, rect_y, rect_width, rect_height))

        text_surface = font.render(f"{key}: {value}", True, text_color)
        screen.blit(text_surface, (650 + column * 90, 350 + row * 30))

    pygame.display.update()


def render_T_start_dic(T, screen):
    font = pygame.font.Font(None, 22)
    text_color = RED2

    # Determine the number of columns to arrange the keys
    num_columns = min(len(T), 1)

    # Render the T dictionary on the screen with special positioning
    for idx, (key, value) in enumerate(T.items()):
        column = idx % num_columns
        row = idx // num_columns

        # Draw a blue rectangle before rendering text
        rect_x = 740 + column * 90
        rect_y = 345 + row * 30
        rect_width = 130
        rect_height = 305
        pygame.draw.rect(screen, BLUE, (rect_x, rect_y, rect_width, rect_height))

        if isinstance(value, (list, np.ndarray)):
            if len(value) > 0:
                last_value = value[0]  # Get the last value from the array
                formatted_value = "{:.1f}".format(last_value)  # Format to 1 decimal places
                text_surface = font.render(f"T_start : {formatted_value}", True, text_color)
                screen.blit(text_surface, (750 + column * 90, 350 + row * 30))
        else:
            text_surface = font.render(f"T_Start: {value}", True, text_color)
            screen.blit(text_surface, (750 + column * 90, 350 + row * 30))

    pygame.display.update()


def render_T_end_dic(T, screen):
    font = pygame.font.Font(None, 22)
    text_color = RED2

    # Determine the number of columns to arrange the keys
    num_columns = min(len(T), 1)

    # Render the T dictionary on the screen with special positioning
    for idx, (key, value) in enumerate(T.items()):
        column = idx % num_columns
        row = idx // num_columns

        # Draw a blue rectangle before rendering text
        rect_x = 870 + column * 90
        rect_y = 345 + row * 30
        rect_width = 160
        rect_height = 305
        pygame.draw.rect(screen, BLUE, (rect_x, rect_y, rect_width, rect_height))

        if isinstance(value, (list, np.ndarray)):
            if len(value) > 0:
                last_value = value[-1]  # Get the last value from the array
                formatted_value = "{:.1f}".format(last_value)  # Format to 1 decimal place
                text_surface = font.render(f"T_end : {formatted_value}", True, text_color)
                screen.blit(text_surface, (875 + column * 90, 350 + row * 30))
        else:
            text_surface = font.render(f"T_end: {value}", True, text_color)
            screen.blit(text_surface, (875 + column * 90, 350 + row * 30))

    pygame.display.update()


def game_over():
    global Starting_Q, Qtot_depl, Qtot_head, player_budget, Qhouse0_in, Qhouse1_in, Qhouse2_in, Qghouse0_in, Qghouse1_in, rw_existence, screen

    font = pygame.font.Font(info_font, 15)
    font2 = pygame.font.Font(info_font, 30)
    font3 = pygame.font.Font(None, 30)
    lreason_1 = "Η παροχή άντλησης γεωθερμικού ρευστού που εισήγαγες Qtotal (Q1) είναι λάθος. Συμβουλέψου τη θεωρία 1."
    tip_1 = "Η παροχή άντλησης γεωθερμικού ρευστού που εισήγαγες είναι μεγαλύτερη από τη μέγιστη παροχή άντλησης την οποία μπορεί να δεχθεί ο υδροφορέας χωρίς κίνδυνος εξάντλησης. Παρακαλώ επιλέξτε παροχή άντλησης μικρότερη ή ίση της μέγιστης επιτρεπτής."
    lreason_2 = (
        "Η παροχή άντλησης γεωθερμικού ρευστού που εισήγαγες Qtotal (Q1) είναι λάθος. Συμβουλέψου τη θεωρία 2.")
    tip_2 = "Η παροχή άντλησης γεωθερμικού ρευστού που εισήγαγες Qtotal (Q1) θα προκαλέσει μακροπρόθεσμα σημαντική πτώση στάθμης στον υδροφορέα."
    lreason__3 = "Η παροχή άντλησης γεωθερμικού ρευστού που εισήγαγες Qtotal (Q1) είναι λάθος. Συμβουλέψου τη θεωρία 3."
    tip_3 = "Η παροχή άντλησης γεωθερμικού ρευστού που εισήγαγες Qtotal (Q1) δεν θα μπορεί να ικανοποιήσει τουλάχιστον τον πιο απαιτητικό από άποψη παροχής χρήστη. Πρέπει να επιλεγεί παροχή ίση ή μεγαλύτερη της μέγιστης παροχής ζήτησης του κάθε χρήστη."
    lreason_4 = "Η παροχή στο συγκεκρίμενο χρήστη ήταν λανθασμένη"
    tip_4 = "Η παροχή που καταλίγει στο χρήστη πρέπει να είναι ίση με αυτή των δεδομένων"
    lreason_5 = "Το budget σου εξαντήθηκε"
    tip_5 = "Χρησιμοποίησε τους πόρους πιο σωστά"

    rendered_lreason_1 = font.render(lreason_1, True, (255, 255, 255))
    rendered_lreason_2 = font.render(lreason_2, True, (255, 255, 255))
    rendered_lreason_3 = font.render(lreason__3, True, (255, 255, 255))
    rendered_lreason_4 = font.render(lreason_4, True, (255, 255, 255))
    rendered_lreason_5 = font.render(lreason_5, True, (255, 255, 255))

    rendered_tip_1 = font.render(tip_1, True, (255, 255, 255))
    rendered_tip_2 = font.render(tip_2, True, (255, 255, 255))
    rendered_tip_3 = font.render(tip_3, True, (255, 255, 255))
    rendered_tip_4 = font.render(tip_4, True, (255, 255, 255))
    rendered_tip_5 = font.render(tip_5, True, (255, 255, 255))

    rendered_lreason_1_rect = rendered_lreason_1.get_rect(center=(screen_width // 2, screen_height // 2))
    rendered_lreason_2_rect = rendered_lreason_2.get_rect(center=(screen_width // 2, screen_height // 2))
    rendered_lreason_3_rect = rendered_lreason_3.get_rect(center=(screen_width // 2, screen_height // 2))
    rendered_lreason_4_rect = rendered_lreason_4.get_rect(center=(screen_width // 2, screen_height // 2))
    rendered_lreason_5_rect = rendered_lreason_5.get_rect(center=(screen_width // 2, screen_height // 2))

    rendered_tip_1_rect = pygame.Rect((0, 0), (700, 50))
    rendered_tip_2_rect = pygame.Rect((0, 0), (700, 50))
    rendered_tip_3_rect = pygame.Rect((0, 0), (700, 50))
    rendered_tip_4_rect = pygame.Rect((0, 0), (700, 50))
    rendered_tip_5_rect = pygame.Rect((0, 0), (700, 50))

    wrapped_tip_1 = render_text_rect(tip_1, font, rendered_tip_1_rect, (255, 255, 255), (BLACK), wrap=True)
    wrapped_tip_2 = render_text_rect(tip_2, font, rendered_tip_2_rect, (255, 255, 255), (BLACK), wrap=True)
    wrapped_tip_3 = render_text_rect(tip_3, font, rendered_tip_3_rect, (255, 255, 255), (BLACK), wrap=True)
    wrapped_tip_4 = render_text_rect(tip_4, font, rendered_tip_4_rect, (255, 255, 255), (BLACK), wrap=True)
    wrapped_tip_5 = render_text_rect(tip_5, font, rendered_tip_5_rect, (255, 255, 255), (BLACK), wrap=True)

    # Draw the Retry section button
    retry_button_width = 150
    retry_button_height = 50
    retry_button_x = 450
    retry_button_y = 500
    retry_text = font2.render("Retry", True, WHITE)
    retry_text_rect = retry_text.get_rect(  # Corrected this line
        center=(retry_button_x + retry_button_width // 2, retry_button_y + retry_button_height // 2))

    # Draw the Tip section button
    tip_button_width = 80
    tip_button_height = 50
    tip_button_x = 800
    tip_button_y = 100
    tip_text = font2.render("Tip", True, WHITE)
    tip_text_rect = tip_text.get_rect(
        center=(tip_button_x + tip_button_width // 2, tip_button_y + tip_button_height // 2))

    # if for reason_lost_1 and tip button on game over screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if Starting_Q > Qtot_depl[dataset] + 1:
                screen.fill(BLUE3)
                screen.blit(rendered_lreason_1, rendered_lreason_1_rect)
                pygame.draw.rect(screen, GRAY,
                                 (retry_button_x, retry_button_y, retry_button_width, retry_button_height))
                screen.blit(retry_text, retry_text_rect)
                pygame.draw.rect(screen, GRAY,
                                 (tip_button_x, tip_button_y, tip_button_width, tip_button_height))
                screen.blit(tip_text, tip_text_rect)
                pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if retry_text_rect.collidepoint(mouse_x, mouse_y):
                        combined_start_function()
                    elif tip_text_rect.collidepoint(mouse_x, mouse_y):
                        transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                        pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                        transparent_surface.blit(wrapped_tip_1, (20, 10))
                        screen.blit(transparent_surface, (100, 200))
                        pygame.display.update()
            elif Starting_Q < Qtot_head[dataset]:
                if Starting_Q < (
                        Qhouse0_in[dataset] and Qhouse1_in[dataset] and Qhouse2_in[dataset] and Qghouse0_in[dataset] and
                        Qghouse1_in[dataset]):
                    screen.fill(BLUE3)
                    screen.blit(rendered_lreason_3, rendered_lreason_3_rect)
                    pygame.draw.rect(screen, GRAY,
                                     (retry_button_x, retry_button_y, retry_button_width, retry_button_height))
                    screen.blit(retry_text, retry_text_rect)
                    pygame.draw.rect(screen, GRAY,
                                     (tip_button_x, tip_button_y, tip_button_width, tip_button_height))
                    screen.blit(tip_text, tip_text_rect)
                    pygame.display.update()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if retry_text_rect.collidepoint(mouse_x, mouse_y):
                            combined_start_function()
                        elif tip_text_rect.collidepoint(mouse_x, mouse_y):
                            transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                            pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                            transparent_surface.blit(wrapped_tip_3, (20, 10))
                            screen.blit(transparent_surface, (100, 200))
                            pygame.display.update()
                elif rw_existence == True:
                    screen.fill(BLUE3)
                    screen.blit(rendered_lreason_2, rendered_lreason_2_rect)
                    pygame.draw.rect(screen, GRAY,
                                     (retry_button_x, retry_button_y, retry_button_width, retry_button_height))
                    screen.blit(retry_text, retry_text_rect)
                    pygame.draw.rect(screen, GRAY,
                                     (tip_button_x, tip_button_y, tip_button_width, tip_button_height))
                    screen.blit(tip_text, tip_text_rect)
                    pygame.display.update()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if retry_text_rect.collidepoint(mouse_x, mouse_y):
                            combined_start_function()
                        elif tip_text_rect.collidepoint(mouse_x, mouse_y):
                            transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                            pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                            transparent_surface.blit(wrapped_tip_2, (20, 10))
                            screen.blit(transparent_surface, (100, 200))
                            pygame.display.update()
                else:
                    return
            elif Starting_Q > Qtot_head[dataset]:
                if Starting_Q < (
                        Qhouse0_in[dataset] and Qhouse1_in[dataset] and Qhouse2_in[dataset] and Qghouse0_in[dataset] and
                        Qghouse1_in[dataset]):
                    screen.fill(BLUE3)
                    screen.blit(rendered_lreason_3, (80, screen_height // 2))
                    pygame.draw.rect(screen, GRAY,
                                     (retry_button_x, retry_button_y, retry_button_width, retry_button_height))
                    screen.blit(retry_text, retry_text_rect)
                    pygame.draw.rect(screen, GRAY,
                                     (tip_button_x, tip_button_y, tip_button_width, tip_button_height))
                    screen.blit(tip_text, tip_text_rect)
                    pygame.display.update()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if retry_text_rect.collidepoint(mouse_x, mouse_y):
                            combined_start_function()
                        elif tip_text_rect.collidepoint(mouse_x, mouse_y):
                            transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                            pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                            transparent_surface.blit(wrapped_tip_3, (20, 10))
                            screen.blit(transparent_surface, (100, 200))
                            pygame.display.update()
                elif rw_existence == False:
                    screen.fill(BLUE3)
                    screen.blit(rendered_lreason_2, (80, screen_height // 2))
                    pygame.draw.rect(screen, GRAY,
                                     (retry_button_x, retry_button_y, retry_button_width, retry_button_height))
                    screen.blit(retry_text, retry_text_rect)
                    pygame.draw.rect(screen, GRAY,
                                     (tip_button_x, tip_button_y, tip_button_width, tip_button_height))
                    screen.blit(tip_text, tip_text_rect)
                    pygame.display.update()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if retry_text_rect.collidepoint(mouse_x, mouse_y):
                            combined_start_function()
                        elif tip_text_rect.collidepoint(mouse_x, mouse_y):
                            transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                            pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                            transparent_surface.blit(wrapped_tip_2, (20, 10))
                            screen.blit(transparent_surface, (100, 200))
                            pygame.display.update()
                else:
                    return
            else:
                return


"""
Μήπως για πιο περίπλοκα ή απλά περισσότερα ποσοτικά προβλήματα χρειάζεται το αν υπάρχει ή όχι recharging well να εισάγεται απο το Excel"
"""


def game_over_budget():
    global player_budget
    screen.fill(BLUE3)
    font = pygame.font.Font(None, 20)
    font2 = pygame.font.Font(info_font, 40)

    lreason_5 = "Το budget σου εξαντήθηκε"
    tip_5 = "Χρησιμοποίησε τους πόρους πιο σωστά"

    rendered_lreason_5 = font.render(lreason_5, True, (255, 255, 255))
    rendered_tip_5_rect = pygame.Rect((0, 0), (700, 50))
    rendered_tip_5 = font.render(tip_5, True, (255, 255, 255))

    wrapped_tip_5 = render_text_rect(tip_5, font, rendered_tip_5_rect, (255, 255, 255), (BLACK), wrap=True)

    # Draw the Retry section button
    retry_button_width = 150
    retry_button_height = 50
    retry_button_x = 450
    retry_button_y = 500
    retry_text = font2.render("Retry", True, WHITE)
    retry_text_rect = retry_text.get_rect(  # Corrected this line
        center=(retry_button_x + retry_button_width // 2, retry_button_y + retry_button_height // 2))

    # Draw the Tip section button
    tip_button_width = 80
    tip_button_height = 50
    tip_button_x = 800
    tip_button_y = 100
    tip_text = font2.render("Tip", True, WHITE)
    tip_text_rect = tip_text.get_rect(
        center=(tip_button_x + tip_button_width // 2, tip_button_y + tip_button_height // 2))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if player_budget < 0:
                screen.fill(BLUE3)
                screen.blit(rendered_lreason_5, (80, screen_height // 2))
                pygame.draw.rect(screen, GRAY,
                                 (retry_button_x, retry_button_y, retry_button_width, retry_button_height))
                screen.blit(retry_text, retry_text_rect)
                pygame.draw.rect(screen, GRAY,
                                 (tip_button_x, tip_button_y, tip_button_width, tip_button_height))
                screen.blit(tip_text, tip_text_rect)
                pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if retry_text_rect.collidepoint(mouse_x, mouse_y):
                        combined_start_function()
                    elif tip_text_rect.collidepoint(mouse_x, mouse_y):
                        transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                        pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                        transparent_surface.blit(wrapped_tip_5, (0, 10))
                        screen.blit(transparent_surface, (100, 200))
                        pygame.display.update()
            else:
                return


# Creating Q Parameters
Q = {}
T = {}
T[pipe_section] = []
Q2 = {}
T2 = {}
Starting_Q = 0
Starting_T = T0[dataset]
number_of_items = 0
player_budget = 3000
tip_button_box = False
# Starting_Q= float(input(f"Q{pipe_section}:"))
# print(Q[0])
# wait = input("666")

# Main game loop
clock = pygame.time.Clock()
combined_start_function()
# Clear the screen
running = True
placed_new_item = False  # Flag to track if a new item is placed
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not dropdown_open:
            # Check if the button to reset the grid is clicked
            if button_x <= event.pos[0] <= button_x + button_width and button_y <= event.pos[
                1] <= button_y + button_height:
                reset_grid()
                initialize_grid()
            # Check if the button to undo is clicked
            elif undo_button_x <= event.pos[0] <= undo_button_x + button_width and undo_button_y <= event.pos[
                1] <= undo_button_y + button_height:
                undo()
                # Check if the Tip button is clicked
            elif button_x + 110 <= event.pos[0] <= button_x + 110 + button_width and button_y <= event.pos[
                1] <= button_y + button_height:
                transparent_width = 330
                transparent_height = 250
                tip_button_box = not tip_button_box
                info_text1 = "How to use triplets."
                info_text2 = "If you want to combine or split Q use these icons icons"
                info_text3 = "Be careful."
                info_text4 = "To split 1 Q set it up like this, 1 should split to 2"
                info_text5 = "To combine 2 Qs they must be seet up like this, 2 come and add to 1"
                font = pygame.font.Font(info_font, 10)
                font2 = pygame.font.Font(info_font, 16)
                transparent_surface = pygame.Surface((transparent_width, transparent_height), pygame.SRCALPHA)
                pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                text1 = font2.render(info_text1, True, WHITE)
                text2 = font.render(info_text2, True, WHITE)
                text3 = font2.render(info_text3, True, WHITE)
                text4 = font.render(info_text4, True, WHITE)
                text5 = font.render(info_text5, True, WHITE)
                text_rect1 = text1.get_rect(center=(transparent_width / 2, 20))
                text_rect2 = text2.get_rect(center=(transparent_width / 2, 50))
                text_rect3 = text3.get_rect(center=(transparent_width / 2, 120))
                text_rect4 = text4.get_rect(center=(transparent_width / 2, 150))
                text_rect5 = text5.get_rect(center=(transparent_width / 2, 200))

                icon1 = pygame.transform.scale(icons[6], (25, 25))
                icon2 = pygame.transform.scale(icons[7], (25, 25))
                icon3 = pygame.transform.scale(icons[8], (25, 25))
                icon4 = pygame.transform.scale(icons[9], (25, 25))

                if tip_button_box == True:
                    transparent_surface.blit(text1, (text_rect1))
                    transparent_surface.blit(text2, (text_rect2))
                    transparent_surface.blit(text3, (text_rect3))
                    transparent_surface.blit(text4, (text_rect4))
                    transparent_surface.blit(text5, (text_rect5))
                    transparent_surface.blit(icon1, (160 - 50, 70))
                    transparent_surface.blit(icon2, (190 - 50, 70))
                    transparent_surface.blit(icon3, (220 - 50, 70))
                    transparent_surface.blit(icon4, (250 - 50, 70))

                    screen.blit(transparent_surface, (650, 400))

                    pygame.display.update()
                elif tip_button_box == False:
                    pygame.draw.rect(screen, BLUE, (650, 400, 100, 250))
                    render_q2_dictionary(Q2)
                    render_T_start_dic(T, screen)
                    render_T_end_dic(T, screen)
                "lines for correction"  # Decide what the pipe_section_button is going to do OR will it be removed

            if 64 <= event.pos[0] <= 544 + 64 and 64 <= event.pos[1] <= 544 + 64:  # The pixel "space" of the grid
                row = (event.pos[1] - square_y) // square_size
                col = (event.pos[0] - square_x) // square_size
                available_icons, connection_type = get_available_icons(row, col)
                print("connection_type", connection_type)
                print('out', available_icons)
                print('out2', len(available_icons))
                if 0 <= row < grid_size and 0 <= col < grid_size and (
                        (row + 1 < grid_size and (
                                (placement_grid[row + 1][col] == 11 and 0 <= placement_grid[row + 2][col] <= 10) or (
                                0 <= placement_grid[row + 1][col] <= 10))) or
                        (row - 1 >= 0 and (
                                (placement_grid[row - 1][col] == 11 and 0 <= placement_grid[row - 2][col] <= 10) or (
                                0 <= placement_grid[row - 1][col] <= 10))) or
                        (col - 1 >= 0 and (
                                (placement_grid[row][col - 1] == 11 and 0 <= placement_grid[row][col - 2] <= 10) or (
                                0 <= placement_grid[row][col - 1] <= 10))) or
                        (col + 1 < grid_size and (
                                (placement_grid[row][col + 1] == 11 and 0 <= placement_grid[row][col + 2] <= 10) or (
                                0 <= placement_grid[row][col + 1] <= 10)))
                ):
                    if placement_grid[row][col] == -1:
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

                if dropdown_open == True and placed_new_item == False and 0 <= icon_index <= 5 and \
                        T_grid[pw_row[dataset] - 1][pw_col[dataset]] != 0:
                    if pipe_section_grid[row][col] == 0:
                        things_around = 0
                        # i: 0=left, 1=up, 2=right, 3=down
                        for i in range(0, 4):
                            tx = (i + 2) % 4
                            print(tx)
                            if i == 0:  # ti icon type exei to row-1
                                ty = placement_grid[row][col - 1]
                                trow = row
                                tcol = col - 1
                                # print(ty)
                                ty_1 = ty
                                if ty_1 > -1 and conn[i][icon_index] * conn[tx][ty] > 0:
                                    things_around += 1
                            elif i == 1:
                                ty = placement_grid[row - 1][col]
                                trow = row - 1
                                tcol = col
                                # print(ty)
                                ty_2 = ty
                                if ty_2 > -1 and conn[i][icon_index] * conn[tx][ty] > 0:
                                    things_around += 1
                            elif i == 2:
                                ty = placement_grid[row][col + 1]
                                trow = row
                                tcol = col + 1
                                # print(ty)
                                ty_3 = ty
                                if ty_3 > -1 and conn[i][icon_index] * conn[tx][ty] > 0:
                                    things_around += 1
                            elif i == 3:
                                ty = placement_grid[row + 1][col]
                                trow = row + 1
                                tcol = col
                                # print(ty)
                                ty_4 = ty
                                if ty_4 > -1 and conn[i][icon_index] * conn[tx][ty] > 0:
                                    things_around += 1
                            if ty == -1: conn[tx][ty] = 0
                            if conn[i][icon_index] * conn[tx][ty] > 0 and things_around <= 1 and \
                                    placement_grid[row - 1][col] <= 9:
                                pipe_section_grid[row][col] = pipe_section_grid[trow][tcol]
                                # print(T[pipe_section_grid[row][col]][-1])
                                # wait = input("here")
                                T_val = T[pipe_section_grid[row][col]][-1] - Tloss_pipe[dataset]
                                T[pipe_section_grid[row][col]] = np.append(T[pipe_section_grid[row][col]],
                                                                           T_val)  # Append the new value
                                # T[pipe_section_grid[row][col]] -= Tloss_pipe
                                T_grid[row][col] = T[pipe_section_grid[row][col]][-1]
                                print(T[pipe_section_grid[row][col]])
                            if conn[i][icon_index] * conn[tx][ty] > 0 and things_around <= 1 and \
                                    placement_grid[row - 1][col] > 9:
                                pipe_section += 1
                                pipe_section_grid[row][col] = pipe_section
                                Q[pipe_section_grid[row][col]] = Q_grid[row - 1][col]
                                T[pipe_section_grid[row][col]] = [(min(T_grid[row - 1][col]) - Tloss_pipe[dataset])]
                                # T[pipe_section_grid[row][col]] = min(T_grid[row - 1][col])
                                T_grid[row][col] = T[pipe_section_grid[row][col]]

                            if conn[i][icon_index] * conn[tx][ty] > 0 and things_around > 1:
                                pipe_section_grid[row][col] = pipe_section_grid[row - 1][
                                    col]  # min(element for element in[pipe_section_grid[row][col - 1],pipe_section_grid[row - 1][col], pipe_section_grid[row][col + 1], pipe_section_grid[row + 1][col]] if element > 0)
                                Q_grid[row][col] = Q[pipe_section_grid[row][col]]
                                # T[pipe_section_grid[row][col]] -= Tloss_pipe
                                # sygrinw tin timi eisodou toy house me tin ypologismeni T_grid[row][col]
                                # Q_grid[row + 1][col] = Q_grid[row][col]
                        Q_grid[row][col] = Q[pipe_section_grid[row][col]]
                        # T_grid[row][col] = T[pipe_section_grid[row][col]][-1] - Tloss_pipe
                    elif pipe_section_grid[row][col] != 0 and Q_grid[row][col] != 0:
                        Q_grid[row][col] = Q[pipe_section_grid[row][col]]
                        T_grid[row][col] = float(T[pipe_section_grid[row][col]] - Tloss_pipe[dataset])
                        T[pipe_section_grid[row][col]] -= Tloss_pipe[dataset]
                        # T[pipe_section_grid[row][col]][-1] -= Tloss_pipe
                        print("I was here")
                    else:
                        Q_grid[row][col] = Q[pipe_section_grid[row][col]]
                        T_grid[row][col] = T[pipe_section_grid[row][col]][-1] - Tloss_pipe[dataset]

                if dropdown_open == True and placed_new_item == False and 0 <= icon_index <= 5 and \
                        T_grid[pw_row[dataset] - 1][pw_col[dataset]] == 0:
                    Q_grid[row][col] = Starting_Q
                    T_grid[row + 1][col] = Starting_T
                    T_grid[row][col] = float(Starting_T - Tloss_pipe[dataset])
                    T[pipe_section] = [T_grid[row][col]]
                    Q[pipe_section] = Q_grid[row][col]
                    print(Q[pipe_section])

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
                                T[pipe_section] = [T[pipe_section_grid[row + 1][col]][-1] - Tloss_pipe[dataset]]
                                T[pipe_section_grid[row][col - 1]] = T[pipe_section]

                                pipe_section += 1
                                right_arrow_appears()  # Right arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row][col + 1] = Q[pipe_section]
                                pipe_section_grid[row][col + 1] = pipe_section
                                T[pipe_section] = [T[pipe_section_grid[row + 1][col]][-1] - Tloss_pipe[dataset]]
                                T[pipe_section_grid[row][col + 1]] = T[pipe_section]

                                #T of the triplet
                                T_grid[row][col] = float(T[pipe_section_grid[row + 1][col]][-1] - Tloss_pipe[dataset])

                            elif placement_grid[row][col - 1] != -1:
                                pipe_section += 1
                                right_arrow_appears()  # Right arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row][col + 1] = Q[pipe_section]
                                pipe_section_grid[row][col + 1] = pipe_section
                                T[pipe_section] = [T[pipe_section_grid[row][col - 1]][-1] - Tloss_pipe[dataset]]
                                T[pipe_section_grid[row][col + 1]] = T[pipe_section]

                                pipe_section += 1
                                down_arrow_appears()  # Down arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row + 1][col] = Q[pipe_section]
                                pipe_section_grid[row + 1][col] = pipe_section
                                T[pipe_section] = [T[pipe_section_grid[row][col - 1]][-1] - Tloss_pipe[dataset]]
                                T[pipe_section_grid[row + 1][col]] = T[pipe_section]

                                #T of the triplet
                                T_grid[row][col] = float(T[pipe_section_grid[row][col - 1]][-1] - Tloss_pipe[dataset])

                            elif placement_grid[row][col + 1] != -1:
                                pipe_section += 1
                                left_arrow_appears()  # Left arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row][col - 1] = Q[pipe_section]
                                pipe_section_grid[row][col - 1] = pipe_section
                                T[pipe_section] = [T[pipe_section_grid[row][col + 1]][-1] - Tloss_pipe[dataset]]
                                T[pipe_section_grid[row][col - 1]] = T[pipe_section]

                                pipe_section += 1
                                down_arrow_appears()  # Down arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row + 1][col] = Q[pipe_section]
                                pipe_section_grid[row + 1][col] = pipe_section
                                T[pipe_section] = [T[pipe_section_grid[row][col + 1]][-1] - Tloss_pipe[dataset]]
                                T[pipe_section_grid[row + 1][col]] = T[pipe_section]

                                # T of the triplet
                                T_grid[row][col] = float(T[pipe_section_grid[row][col + 1]][-1] - Tloss_pipe[dataset])

                            Q_grid[row][col] = Q[min(pipe_section_grid[row + 1][col], pipe_section_grid[row][col - 1],
                                                     pipe_section_grid[row][col + 1])]
                            pipe_section_grid[row][col] = -icon_index
                            if Q_grid[row][col] != (Q[pipe_section - 1] + Q[pipe_section]) or (
                                    Q[pipe_section - 1] == 0 or Q[pipe_section] == 0):
                                print(
                                    f"You have made a mistake. Please enter Q{pipe_section - 1} and Q{pipe_section} properly")
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
                                left_arrow_appears()  # Left arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row][col - 1] = Q[pipe_section]
                                pipe_section_grid[row][col - 1] = pipe_section
                                T[pipe_section] = [T[pipe_section - 1][-1] - Tloss_pipe[dataset]]

                                pipe_section += 1
                                down_arrow_appears()  # Down arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row + 1][col] = Q[pipe_section]
                                pipe_section_grid[row + 1][col] = pipe_section
                                T[pipe_section] = [T[pipe_section - 2][-1] - Tloss_pipe[dataset]]

                            elif placement_grid[row][col - 1] != -1:
                                pipe_section += 1
                                up_arrow_appears()  # Up arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row - 1][col] = Q[pipe_section]
                                pipe_section_grid[row - 1][col] = pipe_section
                                T[pipe_section] = [T[pipe_section - 1][-1] - Tloss_pipe[dataset]]

                                pipe_section += 1
                                down_arrow_appears()  # Down arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row + 1][col] = Q[pipe_section]
                                pipe_section_grid[row + 1][col] = pipe_section
                                T[pipe_section] = [T[pipe_section - 2][-1] - Tloss_pipe[dataset]]

                            elif placement_grid[row + 1][col] != -1:
                                pipe_section += 1
                                left_arrow_appears()  # Left arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row - 1][col] = Q[pipe_section]
                                pipe_section_grid[row - 1][col] = pipe_section
                                T[pipe_section] = [T[pipe_section - 1][-1] - Tloss_pipe[dataset]]

                                pipe_section += 1
                                up_arrow_appears()  # Up arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                Q[pipe_section] = q
                                Q_grid[row - 1][col] = Q[pipe_section]
                                pipe_section_grid[row - 1][col] = pipe_section
                                T[pipe_section] = [T[pipe_section - 2][-1] - Tloss_pipe[dataset]]

                            Q_grid[row][col] = Q[min(pipe_section_grid[row - 1][col], pipe_section_grid[row][col - 1],
                                                     pipe_section_grid[row + 1][col])]
                            pipe_section_grid[row][col] = -icon_index
                            T_grid[row][col] = float(T[pipe_section - 2][-1] - Tloss_pipe[dataset])
                            if Q_grid[row][col] != (Q[pipe_section - 1] + Q[pipe_section]) or (
                                    Q[pipe_section - 1] == 0 or Q[pipe_section] == 0):
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
                                T[pipe_section] = [T[pipe_section - 1][-1] - Tloss_pipe[dataset]]

                                pipe_section += 1
                                right_arrow_appears()  # Right arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row][col + 1] = Q[pipe_section]
                                pipe_section_grid[row][col + 1] = pipe_section
                                T[pipe_section] = [T[pipe_section - 2][-1] - Tloss_pipe[dataset]]

                            elif placement_grid[row][col - 1] != -1:
                                pipe_section += 1
                                up_arrow_appears()  # Up arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row - 1][col] = Q[pipe_section]
                                pipe_section_grid[row - 1][col] = pipe_section
                                T[pipe_section] = [T[pipe_section - 1][-1] - Tloss_pipe[dataset]]

                                pipe_section += 1
                                right_arrow_appears()  # Right arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row][col + 1] = Q[pipe_section]
                                pipe_section_grid[row][col + 1] = pipe_section
                                T[pipe_section] = [T[pipe_section - 2][-1] - Tloss_pipe[dataset]]

                            elif placement_grid[row][col + 1] != -1:
                                pipe_section += 1
                                left_arrow_appears()  # Left arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row][col - 1] = Q[pipe_section]
                                pipe_section_grid[row][col - 1] = pipe_section
                                T[pipe_section] = [T[pipe_section - 1][-1] - Tloss_pipe[dataset]]

                                pipe_section += 1
                                up_arrow_appears()  # Down arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row - 1][col] = Q[pipe_section]
                                pipe_section_grid[row - 1][col] = pipe_section
                                T[pipe_section] = [T[pipe_section - 2][-1] - Tloss_pipe[dataset]]

                            Q_grid[row][col] = Q[min(pipe_section_grid[row - 1][col], pipe_section_grid[row][col - 1],
                                                     pipe_section_grid[row][col + 1])]
                            pipe_section_grid[row][col] = -icon_index
                            T_grid[row][col] = float(T[pipe_section - 2][-1] - Tloss_pipe[dataset])
                            if Q_grid[row][col] != (Q[pipe_section - 1] + Q[pipe_section]) or (
                                    Q[pipe_section - 1] == 0 or Q[pipe_section] == 0):
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
                                T[pipe_section] = [T[pipe_section - 1][-1] - Tloss_pipe[dataset]]

                                pipe_section += 1
                                down_arrow_appears()  # Down arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row + 1][col] = Q[pipe_section]
                                pipe_section_grid[row + 1][col] = pipe_section
                                T[pipe_section] = [T[pipe_section - 2][-1] - Tloss_pipe[dataset]]

                            elif placement_grid[row][col + 1] != -1:
                                pipe_section += 1
                                up_arrow_appears()  # Up arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row - 1][col] = Q[pipe_section]
                                pipe_section_grid[row - 1][col] = pipe_section
                                T[pipe_section] = [T[pipe_section - 1][-1] - Tloss_pipe[dataset]]

                                pipe_section += 1
                                down_arrow_appears()  # Down arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row + 1][col] = Q[pipe_section]
                                pipe_section_grid[row + 1][col] = pipe_section
                                T[pipe_section] = [T[pipe_section - 2][-1] - Tloss_pipe[dataset]]

                            elif placement_grid[row + 1][col] != -1:
                                pipe_section += 1
                                up_arrow_appears()  # Up arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row - 1][col] = Q[pipe_section]
                                pipe_section_grid[row - 1][col] = pipe_section
                                T[pipe_section] = [T[pipe_section - 1][-1] - Tloss_pipe[dataset]]

                                pipe_section += 1
                                right_arrow_appears()  # Right arrow appears
                                q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                q = int(q)
                                covering_the_arrow(screen)
                                Q[pipe_section] = q
                                Q_grid[row][col + 1] = Q[pipe_section]
                                pipe_section_grid[row][col + 1] = pipe_section
                                T[pipe_section] = [T[pipe_section - 2][-1] - Tloss_pipe[dataset]]

                            Q_grid[row][col] = Q[min(pipe_section_grid[row - 1][col], pipe_section_grid[row][col + 1],
                                                     pipe_section_grid[row + 1][col])]
                            pipe_section_grid[row][col] = -icon_index
                            T_grid[row][col] = float(T[pipe_section - 2][-1] - Tloss_pipe[dataset])
                            if Q_grid[row][col] != (Q[pipe_section - 1] + Q[pipe_section]) or (
                                    Q[pipe_section - 1] == 0 or Q[pipe_section] == 0):
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
                        T[pipe_section_grid[row][col + 1]] = [round(float((np.array(Q_grid[row + 1][col]) * T_grid[row + 1][col] +
                                                                           Q_grid[row][col - 1] * T_grid[row][
                                                                               col - 1]) / (
                                                                                  Q_grid[row + 1][col] + Q_grid[row][
                                                                              col - 1]) - Tloss_pipe[dataset]), 1)]
                        T_grid[row][col] = T[pipe_section_grid[row][col + 1]]
                    if placement_grid[row + 1][col] != -1 and placement_grid[row][col + 1] != -1:
                        Q_grid[row][col - 1] = Q_grid[row + 1][col] + Q_grid[row][col + 1]
                        pipe_section_grid[row][col - 1] = pipe_section
                        Q[pipe_section] = Q_grid[row][col - 1]
                        Q_grid[row][col] = Q_grid[row + 1][col] + Q_grid[row][col + 1]
                        T[pipe_section_grid[row][col - 1]] = [round(float((np.array(Q_grid[row + 1][col]) * T_grid[row + 1][col] +
                                                                           Q_grid[row][col + 1] * T_grid[row][
                                                                               col + 1]) / (
                                                                                  Q_grid[row + 1][col] + Q_grid[row][
                                                                              col + 1]) - Tloss_pipe[dataset]), 1)]
                        T_grid[row][col] = T[pipe_section_grid[row][col - 1]]
                    if placement_grid[row][col - 1] != -1 and placement_grid[row][col + 1] != -1:
                        Q_grid[row + 1][col] = Q_grid[row][col - 1] + Q_grid[row][col + 1]
                        pipe_section_grid[row + 1][col] = pipe_section
                        Q[pipe_section] = Q_grid[row + 1][col]
                        Q_grid[row][col] = Q_grid[row][col - 1] + Q_grid[row][col + 1]
                        T[pipe_section_grid[row + 1][col]] = [round(float((np.array(Q_grid[row][col - 1]) * T_grid[row][col - 1] +
                                                                           Q_grid[row][col + 1] * T_grid[row][
                                                                               col + 1]) / (
                                                                                  Q_grid[row][col - 1] + Q_grid[row][
                                                                              col + 1]) - Tloss_pipe[dataset]), 1)]
                        T_grid[row][col] = T[pipe_section_grid[row + 1][col]]
                    pipe_section_grid[row][col] = -icon_index
                elif dropdown_open == True and placed_new_item == False and icon_index == 7 and connection_type == 2:
                    pipe_section += 1
                    if placement_grid[row + 1][col] != -1 and placement_grid[row][col - 1] != -1:
                        Q_grid[row - 1][col] = Q_grid[row + 1][col] + Q_grid[row][col - 1]
                        pipe_section_grid[row - 1][col] = pipe_section
                        Q[pipe_section] = Q_grid[row - 1][col]
                        Q_grid[row][col] = Q_grid[row + 1][col] + Q_grid[row][col - 1]
                        T[pipe_section_grid[row - 1][col]] = [round(float((np.array(Q_grid[row + 1][col]) * T_grid[row + 1][col] +
                                                                           Q_grid[row][col - 1] * T_grid[row][
                                                                               col - 1]) / (
                                                                                  Q_grid[row + 1][col] + Q_grid[row][
                                                                              col - 1]) - Tloss_pipe[dataset]), 1)]
                        T_grid[row][col] = T[pipe_section_grid[row - 1][col]]
                    if placement_grid[row + 1][col] != -1 and placement_grid[row - 1][col] != -1:
                        Q_grid[row][col - 1] = Q_grid[row + 1][col] + Q_grid[row - 1][col]
                        pipe_section_grid[row][col - 1] = pipe_section
                        Q[pipe_section] = Q_grid[row][col - 1]
                        Q_grid[row][col] = Q_grid[row + 1][col] + Q_grid[row - 1][col]
                        T[pipe_section_grid[row][col - 1]] = [round(float((np.array(Q_grid[row + 1][col]) * T_grid[row + 1][col] +
                                                                           Q_grid[row - 1][col] * T_grid[row - 1][
                                                                               col]) / (
                                                                                  Q_grid[row + 1][col] +
                                                                                  Q_grid[row - 1][
                                                                                      col]) - Tloss_pipe[dataset]), 1)]
                        T_grid[row][col] = T[pipe_section_grid[row][col - 1]]
                    if placement_grid[row][col - 1] != -1 and placement_grid[row - 1][col] != -1:
                        Q_grid[row + 1][col] = Q_grid[row][col - 1] + Q_grid[row - 1][col]
                        pipe_section_grid[row + 1][col] = pipe_section
                        Q[pipe_section] = Q_grid[row + 1][col]
                        Q_grid[row][col] = Q_grid[row][col - 1] + Q_grid[row - 1][col]
                        T[pipe_section_grid[row + 1][col]] = [round(float((np.array(Q_grid[row][col - 1]) * T_grid[row][col - 1] +
                                                                           Q_grid[row - 1][col] * T_grid[row - 1][
                                                                               col]) / (
                                                                                  Q_grid[row][col - 1] +
                                                                                  Q_grid[row - 1][
                                                                                      col]) - Tloss_pipe[dataset]), 1)]
                        T_grid[row][col] = T[pipe_section_grid[row + 1][col]]
                    pipe_section_grid[row][col] = -icon_index
                elif dropdown_open == True and placed_new_item == False and icon_index == 8 and connection_type == 2:
                    pipe_section += 1
                    if placement_grid[row - 1][col] != -1 and placement_grid[row][col - 1] != -1:
                        Q_grid[row][col + 1] = Q_grid[row - 1][col] + Q_grid[row][col - 1]
                        pipe_section_grid[row][col + 1] = pipe_section
                        Q[pipe_section] = Q_grid[row][col + 1]
                        Q_grid[row][col] = Q_grid[row - 1][col] + Q_grid[row][col - 1]
                        T[pipe_section_grid[row][col + 1]] = [round(float((np.array(Q_grid[row - 1][col]) * T_grid[row - 1][col] +
                                                                           Q_grid[row][col - 1] * T_grid[row][
                                                                               col - 1]) / (
                                                                                  Q_grid[row - 1][col] + Q_grid[row][
                                                                              col - 1]) - Tloss_pipe[dataset]), 1)]
                        T_grid[row][col] = T[pipe_section_grid[row][col + 1]]
                    if placement_grid[row - 1][col] != -1 and placement_grid[row][col + 1] != -1:
                        Q_grid[row][col - 1] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                        pipe_section_grid[row][col - 1] = pipe_section
                        Q[pipe_section] = Q_grid[row][col - 1]
                        Q_grid[row][col] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                        T[pipe_section_grid[row][col - 1]] = [round(float((np.array(Q_grid[row - 1][col]) * T_grid[row - 1][col] +
                                    Q_grid[row][col + 1] * T_grid[row][col + 1]) / (Q_grid[row - 1][col] + Q_grid[row][col + 1]) - Tloss_pipe[dataset]), 1)]
                        T_grid[row][col] = T[pipe_section_grid[row][col - 1]]
                    if placement_grid[row][col - 1] != -1 and placement_grid[row][col + 1] != -1:
                        Q_grid[row - 1][col] = Q_grid[row][col - 1] + placement_grid[row][col + 1]
                        pipe_section_grid[row - 1][col] = pipe_section
                        Q[pipe_section] = Q_grid[row - 1][col]
                        Q_grid[row][col] = Q_grid[row][col - 1] + placement_grid[row][col + 1]
                        T[pipe_section_grid[row - 1][col]] = [round(float((np.array(Q_grid[row][col - 1]) * T_grid[row][col - 1] +
                                                                           Q_grid[row][col + 1] * T_grid[row][
                                                                               col + 1]) / (
                                                                                  Q_grid[row][col - 1] + Q_grid[row][
                                                                              col + 1]) - Tloss_pipe[dataset]), 1)]
                        T_grid[row][col] = T[pipe_section_grid[row - 1][col]]
                    pipe_section_grid[row][col] = -icon_index
                elif dropdown_open == True and placed_new_item == False and icon_index == 9 and connection_type == 2:
                    pipe_section += 1
                    if placement_grid[row + 1][col] != -1 and placement_grid[row][col + 1] != -1:
                        Q_grid[row - 1][col] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                        pipe_section_grid[row - 1][col] = pipe_section
                        Q[pipe_section] = Q_grid[row - 1][col]
                        Q_grid[row][col] = Q_grid[row + 1][col] + Q_grid[row][col + 1]
                        T[pipe_section_grid[row - 1][col]] = [round(float(np.array((Q_grid[row + 1][col]) * T_grid[row + 1][col] +
                                                                           Q_grid[row][col + 1] * T_grid[row][
                                                                               col + 1]) / (
                                                                                  Q_grid[row + 1][col] + Q_grid[row][
                                                                              col + 1]) - Tloss_pipe[dataset]), 1)]
                        T_grid[row][col] = T[pipe_section_grid[row - 1][col]]
                    if placement_grid[row - 1][col] != -1 and placement_grid[row][col + 1] != -1:
                        Q_grid[row + 1][col] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                        pipe_section_grid[row + 1][col] = pipe_section
                        Q[pipe_section] = Q_grid[row + 1][col]
                        Q_grid[row][col] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                        T[pipe_section_grid[row + 1][col]] = [round(float((np.array(Q_grid[row - 1][col]) * T_grid[row - 1][col] +
                                                                           Q_grid[row][col + 1] * T_grid[row][
                                                                               col + 1]) / (
                                                                                  Q_grid[row - 1][col] + Q_grid[row][
                                                                              col + 1]) - Tloss_pipe[dataset]), 1)]
                        T_grid[row][col] = T[pipe_section_grid[row + 1][col]]
                    if placement_grid[row - 1][col] != -1 and placement_grid[row + 1][col] != -1:
                        Q_grid[row][col + 1] = Q_grid[row - 1][col] + Q_grid[row + 1][col]
                        pipe_section_grid[row][col + 1] = pipe_section
                        Q[pipe_section] = Q_grid[row][col + 1]
                        Q_grid[row][col] = Q_grid[row - 1][col] + Q_grid[row + 1][col]
                        T[pipe_section_grid[row][col + 1]] = [round(float((np.array(Q_grid[row + 1][col]) * T_grid[row + 1][col] +
                                                                           Q_grid[row - 1][col] * T_grid[row - 1][
                                                                               col]) / (
                                                                                  Q_grid[row + 1][col] +
                                                                                  Q_grid[row - 1][
                                                                                      col]) - Tloss_pipe[dataset]), 1)]
                        T_grid[row][col] = T[pipe_section_grid[row][col + 1]]
                    pipe_section_grid[row][col] = -icon_index
                dropdown_open = False
                number_of_items += 1
                # Add the placed icon to the undo stack
                undo_stack.append((row, col))
                placed_new_item = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and not dropdown_open:
            row = (event.pos[1] - square_y) // square_size
            col = (event.pos[0] - square_x) // square_size
            right_click_grid_cell_info(event, row, col)
        elif player_budget < 0:
            game_over_budget()
        # Arrange the pipe_section_grid properly
        info_ghouse_blue_square()
        if house0_row[dataset] > 0: pipe_section_grid_for_icon_house0()
        if house1_row[dataset] > 0: pipe_section_grid_for_icon_house1()
        if house2_row[dataset] > 0: pipe_section_grid_for_icon_house2()
        if greenhouse0_row[dataset] > 0: pipe_section_grid_for_icon_greenhouse0()
        if greenhouse1_row[dataset] > 0: pipe_section_grid_for_icon_greenhouse1()

        budget_calculator()
        draw_buttons(screen, button_x, button_y, button_width, button_height, undo_button_x, undo_button_y)
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

    icon_index = 100

    # if rw_row[dataset] > 0:

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
        Q2 = {'Q' + str(key + 1): value for key, value in Q.items()}
        print(Q2)
        for key, values_list in T.items():
            print(T)
        print(Starting_Q)
        render_q2_dictionary(Q2)
        render_T_start_dic(T, screen)
        render_T_end_dic(T, screen)
        print(username)
    # Limit the frame rate to reduce blinking
    clock.tick(60)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
