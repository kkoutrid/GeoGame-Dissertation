import pygame
import sys
import os
import numpy as np  # Numeric functions and arrays
import pandas as pd
import datetime
from collections import Counter
import copy
import textwrap
import webbrowser
from openpyxl import load_workbook
import math
import time

"""where i left off is where to continue from"""
# IMPORTANT part of the code that need fixing are found using the search "lines for correction"

# Set the position of the Pygame window
os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'

# Initialize Pygame
pygame.init()

# Settings for the opening/loading screen

display_info = pygame.display.Info()
#Settings for game screen scaling
'''playerscreen_width = display_info.current_w
playerscreen_height = display_info.current_h
scale_variable = 0.7'''

"""Σημείωσεις για προσθήκες εκτός των bugs με σειρά προτεραιότητας
    - Αγγλικές οδηγίες μετά από αποτυχημένη προσπάθεια DONE!!!!!
    - Να φτιάξω το Tutorial DONE!!!
    - Αν μπορώ ακόμα περισσότερα level και προβλήματα (ΝΑ ΚΑΝΩ ΤΟ 8 ΜΕ ΣΠΙΤΙ ΑΝΤΙ ΓΙΑ ΘΕΡΜΟΚΗΠΕΙΟ)
    - Exam Mode με χρονικό περιορισμό λειτουργίας PENDING
    - Αλλαγή των διαστάσεων ανάλογα με το μέγεθος την οθόνης NOT NOW
    """

#print(f"Detected screen resolution: {playerscreen_width}x{playerscreen_height}")

opening_screen_width = 610
opening_screen_height = 200

# Create the Pygame window with specific settings
screen = pygame.display.set_mode(
    (opening_screen_width, opening_screen_height),
    pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SRCALPHA | pygame.NOFRAME)

# Load image
icon_loading_screen_path = os.path.join("GameAssets", "icons", "icon_loading_screen.png")
icon_loading_screen = pygame.image.load(icon_loading_screen_path).convert_alpha()

# Adjust position of the loading screen
loading_screen_rect = icon_loading_screen.get_rect(center=(opening_screen_width // 2, opening_screen_height // 2))

# Blit the transparent image onto the screen
screen.blit(icon_loading_screen, loading_screen_rect)

# Update the display
pygame.display.flip()


class Button:
    def __init__(self, x, y, width, height, text, color=(128, 128, 128), text_color=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)  # You can adjust the font size here

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = self.rect.center
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class IconButton:
    def __init__(self, x, y, width, height, icon, icon_size=(32, 32), color=(128, 128, 128)):
        self.rect = pygame.Rect(x, y, width, height)
        self.icon = icon
        self.icon_size = icon_size
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

        if self.icon:
            icon_surface = pygame.transform.scale(self.icon, self.icon_size)
            icon_rect = icon_surface.get_rect()
            icon_rect.center = self.rect.center
            screen.blit(icon_surface, icon_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


root_dir = os.path.dirname(os.path.abspath(__file__))

'read input data'
# idata = pd.read_excel(r"C:\\Diplomatikh\diplomatikh\2023-07-09(UPDATED)\geodata.xlsx", sheet_name="na_icons")  # kostas pc
# idata = pd.read_excel(r"C:\Users\User\.spyder-py3\geodata.xlsx",  sheet_name="na_icons") #yiannis pc
idata = pd.read_excel(root_dir + "\GameAssets\geodata.xlsx", sheet_name="na_icons")
na_icons_L = idata['left'].to_numpy()
na_icons_R = idata['right'].to_numpy()
na_icons_U = idata['up'].to_numpy()
na_icons_D = idata['down'].to_numpy()
na_icons0 = np.concatenate((na_icons_L, na_icons_R, na_icons_U, na_icons_D))
na_icons = np.reshape(na_icons0, (4, 13))
idata = pd.read_excel(root_dir + "\GameAssets\geodata.xlsx", sheet_name="pipe_connections")
conn_L = idata['left'].to_numpy()
conn_U = idata['up'].to_numpy()
conn_R = idata['right'].to_numpy()
conn_D = idata['down'].to_numpy()
conn0 = np.concatenate((conn_L, conn_U, conn_R, conn_D))
conn = np.reshape(conn0, (4, 13))
# conn[x][y] simainei x=0,1,2,3 left, up, right, down kai y = icon index
idata = pd.read_excel(root_dir + "\GameAssets\geodata.xlsx", sheet_name="info")
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
aux_cost = idata['aux_cost'].to_numpy().astype(float)
player_budget = idata['player_budget'].to_numpy().astype(float)
completed_level = idata['completed_level'].to_numpy().astype
high_score = idata['high_score'].to_numpy().astype
extraction_cost = idata['extraction_cost'].to_numpy().astype(float)

# Grid dimensions
grid_size = 18
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
GREEN = (46, 147, 60)

# Create the screen
# pygame.NOFRAME makes the window bar disappear
# pygame.FULLSCREEN makes the fame run at FULLSCREEN

# screen_width = 1005
# screen_height = 750
# screen = pygame.display.set_mode((screen_width, screen_height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SRCALPHA)


# pygame.display.set_caption("Geogame")
# Load the sounds
# click_sound = pygame.mixer.Sound("C:\Diplomatikh\diplomatikh\\2023-07-09(UPDATED)\SoundEffects\MouseClick.wav")
# enter_input_sound = pygame.mixer.Sound("C:\Diplomatikh\diplomatikh\\2023-07-09(UPDATED)\SoundEffects\EnterInputSound.wav") #kostas
# enter_input_sound = pygame.mixer.Sound("C:\Diplomatikh\diplomatikh\\2023-07-09(UPDATED)\SoundEffects\EnterInputSound.wav") #yiannis
# enter_input_sound = pygame.mixer.Sound(root_dir + "\GameAssets\SoundEffects\EnterInputSound.wav")
try:
    enter_input_sound = pygame.mixer.Sound(root_dir + "\GameAssets\SoundEffects\EnterInputSound.wav")
except pygame.error:
    enter_input_sound = None  # Assign None if the sound cannot be loaded
# Volume Management
# click_sound.set_volume(0.3)
# enter_input_sound.set_volume(0.0)  # volume
if enter_input_sound is not None:
    enter_input_sound.set_volume(0.0)  # volume
# Load the icons
icon_dir = "GameAssets\icons"
tutorial_icon_dir = "GameAssets\Tutorial_Pictures"
en_tutorial_icon_dir = "GameAssets\Tutorial_Pictures\Edited_English"
icons = []
icon_pw_path = os.path.join(icon_dir, "icon11.png")
icon_pw = pygame.image.load(icon_pw_path).convert_alpha()
icon_building1_path = os.path.join(icon_dir, "icon12.png")
icon_building1 = pygame.image.load(icon_building1_path).convert_alpha()
icon_building2_path = os.path.join(icon_dir, "icon13.png")
icon_building2 = pygame.image.load(icon_building2_path).convert_alpha()
icon_building3_path = os.path.join(icon_dir, "icon18.png")
icon_building3 = pygame.image.load(icon_building3_path).convert_alpha()
icon_greenhouse_path = os.path.join(icon_dir, "icon14.png")
icon_greenhouse = pygame.image.load(icon_greenhouse_path).convert_alpha()
icon_rw_path = os.path.join(icon_dir, "icon15.png")
icon_rw = pygame.image.load(icon_rw_path).convert_alpha()
icon_outflow_path = os.path.join(icon_dir, "outflow.png")
icon_outflow = pygame.image.load(icon_outflow_path).convert_alpha()
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
icon_tripletqsplit_path = os.path.join(icon_dir, "tripletqsplit.png")
icon_tripletqsplit = pygame.image.load(icon_tripletqsplit_path).convert_alpha()
icon_tripletqcombine1_path = os.path.join(icon_dir, "tripletqcombine1.png")
icon_tripletqcombine1 = pygame.image.load(icon_tripletqcombine1_path).convert_alpha()
icon_tripletqcombine2_path = os.path.join(icon_dir, "tripletqcombine2.png")
icon_tripletqcombine2 = pygame.image.load(icon_tripletqcombine2_path).convert_alpha()
icon_tripletqcombine3_path = os.path.join(icon_dir, "tripletqcombine3.png")
icon_tripletqcombine3 = pygame.image.load(icon_tripletqcombine3_path).convert_alpha()
icon_UKflag_path = os.path.join(icon_dir, "UKflag.png")
icon_UKflag = pygame.image.load(icon_UKflag_path).convert_alpha()
icon_Greeceflag_path = os.path.join(icon_dir, "Greeceflag.png")
icon_Greeceflag = pygame.image.load(icon_Greeceflag_path).convert_alpha()
icon_bug_report_path = os.path.join(icon_dir, "bug_report.png")
icon_bug_report = pygame.image.load(icon_bug_report_path).convert_alpha()
icon_menu_button_path = os.path.join(icon_dir, "icon_menu_button.png")
icon_menu_button = pygame.image.load(icon_menu_button_path).convert_alpha()
# Load the fonts
title_font = root_dir + "\GameAssets\Fonts\Handjet\static\Handjet-Light.ttf"
info_font = root_dir + "\GameAssets\Fonts\Roboto\Roboto-Medium.ttf"
info_font2 = root_dir + "\GameAssets\Fonts\PtSerif\PTSerif-Bold.ttf"

# pygame.time.wait(2000)

# Screen settings for normal game
"""playerscreen_width = display_info.current_w
playerscreen_height = display_info.current_h"""

screen_width = 1005
screen_height = 750
#screen_width = int(playerscreen_width*scale_variable)
#screen_height = int(playerscreen_height*scale_variable)

screen = pygame.display.set_mode((screen_width, screen_height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SRCALPHA)

pygame.display.set_caption("Geogame")

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
# Language button position
language_button_x = screen_width - 133
language_button_y = screen_height - 95
language_button_width = 65
language_button_height = 50
icon_UKflag_scaled = pygame.transform.scale(icon_UKflag, (language_button_width, language_button_height))
icon_Greeceflag_scaled = pygame.transform.scale(icon_Greeceflag, (language_button_width, language_button_height))
bug_report_button_x = screen_width // 2 - 25
bug_report_button_y = screen_height // 2 + 300
bug_report_button_width = 50
bug_report_button_height = 50
icon_bug_report_button_scaled = pygame.transform.scale(icon_bug_report,
                                                       (bug_report_button_width, bug_report_button_height))
bug_report_button = IconButton(bug_report_button_x, bug_report_button_y, bug_report_button_width,
                               bug_report_button_height, icon_bug_report,
                               icon_size=(bug_report_button_width, bug_report_button_height), color=BLUE3)
available_icons = []

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
    info_text = (f"simple pipe cost = {int(simple_pipe_cost[dataset])}")
    info_text2 = (f"corner pipe cost = {int(corner_pipe_cost[dataset])}")
    info_text3 = (f"triplet pipe cost = {int(triplet_pipe_cost[dataset])}")

    icon0 = pygame.transform.scale(icons[0], (20, 20))
    icon0_rect = icon0.get_rect(center=(45, 40))  # Adjust position as needed

    icon1 = pygame.transform.scale(icons[1], (20, 20))
    icon1_rect = icon1.get_rect(center=(50 + 20, 40))  # Adjust position as needed

    icon2 = pygame.transform.scale(icons[2], (20, 20))
    icon2_rect = icon2.get_rect(center=(170 + 15, 40))  # Adjust position as needed

    icon3 = pygame.transform.scale(icons[3], (20, 20))
    icon3_rect = icon3.get_rect(center=(170 + 40, 40))  # Adjust position as needed

    icon4 = pygame.transform.scale(icons[4], (20, 20))
    icon4_rect = icon4.get_rect(center=(170 + 65, 40))  # Adjust position as needed

    icon5 = pygame.transform.scale(icons[5], (20, 20))
    icon5_rect = icon5.get_rect(center=(170 + 90, 40))  # Adjust position as needed

    icon6 = pygame.transform.scale(icons[6], (20, 20))
    icon6_rect = icon6.get_rect(center=(320 + 15, 40))  # Adjust position as needed

    icon7 = pygame.transform.scale(icons[7], (20, 20))
    icon7_rect = icon7.get_rect(center=(320 + 40, 40))  # Adjust position as needed

    icon8 = pygame.transform.scale(icons[8], (20, 20))
    icon8_rect = icon8.get_rect(center=(320 + 65, 40))  # Adjust position as needed

    icon9 = pygame.transform.scale(icons[9], (20, 20))
    icon9_rect = icon9.get_rect(center=(320 + 90, 40))  # Adjust position as needed

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
    global screen

    font = pygame.font.Font(None, 36)
    credits_font = pygame.font.Font(None, 17)
    font_title = pygame.font.Font(title_font, 200)
    title_rect = pygame.Rect(screen_width // 2 - 350, screen_height // 2 - 275, 700, 200)
    title_text = font_title.render("GeoGame", True, (0, 0, 0))
    companyname_text = credits_font.render("yiakou-games", True, (255, 255, 255))
    creditsmail_text1 = credits_font.render("Yiannis Kontos", True, (255, 255, 255))
    creditsmail_text2 = credits_font.render("Konstantinos Koutridis", True, (255, 255, 255))
    creditsmail_text1_button = Button(10, screen_height - 40, 120, 10, "Y", BLUE, WHITE)
    creditsmail_text2_button = Button(10, screen_height - 25, 160, 10, "K", BLUE, WHITE)
    play_button = Button(screen_width // 2 - 100, screen_height // 2 - 50, 200, 50, "Play", RED, WHITE)
    instructions_button = Button(screen_width // 2 - 100, screen_height // 2 + 25, 200, 50, "Instructions", RED, WHITE)
    language_button = Button(language_button_x, language_button_y, language_button_width, language_button_height, "L",
                             BLUE3, WHITE)
    high_score_button = Button(screen_width // 2 - 100, screen_height // 2 + 100, 200, 50, "High Scores", RED, WHITE)
    exam_mode_button = Button(screen_width // 2 - 100, screen_height // 2 + 175, 200, 50, "Exam", RED, WHITE)
    # settings_button = Button(screen_width // 2 - 100, screen_height // 2 + 50, 200, 50, "Settings", RED, WHITE)
    # minimize_button = Button(screen_width - 120, 10, 30, 30, "M", RED, GRAY)
    # maximize_button = Button(screen_width - 80, 10, 30, 30, "■", RED, GRAY)
    # exit_button = Button(screen_width - 40, 10, 30, 30, "X", RED, GRAY)

    # screen.blit(icon_Greeceflag_scaled, (language_button_x, language_button_y))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.is_clicked(pygame.mouse.get_pos()):
                    return  # Exit the function to start the game
                elif instructions_button.is_clicked(pygame.mouse.get_pos()):
                    instructions()
                elif high_score_button.is_clicked(pygame.mouse.get_pos()):
                    leaderboard()
                elif language_button.is_clicked(pygame.mouse.get_pos()):
                    language_change()
                elif bug_report_button.is_clicked(pygame.mouse.get_pos()):
                    bug_report_button_uploader_2()
                elif creditsmail_text1_button.is_clicked(pygame.mouse.get_pos()):
                    webbrowser.open(
                        'https://linktr.ee/ykontos?fbclid=IwAR3LGlifCCUtuedy9w462lHdA9MX8qxXtM0asjq8d3XgOyxaYBW_OvLuQbE')
                elif creditsmail_text2_button.is_clicked(pygame.mouse.get_pos()):
                    webbrowser.open(
                        'https://linktr.ee/kkoutrid?fbclid=IwAR0gxJALYl2qcR6uA9Ls2fHTdwpdv_HjbPE816o-ONUtUYrXDU6_jga66aY')
                elif exam_mode_button.is_clicked(pygame.mouse.get_pos()) and number_of_exam_tries <= 2:
                    key = show_input_box_exam_key(10, 10, screen_width, screen_height, text="")
                    if key == 172:
                        exam_mode()
                    else:
                        pass
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                return  # Exit the function to start the game
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                instructions()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                leaderboard()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                language_change()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                reset_high_scores(file_path)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e and number_of_exam_tries <= 2:
                key = show_input_box_exam_key(10, 10, screen_width, screen_height, text="")
                if key == 172:
                    exam_mode()
                else:
                    pass
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                if screen.get_flags() & pygame.FULLSCREEN:  # Check if currently in fullscreen mode
                    screen = pygame.display.set_mode((screen_width, screen_height))  # Switch to windowed mode
                else:
                    screen = pygame.display.set_mode((screen_width, screen_height),
                                                     pygame.NOFRAME | pygame.FULLSCREEN)  # Switch to borderless fullscreen mode
                """elif minimize_button.is_clicked(pygame.mouse.get_pos()):
                    pygame.display.iconify()
                elif exit_button.is_clicked(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
                elif maximize_button.is_clicked(pygame.mouse.get_pos()):
                    if screen.get_flags() & pygame.FULLSCREEN:
                        pygame.display.set_mode((screen_width, screen_height))
                    else:
                        pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)"""

        creditsmail_text2_button.draw(screen)
        creditsmail_text1_button.draw(screen)
        screen.fill(BLUE)
        play_button.draw(screen)
        instructions_button.draw(screen)
        language_button.draw(screen)
        bug_report_button.draw(screen)
        high_score_button.draw(screen)
        exam_mode_button.draw(screen)
        """minimize_button.draw(screen)
        exit_button.draw(screen)
        maximize_button.draw(screen)"""

        if language == 'gr':
            screen.blit(icon_Greeceflag_scaled, (language_button_x, language_button_y))
        elif language == 'en':
            screen.blit(icon_UKflag_scaled, (language_button_x, language_button_y))
        pygame.draw.rect(screen, (BLUE), title_rect)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 2 - 300))
        screen.blit(companyname_text, (865, screen_height - 40))
        screen.blit(creditsmail_text1, (10, screen_height - 40))
        screen.blit(creditsmail_text2, (10, screen_height - 25))

        pygame.display.flip()

def exam_mode():
    global dataset
    dataset = 11
    initialize_grid()
    #drawing_grid()
    main_loop_exam_mode()
    #i want to have everything to work the same but only have one specific level,
    #if fail to not restart but lose a point internally. To be able to deduce if the mistake has been fixed,
    #so maybe undo or reset the lost point, have a time limit for the player, unlock the exam mode with a code,
    #setting a different code after the player leaves the exam mode so he cant retry, to have the answer saved separately
    #and finally a time limir or a try limit or both
def language_change():
    global language

    if language == 'en':
        language = 'gr'
    elif language == 'gr':
        language = 'en'
    return language


def instructions():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_instruction_button.is_clicked(pygame.mouse.get_pos()):
                    return

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
        icon2_rect = icon2.get_rect(topright=(screen_width - 658, 250))  # Adjust position as needed

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
        back_instruction_button = Button(0, 0, 200, 50, "Back", RED, WHITE)
        back_instruction_button.draw(screen)

        pygame.display.flip()
        # Check for button click


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
                choosing_the_level(screen)
                screen.fill(BLUE2)
                return

        pygame.display.update()

def username_to_info_and_start_exam_mode():
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
                return

        pygame.display.update()
def choosing_the_level(screen):
    global dataset

    # Define the vertical and horizontal spacing between buttons
    vertical_spacing = 10  # Adjust this value as needed
    horizontal_spacing = 10  # Adjust this value as needed

    # Number of buttons to create
    idata = pd.read_excel(root_dir + "\GameAssets\geodata.xlsx", sheet_name="info")
    dataset_column = idata["Dataset"]
    completed_level_column = idata["high_score"]
    # dataset_column.dropna() keeps every kind of data
    # non_empty_text_values = dataset_column[dataset_column.apply(lambda x: isinstance(x, str))] for text values
    non_empty_number_values = dataset_column[dataset_column.apply(lambda x: isinstance(x, (int, float)))]
    num_buttons = len(non_empty_number_values)
    button_label = [None] * (num_buttons + 1)
    # List to store the buttons
    buttons = []
    button_label_tutorial = f"Tutorial"
    level_number_str = ""

    # Define initial coordinates
    x = 15 + 113 + 10  # horizontal_spacing
    y = 15
    tutorial_button_x = 15
    tutorial_button_y = 15

    # Create buttons with correlated positions
    for i in range(1, num_buttons + 1):
        button_label[i] = f"Level {i}"
        button = Button(x, y, 113, 50, button_label[i], GRAY, BLACK)
        buttons.append(button)

        # Update coordinates for the next button
        x += 113 + horizontal_spacing  # Move horizontally

        # Check if we need to start a new row
        if (i + 1) % 8 == 0:  # Start a new row if the next button completes a row
            x = 15
            y += 50 + vertical_spacing  # Move vertically to the next row

            # Reset Y-coordinate if it exceeds 750
            if y > 750:
                y = 10

    screen.fill(BLUE)
    for i, button in enumerate(buttons):
        button.draw(screen)  # Draw the button itself
        if completed_level_column[i] > 0:
            pygame.draw.rect(screen, GREEN, button.rect, 2)  # Draw green rectangle around the button
            print("I was here")

    tutorial_button = Button(tutorial_button_x, tutorial_button_y, 113, 50, button_label_tutorial, GRAY, BLACK)
    tutorial_button.draw(screen)
    bug_report_button.draw(screen)
    pygame.display.update()

    tutorial_button = Button(tutorial_button_x, tutorial_button_y, 113, 50, button_label_tutorial, GRAY, BLACK)
    tutorial_button.draw(screen)
    bug_report_button.draw(screen)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    # Handle the tutorial event
                    tutorial_icon_width = 1005
                    tutorial_icon_height = 750
                    tutorial_icon_1_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_1.png")
                    tutorial_icon_1 = pygame.image.load(tutorial_icon_1_path).convert_alpha()
                    tutorial_icon_scaled_1 = pygame.transform.scale(tutorial_icon_1, (
                        tutorial_icon_width, tutorial_icon_height))
                    screen.blit(tutorial_icon_scaled_1, (0, 0))
                    pygame.display.update()
                    tutorial()
                    choosing_the_level(screen)
                elif event.type == pygame.KEYDOWN:
                    if pygame.K_0 <= event.key <= pygame.K_9 or event.key == pygame.K_KP0 or event.key == pygame.K_KP1 or event.key == pygame.K_KP2 or event.key == pygame.K_KP3 or event.key == pygame.K_KP4 or event.key == pygame.K_KP5 or event.key == pygame.K_KP6 or event.key == pygame.K_KP7 or event.key == pygame.K_KP8 or event.key == pygame.K_KP9:
                        # Handle numeric key presses (0-9 and keypad 0-9)
                        level_number_str += pygame.key.name(event.key)
                    elif event.key == pygame.K_BACKSPACE:
                        level_number_str = level_number_str[:-1]
                    elif event.key == pygame.K_RETURN:
                        if level_number_str:
                            # If a number has been entered, convert it to an integer and process
                            level_number = int(level_number_str)
                            print(f"Selected level: {level_number}")
                            # Process the selected level here, for example:
                            dataset = level_number - 1
                            # Clear the stored level number string for the next selection
                            level_number_str = ""
                            # Return or process the selected level here
                            return dataset
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if bug_report_button.is_clicked(pygame.mouse.get_pos()):
                    bug_report_button_uploader_2()
                else:  # Check if the click intersects with any button
                    for button in buttons:
                        if button.is_clicked(pygame.mouse.get_pos()):
                            print(f"Clicked on {button.text}")  # Print the button label
                            level_number = int(button.text.split()[1])
                            dataset = level_number - 1
                            return
                        if tutorial_button.is_clicked(pygame.mouse.get_pos()):
                            tutorial_icon_width = 1005
                            tutorial_icon_height = 750
                            tutorial_icon_1_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_1.PNG")
                            tutorial_icon_1 = pygame.image.load(tutorial_icon_1_path).convert_alpha()
                            tutorial_icon_scaled_1 = pygame.transform.scale(tutorial_icon_1, (
                                tutorial_icon_width, tutorial_icon_height))
                            screen.blit(tutorial_icon_scaled_1, (0, 0))
                            pygame.display.update()
                            tutorial()
                            choosing_the_level(screen)
                            # problem is that i have to click the level twice cause 2 returns are required

def house_and_greenhouses_info():
    # Render Information for house0
    if house0_row[dataset] > 0:
        font = pygame.font.Font(info_font, 15)
        text_content1_0 = f"T_in = {int(Thouse0_in[dataset])}"
        text_content2_0 = f"T_out = {int(Thouse0_out[dataset])}"
        text_content3_0 = f"Q_in = {int(Qhouse0_in[dataset])}"
        text_surface1_0 = font.render(text_content1_0, True, (255, 255, 255))  # White text color
        text_position1_0 = (675-150, 25+500)  # Position to render the text
        text_surface2_0 = font.render(text_content2_0, True, (255, 255, 255))  # White text color
        text_position2_0 = (675-150, 50+500)  # Position to render the text
        text_surface3_0 = font.render(text_content3_0, True, (255, 255, 255))  # White text color
        text_position3_0 = (675-150, 75+500)  # Position to render the text
        new_width_0 = 40
        new_height_0 = 40
        icon_building1_resized_0 = pygame.transform.scale(icon_building1, (new_width_0, new_height_0))
        screen.blit(icon_building1_resized_0, (625-150, 38+500))
        screen.blit(text_surface1_0, text_position1_0)
        screen.blit(text_surface2_0, text_position2_0)
        screen.blit(text_surface3_0, text_position3_0)
    # Render Information for house1
    if house1_row[dataset] > 0:
        text_content1_1 = f"T_in = {int(Thouse1_in[dataset])}"
        text_content2_1 = f"T_out = {int(Thouse1_out[dataset])}"
        text_content3_1 = f"Q_in = {int(Qhouse1_in[dataset])}"
        text_surface1_1 = font.render(text_content1_1, True, (255, 255, 255))  # White text color
        text_position1_1 = (875-150, 25+500)  # Position to render the text
        text_surface2_1 = font.render(text_content2_1, True, (255, 255, 255))  # White text color
        text_position2_1 = (875-150, 50+500)  # Position to render the text
        text_surface3_1 = font.render(text_content3_1, True, (255, 255, 255))  # White text color
        text_position3_1 = (875-150, 75+500)  # Position to render the text
        new_width_1 = 40
        new_height_1 = 40
        icon_building2_resized_1 = pygame.transform.scale(icon_building2, (new_width_1, new_height_1))
        screen.blit(icon_building2_resized_1, (825-150, 38+500))
        screen.blit(text_surface1_1, text_position1_1)
        screen.blit(text_surface2_1, text_position2_1)
        screen.blit(text_surface3_1, text_position3_1)
    # Render Information for house2
    if house2_row[dataset] > 0:
        text_content1_2 = f"T_in = {int(Thouse2_in[dataset])}"
        text_content2_2 = f"T_out = {int(Thouse2_out[dataset])}"
        text_content3_2 = f"Q_in = {int(Qhouse2_in[dataset])}"
        text_surface1_2 = font.render(text_content1_2, True, (255, 255, 255))  # White text color
        text_position1_2 = (875-150, 125+500)  # Position to render the text
        text_surface2_2 = font.render(text_content2_2, True, (255, 255, 255))  # White text color
        text_position2_2 = (875-150, 150+500)  # Position to render the text
        text_surface3_2 = font.render(text_content3_2, True, (255, 255, 255))  # White text color
        text_position3_2 = (875-150, 175+500)  # Position to render the text
        new_width_2 = 40
        new_height_2 = 40
        icon_building3_resized_2 = pygame.transform.scale(icon_building3,
                                                        (new_width_2, new_height_2))  # "To icon 3 θεωριτικά"
        screen.blit(icon_building3_resized_2, (825-150, 138+500))
        screen.blit(text_surface1_2, text_position1_2)
        screen.blit(text_surface2_2, text_position2_2)
        screen.blit(text_surface3_2, text_position3_2)
    # Render Information for greenhouse0
    if greenhouse0_row[dataset] > 0:
        text_content1_g0 = f"T_in = {int(Tgreenhouse0_in[dataset])}"
        text_content2_g0 = f"T_out = {int(Tgreenhouse0_out[dataset])}"
        text_content3_g0 = f"Q_in = {int(Qghouse0_in[dataset])}"
        text_surface1_g0 = font.render(text_content1_g0, True, (255, 255, 255))  # White text color
        text_position1_g0 = (675-150, 125+500)  # Position to render the text
        text_surface2_g0 = font.render(text_content2_g0, True, (255, 255, 255))  # White text color
        text_position2_g0 = (675-150, 150+500)  # Position to render the text
        text_surface3_g0 = font.render(text_content3_g0, True, (255, 255, 255))  # White text color
        text_position3_g0 = (675-150, 175+500)  # Position to render the text
        new_width_g0 = 40
        new_height_g0 = 40
        icon_greenhouse_resized_g0 = pygame.transform.scale(icon_greenhouse, (new_width_g0, new_height_g0))
        screen.blit(icon_greenhouse_resized_g0, (625-150, 138+500))
        screen.blit(text_surface1_g0, text_position1_g0)
        screen.blit(text_surface2_g0, text_position2_g0)
        screen.blit(text_surface3_g0, text_position3_g0)
    # Render Information for greenhouse1
    if greenhouse1_row[dataset] > 0:
        text_content1_g1 = f"T_in = {int(Tgreenhouse1_in[dataset])}"
        text_content2_g1 = f"T_out = {int(Tgreenhouse1_out[dataset])}"
        text_content3_g1 = f"Q_in = {int(Qghouse1_in[dataset])}"
        text_surface1_g1 = font.render(text_content1_g1, True, (255, 255, 255))  # White text color
        text_position1_g1 = (925-50, 225+350)  # Position to render the text
        text_surface2_g1 = font.render(text_content2_g1, True, (255, 255, 255))  # White text color
        text_position2_g1 = (925-50, 250+350)  # Position to render the text
        text_surface3_g1 = font.render(text_content3_g1, True, (255, 255, 255))  # White text color
        text_position3_g1 = (925-50, 275+350)  # Position to render the text
        new_width_g1 = 40
        new_height_g1 = 40
        icon_greenhouse_resized_g1 = pygame.transform.scale(icon_greenhouse, (new_width_g1, new_height_g1))
        screen.blit(icon_greenhouse_resized_g1, (925-100, 238+350))
        screen.blit(text_surface1_g1, text_position1_g1)
        screen.blit(text_surface2_g1, text_position2_g1)
        screen.blit(text_surface3_g1, text_position3_g1)






def choose_the_starting_Q():
    global Starting_Q, rw_existence, language

    screen.fill(BLUE3)
    font = pygame.font.Font(info_font, 20)
    font2 = pygame.font.Font(info_font, 24)
    icon1 = pygame.transform.scale(icon_pw, (40, 40))
    icon1_rect = icon1.get_rect(center=(850, 490))  # Adjust position as needed
    info_text_width = 900  # Change this if you want a different width for the text box
    info_text_height = 500  # Change this if you want a different height for the text box
    info_text_x = 50
    info_text_y = 40

    # Create the text rectangle and render the wrapped text
    font = pygame.font.Font(info_font, 18)
    # Greek translations
    info_text_gr1 = "Συμπληρώστε το σκαρίφημα του συστήματος θέρμανσης των συγκροτημάτων κατοικιών Α, Β και θερμοκηπίων Γ του σχήματος. Δίνεται ότι:"
    info_text_gr1_1 = "Συμπληρώστε το σκαρίφημα του συστήματος θέρμανσης του συγκροτήματος κατοικιών Α του σχήματος. Δίνεται ότι:"
    info_text_gr1_2 = "Συμπληρώστε το σκαρίφημα του συστήματος θέρμανσης των συγκροτημάτων κατοικιών Α, Β του σχήματος. Δίνεται ότι:"
    info_text_gr1_3 = "Συμπληρώστε το σκαρίφημα του συστήματος θέρμανσης των συγκροτημάτων κατοικιών Α, Β, Γ και θερμοκηπίων Δ του σχήματος. Δίνεται ότι:"

    info_text_gr2 = "1-Η θερμοκρασία του γεωθερμικού νερού είναι 85 °C."
    info_text_gr3 = "2-Η ποιότητά του είναι καλή."
    info_text_gr4 = f"3-Η απαιτούμενη παροχή θερμού νερού είναι ίση με {Qhouse0_in[dataset]} και {Qhouse1_in[dataset]} για τα συγκροτήματα κατοικιών Α, Β και {Qghouse0_in[dataset]} για το θερμοκήπιο Γ."
    info_text_gr4_1 = f"3-Η απαιτούμενη παροχή θερμού νερού είναι ίση με {Qhouse0_in[dataset]} για τα συγκρότημα κατοικιών Α."
    info_text_gr4_2 = f"3-Η απαιτούμενη παροχή θερμού νερού είναι ίση με {Qhouse0_in[dataset]} και {Qhouse1_in[dataset]} για τα συγκροτήματα κατοικιών Α, Β."
    info_text_gr4_3 = f"3-Η απαιτούμενη παροχή θερμού νερού είναι ίση με {Qhouse0_in[dataset]} και {Qhouse1_in[dataset]} και {Qhouse2_in[dataset]} για τα συγκροτήματα κατοικιών Α, Β και Γ αντίστοιχα και {Qghouse0_in[dataset]} για το θερμοκήπιο Δ."

    info_text_gr5 = f"4-Δεν υπάρχει κίνδυνος εξάντλησης του υδροφορέα, αν η συνολικά αντλούμενη παροχή QΣ είναι μικρότερη από {Qtot_depl[dataset]}."
    info_text_gr6 = f"5-Προκαλείται όμως σημαντική πτώση στάθμης του πιεζομετρικού φορτίου, αν η QΣ είναι μεγαλύτερη από {Qtot_head[dataset]}."
    info_text_gr7 = "6-Οι απαιτούμενες θερμοκρασίες εισόδου και εξόδου φαίνονται στο σχήμα."

    """Να γίνει και στα αγγλικά"""

    # English translations
    info_text_en1 = "Complete the sketch of the heating system of residential complexes A, B, and greenhouses Γ shown below. It's given that:"
    info_text_en1_1 = "Complete the sketch of the heating system of the residential complex A shown below. It's given that:"
    info_text_en1_2 = "Complete the sketch of the heating system of residential complexes A, B shown below. It's given that:"
    info_text_en1_3 = "Complete the sketch of the heating system of residential complexes A, B, C and greenhouses D shown below. It's given that:"

    info_text_en2 = "1-The temperature of geothermal water is 85 °C."
    info_text_en3 = "2-Its quality is good."
    info_text_en4 = f"3-The required hot water supply is equal to {Qhouse0_in[dataset]} and {Qhouse1_in[dataset]} for residential complexes A, B and {Qghouse0_in[dataset]} for greenhouse C."
    info_text_en4_1 = f"3-The required hot water supply is equal to {Qhouse0_in[dataset]} for residential complex A."
    info_text_en4_2 = f"3-The required hot water supply is equal to {Qhouse0_in[dataset]} and {Qhouse1_in[dataset]} for residential complexes A, B."
    info_text_en4_3 = f"3-The required hot water supply is equal to {Qhouse0_in[dataset]} and {Qhouse1_in[dataset]} and {Qhouse2_in[dataset]} for residential complexes A, B and C and {Qghouse0_in[dataset]} for greenhouse D."

    info_text_en5 = f"4-There is no risk of depleting the aquifer if the total pumped supply QΣ is less than {Qtot_depl[dataset]}."
    info_text_en6 = f"5-However, a significant drawdown in the piezometric load occurs if QΣ is less than {Qtot_head[dataset]}."
    info_text_en7 = "6-The required input and output temperatures are shown in the diagram."

    step_h = 50
    text_rect1 = pygame.Rect(info_text_x, info_text_y + 0 * step_h, info_text_width, info_text_height)
    text_rect2 = pygame.Rect(30 + info_text_x, info_text_y + 1 * step_h, info_text_width, info_text_height)
    text_rect3 = pygame.Rect(30 + info_text_x, info_text_y + 2 * step_h - 15, info_text_width, info_text_height)
    text_rect4 = pygame.Rect(30 + info_text_x, info_text_y + 3 * step_h - 25, info_text_width, info_text_height)
    text_rect5 = pygame.Rect(30 + info_text_x, info_text_y + 4 * step_h - 15, info_text_width, info_text_height)
    text_rect6 = pygame.Rect(30 + info_text_x, info_text_y + 5 * step_h - 5, info_text_width, info_text_height)
    text_rect7 = pygame.Rect(30 + info_text_x, info_text_y + 6 * step_h - 5, info_text_width, info_text_height)

    wrapped_info_text_gr1 = render_text_rect(info_text_gr1, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr1_1 = render_text_rect(info_text_gr1_1, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr1_2 = render_text_rect(info_text_gr1_2, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr1_3 = render_text_rect(info_text_gr1_3, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_gr2 = render_text_rect(info_text_gr2, font, text_rect2, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr3 = render_text_rect(info_text_gr3, font, text_rect3, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_gr4 = render_text_rect(info_text_gr4, font, text_rect4, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr4_1 = render_text_rect(info_text_gr4_1, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr4_2 = render_text_rect(info_text_gr4_2, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr4_3 = render_text_rect(info_text_gr4_3, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_gr5 = render_text_rect(info_text_gr5, font, text_rect5, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr6 = render_text_rect(info_text_gr6, font, text_rect6, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr7 = render_text_rect(info_text_gr7, font, text_rect7, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_en1 = render_text_rect(info_text_en1, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en1_1 = render_text_rect(info_text_en1_1, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en1_2 = render_text_rect(info_text_en1_2, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en1_3 = render_text_rect(info_text_en1_3, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_en2 = render_text_rect(info_text_en2, font, text_rect2, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en3 = render_text_rect(info_text_en3, font, text_rect3, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_en4 = render_text_rect(info_text_en4, font, text_rect4, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en4_1 = render_text_rect(info_text_en4_1, font, text_rect4, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en4_2 = render_text_rect(info_text_en4_2, font, text_rect4, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en4_3 = render_text_rect(info_text_en4_3, font, text_rect4, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_en5 = render_text_rect(info_text_en5, font, text_rect5, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en6 = render_text_rect(info_text_en6, font, text_rect6, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en7 = render_text_rect(info_text_en7, font, text_rect7, (255, 255, 255), (BLUE3), wrap=True)

    language_button = Button(language_button_x, language_button_y, language_button_width, language_button_height, "L",
                             BLUE3, WHITE)
    icon_UKflag_scaled = pygame.transform.scale(icon_UKflag, (language_button_width, language_button_height))
    icon_Greeceflag_scaled = pygame.transform.scale(icon_Greeceflag, (language_button_width, language_button_height))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                #{Qhouse0_in[dataset]} and {Qhouse1_in[dataset]} and {Qhouse2_in[dataset]} and {Qghouse0_in[dataset]}
                #int(Qhouse0_in[dataset])
            if language == 'gr':
                if int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) > 0:
                    screen.blit(wrapped_info_text_gr1, text_rect1)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) == 0 and int(Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                    screen.blit(wrapped_info_text_gr1_1, text_rect1)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                    screen.blit(wrapped_info_text_gr1_2, text_rect1)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(Qhouse2_in[dataset]) > 0 and int(Qghouse0_in[dataset]) > 0:
                    screen.blit(wrapped_info_text_gr1_3, text_rect1)
                screen.blit(wrapped_info_text_gr2, text_rect2)
                screen.blit(wrapped_info_text_gr3, text_rect3)
                if int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                        Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) > 0:
                    screen.blit(wrapped_info_text_gr4, text_rect4)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) == 0 and int(
                        Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                    screen.blit(wrapped_info_text_gr4_1, text_rect4)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                        Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                    screen.blit(wrapped_info_text_gr4_2, text_rect4)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                        Qhouse2_in[dataset]) > 0 and int(Qghouse0_in[dataset]) > 0:
                    screen.blit(wrapped_info_text_gr4_3, text_rect4)
                screen.blit(wrapped_info_text_gr5, text_rect5)
                screen.blit(wrapped_info_text_gr6, text_rect6)
                screen.blit(wrapped_info_text_gr7, text_rect7)
                screen.blit(icon1, icon1_rect)
                screen.blit(icon_UKflag_scaled, (language_button_x, language_button_y))
                language_button.draw(screen)
                house_and_greenhouses_info()
                drawing_grid2()
                Starting_Q = show_input_box3(10, 10, screen_width, screen_height)
                rw_existence = True
                fill_area_rect = pygame.Rect(280, 420, 450, 300)
                pygame.draw.rect(screen, BLUE3, fill_area_rect)
                pygame.display.update()
                drawing_grid2()
                return  # Exit the function to start the game
            elif language == 'en':
                if int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) > 0:
                    screen.blit(wrapped_info_text_en1, text_rect1)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) == 0 and int(Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                    screen.blit(wrapped_info_text_en1_1, text_rect1)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                    screen.blit(wrapped_info_text_en1_2, text_rect1)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(Qhouse2_in[dataset]) > 0 and int(Qghouse0_in[dataset]) > 0:
                    screen.blit(wrapped_info_text_en1_3, text_rect1)
                screen.blit(wrapped_info_text_en2, text_rect2)
                screen.blit(wrapped_info_text_en3, text_rect3)
                if int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                        Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) > 0:
                    screen.blit(wrapped_info_text_en4, text_rect4)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) == 0 and int(
                        Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                    screen.blit(wrapped_info_text_en4_1, text_rect4)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                        Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                    screen.blit(wrapped_info_text_en4_2, text_rect4)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                        Qhouse2_in[dataset]) > 0 and int(Qghouse0_in[dataset]) > 0:
                    screen.blit(wrapped_info_text_en4_3, text_rect4)
                screen.blit(wrapped_info_text_en5, text_rect5)
                screen.blit(wrapped_info_text_en6, text_rect6)
                screen.blit(wrapped_info_text_en7, text_rect7)
                screen.blit(icon1, icon1_rect)
                language_button.draw(screen)
                screen.blit(icon_Greeceflag_scaled, (language_button_x, language_button_y))
                house_and_greenhouses_info()
                drawing_grid2()
                Starting_Q = show_input_box3(10, 10, screen_width, screen_height)
                rw_existence = True
                fill_area_rect = pygame.Rect(280, 420, 450, 300)
                pygame.draw.rect(screen, BLUE3, fill_area_rect)
                pygame.display.update()
                drawing_grid2()
                return  Starting_Q# Exit the function to start the game

        pygame.display.update()


def choose_the_use_of_rw_well():
    global rw_existence
    yes_button = pygame.Rect(screen_width // 2 - 150 + 150, screen_height // 2 + 270, 100, 50)
    no_button = pygame.Rect(screen_width // 2 + 50 + 150, screen_height // 2 + 270, 100, 50)

    font = pygame.font.Font(info_font, 20)
    font2 = pygame.font.Font(info_font, 22)

    yes_text = font.render("Yes", True, (255, 255, 255))
    no_text = font.render("No", True, (255, 255, 255))

    rw_text_gr = "Χρησιμοποιείται πηγάδι επαναφοράς?"
    rw_text_en = "Are you using a recharging well?"
    text_surface_gr = font2.render(rw_text_gr, True, (255, 255, 255))
    text_rect_gr = text_surface_gr.get_rect(center=(500 + 150, 450))
    text_surface_en = font2.render(rw_text_en, True, (255, 255, 255))
    text_rect_en = text_surface_en.get_rect(center=(500 + 150, 450))

    icon1 = pygame.transform.scale(icon_rw, (100, 100))
    icon1_rect = icon1.get_rect(topright=(screen_width // 2 + 50 + 150, 500))  # Adjust position as needed

    screen.fill(BLUE3)
    font = pygame.font.Font(info_font, 18)
    font2 = pygame.font.Font(info_font, 24)
    info_text_width = 900  # Change this if you want a different width for the text box
    info_text_height = 500  # Change this if you want a different height for the text box
    info_text_x = 50
    info_text_y = 40

    # Greek translations
    info_text_gr1 = "Συμπληρώστε το σκαρίφημα του συστήματος θέρμανσης των συγκροτημάτων κατοικιών Α, Β και θερμοκηπίων Γ του σχήματος. Δίνεται ότι:"
    info_text_gr1_1 = "Συμπληρώστε το σκαρίφημα του συστήματος θέρμανσης του συγκροτήματος κατοικιών Α του σχήματος. Δίνεται ότι:"
    info_text_gr1_2 = "Συμπληρώστε το σκαρίφημα του συστήματος θέρμανσης των συγκροτημάτων κατοικιών Α, Β του σχήματος. Δίνεται ότι:"
    info_text_gr1_3 = "Συμπληρώστε το σκαρίφημα του συστήματος θέρμανσης των συγκροτημάτων κατοικιών Α, Β, Γ και θερμοκηπίων Δ του σχήματος. Δίνεται ότι:"

    info_text_gr2 = "1-Η θερμοκρασία του γεωθερμικού νερού είναι 85 °C."
    info_text_gr3 = "2-Η ποιότητά του είναι καλή."
    info_text_gr4 = f"3-Η απαιτούμενη παροχή θερμού νερού είναι ίση με {Qhouse0_in[dataset]} και {Qhouse1_in[dataset]} για τα συγκροτήματα κατοικιών Α, Β και {Qghouse0_in[dataset]} για το θερμοκήπιο Γ."
    info_text_gr4_1 = f"3-Η απαιτούμενη παροχή θερμού νερού είναι ίση με {Qhouse0_in[dataset]} για τα συγκρότημα κατοικιών Α."
    info_text_gr4_2 = f"3-Η απαιτούμενη παροχή θερμού νερού είναι ίση με {Qhouse0_in[dataset]} και {Qhouse1_in[dataset]} για τα συγκροτήματα κατοικιών Α, Β."
    info_text_gr4_3 = f"3-Η απαιτούμενη παροχή θερμού νερού είναι ίση με {Qhouse0_in[dataset]} και {Qhouse1_in[dataset]} και {Qhouse2_in[dataset]} για τα συγκροτήματα κατοικιών Α, Β και Γ αντίστοιχα και {Qghouse0_in[dataset]} για το θερμοκήπιο Δ."

    info_text_gr5 = f"4-Δεν υπάρχει κίνδυνος εξάντλησης του υδροφορέα, αν η συνολικά αντλούμενη παροχή QΣ είναι μικρότερη από {Qtot_depl[dataset]}."
    info_text_gr6 = f"5-Προκαλείται όμως σημαντική πτώση στάθμης του πιεζομετρικού φορτίου, αν η QΣ είναι μεγαλύτερη από {Qtot_head[dataset]}."
    info_text_gr7 = "6-Οι απαιτούμενες θερμοκρασίες εισόδου και εξόδου φαίνονται στο σχήμα."

    """Να γίνει και στα αγγλικά"""

    # English translations
    info_text_en1 = "Complete the sketch of the heating system of residential complexes A, B, and greenhouses Γ shown below. It's given that:"
    info_text_en1_1 = "Complete the sketch of the heating system of the residential complex A shown below. It's given that:"
    info_text_en1_2 = "Complete the sketch of the heating system of residential complexes A, B shown below. It's given that:"
    info_text_en1_3 = "Complete the sketch of the heating system of residential complexes A, B, C and greenhouses D shown below. It's given that:"

    info_text_en2 = "1-The temperature of geothermal water is 85 °C."
    info_text_en3 = "2-Its quality is good."
    info_text_en4 = f"3-The required hot water supply is equal to {Qhouse0_in[dataset]} and {Qhouse1_in[dataset]} for residential complexes A, B and {Qghouse0_in[dataset]} for greenhouse C."
    info_text_en4_1 = f"3-The required hot water supply is equal to {Qhouse0_in[dataset]} for residential complex A."
    info_text_en4_2 = f"3-The required hot water supply is equal to {Qhouse0_in[dataset]} and {Qhouse1_in[dataset]} for residential complexes A, B."
    info_text_en4_3 = f"3-The required hot water supply is equal to {Qhouse0_in[dataset]} and {Qhouse1_in[dataset]} and {Qhouse2_in[dataset]} for residential complexes A, B and C and {Qghouse0_in[dataset]} for greenhouse D."

    info_text_en5 = f"4-There is no risk of depleting the aquifer if the total pumped supply QΣ is less than {Qtot_depl[dataset]}."
    info_text_en6 = f"5-However, a significant drawdown in the piezometric load occurs if QΣ is less than {Qtot_head[dataset]}."
    info_text_en7 = "6-The required input and output temperatures are shown in the diagram."

    step_h = 50
    text_rect1 = pygame.Rect(info_text_x, info_text_y + 0 * step_h, info_text_width, info_text_height)
    text_rect2 = pygame.Rect(30 + info_text_x, info_text_y + 1 * step_h, info_text_width, info_text_height)
    text_rect3 = pygame.Rect(30 + info_text_x, info_text_y + 2 * step_h - 15, info_text_width, info_text_height)
    text_rect4 = pygame.Rect(30 + info_text_x, info_text_y + 3 * step_h - 25, info_text_width, info_text_height)
    text_rect5 = pygame.Rect(30 + info_text_x, info_text_y + 4 * step_h - 15, info_text_width, info_text_height)
    text_rect6 = pygame.Rect(30 + info_text_x, info_text_y + 5 * step_h - 5, info_text_width, info_text_height)
    text_rect7 = pygame.Rect(30 + info_text_x, info_text_y + 6 * step_h - 5, info_text_width, info_text_height)

    wrapped_info_text_gr1 = render_text_rect(info_text_gr1, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr1_1 = render_text_rect(info_text_gr1_1, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr1_2 = render_text_rect(info_text_gr1_2, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr1_3 = render_text_rect(info_text_gr1_3, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_gr2 = render_text_rect(info_text_gr2, font, text_rect2, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr3 = render_text_rect(info_text_gr3, font, text_rect3, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_gr4 = render_text_rect(info_text_gr4, font, text_rect4, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr4_1 = render_text_rect(info_text_gr4_1, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr4_2 = render_text_rect(info_text_gr4_2, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr4_3 = render_text_rect(info_text_gr4_3, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_gr5 = render_text_rect(info_text_gr5, font, text_rect5, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr6 = render_text_rect(info_text_gr6, font, text_rect6, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr7 = render_text_rect(info_text_gr7, font, text_rect7, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_en1 = render_text_rect(info_text_en1, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en1_1 = render_text_rect(info_text_en1_1, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en1_2 = render_text_rect(info_text_en1_2, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en1_3 = render_text_rect(info_text_en1_3, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_en2 = render_text_rect(info_text_en2, font, text_rect2, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en3 = render_text_rect(info_text_en3, font, text_rect3, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_en4 = render_text_rect(info_text_en4, font, text_rect4, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en4_1 = render_text_rect(info_text_en4_1, font, text_rect4, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en4_2 = render_text_rect(info_text_en4_2, font, text_rect4, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en4_3 = render_text_rect(info_text_en4_3, font, text_rect4, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_en5 = render_text_rect(info_text_en5, font, text_rect5, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en6 = render_text_rect(info_text_en6, font, text_rect6, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en7 = render_text_rect(info_text_en7, font, text_rect7, (255, 255, 255), (BLUE3), wrap=True)

    language_button = Button(language_button_x, language_button_y, language_button_width, language_button_height, "L",
                             BLUE3, WHITE)
    icon_UKflag_scaled = pygame.transform.scale(icon_UKflag, (language_button_width, language_button_height))
    icon_Greeceflag_scaled = pygame.transform.scale(icon_Greeceflag, (language_button_width, language_button_height))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if language_button.is_clicked(pygame.mouse.get_pos()):
                    language_change()
            if language == 'gr':
                if int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                        Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) > 0:
                    screen.blit(wrapped_info_text_gr1, text_rect1)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) == 0 and int(
                        Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                    screen.blit(wrapped_info_text_gr1_1, text_rect1)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                        Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                    screen.blit(wrapped_info_text_gr1_2, text_rect1)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                        Qhouse2_in[dataset]) > 0 and int(Qghouse0_in[dataset]) > 0:
                    screen.blit(wrapped_info_text_gr1_3, text_rect1)
                screen.blit(wrapped_info_text_gr2, text_rect2)
                screen.blit(wrapped_info_text_gr3, text_rect3)
                if int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                        Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) > 0:
                    screen.blit(wrapped_info_text_gr4, text_rect4)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) == 0 and int(
                        Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                    screen.blit(wrapped_info_text_gr4_1, text_rect4)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                        Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                    screen.blit(wrapped_info_text_gr4_2, text_rect4)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                        Qhouse2_in[dataset]) > 0 and int(Qghouse0_in[dataset]) > 0:
                    screen.blit(wrapped_info_text_gr4_3, text_rect4)
                screen.blit(wrapped_info_text_gr5, text_rect5)
                screen.blit(wrapped_info_text_gr6, text_rect6)
                screen.blit(wrapped_info_text_gr7, text_rect7)
                pygame.draw.rect(screen, (RED), yes_button)
                screen.blit(yes_text,
                            (screen_width // 2 - yes_text.get_width() // 2 - 100 + 150, screen_height // 2 + 280))
                pygame.draw.rect(screen, (RED), no_button)
                screen.blit(no_text,
                            (screen_width // 2 - no_text.get_width() // 2 + 100 + 150, screen_height // 2 + 280))
                screen.blit(text_surface_gr, text_rect_gr)
                screen.blit(icon1, icon1_rect)
                language_button.draw(screen)
                screen.blit(icon_UKflag_scaled, (language_button_x, language_button_y))
                drawing_grid2()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_button.collidepoint(
                            pygame.mouse.get_pos()):  # or (event.type == pygame.KEYDOWN and (event.key == pygame.K_y or event.key == pygame.K_Y)):
                        screen.fill(BLUE)
                        rw_existence = True  # Use single '=' for assignment
                        return  # Exit the function to start the game
                    elif no_button.collidepoint(pygame.mouse.get_pos()):  # or pygame.key.get_pressed()[pygame.K_y]:
                        screen.fill(BLUE)
                        rw_existence = False  # Use single '=' for assignment
                        return  # Exit the function to start the game
            elif language == 'en':
                if int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                        Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) > 0:
                    screen.blit(wrapped_info_text_en1, text_rect1)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) == 0 and int(
                        Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                    screen.blit(wrapped_info_text_en1_1, text_rect1)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                        Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                    screen.blit(wrapped_info_text_en1_2, text_rect1)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                        Qhouse2_in[dataset]) > 0 and int(Qghouse0_in[dataset]) > 0:
                    screen.blit(wrapped_info_text_en1_3, text_rect1)
                screen.blit(wrapped_info_text_en2, text_rect2)
                screen.blit(wrapped_info_text_en3, text_rect3)
                if int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                        Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) > 0:
                    screen.blit(wrapped_info_text_en4, text_rect4)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) == 0 and int(
                        Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                    screen.blit(wrapped_info_text_en4_1, text_rect4)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                        Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                    screen.blit(wrapped_info_text_en4_2, text_rect4)
                elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                        Qhouse2_in[dataset]) > 0 and int(Qghouse0_in[dataset]) > 0:
                    screen.blit(wrapped_info_text_en4_3, text_rect4)
                screen.blit(wrapped_info_text_en5, text_rect5)
                screen.blit(wrapped_info_text_en6, text_rect6)
                screen.blit(wrapped_info_text_en7, text_rect7)
                pygame.draw.rect(screen, (RED), yes_button)
                screen.blit(yes_text,
                            (screen_width // 2 - yes_text.get_width() // 2 - 100 + 150, screen_height // 2 + 280))
                pygame.draw.rect(screen, (RED), no_button)
                screen.blit(no_text,
                            (screen_width // 2 - no_text.get_width() // 2 + 100 + 150, screen_height // 2 + 280))
                screen.blit(text_surface_en, text_rect_en)
                screen.blit(icon1, icon1_rect)
                language_button.draw(screen)
                screen.blit(icon_Greeceflag_scaled, (language_button_x, language_button_y))
                drawing_grid2()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_button.collidepoint(
                            pygame.mouse.get_pos()):  # or (event.type == pygame.KEYDOWN and (event.key == pygame.K_y or event.key == pygame.K_Y)):
                        screen.fill(BLUE)
                        rw_existence = True  # Use single '=' for assignment
                        return  # Exit the function to start the game
                    elif no_button.collidepoint(pygame.mouse.get_pos()):  # or pygame.key.get_pressed()[pygame.K_y]:
                        screen.fill(BLUE)
                        rw_existence = False  # Use single '=' for assignment
                        return  # Exit the function to start the game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                    screen.fill(BLUE)
                    rw_existence = True  # Use single '=' for assignment
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                    screen.fill(BLUE)
                    rw_existence = False  # Use single '=' for assignment
                    return

        pygame.display.flip()


def combined_start_function():
    global rw_existence
    display_start_menu()
    username_to_info_and_start()
    screen.fill(BLUE)
    pygame.display.update()
    initialize_grid()
    pygame.display.update()
def combined_start_function_RE():
    global rw_existence
    initialising_the_values()
    username_to_info_and_start()
    print(Q)
    print(Starting_Q)
    print(dataset)
    screen.fill(BLUE)
    pygame.display.update()
    initialize_grid()
    pygame.display.update()
def combined_start_function_RE_2():
    global rw_existence
    display_start_menu()
    initialising_the_values()
    username_to_info_and_start()
    print(Q)
    print(Starting_Q)
    print(dataset)
    screen.fill(BLUE)
    pygame.display.update()
    initialize_grid()
    pygame.display.update()
def starting_the_puzzle():
    choose_the_starting_Q()
    choose_the_use_of_rw_well()
    game_over()
    return
def starting_the_puzzle_exam_mode():
    username_to_info_and_start_exam_mode()
    choose_the_starting_Q()
    choose_the_use_of_rw_well()
    game_over_exam_mode()
    return



def retry_after_fail():
    global things_around_up, things_around_down, things_around_left, things_around_right, things_around, number_of_items, dropdown_open, Starting_Q, pipe_section
    combined_start_function_RE()
    main_loop()
    #pygame.display.update()
    #reset_grid()
    #initialize_grid()
    #starting_the_puzzle()
    #pygame.display.update()
    #main_loop()


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
    if house2_row[dataset] > 0: grid[house2_row[dataset]][house2_col[dataset]] = icon_building3
    if greenhouse0_row[dataset] > 0: grid[greenhouse0_row[dataset]][greenhouse0_col[dataset]] = icon_greenhouse
    if greenhouse1_row[dataset] > 0: grid[greenhouse1_row[dataset]][greenhouse1_col[dataset]] = icon_greenhouse
    if rw_row[dataset] > 0 and rw_existence == True:
        grid[rw_row[dataset]][rw_col[dataset]] = icon_rw
        grid[rw_row[dataset] - 1][rw_col[dataset]] = icon_ending_spot  # solution
    else:
        grid[outflow_row[dataset]][outflow_col[dataset]] = icon_outflow  # na valoume eikonidio outflow
        grid[outflow_row[dataset] - 1][outflow_col[dataset]] = icon_ending_spot  # solution
    # What is happening in the placement_grid
    if pw_row[dataset] > 0: placement_grid[pw_row[dataset]][pw_col[dataset]] = 10
    if house0_row[dataset] > 0: placement_grid[house0_row[dataset]][house0_col[dataset]] = 11
    if house1_row[dataset] > 0: placement_grid[house1_row[dataset]][house1_col[dataset]] = 11
    if house2_row[dataset] > 0: placement_grid[house2_row[dataset]][house2_col[dataset]] = 11
    if greenhouse0_row[dataset] > 0: placement_grid[greenhouse0_row[dataset]][greenhouse0_col[dataset]] = 11
    if greenhouse1_row[dataset] > 0: placement_grid[greenhouse1_row[dataset]][greenhouse1_col[dataset]] = 11
    if rw_row[dataset] > 0 and rw_existence == True: placement_grid[rw_row[dataset]][rw_col[dataset]] = 12
    if outflow_row[dataset] > 0 and rw_existence == False:
        placement_grid[outflow_row[dataset]][
            outflow_col[dataset]] = 12
        rw_row[dataset] = outflow_row[dataset]
        rw_col[dataset] = outflow_col[dataset]


def pipe_section_grid_for_icon_house0():
    global pipe_section
    pipe_section_grid[house0_row[dataset]][house0_col[dataset]] = -11
    T_grid[house0_row[dataset]][house0_col[dataset]] = Thouse0_in[dataset], Thouse0_out[dataset]
    Q_grid[house0_row[dataset]][house0_col[dataset]] = float(Qhouse0_in[dataset])
    # Q_grid[house0_row[dataset]][house0_col[dataset]] =
    font = pygame.font.Font(info_font, 15)
    text_content1 = f"T_in = {int(Thouse0_in[dataset])}"
    text_content2 = f"T_out = {int(Thouse0_out[dataset])}"
    text_content3 = f"Q_in = {int(Qhouse0_in[dataset])}"
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
    global heat_help_h0
    try:
        if max(T_grid[house0_row[dataset]][house0_col[dataset]]) > T_grid[house0_row[dataset] - 1][
            house0_col[dataset]] and \
                T_grid[house0_row[dataset] - 1][house0_col[dataset]] != 0:
            heat_help_h0 = float(
                (max(T_grid[house0_row[dataset]][house0_col[dataset]]) - T_grid[house0_row[dataset] - 1][
                    house0_col[dataset]]) * aux_cost[dataset])
            return heat_help_h0
        else:
            heat_help_h0 = 0
    except TypeError:
        heat_help_h0 = 0


def pipe_section_grid_for_icon_house1():
    global pipe_section
    pipe_section_grid[house1_row[dataset]][house1_col[dataset]] = -11
    T_grid[house1_row[dataset]][house1_col[dataset]] = Thouse1_in[dataset], Thouse1_out[dataset]
    Q_grid[house1_row[dataset]][house1_col[dataset]] = float(Qhouse1_in[dataset])
    font = pygame.font.Font(info_font, 15)
    text_content1 = f"T_in = {int(Thouse1_in[dataset])}"
    text_content2 = f"T_out = {int(Thouse1_out[dataset])}"
    text_content3 = f"Q_in = {int(Qhouse1_in[dataset])}"
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
    global house1_executed, heat_help_h1
    try:
        if max(T_grid[house1_row[dataset]][house1_col[dataset]]) > T_grid[house1_row[dataset] - 1][
            house1_col[dataset]] and \
                T_grid[house1_row[dataset] - 1][house1_col[dataset]] != 0:
            heat_help_h1 = float(
                (max(T_grid[house1_row[dataset]][house1_col[dataset]]) - T_grid[house1_row[dataset] - 1][
                    house1_col[dataset]]) * aux_cost[dataset])
        else:
            heat_help_h1 = 0
    except TypeError:
        heat_help_h1 = 0


def pipe_section_grid_for_icon_house2():
    global pipe_section
    pipe_section_grid[house2_row[dataset]][house2_col[dataset]] = -11
    T_grid[house2_row[dataset]][house2_col[dataset]] = Thouse2_in[dataset], Thouse2_out[dataset]
    Q_grid[house2_row[dataset]][house2_col[dataset]] = float(Qhouse2_in[dataset])
    font = pygame.font.Font(info_font, 15)
    text_content1 = f"T_in = {int(Thouse2_in[dataset])}"
    text_content2 = f"T_out = {int(Thouse2_out[dataset])}"
    text_content3 = f"Q_in = {int(Qhouse2_in[dataset])}"
    text_surface1 = font.render(text_content1, True, (255, 255, 255))  # White text color
    text_position1 = (875, 125)  # Position to render the text
    text_surface2 = font.render(text_content2, True, (255, 255, 255))  # White text color
    text_position2 = (875, 150)  # Position to render the text
    text_surface3 = font.render(text_content3, True, (255, 255, 255))  # White text color
    text_position3 = (875, 175)  # Position to render the text
    new_width = 40
    new_height = 40
    icon_building3_resized = pygame.transform.scale(icon_building3, (new_width, new_height))  # "To icon 3 θεωριτικά"
    screen.blit(icon_building3_resized, (825, 138))
    screen.blit(text_surface1, text_position1)
    screen.blit(text_surface2, text_position2)
    screen.blit(text_surface3, text_position3)


def budget_calculator_for_icon_house2():
    global house2_executed, heat_help_h2
    try:
        if max(T_grid[house2_row[dataset]][house2_col[dataset]]) > T_grid[house2_row[dataset] - 1][
            house2_col[dataset]] and \
                T_grid[house2_row[dataset] - 1][house2_col[dataset]] != 0:
            heat_help_h2 = float(
                (max(T_grid[house2_row[dataset]][house2_col[dataset]]) - T_grid[house2_row[dataset] - 1][
                    house2_col[dataset]]) * aux_cost[dataset])
        else:
            heat_help_h2 = 0
    except TypeError:
        heat_help_h2 = 0


def pipe_section_grid_for_icon_greenhouse0():
    global pipe_section
    pipe_section_grid[greenhouse0_row[dataset]][greenhouse0_col[dataset]] = -12
    T_grid[greenhouse0_row[dataset]][greenhouse0_col[dataset]] = Tgreenhouse0_in[dataset], Tgreenhouse0_out[dataset]
    Q_grid[greenhouse0_row[dataset]][greenhouse0_col[dataset]] = float(Qghouse0_in[dataset])
    font = pygame.font.Font(info_font, 15)
    text_content1 = f"T_in = {int(Tgreenhouse0_in[dataset])}"
    text_content2 = f"T_out = {int(Tgreenhouse0_out[dataset])}"
    text_content3 = f"Q_in = {int(Qghouse0_in[dataset])}"
    text_surface1 = font.render(text_content1, True, (255, 255, 255))  # White text color
    text_position1 = (675, 125)  # Position to render the text
    text_surface2 = font.render(text_content2, True, (255, 255, 255))  # White text color
    text_position2 = (675, 150)  # Position to render the text
    text_surface3 = font.render(text_content3, True, (255, 255, 255))  # White text color
    text_position3 = (675, 175)  # Position to render the text
    new_width = 40
    new_height = 40
    icon_greenhouse_resized = pygame.transform.scale(icon_greenhouse, (new_width, new_height))
    screen.blit(icon_greenhouse_resized, (625, 138))
    screen.blit(text_surface1, text_position1)
    screen.blit(text_surface2, text_position2)
    screen.blit(text_surface3, text_position3)


def budget_calculator_for_icon_greenhouse0():
    global ghouse0_executed, heat_help_g0
    try:
        if max(T_grid[greenhouse0_row[dataset]][greenhouse0_col[dataset]]) > T_grid[greenhouse0_row[dataset] - 1][
            greenhouse0_col[dataset]] and \
                T_grid[greenhouse0_row[dataset] - 1][greenhouse0_col[dataset]] != 0:
            heat_help_g0 = float(
                (max(T_grid[greenhouse0_row[dataset]][greenhouse0_col[dataset]]) - T_grid[greenhouse0_row[dataset] - 1][
                    greenhouse0_col[dataset]]) * aux_cost[dataset])
        else:
            heat_help_g0 = 0
    except TypeError:
        heat_help_g0 = 0


def pipe_section_grid_for_icon_greenhouse1():
    global pipe_section
    pipe_section_grid[greenhouse1_row[dataset]][greenhouse1_col[dataset]] = -12
    T_grid[greenhouse1_row[dataset]][greenhouse1_col[dataset]] = Tgreenhouse1_in[dataset], Tgreenhouse1_out[dataset]
    Q_grid[greenhouse1_row[dataset]][greenhouse1_col[dataset]] = float(Qghouse1_in[dataset])
    font = pygame.font.Font(info_font, 15)
    text_content1 = f"T_in = {int(Tgreenhouse1_in[dataset])}"
    text_content2 = f"T_out = {int(Tgreenhouse1_out[dataset])}"
    text_content3 = f"Q_in = {int(Qghouse1_in[dataset])}"
    text_surface1 = font.render(text_content1, True, (255, 255, 255))  # White text color
    text_position1 = (875, 225)  # Position to render the text
    text_surface2 = font.render(text_content2, True, (255, 255, 255))  # White text color
    text_position2 = (875, 250)  # Position to render the text
    text_surface3 = font.render(text_content3, True, (255, 255, 255))  # White text color
    text_position3 = (875, 275)  # Position to render the text
    new_width = 40
    new_height = 40
    icon_greenhouse_resized = pygame.transform.scale(icon_greenhouse, (new_width, new_height))
    screen.blit(icon_greenhouse_resized, (825, 238))
    screen.blit(text_surface1, text_position1)
    screen.blit(text_surface2, text_position2)
    screen.blit(text_surface3, text_position3)


def budget_calculator_for_icon_greenhouse1():
    global ghouse1_executed, heat_help_g1
    try:
        if max(T_grid[greenhouse1_row[dataset]][greenhouse1_col[dataset]]) > T_grid[greenhouse1_row[dataset] - 1][
            greenhouse1_col[dataset]] and \
                T_grid[greenhouse1_row[dataset] - 1][greenhouse1_col[dataset]] != 0:
            heat_help_g1 = float(
                (max(T_grid[greenhouse1_row[dataset]][greenhouse1_col[dataset]]) - T_grid[greenhouse1_row[dataset] - 1][
                    greenhouse1_col[dataset]]) * aux_cost[dataset])
        else:
            heat_help_g1 = 0
    except TypeError:
        heat_help_g1 = 0


def info_ghouse_blue_square():
    # Draw a blue rectangle background
    rect_x = 610
    rect_y = 0
    rect_width = 390  # Adding a little extra for padding
    rect_height = 330
    pygame.draw.rect(screen, BLUE, (rect_x, rect_y, rect_width, rect_height))


def tip_button_main_game_click():
    global tip_button_box
    transparent_width = 330
    transparent_height = 250
    tip_button_box = not tip_button_box
    info_text1 = "How to use triplets."
    info_text2 = "If you want to combine or split Q use these icons icons"
    info_text3 = "Be careful."
    info_text4 = "To split 1 Q set it up like this, 1 should split to 2"
    info_text5 = "To combine 2 Qs they must be set up like this, 2 come and add to 1"
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
    icon5 = pygame.transform.scale(icon_tripletqsplit, (25, 25))
    icon6 = pygame.transform.scale(icon_tripletqcombine1, (25, 25))
    icon7 = pygame.transform.scale(icon_tripletqcombine2, (25, 25))
    icon8 = pygame.transform.scale(icon_tripletqcombine3, (25, 25))

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
        transparent_surface.blit(icon5, (205 - 50, 163))
        transparent_surface.blit(icon6, (175 - 50, 213))
        transparent_surface.blit(icon7, (205 - 50, 213))
        transparent_surface.blit(icon8, (235 - 50, 213))
        screen.blit(transparent_surface, (650, 400))

        pygame.display.update()
    elif tip_button_box == False:
        pygame.draw.rect(screen, BLUE, (650, 400, 100, 250))
        render_q2_dictionary(Q2, T, screen)


transparent_surface_visible = False


def display_for_pipe_cost():
    global transparent_surface_visible
    transparent_surface_visible = not transparent_surface_visible
    transparent_surface_width = 300
    transparent_surface_height = 250
    font = pygame.font.Font(info_font, 16)
    print("I was pressed")
    simple_text_1 = f"cost = {int(simple_pipe_cost[dataset])}"
    simple_text = font.render(simple_text_1, True, WHITE)
    cost_text_2 = f"cost = {int(corner_pipe_cost[dataset])}"
    corner_text = font.render(cost_text_2, True, WHITE)
    cost_text_3 = f"cost = {int(triplet_pipe_cost[dataset])}"
    triplet_text = font.render(cost_text_3, True, WHITE)

    transparent_surface = pygame.Surface((transparent_surface_width, transparent_surface_height), pygame.SRCALPHA)
    pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
    icon1 = pygame.transform.scale(icons[0], (25, 25))
    icon2 = pygame.transform.scale(icons[1], (25, 25))
    icon3 = pygame.transform.scale(icons[2], (25, 25))
    icon5 = pygame.transform.scale(icons[4], (25, 25))
    icon4 = pygame.transform.scale(icons[3], (25, 25))
    icon6 = pygame.transform.scale(icons[5], (25, 25))
    icon7 = pygame.transform.scale(icons[6], (25, 25))
    icon8 = pygame.transform.scale(icons[7], (25, 25))
    icon9 = pygame.transform.scale(icons[8], (25, 25))
    icon10 = pygame.transform.scale(icons[9], (25, 25))
    if transparent_surface_visible == True:
        transparent_surface.blit(icon1, (20, 20))
        transparent_surface.blit(icon2, (20 + 40, 20))
        transparent_surface.blit(simple_text, (50 + 80, 20))
        transparent_surface.blit(icon3, (20, 100))
        transparent_surface.blit(icon4, (20 + 40, 100))
        transparent_surface.blit(icon5, (20 + 80, 100))
        transparent_surface.blit(icon6, (20 + 120, 100))
        transparent_surface.blit(corner_text, (50 + 160, 100))
        transparent_surface.blit(icon7, (20, 180))
        transparent_surface.blit(icon8, (20 + 40, 180))
        transparent_surface.blit(icon9, (20 + 80, 180))
        transparent_surface.blit(icon10, (20 + 120, 180))
        transparent_surface.blit(triplet_text, (50 + 160, 180))
        screen.blit(transparent_surface, (650, 350))
    elif (transparent_surface_visible == False) : #or (event.type == pygame.MOUSEBUTTONDOWN)
        pygame.draw.rect(screen, BLUE, (650, 350, 300, 250))
        render_q2_dictionary(Q2, T, screen)
        return


def budget_calculator():  # #problem
    global icon_index, budget, heat_help_h0, heat_help_h1, heat_help_h2, heat_help_g0, heat_help_g1, budget_calculated, extraction_cost, Starting_Q

    new_width = 40
    new_height = 40
    font = pygame.font.Font(None, 30)

    if house0_row[dataset] > 0: budget_calculator_for_icon_house0()
    if house1_row[dataset] > 0: budget_calculator_for_icon_house1()
    if house2_row[dataset] > 0: budget_calculator_for_icon_house2()
    if greenhouse0_row[dataset] > 0: budget_calculator_for_icon_greenhouse0()
    if greenhouse1_row[dataset] > 0: budget_calculator_for_icon_greenhouse1()

    flat_placement_grid = [num for row in placement_grid for num in row]
    pipe_type_counter = Counter(flat_placement_grid)

    Starting_Q_affection = Starting_Q * float(extraction_cost[dataset])
    cost_calculated = (Starting_Q_affection +
                                      ((pipe_type_counter[0] + pipe_type_counter[1]) * 50) +
                                      ((pipe_type_counter[2] + pipe_type_counter[3] + pipe_type_counter[4] +
                                        pipe_type_counter[5]) * 60) +
                                      ((pipe_type_counter[6] + pipe_type_counter[7] + pipe_type_counter[8] +
                                        pipe_type_counter[9]) * 100) +
                                      (heat_help_h0 + heat_help_h1 + heat_help_h2 + heat_help_g0 + heat_help_g1))

    #if icon_index != 100:
    for number in range(10):
        count = pipe_type_counter.get(number, 0)
        #print(f"Number {number} occurs {count} times.")
        #print(count)
    budget_calculated = budget - cost_calculated

    text_content = f"Budget = {'{:.0f}'.format(float(budget_calculated))}"
    text_surface = font.render(text_content, True, WHITE)  # White text color

    # Get dimensions of the text surface
    text_width, text_height = text_surface.get_size()

    # Draw a blue rectangle background
    rect_x = 0
    rect_y = 660
    rect_width = text_width + 460  # Adding a little extra for padding
    rect_height = 150
    pygame.draw.rect(screen, BLUE, (rect_x, rect_y, rect_width, rect_height))  # change

    # Position to render the text and icon
    text_position = (80, 680)
    icon_dollar_sign_resized = pygame.transform.scale(icon_dollar_sign, (new_width, new_height))

    screen.blit(icon_dollar_sign_resized, (40, 668))
    screen.blit(text_surface, text_position)
    pygame.display.update()


def red_outlines():
    try:
        if house0_row[dataset] > 0 and (
                max(T_grid[house0_row[dataset]][house0_col[dataset]]) > T_grid[house0_row[dataset] - 1][
            house0_col[dataset]] and \
                T_grid[house0_row[dataset] - 1][house0_col[dataset]] != 0):
            row1 = house0_row[dataset]
            col1 = house0_col[dataset]
            x_pos = 64 + (col1) * 32
            y_pos = 64 + (row1 - 1) * 32
            pygame.draw.rect(screen, RED, (x_pos, y_pos, 32, 32), 2)
        if house1_row[dataset] > 0 and (
                max(T_grid[house1_row[dataset]][house1_col[dataset]]) > T_grid[house1_row[dataset] - 1][
            house1_col[dataset]] and \
                T_grid[house1_row[dataset] - 1][house1_col[dataset]] != 0):
            row1 = house1_row[dataset]
            col1 = house1_col[dataset]
            x_pos = 64 + (col1) * 32
            y_pos = 64 + (row1 - 1) * 32
            pygame.draw.rect(screen, RED, (x_pos, y_pos, 32, 32), 2)

        if house2_row[dataset] > 0 and (
                max(T_grid[house2_row[dataset]][house2_col[dataset]]) > T_grid[house2_row[dataset] - 1][
            house2_col[dataset]] and \
                T_grid[house2_row[dataset] - 1][house2_col[dataset]] != 0):
            row1 = house2_row[dataset]
            col1 = house2_col[dataset]
            x_pos = 64 + (col1) * 32
            y_pos = 64 + (row1 - 1) * 32
            pygame.draw.rect(screen, RED, (x_pos, y_pos, 32, 32), 2)

        if greenhouse0_row[dataset] > 0 and (
                max(T_grid[greenhouse0_row[dataset]][greenhouse0_col[dataset]]) > T_grid[greenhouse0_row[dataset] - 1][
            greenhouse0_col[dataset]] and \
                T_grid[greenhouse0_row[dataset] - 1][greenhouse0_col[dataset]] != 0):
            row1 = greenhouse0_row[dataset]
            col1 = greenhouse0_col[dataset]
            x_pos = 64 + (col1) * 32
            y_pos = 64 + (row1 - 1) * 32
            pygame.draw.rect(screen, RED, (x_pos, y_pos, 32, 32), 2)

        if greenhouse1_row[dataset] > 0 and (
                max(T_grid[greenhouse1_row[dataset]][greenhouse1_col[dataset]]) > T_grid[greenhouse1_row[dataset] - 1][
            greenhouse1_col[dataset]] and \
                T_grid[greenhouse1_row[dataset] - 1][greenhouse1_col[dataset]] != 0):
            row1 = greenhouse1_row[dataset]
            col1 = greenhouse1_row[dataset]
            x_pos = 64 + (col1) * 32
            y_pos = 64 + (row1 - 1) * 32
            pygame.draw.rect(screen, RED, (x_pos, y_pos, 32, 32), 2)
    except TypeError:
        return


def right_click_grid_cell_info(event, row, col):
    if 64 <= event.pos[0] <= 544 + 64 and 64 <= event.pos[1] <= 544 + 64 and placement_grid[row][col] != -1:
        transparent_surface = pygame.Surface((150, 100), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
        font = pygame.font.Font(None, 15)
        # text1 = font.render(f" Pipe_Section:{pipe_section_grid[row][col] + 1}", True, WHITE)
        if placement_grid[row][col] != -1 and placement_grid[row + 1][col] >= 9 and max(T_grid[row + 1][col]) > \
                T_grid[row][col]:
            text1 = font.render(f" Pipe_Section:{pipe_section_grid[row][col] + 1}", True, WHITE)
            text2 = font.render(f" T: {T_grid[row][col]}", True, WHITE)
            text3 = font.render(f" aux_cost {heat_help_h0}", True, WHITE)
            transparent_surface.blit(text1, (0, 10))
            transparent_surface.blit(text2, (0, 30))
            transparent_surface.blit(text3, (0, 50))
        if 0 <= placement_grid[row][col] <= 1:
            text1 = font.render(f" Pipe_Section:{pipe_section_grid[row][col] + 1}", True, WHITE)
            text2 = font.render(f" T: {T_grid[row][col]}", True, WHITE)
            text3_simple = font.render(f" pipe_cost = {int(simple_pipe_cost[dataset])}", True, WHITE)
            transparent_surface.blit(text1, (0, 10))
            transparent_surface.blit(text2, (0, 30))
            transparent_surface.blit(text3_simple, (0, 50))
        if 2 <= placement_grid[row][col] <= 5:
            text2 = font.render(f" T: {T_grid[row][col]}", True, WHITE)
            text1 = font.render(f" Pipe_Section:{pipe_section_grid[row][col] + 1}", True, WHITE)
            text3_corner = font.render(f" pipe_cost = {int(corner_pipe_cost[dataset])}", True, WHITE)
            transparent_surface.blit(text1, (0, 10))
            transparent_surface.blit(text2, (0, 30))
            transparent_surface.blit(text3_corner, (0, 50))
        if 6 <= placement_grid[row][col] <= 9:
            text1 = font.render(f" Pipe_Section:{pipe_section_grid[row][col] + 1}", True, WHITE)
            text2 = font.render(f" T: {T_grid[row][col]}", True, WHITE)
            text3_triplet = font.render(f" pipe_cost = {int(triplet_pipe_cost[dataset])}", True, WHITE)
            transparent_surface.blit(text1, (0, 10))
            transparent_surface.blit(text2, (0, 30))
            transparent_surface.blit(text3_triplet, (0, 50))
        if pipe_section_grid[row][col] < -10:
            text1 = font.render(f"Q_in = {int(Qhouse0_in[dataset])}", True, WHITE)
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
    global Starting_Q, pipe_section, row, col, Starting_T, budget

    for i in range((grid_size - 1)):
        for j in range((grid_size - 1)):
            # if grid[i][j] is not None:  # and grid[i][j] != icon_pw and grid[i][j] != icon_building1 and grid[i][j] != icon_building2 and grid[i][j] != icon_greenhouse and grid[i][j] != icon_rw:
            grid[i][j] = None
            placement_grid[i][j] = -1
            Q_grid[i][j] = -2
            T_grid[i][j] = 0
            pipe_section_grid[i][j] = 0


    Q.clear()
    T.clear()
    Q2.clear()
    T[pipe_section] = []
    pipe_section = 0
    Q_grid[pw_row[dataset] - 1][pw_col[dataset]] = int(Starting_Q)
    T_grid[pw_row[dataset]][pw_col[dataset]] = Starting_T
    T[pipe_section] = [T_grid[pw_row[dataset] - 1][pw_col[dataset]]]
    Q[pipe_section] = [Q_grid[pw_row[dataset] - 1][pw_col[dataset]]]
    budget = player_budget[dataset]
    row = pw_row - 1
    col = pw_col
    # pygame.draw.rect(screen, BLUE, (screen_width - 395, screen_height - 400, 400, 400))


def undo():
    if undo_stack:
        # Retrieve the last state from the undo stack
        global row, col, icon_index, pipe_section, placement_grid, Q_grid, T_grid, pipe_section_grid, T, Q, Q2
        row, col, icon_index = undo_stack.pop()
        previous_version = grid_versions.pop()
        value1 = pipe_section_grid[row][col]
        value2 = T_grid[row][col]

        # Update each grid with the previous state
        grid[row][col] = None
        placement_grid = previous_version['placement_grid']
        Q_grid = previous_version['Q_grid']
        T_grid = previous_version['T_grid']
        pipe_section_grid = previous_version['pipe_section_grid']

        flat_pipe_section_grid = [num for row in pipe_section_grid for num in row]
        pipe_section_grid_values = set(flat_pipe_section_grid)
        print(pipe_section_grid_values)

        """if value1 in list(Q.keys()):
            if value1 not in pipe_section_grid_values:
                del Q[value1]"""
        for key in list(Q.keys()):
            if key not in flat_pipe_section_grid:
                del Q[key]
                pipe_section -= 1

        for key in list(T.keys()):
            if key not in flat_pipe_section_grid:
                del T[key]
            elif value1 in T and value1 in pipe_section_grid_values:
                if len(T[value1]) > 1:
                    # Remove value2 from the array associated with value1
                    T[value1] = [item for item in T[value1] if item != value2]
                else:
                    T[value1] = [
                        value2 + Tloss_pipe[dataset]]  # πρέπει να μπει το T_losspipe αλλά αν μπει βγαίνει error

        render_q2_dictionary(Q2, T, screen)
        """if value1 in list(T.keys()) and value1 not in pipe_section_grid_values:
            del T[value1]
        elif value1 in T and value1 in pipe_section_grid_values:
            if len(T[value1]) > 1:
                # Remove value2 from the array associated with value1
                T[value1] = [item for item in T[value1] if item != value2]"""

        """flat_pipe_section_grid = [num for row in pipe_section_grid for num in row]
        pipe_section_grid_values = set(flat_pipe_section_grid)

        flat_T_grid = [num for row in T_grid for num in row]
        T_grid_values = set(flat_T_grid)
        print(f" These are {pipe_section_grid_values}")
        for key in list(Q.keys()):
            if key not in flat_pipe_section_grid:
                del Q[key]
        for key in list(T.keys()):
            if key not in flat_pipe_section_grid:
                del T[key]
            else:
                T[key] = [value for value in T[key] if value in T_grid_values]"""  # method that didn't work, keep for safety
        print(f" T: {T}")
        print(f" Q: {Q}")
        print(f" Q2: {Q2}")
        """T = T.popitem()
        Q = Q.popitem()
        Q2 = Q2.popitem()"""
        for row in placement_grid:
            print(row)
        for row in Q_grid:
            print(row)
        for row in T_grid:
            print(row)
        for row in pipe_section_grid:
            print(row)
        return placement_grid, Q_grid, T_grid, pipe_section_grid


def show_input_box(x, y, screen_width, screen_height, text=""):
    """Show an input box on the screen and return the player's input as an integer."""
    global pipe_section
    input_box_font = pygame.font.Font(None, 30)
    active = True
    if enter_input_sound is not None:
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
                # elif event.key == pygame.K_ESCAPE:
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        input_box_x = 680
        input_box_y = 255
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

        # Determine cursor position based on text width
        cursor_x = input_text_rect.right + 2
        cursor_y = input_text_rect.y + 2

        # Calculate cursor height to match text height
        cursor_height = input_text_rect.height - 4

        # Toggle cursor visibility (blinking effect)
        if pygame.time.get_ticks() % 1000 < 500:  # Adjust blinking speed
            pygame.draw.rect(screen, BLACK, (cursor_x, cursor_y, 2, cursor_height))  # Draw cursor

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
    if enter_input_sound is not None:
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

        # Determine cursor position based on text width
        cursor_x = input_text_rect.right + 2
        cursor_y = input_text_rect.y + 2

        # Calculate cursor height to match text height
        cursor_height = input_text_rect.height - 4

        # Toggle cursor visibility (blinking effect)
        if pygame.time.get_ticks() % 1000 < 500:  # Adjust blinking speed
            pygame.draw.rect(screen, BLACK, (cursor_x, cursor_y, 2, cursor_height))  # Draw cursor

        # Draw the input label
        input_label_text = input_label_font.render(f"Username", True, WHITE)
        input_label_text_rect = input_label_text.get_rect(center=(screen_width // 2 + 480, input_box_y - 25))
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
    if enter_input_sound is not None:
        enter_input_sound.play(0)
    input_label_font = pygame.font.Font(info_font, 30)  # New font for the input label
    submitted = False  # Initialize the variable here

    font = pygame.font.Font(info_font, 20)
    font2 = pygame.font.Font(info_font, 24)
    icon1 = pygame.transform.scale(icon_pw, (40, 40))
    icon1_rect = icon1.get_rect(center=(850, 490))  # Adjust position as needed
    info_text_width = 900  # Change this if you want a different width for the text box
    info_text_height = 500  # Change this if you want a different height for the text box
    info_text_x = 50
    info_text_y = 40

    # Create the text rectangle and render the wrapped text
    font = pygame.font.Font(info_font, 18)
    # Greek translations
    info_text_gr1 = "Συμπληρώστε το σκαρίφημα του συστήματος θέρμανσης των συγκροτημάτων κατοικιών Α, Β και θερμοκηπίων Γ του σχήματος. Δίνεται ότι:"
    info_text_gr1_1 = "Συμπληρώστε το σκαρίφημα του συστήματος θέρμανσης του συγκροτήματος κατοικιών Α του σχήματος. Δίνεται ότι:"
    info_text_gr1_2 = "Συμπληρώστε το σκαρίφημα του συστήματος θέρμανσης των συγκροτημάτων κατοικιών Α, Β του σχήματος. Δίνεται ότι:"
    info_text_gr1_3 = "Συμπληρώστε το σκαρίφημα του συστήματος θέρμανσης των συγκροτημάτων κατοικιών Α, Β, Γ και θερμοκηπίων Δ του σχήματος. Δίνεται ότι:"

    info_text_gr2 = "1-Η θερμοκρασία του γεωθερμικού νερού είναι 85 °C."
    info_text_gr3 = "2-Η ποιότητά του είναι καλή."
    info_text_gr4 = f"3-Η απαιτούμενη παροχή θερμού νερού είναι ίση με {Qhouse0_in[dataset]} και {Qhouse1_in[dataset]} για τα συγκροτήματα κατοικιών Α, Β και {Qghouse0_in[dataset]} για το θερμοκήπιο Γ."
    info_text_gr4_1 = f"3-Η απαιτούμενη παροχή θερμού νερού είναι ίση με {Qhouse0_in[dataset]} για τα συγκρότημα κατοικιών Α."
    info_text_gr4_2 = f"3-Η απαιτούμενη παροχή θερμού νερού είναι ίση με {Qhouse0_in[dataset]} και {Qhouse1_in[dataset]} για τα συγκροτήματα κατοικιών Α, Β."
    info_text_gr4_3 = f"3-Η απαιτούμενη παροχή θερμού νερού είναι ίση με {Qhouse0_in[dataset]} και {Qhouse1_in[dataset]} και {Qhouse2_in[dataset]} για τα συγκροτήματα κατοικιών Α, Β και Γ αντίστοιχα και {Qghouse0_in[dataset]} για το θερμοκήπιο Δ."

    info_text_gr5 = f"4-Δεν υπάρχει κίνδυνος εξάντλησης του υδροφορέα, αν η συνολικά αντλούμενη παροχή QΣ είναι μικρότερη από {Qtot_depl[dataset]}."
    info_text_gr6 = f"5-Προκαλείται όμως σημαντική πτώση στάθμης του πιεζομετρικού φορτίου, αν η QΣ είναι μικρότερη από {Qtot_head[dataset]}."
    info_text_gr7 = "6-Οι απαιτούμενες θερμοκρασίες εισόδου και εξόδου φαίνονται στο σχήμα."

    # English translations
    info_text_en1 = "Complete the sketch of the heating system of residential complexes A, B, and greenhouses Γ shown below. It's given that:"
    info_text_en1_1 = "Complete the sketch of the heating system of the residential complex A shown below. It's given that:"
    info_text_en1_2 = "Complete the sketch of the heating system of residential complexes A, B shown below. It's given that:"
    info_text_en1_3 = "Complete the sketch of the heating system of residential complexes A, B, C and greenhouses D shown below. It's given that:"

    info_text_en2 = "1-The temperature of geothermal water is 85 °C."
    info_text_en3 = "2-Its quality is good."
    info_text_en4 = f"3-The required hot water supply is equal to {Qhouse0_in[dataset]} and {Qhouse1_in[dataset]} for residential complexes A, B and {Qghouse0_in[dataset]} for greenhouse C."
    info_text_en4_1 = f"3-The required hot water supply is equal to {Qhouse0_in[dataset]} for residential complex A."
    info_text_en4_2 = f"3-The required hot water supply is equal to {Qhouse0_in[dataset]} and {Qhouse1_in[dataset]} for residential complexes A, B."
    info_text_en4_3 = f"3-The required hot water supply is equal to {Qhouse0_in[dataset]} and {Qhouse1_in[dataset]} and {Qhouse2_in[dataset]} for residential complexes A, B and C and {Qghouse0_in[dataset]} for greenhouse D."

    info_text_en5 = f"4-There is no risk of depleting the aquifer if the total pumped supply QΣ is less than {Qtot_depl[dataset]}."
    info_text_en6 = f"5-However, a significant drawdown in the piezometric load occurs if QΣ is less than {Qtot_head[dataset]}."
    info_text_en7 = "6-The required input and output temperatures are shown in the diagram."

    step_h = 50
    text_rect1 = pygame.Rect(info_text_x, info_text_y + 0 * step_h, info_text_width, info_text_height)
    text_rect2 = pygame.Rect(30 + info_text_x, info_text_y + 1 * step_h, info_text_width, info_text_height)
    text_rect3 = pygame.Rect(30 + info_text_x, info_text_y + 2 * step_h - 15, info_text_width, info_text_height)
    text_rect4 = pygame.Rect(30 + info_text_x, info_text_y + 3 * step_h - 25, info_text_width, info_text_height)
    text_rect5 = pygame.Rect(30 + info_text_x, info_text_y + 4 * step_h - 15, info_text_width, info_text_height)
    text_rect6 = pygame.Rect(30 + info_text_x, info_text_y + 5 * step_h - 5, info_text_width, info_text_height)
    text_rect7 = pygame.Rect(30 + info_text_x, info_text_y + 6 * step_h - 5, info_text_width, info_text_height)

    wrapped_info_text_gr1 = render_text_rect(info_text_gr1, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr1_1 = render_text_rect(info_text_gr1_1, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr1_2 = render_text_rect(info_text_gr1_2, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr1_3 = render_text_rect(info_text_gr1_3, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_gr2 = render_text_rect(info_text_gr2, font, text_rect2, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr3 = render_text_rect(info_text_gr3, font, text_rect3, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_gr4 = render_text_rect(info_text_gr4, font, text_rect4, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr4_1 = render_text_rect(info_text_gr4_1, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr4_2 = render_text_rect(info_text_gr4_2, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr4_3 = render_text_rect(info_text_gr4_3, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_gr5 = render_text_rect(info_text_gr5, font, text_rect5, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr6 = render_text_rect(info_text_gr6, font, text_rect6, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_gr7 = render_text_rect(info_text_gr7, font, text_rect7, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_en1 = render_text_rect(info_text_en1, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en1_1 = render_text_rect(info_text_en1_1, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en1_2 = render_text_rect(info_text_en1_2, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en1_3 = render_text_rect(info_text_en1_3, font, text_rect1, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_en2 = render_text_rect(info_text_en2, font, text_rect2, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en3 = render_text_rect(info_text_en3, font, text_rect3, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_en4 = render_text_rect(info_text_en4, font, text_rect4, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en4_1 = render_text_rect(info_text_en4_1, font, text_rect4, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en4_2 = render_text_rect(info_text_en4_2, font, text_rect4, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en4_3 = render_text_rect(info_text_en4_3, font, text_rect4, (255, 255, 255), (BLUE3), wrap=True)

    wrapped_info_text_en5 = render_text_rect(info_text_en5, font, text_rect5, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en6 = render_text_rect(info_text_en6, font, text_rect6, (255, 255, 255), (BLUE3), wrap=True)
    wrapped_info_text_en7 = render_text_rect(info_text_en7, font, text_rect7, (255, 255, 255), (BLUE3), wrap=True)

    language_button = Button(language_button_x, language_button_y, language_button_width, language_button_height, "L",
                             BLUE3, WHITE)
    icon_UKflag_scaled = pygame.transform.scale(icon_UKflag, (language_button_width, language_button_height))
    icon_Greeceflag_scaled = pygame.transform.scale(icon_Greeceflag, (language_button_width, language_button_height))

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if language_button.is_clicked(pygame.mouse.get_pos()):
                    print("Click was made")
                    language_change()
                if language == 'gr':
                    if int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                            Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) > 0:
                        screen.blit(wrapped_info_text_gr1, text_rect1)
                    elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) == 0 and int(
                            Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                        screen.blit(wrapped_info_text_gr1_1, text_rect1)
                    elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                            Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                        screen.blit(wrapped_info_text_gr1_2, text_rect1)
                    elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                            Qhouse2_in[dataset]) > 0 and int(Qghouse0_in[dataset]) > 0:
                        screen.blit(wrapped_info_text_gr1_3, text_rect1)
                    screen.blit(wrapped_info_text_gr2, text_rect2)
                    screen.blit(wrapped_info_text_gr3, text_rect3)
                    if int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                            Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) > 0:
                        screen.blit(wrapped_info_text_gr4, text_rect4)
                    elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) == 0 and int(
                            Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                        screen.blit(wrapped_info_text_gr4_1, text_rect4)
                    elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                            Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                        screen.blit(wrapped_info_text_gr4_2, text_rect4)
                    elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                            Qhouse2_in[dataset]) > 0 and int(Qghouse0_in[dataset]) > 0:
                        screen.blit(wrapped_info_text_gr4_3, text_rect4)
                    screen.blit(wrapped_info_text_gr5, text_rect5)
                    screen.blit(wrapped_info_text_gr6, text_rect6)
                    screen.blit(wrapped_info_text_gr7, text_rect7)
                    screen.blit(icon1, icon1_rect)
                    screen.blit(icon_UKflag_scaled, (language_button_x, language_button_y))
                    house_and_greenhouses_info()
                elif language == 'en':
                    if int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                            Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) > 0:
                        screen.blit(wrapped_info_text_en1, text_rect1)
                    elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) == 0 and int(
                            Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                        screen.blit(wrapped_info_text_en1_1, text_rect1)
                    elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                            Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                        screen.blit(wrapped_info_text_en1_2, text_rect1)
                    elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                            Qhouse2_in[dataset]) > 0 and int(Qghouse0_in[dataset]) > 0:
                        screen.blit(wrapped_info_text_en1_3, text_rect1)
                    screen.blit(wrapped_info_text_en2, text_rect2)
                    screen.blit(wrapped_info_text_en3, text_rect3)
                    if int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                            Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) > 0:
                        screen.blit(wrapped_info_text_en4, text_rect4)
                    elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) == 0 and int(
                            Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                        screen.blit(wrapped_info_text_en4_1, text_rect4)
                    elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                            Qhouse2_in[dataset]) == 0 and int(Qghouse0_in[dataset]) == 0:
                        screen.blit(wrapped_info_text_en4_2, text_rect4)
                    elif int(Qhouse0_in[dataset]) > 0 and int(Qhouse1_in[dataset]) > 0 and int(
                            Qhouse2_in[dataset]) > 0 and int(Qghouse0_in[dataset]) > 0:
                        screen.blit(wrapped_info_text_en4_3, text_rect4)
                    screen.blit(wrapped_info_text_en5, text_rect5)
                    screen.blit(wrapped_info_text_en6, text_rect6)
                    screen.blit(wrapped_info_text_en7, text_rect7)
                    screen.blit(icon1, icon1_rect)
                    screen.blit(icon_Greeceflag_scaled, (language_button_x, language_button_y))
                    house_and_greenhouses_info()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    active = False
                    submitted = True  # Set submitted to True when Enter key is pressed
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        input_box_x = 500 + 150
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

        # Determine cursor position based on text width
        cursor_x = input_text_rect.right + 2
        cursor_y = input_text_rect.y + 2

        # Calculate cursor height to match text height
        cursor_height = input_text_rect.height - 4

        # Toggle cursor visibility (blinking effect)
        if pygame.time.get_ticks() % 1000 < 500:  # Adjust blinking speed
            pygame.draw.rect(screen, BLACK, (cursor_x, cursor_y, 2, cursor_height))  # Draw cursor

        # Draw the input label
        input_label_text = input_label_font.render(f"Starting Q:", True, WHITE)
        input_label_text_rect = input_label_text.get_rect(x=input_box_x - 150, y=input_box_y - 7.5)
        screen.blit(input_label_text, input_label_text_rect)

        drawing_grid2()

        pygame.display.update()

    # Validate the input and ask the player to redo the input if it's not a valid integer
    while True:
        try:
            return int(text)
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            text = show_input_box3(x, y, screen_width, screen_height)  # Recursively call the function to redo the input
def show_input_box_tutorial(x, y, screen_width, screen_height, text=""):
    """Show an input box on the screen and return the player's input as an integer."""
    global pipe_section
    input_box_font = pygame.font.Font(info_font, 22)
    active = True
    if enter_input_sound is not None:
        enter_input_sound.play(0)
    input_label_font = pygame.font.Font(info_font, 30)  # New font for the input label
    submitted = False  # Initialize the variable here
    gate_value_1 = None

    font = pygame.font.Font(info_font, 20)
    font2 = pygame.font.Font(info_font, 24)
    icon1 = pygame.transform.scale(icon_pw, (100, 100))
    icon1_rect = icon1.get_rect(center=(650, 600))  # Adjust position as needed
    info_text_width = 900  # Change this if you want a different width for the text box
    info_text_height = 500  # Change this if you want a different height for the text box
    info_text_x = 50
    info_text_y = 80

    # Create the text rectangle and render the wrapped text
    font = pygame.font.Font(info_font, 18)

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

        input_box_x = 500 + 150
        input_box_y = 475
        input_box_width = 150
        input_box_height = 25

        # Draw the input box
        pygame.draw.rect(screen, WHITE, (input_box_x, input_box_y+1, input_box_width, input_box_height))
        pygame.draw.rect(screen, BLACK, (input_box_x, input_box_y+1, input_box_width, input_box_height), 1)

        # Draw the input text
        input_text = input_box_font.render(text, True, BLACK)
        input_text_rect = input_text.get_rect(
            center=(input_box_x + input_box_width // 2, input_box_y + input_box_height // 2))
        screen.blit(input_text, input_text_rect)

        # Determine cursor position based on text width
        cursor_x = input_text_rect.right + 2
        cursor_y = input_text_rect.y + 2

        # Calculate cursor height to match text height
        cursor_height = input_text_rect.height - 4

        # Toggle cursor visibility (blinking effect)
        if pygame.time.get_ticks() % 1000 < 500:  # Adjust blinking speed
            pygame.draw.rect(screen, BLACK, (cursor_x, cursor_y, 2, cursor_height))  # Draw cursor

        pygame.display.update()

    # Validate the input and ask the player to redo the input if it's not a valid integer
    while True:
        try:
            gate_value_1 = int(text)
            print(gate_value_1)
            return gate_value_1
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            text = show_input_box_tutorial(x, y, screen_width, screen_height, text="")  # Recursively call the function to redo the input
def show_input_box_tutorial_2(x, y, screen_width, screen_height, text=""):
    """Show an input box on the screen and return the player's input as an integer."""
    global pipe_section
    input_box_font = pygame.font.Font(info_font, 22)
    active = True
    if enter_input_sound is not None:
        enter_input_sound.play(0)
    input_label_font = pygame.font.Font(info_font, 30)  # New font for the input label
    submitted = False  # Initialize the variable here
    gate_value_1 = None

    font = pygame.font.Font(info_font, 20)
    font2 = pygame.font.Font(info_font, 24)
    icon1 = pygame.transform.scale(icon_pw, (100, 100))
    icon1_rect = icon1.get_rect(center=(650, 600))  # Adjust position as needed
    info_text_width = 900  # Change this if you want a different width for the text box
    info_text_height = 500  # Change this if you want a different height for the text box
    info_text_x = 50
    info_text_y = 80

    # Create the text rectangle and render the wrapped text
    font = pygame.font.Font(info_font, 18)

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

        input_box_x = 680
        input_box_y = 255
        input_box_width = 100
        input_box_height = 25

        # Draw the input box
        pygame.draw.rect(screen, WHITE, (input_box_x, input_box_y, input_box_width+2, input_box_height+2))
        pygame.draw.rect(screen, BLACK, (input_box_x, input_box_y, input_box_width+2, input_box_height+2), 1)

        # Draw the input text
        input_text = input_box_font.render(text, True, BLACK)
        input_text_rect = input_text.get_rect(
            center=(input_box_x + input_box_width // 2, input_box_y + input_box_height // 2))
        screen.blit(input_text, input_text_rect)

        # Determine cursor position based on text width
        cursor_x = input_text_rect.right + 2
        cursor_y = input_text_rect.y + 2

        # Calculate cursor height to match text height
        cursor_height = input_text_rect.height - 4

        # Toggle cursor visibility (blinking effect)
        if pygame.time.get_ticks() % 1000 < 500:  # Adjust blinking speed
            pygame.draw.rect(screen, BLACK, (cursor_x, cursor_y, 2, cursor_height))  # Draw cursor

        pygame.display.update()

    # Validate the input and ask the player to redo the input if it's not a valid integer
    while True:
        try:
            gate_value_2 = int(text)
            return gate_value_2
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            text = show_input_box_tutorial_2(x, y, screen_width, screen_height, text="")  # Recursively call the function to redo the input
def show_input_box_exam_key(x, y, screen_width, screen_height, text=""):
    """Show an input box on the screen and return the player's input as an integer."""
    global pipe_section
    input_box_font = pygame.font.Font(info_font, 22)
    active = True
    if enter_input_sound is not None:
        enter_input_sound.play(0)
    input_label_font = pygame.font.Font(info_font, 30)  # New font for the input label
    submitted = False  # Initialize the variable here
    gate_value_1 = None

    font = pygame.font.Font(info_font, 20)
    font2 = pygame.font.Font(info_font, 24)
    icon1 = pygame.transform.scale(icon_pw, (100, 100))
    icon1_rect = icon1.get_rect(center=(650, 600))  # Adjust position as needed
    info_text_width = 900  # Change this if you want a different width for the text box
    info_text_height = 500  # Change this if you want a different height for the text box
    info_text_x = 50
    info_text_y = 80

    # Create the text rectangle and render the wrapped text
    font = pygame.font.Font(info_font, 18)

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

        input_box_x = 500 + 150
        input_box_y = 475
        input_box_width = 150
        input_box_height = 25

        # Draw the input box
        pygame.draw.rect(screen, WHITE, (input_box_x+2, input_box_y+2, input_box_width+1, input_box_height+1))
        pygame.draw.rect(screen, BLACK, (input_box_x+2, input_box_y+2, input_box_width+1, input_box_height+1), 1)

        # Draw the input text
        input_text = input_box_font.render(text, True, BLACK)
        input_text_rect = input_text.get_rect(
            center=(input_box_x + input_box_width // 2, input_box_y + input_box_height // 2))
        screen.blit(input_text, input_text_rect)

        # Determine cursor position based on text width
        cursor_x = input_text_rect.right + 2
        cursor_y = input_text_rect.y + 2

        # Calculate cursor height to match text height
        cursor_height = input_text_rect.height - 4

        # Toggle cursor visibility (blinking effect)
        if pygame.time.get_ticks() % 1000 < 500:  # Adjust blinking speed
            pygame.draw.rect(screen, BLACK, (cursor_x, cursor_y, 2, cursor_height))  # Draw cursor

        pygame.display.update()

    # Validate the input and ask the player to redo the input if it's not a valid integer
    while True:
        try:
            gate_value_1 = int(text)
            print(gate_value_1)
            return gate_value_1
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            text = show_input_box3(x, y, screen_width, screen_height)  # Recursively call the function to redo the input


def left_arrow_appears():
    """Display all the information that is necessary for the player to solve the problem"""
    # Change the position of the icon_down_arrow to (x=700, y=50)
    icon_left_arrow_rect = icon_left_arrow.get_rect(x=705, y=200)

    # Scale the size of the icon_down_arrow
    scaled_width = 50  # Change this to the desired width
    scaled_height = 50  # Change this to the desired height
    icon_left_arrow_scaled = pygame.transform.scale(icon_left_arrow, (scaled_width, scaled_height))

    # Draw the scaled icon_down_arrow at the new position
    screen.blit(icon_left_arrow_scaled, icon_left_arrow_rect)


def right_arrow_appears():
    """Display the right arrow icon"""
    # Change the position of the icon_right_arrow to (x=700, y=50) for the right position
    icon_right_arrow_rect = icon_right_arrow.get_rect(x=720, y=200)

    # Scale the size of the icon_right_arrow
    scaled_width = 50  # Change this to the desired width
    scaled_height = 50  # Change this to the desired height
    icon_right_arrow_scaled = pygame.transform.scale(icon_right_arrow, (scaled_width, scaled_height))

    # Draw the scaled icon_right_arrow at the new position
    screen.blit(icon_right_arrow_scaled, icon_right_arrow_rect)


def down_arrow_appears():
    """Display the down arrow icon"""
    # Change the position of the icon_down_arrow to (x=700, y=50) for the down position
    icon_down_arrow_rect = icon_down_arrow.get_rect(x=705, y=200)

    # Scale the size of the icon_down_arrow
    scaled_width = 50  # Change this to the desired width
    scaled_height = 50  # Change this to the desired height
    icon_down_arrow_scaled = pygame.transform.scale(icon_down_arrow, (scaled_width, scaled_height))

    # Draw the scaled icon_down_arrow at the new position
    screen.blit(icon_down_arrow_scaled, icon_down_arrow_rect)


def up_arrow_appears():
    """Display the up arrow icon"""
    # Change the position of the icon_up_arrow to (x=700, y=50) for the up position
    icon_up_arrow_rect = icon_up_arrow.get_rect(x=705, y=200)

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
    # Check the surrounding cells
    i = -1
    icons2rem = []
    for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        i = i + 1
        neighbor_row = row + dr
        neighbor_col = col + dc
        if (
                0 <= neighbor_row < (grid_size - 1)
                and 0 <= neighbor_col < (grid_size - 1)
                and placement_grid[neighbor_row][neighbor_col] > -1
        ):
            # = [int(num) for num in my_string.split(',')]
            icons2rem.append(na_icons[i][placement_grid[neighbor_row][neighbor_col]])
    if len(icons2rem) != 0:
        icons2rem = [int(j) for j in ",".join(icons2rem).split(',')]
        icons2rem = list(set(icons2rem))
        # print('in', icons2rem)
        for j in icons2rem:
            available_icons.remove(icons[j - 1])
        if row == 0:
            for i in [1, 4, 5, 7, 8, 9]:
                if icons[i] in available_icons:
                    available_icons.remove(icons[i])
        if col == 0:
            for i in [0, 3, 4, 6, 7, 8]:
                if icons[i] in available_icons:
                    available_icons.remove(icons[i])
        if row == 16:  # error for last row
            for i in [1, 2, 3, 6, 7, 9]:
                if icons[i] in available_icons:
                    available_icons.remove(icons[i])
        if col == 16:  # error for last column
            for i in [0, 2, 5, 6, 8, 9]:
                if icons[i] in available_icons:
                    available_icons.remove(icons[i])
    return available_icons


def render_q2_dictionary(Q2, T, screen):
    font = pygame.font.Font(None, 22)
    text_color = RED2

    # Determine the number of columns to arrange the keys for Q2 and T dictionaries
    num_columns_q2 = min(len(Q2), 1)
    num_columns_t = min(len(T), 1)

    # Render Q2 dictionary on the screen
    for idx, (key, value) in enumerate(Q2.items()):
        column = idx % num_columns_q2
        row = idx // num_columns_q2

        # Draw a blue rectangle before rendering text
        rect_x = 615 + column * 90
        rect_y = 345 + row * 30
        rect_width = 130
        rect_height = 305
        pygame.draw.rect(screen, BLUE, (rect_x, rect_y, rect_width, rect_height))

        text_surface = font.render(f"{key}: {value}", True, text_color)
        screen.blit(text_surface, (650 + column * 90, 350 + row * 30))

    # Render T dictionary on the screen
    for idx, (key, value) in enumerate(T.items()):
        column = idx % num_columns_t
        row = idx // num_columns_t

        # Draw a blue rectangle before rendering text
        rect_x = 740 + column * 90
        rect_y = 345 + row * 30
        rect_width = 265
        rect_height = 305
        pygame.draw.rect(screen, BLUE, (rect_x, rect_y, rect_width, rect_height))

        if isinstance(value, (list, np.ndarray)):
            if len(value) > 0:
                start_value = value[0]  # Get the start value from the array
                end_value = value[-1]  # Get the end value from the array
                formatted_start = "{:.1f}".format(start_value)  # Format to 1 decimal places
                formatted_end = "{:.1f}".format(end_value)  # Format to 1 decimal places
                text_surface_start = font.render(f"T_start: {formatted_start}", True, text_color)
                text_surface_end = font.render(f"T_end: {formatted_end}", True, text_color)

                # Calculate positions for rendering
                q_position = (650 + column * 90, 350 + row * 30)
                t_start_position = (750 + column * 90, 350 + row * 30)
                t_end_position = (875 + column * 90, 350 + row * 30)

                # Render the values
                screen.blit(text_surface_start, t_start_position)
                screen.blit(text_surface_end, t_end_position)
        else:
            text_surface = font.render(f"{key}: {value}", True, text_color)
            screen.blit(text_surface, (750 + column * 90, 350 + row * 30))

    pygame.display.update()


def game_over():
    global Starting_Q, Qtot_depl, Qtot_head, budget, Qhouse0_in, Qhouse1_in, Qhouse2_in, Qghouse0_in, Qghouse1_in, rw_existence, screen

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

    retry_game_over_button = Button(450, 500, 150, 50, "Retry", GRAY, WHITE)
    tip_game_over_button = Button(800, 100, 80, 50, "Tip", GRAY, WHITE)

    en_lreason_1 = "The supplied geothermal fluid flow rate you entered, Qtotal (Q1), is incorrect. Refer to Theory 1."
    en_tip_1 = "The geothermal fluid flow rate you entered exceeds the maximum allowable extraction rate the aquifer can sustain without risk of depletion. Please select a rate equal to or below the maximum allowable."
    en_lreason_2 = (
        "The geothermal fluid flow rate you entered, Qtotal (Q1), is incorrect. Refer to Theory 2.")
    en_tip_2 = "The geothermal fluid flow rate you entered, Qtotal (Q1), will cause a significant long-term decline in the aquifer level."
    en_lreason__3 = "The geothermal fluid flow rate you entered, Qtotal (Q1), is incorrect. Refer to Theory 3."
    en_tip_3 = "The geothermal fluid flow rate you entered, Qtotal (Q1), will not meet the needs of at least the most demanding user. A rate equal to or greater than each user’s maximum demand is required."
    en_lreason_4 = "The flow rate for this specific user was incorrect"
    en_tip_4 = "The flow rate reaching the user must match the specified data."
    en_lreason_5 = "Your budget has been exhausted."
    en_tip_5 = "Use the resources more effectively."

    en_rendered_lreason_1 = font.render(en_lreason_1, True, (255, 255, 255))
    en_rendered_lreason_2 = font.render(en_lreason_2, True, (255, 255, 255))
    en_rendered_lreason_3 = font.render(en_lreason__3, True, (255, 255, 255))
    en_rendered_lreason_4 = font.render(en_lreason_4, True, (255, 255, 255))
    en_rendered_lreason_5 = font.render(en_lreason_5, True, (255, 255, 255))

    en_rendered_tip_1 = font.render(en_tip_1, True, (255, 255, 255))
    en_rendered_tip_2 = font.render(en_tip_2, True, (255, 255, 255))
    en_rendered_tip_3 = font.render(en_tip_3, True, (255, 255, 255))
    en_rendered_tip_4 = font.render(en_tip_4, True, (255, 255, 255))
    en_rendered_tip_5 = font.render(en_tip_5, True, (255, 255, 255))

    en_rendered_lreason_1_rect = en_rendered_lreason_1.get_rect(center=(screen_width // 2, screen_height // 2))
    en_rendered_lreason_2_rect = en_rendered_lreason_2.get_rect(center=(screen_width // 2, screen_height // 2))
    en_rendered_lreason_3_rect = en_rendered_lreason_3.get_rect(center=(screen_width // 2, screen_height // 2))
    en_rendered_lreason_4_rect = en_rendered_lreason_4.get_rect(center=(screen_width // 2, screen_height // 2))
    en_rendered_lreason_5_rect = en_rendered_lreason_5.get_rect(center=(screen_width // 2, screen_height // 2))

    en_rendered_tip_1_rect = pygame.Rect((0, 0), (700, 50))
    en_rendered_tip_2_rect = pygame.Rect((0, 0), (700, 50))
    en_rendered_tip_3_rect = pygame.Rect((0, 0), (700, 50))
    en_rendered_tip_4_rect = pygame.Rect((0, 0), (700, 50))
    en_rendered_tip_5_rect = pygame.Rect((0, 0), (700, 50))

    en_wrapped_tip_1 = render_text_rect(en_tip_1, font, en_rendered_tip_1_rect, (255, 255, 255), (BLACK), wrap=True)
    en_wrapped_tip_2 = render_text_rect(en_tip_2, font, en_rendered_tip_2_rect, (255, 255, 255), (BLACK), wrap=True)
    en_wrapped_tip_3 = render_text_rect(en_tip_3, font, en_rendered_tip_3_rect, (255, 255, 255), (BLACK), wrap=True)
    en_wrapped_tip_4 = render_text_rect(en_tip_4, font, en_rendered_tip_4_rect, (255, 255, 255), (BLACK), wrap=True)
    en_wrapped_tip_5 = render_text_rect(en_tip_5, font, en_rendered_tip_5_rect, (255, 255, 255), (BLACK), wrap=True)

    # if for reason_lost_1 and tip button on game over screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if Starting_Q > Qtot_depl[dataset] + 1:
                if language == 'gr':
                    screen.fill(BLUE3)
                    screen.blit(rendered_lreason_1, rendered_lreason_1_rect)
                    retry_game_over_button.draw(screen)
                    tip_game_over_button.draw(screen)
                    pygame.display.update()
                elif language == 'en':
                    screen.fill(BLUE3)
                    screen.blit(en_rendered_lreason_1, en_rendered_lreason_1_rect)
                    retry_game_over_button.draw(screen)
                    tip_game_over_button.draw(screen)
                    pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if retry_game_over_button.is_clicked(pygame.mouse.get_pos()):
                        retry_after_fail()
                    elif tip_game_over_button.is_clicked(pygame.mouse.get_pos()):
                        if language == 'gr':
                            transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                            pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                            transparent_surface.blit(wrapped_tip_1, (20, 10))
                            screen.blit(transparent_surface, (100, 200))
                            pygame.display.update()
                        elif language == 'en':
                            transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                            pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                            transparent_surface.blit(en_wrapped_tip_1, (20, 10))
                            screen.blit(transparent_surface, (100, 200))
                            pygame.display.update()
            elif Starting_Q < Qtot_head[dataset]:
                if Starting_Q < max(Qhouse0_in[dataset], Qhouse1_in[dataset], Qhouse2_in[dataset], Qghouse0_in[dataset],
                                    Qghouse1_in[dataset]):
                    if language == 'gr':
                        screen.fill(BLUE3)
                        screen.blit(rendered_lreason_3, rendered_lreason_3_rect)
                        retry_game_over_button.draw(screen)
                        tip_game_over_button.draw(screen)
                        pygame.display.update()
                    elif language == 'en':
                        screen.fill(BLUE3)
                        screen.blit(en_rendered_lreason_3, en_rendered_lreason_3_rect)
                        retry_game_over_button.draw(screen)
                        tip_game_over_button.draw(screen)
                        pygame.display.update()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if retry_game_over_button.is_clicked(pygame.mouse.get_pos()):
                            retry_after_fail()
                        elif tip_game_over_button.is_clicked(pygame.mouse.get_pos()):
                            if language == 'gr':
                                transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                                pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                                transparent_surface.blit(wrapped_tip_3, (20, 10))
                                screen.blit(transparent_surface, (100, 200))
                                pygame.display.update()
                            elif language == 'en':
                                transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                                pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                                transparent_surface.blit(en_wrapped_tip_3, (20, 10))
                                screen.blit(transparent_surface, (100, 200))
                                pygame.display.update()
                elif rw_existence == True:
                    if language == 'gr':
                        screen.fill(BLUE3)
                        retry_game_over_button.draw(screen)
                        tip_game_over_button.draw(screen)
                        screen.blit(rendered_lreason_2, rendered_lreason_2_rect)
                        pygame.display.update()
                    elif language == 'en':
                        screen.fill(BLUE3)
                        retry_game_over_button.draw(screen)
                        tip_game_over_button.draw(screen)
                        screen.blit(en_rendered_lreason_2, en_rendered_lreason_2_rect)
                        pygame.display.update()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if retry_game_over_button.is_clicked(pygame.mouse.get_pos()):
                            retry_after_fail()
                        elif tip_game_over_button.is_clicked(pygame.mouse.get_pos()):
                            if language =='gr':
                                transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                                pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                                transparent_surface.blit(wrapped_tip_2, (20, 10))
                                screen.blit(transparent_surface, (100, 200))
                                pygame.display.update()
                            elif language == 'en':
                               transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                               pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                               transparent_surface.blit(en_wrapped_tip_2, (20, 10))
                               screen.blit(transparent_surface, (100, 200))
                               pygame.display.update()
                else:
                    return
            elif Starting_Q > Qtot_head[dataset]:
                if Starting_Q < max(Qhouse0_in[dataset], Qhouse1_in[dataset], Qhouse2_in[dataset], Qghouse0_in[dataset],
                                    Qghouse1_in[dataset]):
                    if language == 'gr':
                        screen.fill(BLUE3)
                        screen.blit(rendered_lreason_3, (80, screen_height // 2))
                        retry_game_over_button.draw(screen)
                        tip_game_over_button.draw(screen)
                        pygame.display.update()
                    elif language =='en':
                        screen.fill(BLUE3)
                        screen.blit(en_rendered_lreason_3, (80, screen_height // 2))
                        retry_game_over_button.draw(screen)
                        tip_game_over_button.draw(screen)
                        pygame.display.update()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if retry_game_over_button.is_clicked(pygame.mouse.get_pos()):
                            retry_after_fail()
                        elif tip_game_over_button.is_clicked(pygame.mouse.get_pos()):
                            if language == 'gr':
                                transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                                pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                                transparent_surface.blit(wrapped_tip_3, (20, 10))
                                screen.blit(transparent_surface, (100, 200))
                                pygame.display.update()
                            elif language == 'en':
                                transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                                pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                                transparent_surface.blit(en_wrapped_tip_3, (20, 10))
                                screen.blit(transparent_surface, (100, 200))
                                pygame.display.update()
                elif rw_existence == False:
                    if language == 'gr':
                        screen.fill(BLUE3)
                        screen.blit(rendered_lreason_2, (80, screen_height // 2))
                        retry_game_over_button.draw(screen)
                        tip_game_over_button.draw(screen)
                        pygame.display.update()
                    elif language == 'en':
                        screen.fill(BLUE3)
                        screen.blit(en_rendered_lreason_2, (80, screen_height // 2))
                        retry_game_over_button.draw(screen)
                        tip_game_over_button.draw(screen)
                        pygame.display.update()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if retry_game_over_button.is_clicked(pygame.mouse.get_pos()):
                            retry_after_fail()
                        elif tip_game_over_button.is_clicked(pygame.mouse.get_pos()):
                            if language == 'gr':
                                transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                                pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                                transparent_surface.blit(wrapped_tip_2, (20, 10))
                                screen.blit(transparent_surface, (100, 200))
                                pygame.display.update()
                            elif language == 'en':
                                transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                                pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                                transparent_surface.blit(en_wrapped_tip_2, (20, 10))
                                screen.blit(transparent_surface, (100, 200))
                                pygame.display.update()
                else:
                    return
            else:
                return
def game_over_exam_mode():
    global Starting_Q, Qtot_depl, Qtot_head, budget, Qhouse0_in, Qhouse1_in, Qhouse2_in, Qghouse0_in, Qghouse1_in, rw_existence, screen, negative_point_counter
    mistake_1 = 0
    mistake_2 = 0
    mistake_3 = 0
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

    retry_game_over_button = Button(450, 500, 150, 50, "Retry", GRAY, WHITE)
    tip_game_over_button = Button(800, 100, 80, 50, "Tip", GRAY, WHITE)

    en_lreason_1 = "The supplied geothermal fluid flow rate you entered, Qtotal (Q1), is incorrect. Refer to Theory 1."
    en_tip_1 = "The geothermal fluid flow rate you entered exceeds the maximum allowable extraction rate the aquifer can sustain without risk of depletion. Please select a rate equal to or below the maximum allowable."
    en_lreason_2 = (
        "The geothermal fluid flow rate you entered, Qtotal (Q1), is incorrect. Refer to Theory 2.")
    en_tip_2 = "The geothermal fluid flow rate you entered, Qtotal (Q1), will cause a significant long-term decline in the aquifer level."
    en_lreason__3 = "The geothermal fluid flow rate you entered, Qtotal (Q1), is incorrect. Refer to Theory 3."
    en_tip_3 = "The geothermal fluid flow rate you entered, Qtotal (Q1), will not meet the needs of at least the most demanding user. A rate equal to or greater than each user’s maximum demand is required."
    en_lreason_4 = "The flow rate for this specific user was incorrect"
    en_tip_4 = "The flow rate reaching the user must match the specified data."
    en_lreason_5 = "Your budget has been exhausted."
    en_tip_5 = "Use the resources more effectively."

    en_rendered_lreason_1 = font.render(en_lreason_1, True, (255, 255, 255))
    en_rendered_lreason_2 = font.render(en_lreason_2, True, (255, 255, 255))
    en_rendered_lreason_3 = font.render(en_lreason__3, True, (255, 255, 255))
    en_rendered_lreason_4 = font.render(en_lreason_4, True, (255, 255, 255))
    en_rendered_lreason_5 = font.render(en_lreason_5, True, (255, 255, 255))

    en_rendered_tip_1 = font.render(en_tip_1, True, (255, 255, 255))
    en_rendered_tip_2 = font.render(en_tip_2, True, (255, 255, 255))
    en_rendered_tip_3 = font.render(en_tip_3, True, (255, 255, 255))
    en_rendered_tip_4 = font.render(en_tip_4, True, (255, 255, 255))
    en_rendered_tip_5 = font.render(en_tip_5, True, (255, 255, 255))

    en_rendered_lreason_1_rect = en_rendered_lreason_1.get_rect(center=(screen_width // 2, screen_height // 2))
    en_rendered_lreason_2_rect = en_rendered_lreason_2.get_rect(center=(screen_width // 2, screen_height // 2))
    en_rendered_lreason_3_rect = en_rendered_lreason_3.get_rect(center=(screen_width // 2, screen_height // 2))
    en_rendered_lreason_4_rect = en_rendered_lreason_4.get_rect(center=(screen_width // 2, screen_height // 2))
    en_rendered_lreason_5_rect = en_rendered_lreason_5.get_rect(center=(screen_width // 2, screen_height // 2))

    en_rendered_tip_1_rect = pygame.Rect((0, 0), (700, 50))
    en_rendered_tip_2_rect = pygame.Rect((0, 0), (700, 50))
    en_rendered_tip_3_rect = pygame.Rect((0, 0), (700, 50))
    en_rendered_tip_4_rect = pygame.Rect((0, 0), (700, 50))
    en_rendered_tip_5_rect = pygame.Rect((0, 0), (700, 50))

    en_wrapped_tip_1 = render_text_rect(en_tip_1, font, en_rendered_tip_1_rect, (255, 255, 255), (BLACK), wrap=True)
    en_wrapped_tip_2 = render_text_rect(en_tip_2, font, en_rendered_tip_2_rect, (255, 255, 255), (BLACK), wrap=True)
    en_wrapped_tip_3 = render_text_rect(en_tip_3, font, en_rendered_tip_3_rect, (255, 255, 255), (BLACK), wrap=True)
    en_wrapped_tip_4 = render_text_rect(en_tip_4, font, en_rendered_tip_4_rect, (255, 255, 255), (BLACK), wrap=True)
    en_wrapped_tip_5 = render_text_rect(en_tip_5, font, en_rendered_tip_5_rect, (255, 255, 255), (BLACK), wrap=True)

    # if for reason_lost_1 and tip button on game over screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if Starting_Q > Qtot_depl[dataset] + 1 and mistake_1 == 0:
                negative_point_counter -= 1
                mistake_1 == 1
                return
            elif Starting_Q < Qtot_head[dataset] and mistake_2 == 0:
                negative_point_counter -= 1
                mistake_2 = 1
                return
            else:
                return

"""
Μήπως για πιο περίπλοκα ή απλά περισσότερα ποσοτικά προβλήματα χρειάζεται το αν υπάρχει ή όχι recharging well να εισάγεται απο το Excel"
"""


def game_over_triplet_issue():
    global budget, username
    screen.fill(BLUE3)
    font = pygame.font.Font(info_font, 15)
    font2 = pygame.font.Font(info_font, 40)

    lreason_5 = "Κακή χρήση του τριπλού αγωγού. Συναντήθηκε εισροή και εκροή στο ίδιο τμήμα αγωγού."
    tip_5 = "Αρχικά όρισες αγωγό με 1 εισροή και 2 εκροές και στη συνέχεια στη μία εκροή έστειλες εισροή. Την επόμενη φορά πρόσεξε καλύτερα τις οδηγίες για την ορθή χρήση τριπλών αγωγών."

    rendered_lreason_5 = font.render(lreason_5, True, (255, 255, 255))
    rendered_tip_5_rect = pygame.Rect((0, 0), (700, 100))
    rendered_tip_5 = font.render(tip_5, True, (255, 255, 255))

    wrapped_tip_5 = render_text_rect(tip_5, font, rendered_tip_5_rect, (255, 255, 255), (BLACK), wrap=True)

    en_lreason_5 = "Poor use of the triple pipe. Inflow and outflow occurred in the same section of the pipe."
    en_tip_5 = "Initially, you defined a pipe with 1 inflow and 2 outflows, then sent an inflow to one of the outflows. Next time, pay closer attention to the instructions for proper use of triple pipes."

    en_rendered_lreason_5 = font.render(en_lreason_5, True, (255, 255, 255))
    en_rendered_tip_5_rect = pygame.Rect((0, 0), (700, 100))
    en_rendered_tip_5 = font.render(en_tip_5, True, (255, 255, 255))

    en_wrapped_tip_5 = render_text_rect(en_tip_5, font, en_rendered_tip_5_rect, (255, 255, 255), (BLACK), wrap=True)

    retry_game_over_button = Button(450, 500, 150, 50, "Retry", GRAY, WHITE)
    tip_game_over_button = Button(800, 100, 80, 50, "Tip", GRAY, WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if (things_around_up > 0 and pipe_section_grid[row - 1][col] > 0 and pipe_section_grid[row][col] > 0 and
                pipe_section_grid[row - 1][col] != pipe_section_grid[row][col]) or \
                    (things_around_right > 0 and pipe_section_grid[row][col + 1] > 0 and pipe_section_grid[row][
                        col] > 0 and pipe_section_grid[row][col + 1] != pipe_section_grid[row][col]) or \
                    (things_around_down > 0 and pipe_section_grid[row + 1][col] > 0 and pipe_section_grid[row][
                        col] > 0 and pipe_section_grid[row + 1][col] != pipe_section_grid[row][col]) or \
                    (things_around_left > 0 and pipe_section_grid[row][col - 1] > 0 and pipe_section_grid[row][
                        col] > 0 and pipe_section_grid[row][col - 1] != pipe_section_grid[row][col]):
                if language == 'gr':
                    screen.fill(BLUE3)
                    screen.blit(rendered_lreason_5, (80, screen_height // 2))
                    retry_game_over_button.draw(screen)
                    tip_game_over_button.draw(screen)
                    pygame.display.update()
                elif language =='en':
                    screen.fill(BLUE3)
                    screen.blit(en_rendered_lreason_5, (80, screen_height // 2))
                    retry_game_over_button.draw(screen)
                    tip_game_over_button.draw(screen)
                    pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if retry_game_over_button.is_clicked(pygame.mouse.get_pos()):
                        budget = player_budget[dataset]
                        retry_after_fail()
                    elif tip_game_over_button.is_clicked(pygame.mouse.get_pos()):
                        if language == 'gr':
                            transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                            pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                            transparent_surface.blit(wrapped_tip_5, (0, 10))
                            screen.blit(transparent_surface, (100, 200))
                            pygame.display.update()
                        elif language == 'en':
                            transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                            pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                            transparent_surface.blit(en_wrapped_tip_5, (0, 10))
                            screen.blit(transparent_surface, (100, 200))
                            pygame.display.update()
            else:
                return


def game_over_budget():
    global budget, budget_calculated
    screen.fill(BLUE3)
    font = pygame.font.Font(info_font, 15)
    font2 = pygame.font.Font(info_font, 40)

    lreason_5 = "Το budget σου εξαντήθηκε"
    tip_5 = "Χρησιμοποίησε τους πόρους πιο σωστά"

    rendered_lreason_5 = font.render(lreason_5, True, (255, 255, 255))
    rendered_tip_5_rect = pygame.Rect((0, 0), (700, 50))

    wrapped_tip_5 = render_text_rect(tip_5, font, rendered_tip_5_rect, (255, 255, 255), (BLACK), wrap=True)

    en_lreason_5 = "Your budget has been exhausted."
    en_tip_5 = "Use the resources more effectively."

    en_rendered_lreason_5 = font.render(en_lreason_5, True, (255, 255, 255))
    en_rendered_tip_5_rect = pygame.Rect((0, 0), (700, 50))

    en_wrapped_tip_5 = render_text_rect(en_tip_5, font, en_rendered_tip_5_rect, (255, 255, 255), (BLACK), wrap=True)

    retry_game_over_button = Button(450, 500, 150, 50, "Retry", GRAY, WHITE)
    tip_game_over_button = Button(800, 100, 80, 50, "Tip", GRAY, WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if budget_calculated < 0:
                if language == 'gr':
                    screen.fill(BLUE3)
                    screen.blit(rendered_lreason_5, (80, screen_height // 2))
                    retry_game_over_button.draw(screen)
                    tip_game_over_button.draw(screen)
                    pygame.display.update()
                elif language == 'en':
                    screen.fill(BLUE3)
                    screen.blit(en_rendered_lreason_5, (80, screen_height // 2))
                    retry_game_over_button.draw(screen)
                    tip_game_over_button.draw(screen)
                    pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if retry_game_over_button.is_clicked(pygame.mouse.get_pos()):
                        budget_calculated = player_budget[dataset]
                        retry_after_fail()
                    elif tip_game_over_button.is_clicked(pygame.mouse.get_pos()):
                        if language == 'gr':
                            transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                            pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                            transparent_surface.blit(wrapped_tip_5, (0, 10))
                            screen.blit(transparent_surface, (100, 200))
                            pygame.display.update()
                        elif language == 'en':
                            transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                            pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                            transparent_surface.blit(en_wrapped_tip_5, (0, 10))
                            screen.blit(transparent_surface, (100, 200))
                            pygame.display.update()
            else:
                return


def game_over_Q_inconsistent():
    global budget, row, col
    screen.fill(BLUE3)
    font = pygame.font.Font(info_font, 15)
    font2 = pygame.font.Font(info_font, 40)
    print(type(row), type(col), row, col)
    #row = int(row[0])
    #col = int(col[0])
    lreason_5 = "Η εξίσωση συνέχειας δεν ισχύει! Ο αγωγός που μόλις συνέδεσες στον χρήστη είχε διαφορετική παροχή από την απαιτούμενη."
    tip_5 = "Την επόμενη φορά πρόσεχε να στείλεις σε κάθε χρήστη ακριβώς την παροχή που χρειάζεται."

    rendered_lreason_5 = font.render(lreason_5, True, (255, 255, 255))
    rendered_tip_5_rect = pygame.Rect((0, 0), (700, 50))

    wrapped_tip_5 = render_text_rect(tip_5, font, rendered_tip_5_rect, (255, 255, 255), (BLACK), wrap=True)

    retry_game_over_button = Button(450, 500, 150, 50, "Retry", GRAY, WHITE)
    tip_game_over_button = Button(800, 100, 80, 50, "Tip", GRAY, WHITE)
    print("i came through here")

    en_lreason_5 = "The continuity equation does not hold! The pipe you just connected to the user had a different flow rate than required."
    en_tip_5 = "Next time, make sure to send each user exactly the flow rate they need."

    en_rendered_lreason_5 = font.render(en_lreason_5, True, (255, 255, 255))
    en_rendered_tip_5_rect = pygame.Rect((0, 0), (700, 50))

    en_wrapped_tip_5 = render_text_rect(en_tip_5, font, en_rendered_tip_5_rect, (255, 255, 255), (BLACK), wrap=True)

    retry_game_over_button = Button(450, 500, 150, 50, "Retry", GRAY, WHITE)
    tip_game_over_button = Button(800, 100, 80, 50, "Tip", GRAY, WHITE)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            print(type(row), type(col), row, col)  # This will help identify if they are lists
            if Q_grid[row][col] != Q_grid[row + 1][col]:
                print("i came through here 2")
                if language == 'gr':
                    screen.fill(BLUE3)
                    screen.blit(rendered_lreason_5, (80, screen_height // 2))
                    retry_game_over_button.draw(screen)
                    tip_game_over_button.draw(screen)
                    pygame.display.flip()
                elif language == 'en':
                    screen.fill(BLUE3)
                    screen.blit(en_rendered_lreason_5, (80, screen_height // 2))
                    retry_game_over_button.draw(screen)
                    tip_game_over_button.draw(screen)
                    pygame.display.flip()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if retry_game_over_button.is_clicked(pygame.mouse.get_pos()):
                        budget = player_budget[dataset]
                        retry_after_fail()
                    elif tip_game_over_button.is_clicked(pygame.mouse.get_pos()):
                        if language == 'gr':
                            transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                            pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                            transparent_surface.blit(wrapped_tip_5, (0, 10))
                            screen.blit(transparent_surface, (100, 200))
                            pygame.display.update()
                        elif language == 'en':
                            transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                            pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                            transparent_surface.blit(en_wrapped_tip_5, (0, 10))
                            screen.blit(transparent_surface, (100, 200))
                            pygame.display.update()
            else:
                return


def game_over_users_not_satisfied():
    global budget, username
    screen.fill(BLUE3)
    font = pygame.font.Font(info_font, 15)
    font2 = pygame.font.Font(info_font, 40)

    lreason_5 = "Δεν ικανοποιήθηκαν όλοι οι χρήστες."
    tip_5 = "Την επόμενη φορά πρόσεχε να ικανοποιήσεις όλους τους χρήστες με την απαιτούμενη παροχή και θερμοκρασία."

    rendered_lreason_5 = font.render(lreason_5, True, (255, 255, 255))
    rendered_tip_5_rect = pygame.Rect((0, 0), (700, 50))
    rendered_tip_5 = font.render(tip_5, True, (255, 255, 255))

    wrapped_tip_5 = render_text_rect(tip_5, font, rendered_tip_5_rect, (255, 255, 255), (BLACK), wrap=True)

    retry_game_over_button = Button(450, 500, 150, 50, "Retry", GRAY, WHITE)
    tip_game_over_button = Button(800, 100, 80, 50, "Tip", GRAY, WHITE)

    en_lreason_5 = "Not all users were satisfied."
    en_tip_5 = "Next time, ensure that all users are satisfied with the required flow rate and temperature."

    en_rendered_lreason_5 = font.render(en_lreason_5, True, (255, 255, 255))
    en_rendered_tip_5_rect = pygame.Rect((0, 0), (700, 50))
    en_rendered_tip_5 = font.render(en_tip_5, True, (255, 255, 255))

    en_wrapped_tip_5 = render_text_rect(en_tip_5, font, en_rendered_tip_5_rect, (255, 255, 255), (BLACK), wrap=True)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if min(Q_grid[house0_row[dataset] - 1][house0_col[dataset]], \
                   Q_grid[house1_row[dataset] - 1][house1_col[dataset]], \
                   Q_grid[house2_row[dataset] - 1][house2_col[dataset]], \
                   Q_grid[greenhouse0_row[dataset] - 1][greenhouse0_col[dataset]], \
                   Q_grid[greenhouse1_row[dataset] - 1][greenhouse1_col[dataset]]) < 0:
                if language == 'gr':
                    screen.fill(BLUE3)
                    screen.blit(rendered_lreason_5, (80, screen_height // 2))
                    retry_game_over_button.draw(screen)
                    tip_game_over_button.draw(screen)
                    pygame.display.update()
                elif language == 'en':
                    screen.fill(BLUE3)
                    screen.blit(en_rendered_lreason_5, (80, screen_height // 2))
                    retry_game_over_button.draw(screen)
                    tip_game_over_button.draw(screen)
                    pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if retry_game_over_button.is_clicked(pygame.mouse.get_pos()):
                        budget = player_budget[dataset]
                        retry_after_fail()
                    elif tip_game_over_button.is_clicked(pygame.mouse.get_pos()):
                        if language == 'gr':
                            transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                            pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                            transparent_surface.blit(wrapped_tip_5, (0, 10))
                            screen.blit(transparent_surface, (100, 200))
                            pygame.display.update()
                        elif language == 'en':
                            transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                            pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                            transparent_surface.blit(en_wrapped_tip_5, (0, 10))
                            screen.blit(transparent_surface, (100, 200))
                            pygame.display.update()
            else:
                return


file_path = root_dir + "\GameAssets\geodata.xlsx"


def game_over_ending():
    global budget, username, budget_calculated, dataset
    file_path = root_dir + "\GameAssets\geodata.xlsx"
    all_of_the_screen = pygame.Rect(0, 0, 1005, 750)
    grid_area = pygame.Rect(64, 64, 544, 544)
    screenshot = screen.subsurface(grid_area)
    solution = screen.subsurface(all_of_the_screen)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    credits_font = pygame.font.Font(None, 17)
    credits_text = credits_font.render("Yiannis Kontos - Konstantinos Koutridis", True, (0, 0, 0))
    companyname_text = credits_font.render("yiakou-games", True, (0, 0, 0))
    creditsmail_text1 = credits_font.render("ykontos81@gmail.com", True, (0, 0, 0))
    creditsmail_text2 = credits_font.render("kkoutrid@gmail.com", True, (0, 0, 0))
    screen.blit(creditsmail_text1, (10, 710))
    screen.blit(creditsmail_text2, (10, 725))
    screen.blit(credits_text, (375, 710))
    screen.blit(companyname_text, (450, 725))
    save_solution_directory = root_dir + "\GameAssets\Results"
    base_filename = f"{username}Solution_{timestamp}.png"
    save_path = os.path.join(save_solution_directory, base_filename)

    # Check if the file already exists
    if os.path.exists(save_path):
        # Generate a unique filename by adding a suffix
        suffix = 1
        while True:
            new_filename = f"{username}Solution_{timestamp}{suffix}.png"
            new_save_path = os.path.join(save_solution_directory, new_filename)
            if not os.path.exists(new_save_path):
                save_path = new_save_path
                break
            suffix += 1

    pygame.image.save(solution, save_path)
    new_screenshot_width, new_screenshot_height = 450, 450  # Adjust these dimensions as needed
    # Resize the screenshot using pygame.transform.scale()
    resized_screenshot = pygame.transform.scale(screenshot, (new_screenshot_width, new_screenshot_height))
    screen.fill(BLUE3)
    font = pygame.font.Font(info_font, 20)
    font2 = pygame.font.Font(info_font, 30)
    font3 = pygame.font.Font(title_font, 100)

    game_over = f" Solved !!!"
    budget_score = f"Το budget που απέμεινε είναι {budget_calculated}"
    budget_score2 = f"Έχεις αφήσει ανοιχτό βρόχο, δηλαδή κάποιος αγωγός δεν οδηγεί πουθενά."
    tip_5 = "Ξαναδοκίμασε για να κάνεις καλύτερο score"
    tip_6 = "Προσοχή πριν στείλεις την τελική παροχή σε πηγάδι επαναφοράς να είσαι σίγουρος ότι η παροχή αυτή είναι ίση με την παροχή άντλησης. Για να συμβεί αυτό πρέπει να μην υπάρχει αγωγός που δεν οδηγεί πουθενά."
    rendered_game_over = font3.render(game_over, True, WHITE)
    rendered_budget_score = font2.render(budget_score, True, (255, 255, 255))
    rendered_budget_score2 = font.render(budget_score2, True, (255, 255, 255))
    rendered_tip_5_rect = pygame.Rect((0, 0), (700, 50))
    rendered_tip_5 = font.render(tip_5, True, (255, 255, 255))
    rendered_tip_6_rect = pygame.Rect((0, 0), (700, 100))
    rendered_tip_6 = font.render(tip_6, True, (255, 255, 255))

    wrapped_tip_5 = render_text_rect(tip_5, font, rendered_tip_5_rect, (255, 255, 255), (BLACK), wrap=True)
    wrapped_tip_6 = render_text_rect(tip_6, font, rendered_tip_6_rect, (255, 255, 255), (BLACK), wrap=True)

    return_to_start_screen = Button(275, 615, 150, 50, "Start Screen", GRAY, WHITE)
    tip_game_over_ending_button = Button(850, 100, 80, 50, "Tip", GRAY, WHITE)
    retry_game_over_button = Button(450, 500, 150, 50, "Retry", GRAY, WHITE)
    tip_game_over_button = Button(800, 100, 80, 50, "Tip", GRAY, WHITE)
    levels_button = Button(575, 615, 150, 50, "Levels", GRAY, WHITE)
# Start of English Language part
    en_game_over = f" Solved !!!"
    en_budget_score = f"The remaining budget is {budget_calculated}."
    en_budget_score2 = f"You have an open loop, meaning that a pipe is not connected to anything."
    en_tip_5 = "Try again to achieve a better score."
    en_tip_6 = "Before sending the final flow to the recharge well, ensure that this flow matches the extraction rate. To achieve this, there should be no pipe that does not lead anywhere."
    en_rendered_game_over = font3.render(en_game_over, True, WHITE)
    en_rendered_budget_score = font2.render(en_budget_score, True, (255, 255, 255))
    en_rendered_budget_score2 = font.render(en_budget_score2, True, (255, 255, 255))
    en_rendered_tip_5_rect = pygame.Rect((0, 0), (700, 50))
    en_rendered_tip_5 = font.render(en_tip_5, True, (255, 255, 255))
    en_rendered_tip_6_rect = pygame.Rect((0, 0), (700, 100))
    en_rendered_tip_6 = font.render(en_tip_6, True, (255, 255, 255))

    en_wrapped_tip_5 = render_text_rect(en_tip_5, font, en_rendered_tip_5_rect, (255, 255, 255), (BLACK), wrap=True)
    en_wrapped_tip_6 = render_text_rect(en_tip_6, font, en_rendered_tip_6_rect, (255, 255, 255), (BLACK), wrap=True)

    return_to_start_screen = Button(275, 615, 150, 50, "Start Screen", GRAY, WHITE)
    tip_game_over_ending_button = Button(850, 100, 80, 50, "Tip", GRAY, WHITE)
    retry_game_over_button = Button(450, 500, 150, 50, "Retry", GRAY, WHITE)
    tip_game_over_button = Button(800, 100, 80, 50, "Tip", GRAY, WHITE)
    levels_button = Button(575, 615, 150, 50, "Levels", GRAY, WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if Q_grid[rw_row[dataset] - 1][rw_col[dataset]] != -2:
                if Q_grid[rw_row[dataset] - 1][rw_col[dataset]] != Q_grid[pw_row[dataset] - 1][pw_col[dataset]]:
                    if language == 'gr':
                        screen.fill(BLUE3)
                        screen.blit(rendered_budget_score2, (80, screen_height // 2))
                        retry_game_over_button.draw(screen)
                        tip_game_over_button.draw(screen)
                        pygame.display.update()
                    elif language == 'en':
                        screen.fill(BLUE3)
                        screen.blit(en_rendered_budget_score2, (80, screen_height // 2))
                        retry_game_over_button.draw(screen)
                        tip_game_over_button.draw(screen)
                        pygame.display.update()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if retry_game_over_button.is_clicked(pygame.mouse.get_pos()):
                            budget = player_budget[dataset]
                            username = None
                            retry_after_fail()
                        elif tip_game_over_button.is_clicked(pygame.mouse.get_pos()):
                            if language == 'gr':
                                transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                                pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                                transparent_surface.blit(wrapped_tip_6, (0, 10))
                                screen.blit(transparent_surface, (100, 200))
                                pygame.display.update()
                            elif language == 'en':
                                transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                                pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                                transparent_surface.blit(en_wrapped_tip_6, (0, 10))
                                screen.blit(transparent_surface, (100, 200))
                                pygame.display.update()
                else:
                    if language == 'gr':
                        screen.fill(GREEN)
                        screen.blit(rendered_budget_score, (screen_width // 2 - 250, 700))
                        return_to_start_screen.draw(screen)
                        tip_game_over_ending_button.draw(screen)
                        levels_button.draw(screen)
                        screen.blit(rendered_game_over, (screen_width // 2 - 150, 10))
                        screen.blit(resized_screenshot, (screen_width // 2 - 225, 125))
                        screen.blit(credits_text, (775, 710))
                        screen.blit(companyname_text, (850, 725))
                        screen.blit(creditsmail_text1, (10, 710))
                        screen.blit(creditsmail_text2, (10, 725))
                        update_high_score(file_path, dataset, budget_calculated, high_score_column_name)
                        pygame.display.update()
                    elif language == 'en':
                        screen.fill(GREEN)
                        screen.blit(en_rendered_budget_score, (screen_width // 2 - 250, 700))
                        return_to_start_screen.draw(screen)
                        tip_game_over_ending_button.draw(screen)
                        levels_button.draw(screen)
                        screen.blit(en_rendered_game_over, (screen_width // 2 - 150, 10))
                        screen.blit(resized_screenshot, (screen_width // 2 - 225, 125))
                        screen.blit(credits_text, (775, 710))
                        screen.blit(companyname_text, (850, 725))
                        screen.blit(creditsmail_text1, (10, 710))
                        screen.blit(creditsmail_text2, (10, 725))
                        update_high_score(file_path, dataset, budget_calculated, high_score_column_name)
                        pygame.display.update()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if return_to_start_screen.is_clicked(pygame.mouse.get_pos()):
                            budget = player_budget[dataset]
                            username = None
                            reset_grid()
                            combined_start_function()
                            main_loop()
                        elif tip_game_over_ending_button.is_clicked(pygame.mouse.get_pos()):
                            if language == 'gr':
                                transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                                pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                                transparent_surface.blit(wrapped_tip_5, (0, 10))
                                screen.blit(transparent_surface, (100, 200))
                                pygame.display.update()
                            if language == 'en':
                                transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                                pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                                transparent_surface.blit(en_wrapped_tip_5, (0, 10))
                                screen.blit(transparent_surface, (100, 200))
                                pygame.display.update()
                        elif levels_button.is_clicked(pygame.mouse.get_pos()):
                            budget = player_budget[dataset]
                            reset_grid()
                            combined_start_function_RE()
                            main_loop()

            else:
                return
number_of_exam_tries = 0
def game_over_ending_exam_mode():
    global budget, username, budget_calculated, dataset, negative_point_counter, number_of_exam_tries, has_the_exam_run, negative_point_counter
    mistake_1 = 0
    number_of_exam_tries += 1
    file_path = root_dir + "\GameAssets\geodata.xlsx"
    all_of_the_screen = pygame.Rect(0, 0, 1005, 750)
    grid_area = pygame.Rect(64, 64, 544, 544)
    screenshot = screen.subsurface(grid_area)
    solution = screen.subsurface(all_of_the_screen)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    credits_font = pygame.font.Font(None, 17)
    credits_text = credits_font.render("Yiannis Kontos - Konstantinos Koutridis", True, (0, 0, 0))
    companyname_text = credits_font.render("yiakou-games", True, (0, 0, 0))
    creditsmail_text1 = credits_font.render("ykontos81@gmail.com", True, (0, 0, 0))
    creditsmail_text2 = credits_font.render("kkoutrid@gmail.com", True, (0, 0, 0))
    screen.blit(creditsmail_text1, (10, 710))
    screen.blit(creditsmail_text2, (10, 725))
    screen.blit(credits_text, (375, 710))
    screen.blit(companyname_text, (450, 725))
    save_solution_directory = root_dir + "\GameAssets\Results\Exam_Mode_Results"
    base_filename = f"{username}Solution_{timestamp}_with_{abs(negative_point_counter)}_mistakes.png"
    save_path = os.path.join(save_solution_directory, base_filename)

    # Check if the file already exists
    if os.path.exists(save_path):
        # Generate a unique filename by adding a suffix
        suffix = 1
        while True:
            new_filename = f"{username}Solution_{timestamp}{suffix}_with_{abs(negative_point_counter)}_mistakes.png"
            new_save_path = os.path.join(save_solution_directory, new_filename)
            if not os.path.exists(new_save_path):
                save_path = new_save_path
                break
            suffix += 1

    pygame.image.save(solution, save_path)
    new_screenshot_width, new_screenshot_height = 450, 450  # Adjust these dimensions as needed
    # Resize the screenshot using pygame.transform.scale()
    resized_screenshot = pygame.transform.scale(screenshot, (new_screenshot_width, new_screenshot_height))
    screen.fill(BLUE3)
    font = pygame.font.Font(info_font, 20)
    font2 = pygame.font.Font(info_font, 30)
    font3 = pygame.font.Font(title_font, 100)

    game_over = f" Solved !!!"
    budget_score = f"Το budget που απέμεινε είναι {budget_calculated}"
    budget_score2 = f"Έχεις αφήσει ανοιχτό βρόχο, δηλαδή κάποιος αγωγός δεν οδηγεί πουθενά."
    tip_5 = "Ξαναδοκίμασε για να κάνεις καλύτερο score"
    tip_6 = "Προσοχή πριν στείλεις την τελική παροχή σε πηγάδι επαναφοράς να είσαι σίγουρος ότι η παροχή αυτή είναι ίση με την παροχή άντλησης. Για να συμβεί αυτό πρέπει να μην υπάρχει αγωγός που δεν οδηγεί πουθενά."
    rendered_game_over = font3.render(game_over, True, WHITE)
    rendered_budget_score = font2.render(budget_score, True, (255, 255, 255))
    rendered_budget_score2 = font.render(budget_score2, True, (255, 255, 255))
    rendered_tip_5_rect = pygame.Rect((0, 0), (700, 50))
    rendered_tip_5 = font.render(tip_5, True, (255, 255, 255))
    rendered_tip_6_rect = pygame.Rect((0, 0), (700, 100))
    rendered_tip_6 = font.render(tip_6, True, (255, 255, 255))

    wrapped_tip_5 = render_text_rect(tip_5, font, rendered_tip_5_rect, (255, 255, 255), (BLACK), wrap=True)
    wrapped_tip_6 = render_text_rect(tip_6, font, rendered_tip_6_rect, (255, 255, 255), (BLACK), wrap=True)

    return_to_start_screen = Button(275, 615, 150, 50, "Start Screen", GRAY, WHITE)
    tip_game_over_ending_button = Button(850, 100, 80, 50, "Tip", GRAY, WHITE)
    retry_game_over_button = Button(450, 500, 150, 50, "Retry", GRAY, WHITE)
    tip_game_over_button = Button(800, 100, 80, 50, "Tip", GRAY, WHITE)
    levels_button = Button(575, 615, 150, 50, "Levels", GRAY, WHITE)
# Start of English Language part
    en_game_over = f" Solved !!!"
    en_budget_score = f"The remaining budget is {budget_calculated}."
    en_budget_score2 = f"You have an open loop, meaning that a pipe is not connected to anything."
    en_tip_5 = "Try again to achieve a better score."
    en_tip_6 = "Before sending the final flow to the recharge well, ensure that this flow matches the extraction rate. To achieve this, there should be no pipe that does not lead anywhere."
    en_rendered_game_over = font3.render(en_game_over, True, WHITE)
    en_rendered_budget_score = font2.render(en_budget_score, True, (255, 255, 255))
    en_rendered_budget_score2 = font.render(en_budget_score2, True, (255, 255, 255))
    en_rendered_tip_5_rect = pygame.Rect((0, 0), (700, 50))
    en_rendered_tip_5 = font.render(en_tip_5, True, (255, 255, 255))
    en_rendered_tip_6_rect = pygame.Rect((0, 0), (700, 100))
    en_rendered_tip_6 = font.render(en_tip_6, True, (255, 255, 255))

    en_wrapped_tip_5 = render_text_rect(en_tip_5, font, en_rendered_tip_5_rect, (255, 255, 255), (BLACK), wrap=True)
    en_wrapped_tip_6 = render_text_rect(en_tip_6, font, en_rendered_tip_6_rect, (255, 255, 255), (BLACK), wrap=True)

    return_to_start_screen = Button(275, 615, 150, 50, "Start Screen", GRAY, WHITE)
    tip_game_over_ending_button = Button(850, 100, 80, 50, "Tip", GRAY, WHITE)
    retry_game_over_button = Button(450, 500, 150, 50, "Retry", GRAY, WHITE)
    tip_game_over_button = Button(800, 100, 80, 50, "Tip", GRAY, WHITE)
    levels_button = Button(575, 615, 150, 50, "Retry", GRAY, WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if Q_grid[rw_row[dataset] - 1][rw_col[dataset]] != -2 and mistake_1 == 0:
                if Q_grid[rw_row[dataset] - 1][rw_col[dataset]] != Q_grid[pw_row[dataset] - 1][pw_col[dataset]]:
                    negative_point_counter -= 1
                    mistake_1 = 1
            if number_of_exam_tries <= 2:
                if language == 'gr':
                    screen.fill(GREEN)
                    screen.blit(rendered_budget_score, (screen_width // 2 - 250, 700))
                    return_to_start_screen.draw(screen)
                    tip_game_over_ending_button.draw(screen)
                    levels_button.draw(screen)
                    screen.blit(rendered_game_over, (screen_width // 2 - 150, 10))
                    screen.blit(resized_screenshot, (screen_width // 2 - 225, 125))
                    screen.blit(credits_text, (775, 710))
                    screen.blit(companyname_text, (850, 725))
                    screen.blit(creditsmail_text1, (10, 710))
                    screen.blit(creditsmail_text2, (10, 725))
                    pygame.display.update()
                    print(negative_point_counter)
                elif language == 'en':
                    screen.fill(GREEN)
                    screen.blit(en_rendered_budget_score, (screen_width // 2 - 250, 700))
                    return_to_start_screen.draw(screen)
                    tip_game_over_ending_button.draw(screen)
                    levels_button.draw(screen)
                    screen.blit(en_rendered_game_over, (screen_width // 2 - 150, 10))
                    screen.blit(resized_screenshot, (screen_width // 2 - 225, 125))
                    screen.blit(credits_text, (775, 710))
                    screen.blit(companyname_text, (850, 725))
                    screen.blit(creditsmail_text1, (10, 710))
                    screen.blit(creditsmail_text2, (10, 725))
                    pygame.display.update()
                    print(negative_point_counter)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if return_to_start_screen.is_clicked(pygame.mouse.get_pos()):
                        has_the_exam_run = True
                        number_of_exam_tries = 3
                        return
                        """budget = player_budget[dataset]
                        username = None
                        reset_grid()
                        main_loop()"""
                        #combined_start_function()
                    elif tip_game_over_ending_button.is_clicked(pygame.mouse.get_pos()):
                        if language == 'gr':
                            transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                            pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                            transparent_surface.blit(wrapped_tip_5, (0, 10))
                            screen.blit(transparent_surface, (100, 200))
                            pygame.display.update()
                        if language == 'en':
                            transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                            pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                            transparent_surface.blit(en_wrapped_tip_5, (0, 10))
                            screen.blit(transparent_surface, (100, 200))
                            pygame.display.update()
                    elif levels_button.is_clicked(pygame.mouse.get_pos()):
                        negative_point_counter = 0
                        reset_grid()
                        Starting_Q = 0
                        initialize_grid()
                        main_loop_exam_mode()
            if number_of_exam_tries == 3:
                if language == 'gr':
                    screen.fill(GREEN)
                    screen.blit(rendered_budget_score, (screen_width // 2 - 250, 700))
                    return_to_start_screen.draw(screen)
                    tip_game_over_ending_button.draw(screen)
                    screen.blit(rendered_game_over, (screen_width // 2 - 150, 10))
                    screen.blit(resized_screenshot, (screen_width // 2 - 225, 125))
                    screen.blit(credits_text, (775, 710))
                    screen.blit(companyname_text, (850, 725))
                    screen.blit(creditsmail_text1, (10, 710))
                    screen.blit(creditsmail_text2, (10, 725))
                    pygame.display.update()
                    print(negative_point_counter)
                elif language == 'en':
                    screen.fill(GREEN)
                    screen.blit(en_rendered_budget_score, (screen_width // 2 - 250, 700))
                    return_to_start_screen.draw(screen)
                    tip_game_over_ending_button.draw(screen)
                    screen.blit(en_rendered_game_over, (screen_width // 2 - 150, 10))
                    screen.blit(resized_screenshot, (screen_width // 2 - 225, 125))
                    screen.blit(credits_text, (775, 710))
                    screen.blit(companyname_text, (850, 725))
                    screen.blit(creditsmail_text1, (10, 710))
                    screen.blit(creditsmail_text2, (10, 725))
                    pygame.display.update()
                    print(negative_point_counter)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if return_to_start_screen.is_clicked(pygame.mouse.get_pos()):
                        has_the_exam_run = True
                        return
                        """budget = player_budget[dataset]
                        username = None
                        reset_grid()
                        main_loop()
                        #combined_start_function()"""
                    elif tip_game_over_ending_button.is_clicked(pygame.mouse.get_pos()):
                        if language == 'gr':
                            transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                            pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                            transparent_surface.blit(wrapped_tip_5, (0, 10))
                            screen.blit(transparent_surface, (100, 200))
                            pygame.display.update()
                        if language == 'en':
                            transparent_surface = pygame.Surface((700, 100), pygame.SRCALPHA)
                            pygame.draw.rect(transparent_surface, (0, 0, 0, 200), transparent_surface.get_rect())
                            transparent_surface.blit(en_wrapped_tip_5, (0, 10))
                            screen.blit(transparent_surface, (100, 200))
                            pygame.display.update()


def drawing_grid():
    global icon_index, available_icons, dropdown_open

    budget_calculator()
    pygame.draw.rect(screen, BLUE, (0, 608, 544 + 63, 52))
    reset_grid_button.draw(screen)
    undo_button.draw(screen)
    tip_button.draw(screen)
    button_for_menu.draw(screen)
    budget_explainer_button.draw(screen)
    # exercise_info()
    # Draw the grid
    for i in range((grid_size - 1)):
        for j in range((grid_size - 1)):
            rect = pygame.Rect(square_x + j * square_size, square_y + i * square_size, square_size, square_size)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
            red_outlines()
            # Draw the icon in the square if it exists
            icon = grid[i][j]
            if icon is not None:
                if icon == BLACK:
                    pygame.draw.rect(screen, BLACK, rect)
                    pygame.draw.rect(screen, WHITE, rect, 1)
                else:
                    icon_scaled = pygame.transform.scale(icon, (square_size - 2, square_size - 2))
                    screen.blit(icon_scaled, rect.move(1, 1))

    """"# Draw the dropdown menu
    if dropdown_open:
        pygame.draw.rect(screen, WHITE, dropdown_rect)
        pygame.draw.rect(screen, BLACK, dropdown_rect, 1)

        for i, icon in enumerate(available_icons):
            icon_scaled = pygame.transform.scale(icon, (square_size, square_size))
            dropdown_icon_rect = pygame.Rect(dropdown_x, dropdown_y + i * square_size, square_size, square_size)
            screen.blit(icon_scaled, dropdown_icon_rect)
    icon_index = 100"""

def drawing_grid2():
    global icon_index

    square_size_2 = 22
    square_x_2 = 50
    square_y_2 = 370
    grid_width = (grid_size - 1) * square_size_2
    grid_height = (grid_size - 1) * square_size_2
    # pygame.draw.rect(screen, BLUE, (screen_width // 2 - 100, screen_height // 2 - 150, (544 + 63) // 10, 52 // 10))

    # Draw the grid
    for i in range((grid_size - 1)):
        for j in range((grid_size - 1)):
            rect = pygame.Rect(square_x_2 + j * square_size_2, square_y_2 + i * square_size_2, square_size_2,
                               square_size_2)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
            # Draw the icon in the square if it exists
            icon = grid[i][j]
            if icon is not None:
                if icon == BLACK:
                    pygame.draw.rect(screen, BLACK, rect)
                    pygame.draw.rect(screen, WHITE, rect, 1)
                else:
                    icon_scaled = pygame.transform.scale(icon, (square_size_2 - 2, square_size_2 - 2))
                    screen.blit(icon_scaled, rect.move(1, 1))

    # Draw a black rectangle around the entire grid
    grid_rect = pygame.Rect(square_x_2, square_y_2, grid_width, grid_height)
    pygame.draw.rect(screen, BLACK, grid_rect, 1)
    icon_index = 100


def bug_report_button_uploader_2():
    # Open GitHub Issues page in default web browser
    webbrowser.open('https://github.com/kkoutrid/Geogame-Downloader/issues')


reset_grid_button = Button(button_x, button_y, button_width, button_height, "Reset")
undo_button = Button(undo_button_x, undo_button_y, button_width, button_height, "Undo")
tip_button = Button(button_x + 110, button_y, button_width, button_height, "Retry")
button_for_menu = IconButton(20, 20, 40, 40, icon_menu_button, icon_size=(40, 40), color=(BLUE))
budget_explainer_button = IconButton(40, 668, 40, 40, icon_dollar_sign, (40, 40), color=(BLUE))


def tutorial(click_area=None):
    print(f"i have started")
    tutorial_icon_width = 1005
    tutorial_icon_height = 750
    # Define the specific pixel area (x, y, width, height)
    click_area_2 = pygame.Rect(518, 637, 64, 64)
    click_area_3 = pygame.Rect(305, 175, 64, 64)
    click_area_4 = pygame.Rect(303, 172, 64, 64)
    click_area_6 = pygame.Rect(141, 242, 64, 64)
    click_area_7 = pygame.Rect(141, 272, 64, 64)
    click_area_8 = pygame.Rect(303, 462, 64, 64)
    click_area_9 = pygame.Rect(303, 495, 64, 64)
    click_area_10 = pygame.Rect(0, 0, screen_width, screen_height)
    click_area_11 = pygame.Rect(300, 274, 64, 64)
    click_area_16 = pygame.Rect(238-32, 176-32, 64, 64)
    click_area_18 = pygame.Rect(368-32, 340-32, 64, 64)
    click_area_19 = pygame.Rect(365-32, 342-32, 64, 64)
    click_area_21 = pygame.Rect(339-32, 345-32, 64, 64)
    click_area_22 = pygame.Rect(333-32, 402-32, 64, 64)
    click_area_26 = pygame.Rect(172-32, 275-32, 64, 64)



    tutorial_icon_1_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_1.PNG")
    tutorial_icon_1 = pygame.image.load(tutorial_icon_1_path).convert_alpha()
    tutorial_icon_2_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_2.PNG")
    tutorial_icon_2 = pygame.image.load(tutorial_icon_2_path).convert_alpha()
    tutorial_icon_3_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_3.PNG")
    tutorial_icon_3 = pygame.image.load(tutorial_icon_3_path).convert_alpha()
    tutorial_icon_4_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_4.PNG")
    tutorial_icon_4 = pygame.image.load(tutorial_icon_4_path).convert_alpha()
    tutorial_icon_5_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_5.PNG")
    tutorial_icon_5 = pygame.image.load(tutorial_icon_5_path).convert_alpha()
    tutorial_icon_6_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_6.PNG")
    tutorial_icon_6 = pygame.image.load(tutorial_icon_6_path).convert_alpha()
    tutorial_icon_7_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_7.PNG")
    tutorial_icon_7 = pygame.image.load(tutorial_icon_7_path).convert_alpha()
    tutorial_icon_8_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_8.png")
    tutorial_icon_8 = pygame.image.load(tutorial_icon_8_path).convert_alpha()
    tutorial_icon_9_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_9.png")
    tutorial_icon_9 = pygame.image.load(tutorial_icon_9_path).convert_alpha()
    tutorial_icon_10_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_10.PNG")
    tutorial_icon_10 = pygame.image.load(tutorial_icon_10_path).convert_alpha()
    tutorial_icon_11_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_11.png")
    tutorial_icon_11 = pygame.image.load(tutorial_icon_11_path).convert_alpha()
    tutorial_icon_12_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_12.PNG")
    tutorial_icon_12 = pygame.image.load(tutorial_icon_12_path).convert_alpha()
    tutorial_icon_13_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_13.PNG")
    tutorial_icon_13 = pygame.image.load(tutorial_icon_13_path).convert_alpha()
    tutorial_icon_14_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_14.PNG")
    tutorial_icon_14 = pygame.image.load(tutorial_icon_14_path).convert_alpha()
    tutorial_icon_15_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_15.PNG")
    tutorial_icon_15 = pygame.image.load(tutorial_icon_15_path).convert_alpha()
    tutorial_icon_16_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_16.PNG")
    tutorial_icon_16 = pygame.image.load(tutorial_icon_16_path).convert_alpha()
    tutorial_icon_17_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_17.PNG")
    tutorial_icon_17 = pygame.image.load(tutorial_icon_17_path).convert_alpha()
    tutorial_icon_18_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_18.png")
    tutorial_icon_18 = pygame.image.load(tutorial_icon_18_path).convert_alpha()
    tutorial_icon_19_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_19.PNG")
    tutorial_icon_19 = pygame.image.load(tutorial_icon_19_path).convert_alpha()
    tutorial_icon_20_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_20.png")
    tutorial_icon_20 = pygame.image.load(tutorial_icon_20_path).convert_alpha()
    tutorial_icon_21_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_21.png")
    tutorial_icon_21 = pygame.image.load(tutorial_icon_21_path).convert_alpha()
    tutorial_icon_22_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_22.png")
    tutorial_icon_22 = pygame.image.load(tutorial_icon_22_path).convert_alpha()
    tutorial_icon_23_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_23.PNG")
    tutorial_icon_23 = pygame.image.load(tutorial_icon_23_path).convert_alpha()
    tutorial_icon_24_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_24.PNG")
    tutorial_icon_24 = pygame.image.load(tutorial_icon_24_path).convert_alpha()
    tutorial_icon_25_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_25.PNG")
    tutorial_icon_25 = pygame.image.load(tutorial_icon_25_path).convert_alpha()
    tutorial_icon_26_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_26.PNG")
    tutorial_icon_26 = pygame.image.load(tutorial_icon_26_path).convert_alpha()
    tutorial_icon_27_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_27.PNG")
    tutorial_icon_27 = pygame.image.load(tutorial_icon_27_path).convert_alpha()
    tutorial_icon_28_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_28.PNG")
    tutorial_icon_28 = pygame.image.load(tutorial_icon_28_path).convert_alpha()
    tutorial_icon_29_path = os.path.join(tutorial_icon_dir, "Tutorial_icon_29.PNG")
    tutorial_icon_29 = pygame.image.load(tutorial_icon_29_path).convert_alpha()

    en_tutorial_icon_1_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_1.PNG")
    en_tutorial_icon_1 = pygame.image.load(en_tutorial_icon_1_path).convert_alpha()
    en_tutorial_icon_2_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_2.PNG")
    en_tutorial_icon_2 = pygame.image.load(en_tutorial_icon_2_path).convert_alpha()
    en_tutorial_icon_3_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_3.PNG")
    en_tutorial_icon_3 = pygame.image.load(en_tutorial_icon_3_path).convert_alpha()
    en_tutorial_icon_4_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_4.PNG")
    en_tutorial_icon_4 = pygame.image.load(en_tutorial_icon_4_path).convert_alpha()
    en_tutorial_icon_5_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_5.PNG")
    en_tutorial_icon_5 = pygame.image.load(en_tutorial_icon_5_path).convert_alpha()
    en_tutorial_icon_6_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_6.PNG")
    en_tutorial_icon_6 = pygame.image.load(en_tutorial_icon_6_path).convert_alpha()
    en_tutorial_icon_7_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_7.PNG")
    en_tutorial_icon_7 = pygame.image.load(en_tutorial_icon_7_path).convert_alpha()
    en_tutorial_icon_8_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_8.png")
    en_tutorial_icon_8 = pygame.image.load(en_tutorial_icon_8_path).convert_alpha()
    en_tutorial_icon_9_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_9.png")
    en_tutorial_icon_9 = pygame.image.load(en_tutorial_icon_9_path).convert_alpha()
    en_tutorial_icon_10_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_10.PNG")
    en_tutorial_icon_10 = pygame.image.load(en_tutorial_icon_10_path).convert_alpha()
    en_tutorial_icon_11_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_11.png")
    en_tutorial_icon_11 = pygame.image.load(en_tutorial_icon_11_path).convert_alpha()
    en_tutorial_icon_12_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_12.PNG")
    en_tutorial_icon_12 = pygame.image.load(en_tutorial_icon_12_path).convert_alpha()
    en_tutorial_icon_13_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_13.PNG")
    en_tutorial_icon_13 = pygame.image.load(en_tutorial_icon_13_path).convert_alpha()
    en_tutorial_icon_14_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_14.PNG")
    en_tutorial_icon_14 = pygame.image.load(en_tutorial_icon_14_path).convert_alpha()
    en_tutorial_icon_15_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_15.PNG")
    en_tutorial_icon_15 = pygame.image.load(en_tutorial_icon_15_path).convert_alpha()
    en_tutorial_icon_16_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_16.PNG")
    en_tutorial_icon_16 = pygame.image.load(en_tutorial_icon_16_path).convert_alpha()
    en_tutorial_icon_17_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_17.PNG")
    en_tutorial_icon_17 = pygame.image.load(en_tutorial_icon_17_path).convert_alpha()
    en_tutorial_icon_18_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_18.png")
    en_tutorial_icon_18 = pygame.image.load(en_tutorial_icon_18_path).convert_alpha()
    en_tutorial_icon_19_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_19.PNG")
    en_tutorial_icon_19 = pygame.image.load(en_tutorial_icon_19_path).convert_alpha()
    en_tutorial_icon_20_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_20.png")
    en_tutorial_icon_20 = pygame.image.load(en_tutorial_icon_20_path).convert_alpha()
    en_tutorial_icon_21_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_21.png")
    en_tutorial_icon_21 = pygame.image.load(en_tutorial_icon_21_path).convert_alpha()
    en_tutorial_icon_22_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_22.png")
    en_tutorial_icon_22 = pygame.image.load(en_tutorial_icon_22_path).convert_alpha()
    en_tutorial_icon_23_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_23.PNG")
    en_tutorial_icon_23 = pygame.image.load(en_tutorial_icon_23_path).convert_alpha()
    en_tutorial_icon_24_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_24.PNG")
    en_tutorial_icon_24 = pygame.image.load(en_tutorial_icon_24_path).convert_alpha()
    en_tutorial_icon_25_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_25.PNG")
    en_tutorial_icon_25 = pygame.image.load(en_tutorial_icon_25_path).convert_alpha()
    en_tutorial_icon_26_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_26.PNG")
    en_tutorial_icon_26 = pygame.image.load(en_tutorial_icon_26_path).convert_alpha()
    en_tutorial_icon_27_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_27.PNG")
    en_tutorial_icon_27 = pygame.image.load(en_tutorial_icon_27_path).convert_alpha()
    en_tutorial_icon_28_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_28.PNG")
    en_tutorial_icon_28 = pygame.image.load(en_tutorial_icon_28_path).convert_alpha()
    en_tutorial_icon_29_path = os.path.join(en_tutorial_icon_dir, "Tutorial_icon_29.PNG")
    en_tutorial_icon_29 = pygame.image.load(en_tutorial_icon_29_path).convert_alpha()

    tutorial_icon_scaled_1 = pygame.transform.scale(tutorial_icon_1, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_2 = pygame.transform.scale(tutorial_icon_2, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_3 = pygame.transform.scale(tutorial_icon_3, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_4 = pygame.transform.scale(tutorial_icon_4, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_5 = pygame.transform.scale(tutorial_icon_5, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_6 = pygame.transform.scale(tutorial_icon_6, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_7 = pygame.transform.scale(tutorial_icon_7, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_8 = pygame.transform.scale(tutorial_icon_8, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_9 = pygame.transform.scale(tutorial_icon_9, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_10 = pygame.transform.scale(tutorial_icon_10, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_11 = pygame.transform.scale(tutorial_icon_11, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_12 = pygame.transform.scale(tutorial_icon_12, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_13 = pygame.transform.scale(tutorial_icon_13, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_14 = pygame.transform.scale(tutorial_icon_14, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_15 = pygame.transform.scale(tutorial_icon_15, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_16 = pygame.transform.scale(tutorial_icon_16, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_17 = pygame.transform.scale(tutorial_icon_17, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_18 = pygame.transform.scale(tutorial_icon_18, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_19 = pygame.transform.scale(tutorial_icon_19, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_20 = pygame.transform.scale(tutorial_icon_20, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_21 = pygame.transform.scale(tutorial_icon_21, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_22 = pygame.transform.scale(tutorial_icon_22, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_23 = pygame.transform.scale(tutorial_icon_23, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_24 = pygame.transform.scale(tutorial_icon_24, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_25 = pygame.transform.scale(tutorial_icon_25, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_26 = pygame.transform.scale(tutorial_icon_26, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_27 = pygame.transform.scale(tutorial_icon_27, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_28 = pygame.transform.scale(tutorial_icon_28, (tutorial_icon_width, tutorial_icon_height))
    tutorial_icon_scaled_29 = pygame.transform.scale(tutorial_icon_29, (tutorial_icon_width, tutorial_icon_height))

    en_tutorial_icon_scaled_1 = pygame.transform.scale(en_tutorial_icon_1, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_2 = pygame.transform.scale(en_tutorial_icon_2, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_3 = pygame.transform.scale(en_tutorial_icon_3, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_4 = pygame.transform.scale(en_tutorial_icon_4, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_5 = pygame.transform.scale(en_tutorial_icon_5, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_6 = pygame.transform.scale(en_tutorial_icon_6, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_7 = pygame.transform.scale(en_tutorial_icon_7, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_8 = pygame.transform.scale(en_tutorial_icon_8, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_9 = pygame.transform.scale(en_tutorial_icon_9, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_10 = pygame.transform.scale(en_tutorial_icon_10, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_11 = pygame.transform.scale(en_tutorial_icon_11, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_12 = pygame.transform.scale(en_tutorial_icon_12, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_13 = pygame.transform.scale(en_tutorial_icon_13, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_14 = pygame.transform.scale(en_tutorial_icon_14, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_15 = pygame.transform.scale(en_tutorial_icon_15, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_16 = pygame.transform.scale(en_tutorial_icon_16, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_17 = pygame.transform.scale(en_tutorial_icon_17, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_18 = pygame.transform.scale(en_tutorial_icon_18, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_19 = pygame.transform.scale(en_tutorial_icon_19, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_20 = pygame.transform.scale(en_tutorial_icon_20, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_21 = pygame.transform.scale(en_tutorial_icon_21, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_22 = pygame.transform.scale(en_tutorial_icon_22, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_23 = pygame.transform.scale(en_tutorial_icon_23, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_24 = pygame.transform.scale(en_tutorial_icon_24, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_25 = pygame.transform.scale(en_tutorial_icon_25, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_26 = pygame.transform.scale(en_tutorial_icon_26, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_27 = pygame.transform.scale(en_tutorial_icon_27, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_28 = pygame.transform.scale(en_tutorial_icon_28, (tutorial_icon_width, tutorial_icon_height))
    en_tutorial_icon_scaled_29 = pygame.transform.scale(en_tutorial_icon_29, (tutorial_icon_width, tutorial_icon_height))

    counter = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if counter == 1:
                gate_value_1 = show_input_box_tutorial(10, 10, screen_width, screen_height, text="")
                if gate_value_1 == 1700:
                    if language == "gr":
                        screen.blit(tutorial_icon_scaled_2, (0, 0))
                        pygame.display.update()
                    elif language == "en":
                        screen.blit(en_tutorial_icon_scaled_2, (0, 0))
                        pygame.display.update()
                    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    print("Mouse clicked at:", mouse_x, mouse_y)
                    counter += 1
                    print(counter)
                    print(gate_value_1)
                    print("end slide 1")
                else:
                    break
            if gate_value_1 == 1700 and counter == 2:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and click_area_2.collidepoint(event.pos):
                    if language == "gr":
                        screen.blit(tutorial_icon_scaled_3, (0, 0))
                    elif language == "en":
                        screen.blit(en_tutorial_icon_scaled_3, (0, 0))
                    pygame.display.update()
                    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    print("Mouse clicked at:", mouse_x, mouse_y)
                    counter += 1
                    print(counter)
                    print("end slide 2")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 3 and click_area_3.collidepoint(event.pos):
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_4, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_4, (0, 0))
                pygame.display.update()
                print(counter)
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 3")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 4 and click_area_4.collidepoint(event.pos):
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_5, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_5, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 4")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 5:
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_6, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_6, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 5")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 6 and click_area_6.collidepoint(event.pos):
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_7, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_7, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 6")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 7 and click_area_7.collidepoint(event.pos):
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_8, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_8, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 7")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 8: #click_area_8.collidepoint(event.pos):
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_9, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_9, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 8")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 9 and click_area_8.collidepoint(event.pos):
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_10, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_10, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 9")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 10 and click_area_9.collidepoint(event.pos):
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_11, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_11, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 10")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 11 and click_area_10.collidepoint(event.pos):
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_12, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_12, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 11")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 12 and click_area_11.collidepoint(event.pos):
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_13, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_13, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 12")
            elif counter == 13:
                gate_value_2 = show_input_box_tutorial_2(dropdown_x, dropdown_y, dropdown_width, dropdown_height, text="")
                if gate_value_2 == 1300:
                    counter += 1
                    if language == "gr":
                        screen.blit(tutorial_icon_scaled_14, (0, 0))
                    elif language == "en":
                        screen.blit(en_tutorial_icon_scaled_14, (0, 0))
                    pygame.display.update()
                    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    print("Mouse clicked at:", mouse_x, mouse_y)
                    print("end slide 13")
                else:
                    break
            elif counter == 14:
                gate_value_3 = show_input_box_tutorial_2(dropdown_x, dropdown_y, dropdown_width, dropdown_height, text="")
                if gate_value_3 == 200:
                    counter += 1
                    if language == "gr":
                        screen.blit(tutorial_icon_scaled_15, (0, 0))
                    elif language == "en":
                        screen.blit(en_tutorial_icon_scaled_15, (0, 0))
                    pygame.display.update()
                    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    print("Mouse clicked at:", mouse_x, mouse_y)
                    print("end slide 14")
                else:
                    break
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 15:
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_16, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_16, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 15")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and counter == 16 and click_area_16.collidepoint(event.pos):
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_17, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_17, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 16")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 17:
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_18, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_18, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 17")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 18 and click_area_18.collidepoint(event.pos):
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_19, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_19, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 18")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 19 and click_area_19.collidepoint(event.pos):
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_20, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_20, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 19")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 20:
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_21, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_21, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 20")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 21 and click_area_21.collidepoint(event.pos):
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_22, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_22, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 21")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 22 and click_area_22.collidepoint(event.pos):
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_23, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_23, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 22")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 23:
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_24, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_24, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 23")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 24:
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_25, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_25, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 24")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 25:
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_26, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_26, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 25")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 26 and click_area_26.collidepoint(event.pos):
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_27, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_27, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 26")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 27:
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_28, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_28, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 27")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and counter == 28:
                counter += 1
                if language == "gr":
                    screen.blit(tutorial_icon_scaled_29, (0, 0))
                elif language == "en":
                    screen.blit(en_tutorial_icon_scaled_29, (0, 0))
                pygame.display.update()
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (10, 10), 'button': 1}))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at:", mouse_x, mouse_y)
                print("end slide 28")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                counter = 0
                return
def enhancer_system():
    global enhancer_usage
    screen.fill(BLUE)
    pygame.display.update()
    yes_button = Button(screen_width // 2 - 200, screen_height // 2 + 100, 150, 50, "Yes", (RED2), (GRAY))
    no_button = Button(screen_width // 2 + 50, screen_height // 2 + 100, 150, 50, "No", (RED2), (GRAY))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            pygame.draw.rect(screen, WHITE, (screen_width // 2 - 150, 100, 300, 150))
            pygame.draw.rect(screen, BLACK, (screen_width // 2 - 150, 100, 300, 150), 2)  # Outline
            pygame.draw.line(screen, BLACK, (screen_width // 2 - 150, 100), (1005 // 2 + 150, 100 + 150),
                             2)  # Diagonal line
            yes_button.draw(screen)
            no_button.draw(screen)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.is_clicked(pygame.mouse.get_pos()):
                    enhancer_usage = True
                    screen.fill(BLUE)
                    return enhancer_usage
                elif no_button.is_clicked(pygame.mouse.get_pos()):
                    enhancer_usage = False
                    screen.fill(BLUE)
                    return enhancer_usage


def leaderboard():
    font = pygame.font.Font(info_font, 20)
    y_offset = 50
    x_offset = 30
    levels_per_row = 7
    idata = pd.read_excel(root_dir + "\GameAssets\geodata.xlsx", sheet_name="info")
    dataset_column = idata["Dataset"]
    high_score_per_level = idata["high_score"]
    levels_that_exist = dataset_column[dataset_column.apply(lambda x: isinstance(x, (int, float)))]
    number_of_levels = len(levels_that_exist)
    already_created = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # Render and display level and high score for each entry in the dataset
            if not already_created:
                screen.fill(BLUE)
                back_button = Button(0, 0, 200, 50, "Back", RED, WHITE)
                back_button.draw(screen)
                for i, score in enumerate(high_score_per_level):
                    if isinstance(score, (int, float)) and not math.isnan(score):
                        high_score = str(int(score))
                    else:
                        high_score = "N/A"

                    print(f"High score for level {i + 1}: {high_score}")
                    text_surface = font.render(f"Level {i + 1}: {high_score}", True, (255, 255, 255))

                    screen.blit(text_surface, (x_offset, 70 + y_offset))  # Display text at current x and y offsets
                    x_offset += 140  # Move to the next position horizontally

                    # Start a new row if the current row is full
                    if (i + 1) % levels_per_row == 0:
                        x_offset = 30  # Reset x position for the new row
                        y_offset += 50  # Move down to the next row

                    if i == number_of_levels - 1:  # Stop after displaying all levels
                        already_created = True
                        break

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.is_clicked(pygame.mouse.get_pos()):
                    already_created = False
                    return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                already_created = False
                return

        pygame.display.update()


def update_high_score(file_path, dataset, budget_calculated, high_score_column_name):
    # Read the Excel file using openpyxl
    wb = load_workbook(filename=file_path)
    sheet = wb["info"]

    # Find the row index based on the 'Dataset' value, starting from row 2
    dataset_index = None
    for row in sheet.iter_rows(min_row=2):  # Start iterating from row 2
        if row[0].value == dataset:
            dataset_index = row[0].row  # Adjust for 1-based indexing
            break

    if not dataset_index:
        return False  # 'Dataset' value not found

    # Find the high_score column index
    high_score_column_index = None
    for cell in sheet[1]:  # Iterate through the header row
        if cell.value == high_score_column_name:
            high_score_column_index = cell.column  # Adjust for 1-based indexing
            break

    if not high_score_column_index:
        raise ValueError(f"Column '{high_score_column_name}' not found in header row")

    # Get the current high_score value
    current_high_score = sheet.cell(row=dataset_index, column=high_score_column_index).value

    # Update the high_score value only if the new value is higher
    if current_high_score is None or budget_calculated > current_high_score:
        sheet.cell(row=dataset_index, column=high_score_column_index).value = budget_calculated

        # Save the updated workbook
        wb.save(filename=file_path)

        # Load the updated value directly from the modified Excel file
        updated_wb = load_workbook(filename=file_path)
        updated_sheet = updated_wb["info"]
        updated_high_score = updated_sheet.cell(row=dataset_index, column=high_score_column_index).value

        return updated_high_score  # Return the updated high score value
    else:
        return current_high_score  # Return the existing high score value


def reset_high_scores(file_path):
    # Load the Excel file
    workbook = load_workbook(filename=file_path)

    # Choose the sheet by name
    sheet_name = 'info'
    sheet = workbook[sheet_name]

    # Find the column index of 'high_score'
    high_score_column_index = None
    for cell in sheet[1]:  # Assuming the header row is the first row
        if cell.value == 'high_score':
            high_score_column_index = cell.column
            break

    if high_score_column_index:
        # Iterate through each row in the 'high_score' column and set the cell value to 0
        for row in sheet.iter_rows(min_row=2, min_col=high_score_column_index, max_col=high_score_column_index):
            for cell in row:
                cell.value = 0

        # Save the changes to the Excel file
        workbook.save(filename=file_path)
        print("High scores reset to 0.")
    else:
        print("Column 'high_score' not found.")


transparent_surface_visible2 = False


def budget_explainer():
    global transparent_surface_visible2
    print("It worked")

    transparent_surface_visible2 = not transparent_surface_visible2
    transparent_surface2_width = 300
    transparent_surface2_height = 350

    flat_placement_grid = [num for row in placement_grid for num in row]
    pipe_type_counter = Counter(flat_placement_grid)

    simple_pipe_costs = ((pipe_type_counter[0] + pipe_type_counter[1]) * 50)
    corner_pipe_costs = (
                (pipe_type_counter[2] + pipe_type_counter[3] + pipe_type_counter[4] + pipe_type_counter[5]) * 60)
    triplet_pipe_costs = (
                (pipe_type_counter[6] + pipe_type_counter[7] + pipe_type_counter[8] + pipe_type_counter[9]) * 100)
    aux_cost_h0 = heat_help_h0
    aux_cost_h1 = heat_help_h1
    aux_cost_h2 = heat_help_h2
    aux_cost_g0 = heat_help_g0
    aux_cost_g1 = heat_help_g1
    print(simple_pipe_costs, corner_pipe_costs, triplet_pipe_costs, aux_cost_h0, aux_cost_h1, aux_cost_h2, aux_cost_g0,
          aux_cost_g1)

    font = pygame.font.Font(info_font, 16)
    simple_text_1 = f"cost = {int(simple_pipe_costs)}"
    simple_text = font.render(simple_text_1, True, WHITE)
    cost_text_2 = f"cost = {int(corner_pipe_costs)}"
    corner_text = font.render(cost_text_2, True, WHITE)
    cost_text_3 = f"cost = {int(triplet_pipe_costs)}"
    triplet_text = font.render(cost_text_3, True, WHITE)
    cost_text_4 = f"aux cost 1 = {int(aux_cost_h0)}"
    aux_cost_h0_text = font.render(cost_text_4, True, WHITE)
    cost_text_5 = f"aux cost 2 = {int(aux_cost_h1)}"
    aux_cost_h1_text = font.render(cost_text_5, True, WHITE)
    cost_text_6 = f"aux cost 3 = {int(aux_cost_h2)}"
    aux_cost_h1_text = font.render(cost_text_6, True, WHITE)
    cost_text_7 = f"aux cost 3 = {int(aux_cost_g0)}"
    aux_cost_g0_text = font.render(cost_text_7, True, WHITE)
    runs = 0
    if house0_row[dataset] > 0:
        transparent_surface2 = pygame.Surface((transparent_surface2_width, transparent_surface2_height),
                                              pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface2, (0, 0, 0, 200), transparent_surface2.get_rect())
    icon1 = pygame.transform.scale(icons[0], (25, 25))
    icon2 = pygame.transform.scale(icons[1], (25, 25))
    icon3 = pygame.transform.scale(icons[2], (25, 25))
    icon5 = pygame.transform.scale(icons[4], (25, 25))
    icon4 = pygame.transform.scale(icons[3], (25, 25))
    icon6 = pygame.transform.scale(icons[5], (25, 25))
    icon7 = pygame.transform.scale(icons[6], (25, 25))
    icon8 = pygame.transform.scale(icons[7], (25, 25))
    icon9 = pygame.transform.scale(icons[8], (25, 25))
    icon10 = pygame.transform.scale(icons[9], (25, 25))
    iconh0 = pygame.transform.scale(icon_building1, (25, 25))
    iconh1 = pygame.transform.scale(icon_building2, (25, 25))
    iconh2 = pygame.transform.scale(icon_building3, (25, 25))
    icong0 = pygame.transform.scale(icon_greenhouse, (25, 25))

    def open_transparent_display(runs, transparent_surface2):
        if runs == 0 and house0_row[dataset] > 0:
            transparent_surface2.blit(icon1, (20, 20))
            transparent_surface2.blit(icon2, (20 + 40, 20))
            transparent_surface2.blit(simple_text, (50 + 80, 20))
            transparent_surface2.blit(icon3, (20, 100))
            transparent_surface2.blit(icon4, (20 + 40, 100))
            transparent_surface2.blit(icon5, (20 + 80, 100))
            transparent_surface2.blit(icon6, (20 + 120, 100))
            transparent_surface2.blit(corner_text, (50 + 160, 100))
            transparent_surface2.blit(icon7, (20, 180))
            transparent_surface2.blit(icon8, (20 + 40, 180))
            transparent_surface2.blit(icon9, (20 + 80, 180))
            transparent_surface2.blit(icon10, (20 + 120, 180))
            transparent_surface2.blit(triplet_text, (50 + 160, 180))
            if house0_row[dataset] > 0 and not house1_row[dataset] > 0 and not greenhouse0_row[dataset] > 0:
                transparent_surface2.blit(iconh0, (20, 220))
                transparent_surface2.blit(aux_cost_h0_text, (50, 227))
            if house0_row[dataset] > 0 and house1_row[dataset] > 0 and not greenhouse0_row[dataset] > 0:
                transparent_surface2.blit(iconh0, (20, 220))
                transparent_surface2.blit(aux_cost_h0_text, (50, 227))
                transparent_surface2.blit(iconh1, (20, 260))
                transparent_surface2.blit(aux_cost_h1_text, (50, 267))
            if house0_row[dataset] > 0 and house1_row[dataset] > 0 and greenhouse0_row[dataset] > 0:
                transparent_surface2.blit(iconh0, (20, 220))
                transparent_surface2.blit(aux_cost_h0_text, (50, 227))
                transparent_surface2.blit(iconh1, (20, 260))
                transparent_surface2.blit(aux_cost_h1_text, (50, 267))
                transparent_surface2.blit(icong0, (20, 300))
                transparent_surface2.blit(aux_cost_g0_text, (50, 307))
            screen.blit(transparent_surface2, (150, 150))
            pygame.display.update()
            runs = + 1
            return runs
        else:
            pass

    def close_transparent_display():
        return

    while transparent_surface_visible2:  # Keep running while transparent_surface_visible2 is True
        runs = open_transparent_display(runs, transparent_surface2)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                transparent_surface_visible2 = False  # Set visible to False upon click
                break  # Exit the event loop after the click
        close_transparent_display()  # Keep the loop running if transparent_surface_visible2 is True

    return


# game_variables
dataset = 0
things_around_left = 0
things_around_right = 0
things_around_down = 0
things_around_up = 0
things_around = 0
pipe_section = 0
icon_index = 100
rw_existence = True
cell_info = False
username = ""
Q = {}
T = {}
T[pipe_section] = []
Q2 = {}
Starting_Q = 0
Starting_T = T0[dataset]
number_of_items = 0
budget = player_budget[dataset]
budget_calculated = player_budget[dataset]
tip_button_box = False
heat_help_h0 = 0
heat_help_h1 = 0
heat_help_h2 = 0
heat_help_g0 = 0
heat_help_g1 = 0
language = 'en'
enhancer_usage = False
high_score_column_name = 'high_score'
running_number = 0
row = 0
col = 0
#row = pw_row - 1
#col = pw_col
# Stacks
undo_stack = []
grid_versions = []
def initialising_the_values():
    global things_around_left
    global things_around_right
    global things_around_down
    global things_around_up
    global things_around
    global pipe_section
    global icon_index
    global rw_existence
    global cell_info
    global username
    global Q
    global T
    global Q2
    global Starting_Q
    global Starting_T
    global number_of_items
    global budget
    global budget_calculated
    global tip_button_box
    global heat_help_h0
    global heat_help_h1
    global heat_help_h2
    global heat_help_g0
    global heat_help_g1
    global language
    global enhancer_usage
    global high_score_column_name
    global running_number
    global row
    global col
    global undo_stack
    global grid_versions
    global square_x
    global square_y
    global grid
    global placement_grid
    global Q_grid
    global T_grid
    global pipe_section_grid
    global dropdown_open
    global dropdown_x
    global dropdown_y
    global dropdown_width
    global dropdown_height
    global dropdown_rect
    global button_width
    global button_height
    global button_x
    global button_y
    global undo_button_x
    global undo_button_y
    global pipe_section_button_width
    global pipe_section_button_height
    global pipe_section_button_x
    global language_button_x
    global language_button_y
    global language_button_width
    global language_button_height
    global icon_UKflag_scaled
    global icon_Greeceflag_scaled
    global bug_report_button_x
    global bug_report_button_y
    global bug_report_button_width
    global bug_report_button_height
    global icon_bug_report_button_scaled
    global bug_report_button
    global available_icons

    # Initialize the values
    things_around_left = 0
    things_around_right = 0
    things_around_down = 0
    things_around_up = 0
    things_around = 0
    pipe_section = 0
    icon_index = 100
    rw_existence = True
    cell_info = False
    username = ""
    Q = {}
    T = {}
    T[pipe_section] = []
    Q2 = {}
    Starting_Q = 0
    Starting_T = T0[dataset]  # Ensure T0 is defined before using
    number_of_items = 0
    budget = player_budget[dataset]  # Ensure player_budget is defined before using
    budget_calculated = player_budget[dataset]
    tip_button_box = False
    heat_help_h0 = 0
    heat_help_h1 = 0
    heat_help_h2 = 0
    heat_help_g0 = 0
    heat_help_g1 = 0
    language = 'en'
    enhancer_usage = False
    high_score_column_name = 'high_score'
    running_number = 0
    row = 0
    col = 0
    undo_stack = []
    grid_versions = []
    square_x = 64  # Grid top left x coordinate start
    square_y = 64  # Grid top left y coordinate start

    # Initialize the grid state
    grid = [[None] * grid_size for _ in range(grid_size)]
    placement_grid = [[-1] * grid_size for _ in range(grid_size)]
    Q_grid = [[-2] * grid_size for _ in range(grid_size)]
    T_grid = [[0] * grid_size for _ in range(grid_size)]
    pipe_section_grid = [[0] * grid_size for _ in range(grid_size)]
    dropdown_open = False
    dropdown_x = 0
    dropdown_y = 0
    dropdown_width = square_size
    dropdown_height = square_size * len(icons)
    dropdown_rect = pygame.Rect(0, 0, 0, 0)

    button_width = 100
    button_height = 50
    button_x = (((screen_width - 300) - button_width) // 2)
    button_y = 800 - square_size - button_height - 110
    undo_button_x = button_x - button_width - 10
    undo_button_y = button_y
    pipe_section_button_width = 184
    pipe_section_button_height = 50
    pipe_section_button_x = button_x + button_width + 10
    language_button_x = screen_width - 133
    language_button_y = screen_height - 95
    language_button_width = 65
    language_button_height = 50
    icon_UKflag_scaled = pygame.transform.scale(icon_UKflag, (language_button_width, language_button_height))
    icon_Greeceflag_scaled = pygame.transform.scale(icon_Greeceflag, (language_button_width, language_button_height))
    bug_report_button_x = screen_width // 2 - 25
    bug_report_button_y = screen_height // 2 + 300
    bug_report_button_width = 50
    bug_report_button_height = 50
    icon_bug_report_button_scaled = pygame.transform.scale(icon_bug_report,
                                                           (bug_report_button_width, bug_report_button_height))
    bug_report_button = IconButton(bug_report_button_x, bug_report_button_y, bug_report_button_width,
                                   bug_report_button_height, icon_bug_report,
                                   icon_size=(bug_report_button_width, bug_report_button_height), color=BLUE3)
    available_icons = []
negative_point_counter = 0
def main_loop_exam_mode():
    global things_around_up, things_around_down, things_around_left, things_around_right, things_around, number_of_items, dropdown_open, Starting_Q, pipe_section, row, col, negative_point_counter
    clock = pygame.time.Clock()
    mistake_1 = 0
    mistake_2 = 0
    mistake_3 = 0
    mistake_4 = 0
    starting_the_puzzle_exam_mode()
    #combined_start_function()
    screen.fill(BLUE)
    print(type(row), type(col), row, col)
    print(pipe_section_grid)
    "το πρόβλημα φαίνεται πως είναι ότι, για κάποιο λόγο μετά το retry το pipe_section_grid μετατρέπετε σε διαφορετικής μορφής array"
    #row = pw_row - 1
    #col = pw_col
    #reset_grid()
    initialize_grid()
    drawing_grid()
    if house0_row[dataset] > 0: pipe_section_grid_for_icon_house0()
    if house1_row[dataset] > 0: pipe_section_grid_for_icon_house1()
    if house2_row[dataset] > 0: pipe_section_grid_for_icon_house2()
    if greenhouse0_row[dataset] > 0: pipe_section_grid_for_icon_greenhouse0()
    if greenhouse1_row[dataset] > 0: pipe_section_grid_for_icon_greenhouse1()
    # Clear the screen
    running = True
    placed_new_item = False  # Flag to track if a new item is placed
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                undo()
                drawing_grid()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_grid()
                initialize_grid()
                drawing_grid()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                budget_explainer()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not dropdown_open:
                # Check if the button to reset the grid is clicked
                if reset_grid_button.is_clicked(pygame.mouse.get_pos()):
                    reset_grid()
                    initialize_grid()
                    drawing_grid()
                # Check if the button to undo is clicked
                elif undo_button.is_clicked(pygame.mouse.get_pos()):
                    undo()
                    drawing_grid()
                    # Check if the Retry button is clicked
                elif tip_button.is_clicked(pygame.mouse.get_pos()):
                    reset_grid()
                    Starting_Q = 0
                    initialize_grid()
                    main_loop()
                    #starting_the_puzzle()
                    # initialize_grid()
                    # tip_button_main_game_click()
                    # Pipe information cost
                elif button_for_menu.is_clicked(pygame.mouse.get_pos()):
                    display_for_pipe_cost()
                elif budget_explainer_button.is_clicked(pygame.mouse.get_pos()):
                    budget_explainer()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 64 <= event.pos[0] <= 544 + 64 and 64 <= event.pos[1] <= 544 + 64:  # The pixel "space" of the grid
                        print("I reached this part")

                        row = (event.pos[1] - square_y) // square_size
                        print(f"The value of row is {row}")
                        col = (event.pos[0] - square_x) // square_size
                        print(f"The value of col is {col}")
                        #available_icons = get_available_icons(row, col)
                        #get_available_icons(row, col)
                        #return get_available_icons
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
                                    0 <= neighbor_row < (grid_size - 1)
                                    and 0 <= neighbor_col < (grid_size - 1)
                                    and placement_grid[neighbor_row][neighbor_col] > -1
                            ):
                                # = [int(num) for num in my_string.split(',')]
                                icons2rem.append(na_icons[i][placement_grid[neighbor_row][neighbor_col]])
                        if len(icons2rem) != 0:
                            icons2rem = [int(j) for j in ",".join(icons2rem).split(',')]
                            icons2rem = list(set(icons2rem))
                            # print('in', icons2rem)
                            for j in icons2rem:
                                available_icons.remove(icons[j - 1])
                            if row == 0:
                                for i in [1, 4, 5, 7, 8, 9]:
                                    if icons[i] in available_icons:
                                        available_icons.remove(icons[i])
                            if col == 0:
                                for i in [0, 3, 4, 6, 7, 8]:
                                    if icons[i] in available_icons:
                                        available_icons.remove(icons[i])
                            if row == 16:  # error for last row
                                for i in [1, 2, 3, 6, 7, 9]:
                                    if icons[i] in available_icons:
                                        available_icons.remove(icons[i])
                            if col == 16:  # error for last column
                                for i in [0, 2, 5, 6, 8, 9]:
                                    if icons[i] in available_icons:
                                        available_icons.remove(icons[i])
                        print('out', available_icons)
                        print('out2', len(available_icons))
                        if placement_grid[row][col] == 11:
                            pass
                            """enhancer_system()
                            print(enhancer_usage)"""
                        print(f"that's where i stopped1")
                        if 0 <= row < (grid_size - 1) and 0 <= col < (grid_size - 1) and (
                                (row + 1 < (grid_size - 1) and (
                                        (placement_grid[row + 1][col] == 11 and 0 <= placement_grid[row + 2][
                                            col] <= 10) or (
                                                0 <= placement_grid[row + 1][col] <= 10))) or
                                (row - 1 >= 0 and (
                                        (placement_grid[row - 1][col] == 11 and 0 <= placement_grid[row - 2][
                                            col] <= 10) or (
                                                0 <= placement_grid[row - 1][col] <= 10))) or
                                (col - 1 >= 0 and (
                                        (placement_grid[row][col - 1] == 11 and 0 <= placement_grid[row][
                                            col - 2] <= 10) or (
                                                0 <= placement_grid[row][col - 1] <= 10))) or
                                (col + 1 < (grid_size - 1) and (
                                        (placement_grid[row][col + 1] == 11 and 0 <= placement_grid[row][
                                            col + 2] <= 10) or (
                                                0 <= placement_grid[row][col + 1] <= 10)))
                        ):
                            print(f"that's where i stopped1")
                            if placement_grid[row][col] == -1 and (
                                    (placement_grid[row][col - 1] in (0, 2, 5, 6, 8, 9, 10, 12)) or \
                                    (placement_grid[row][col + 1] in (0, 3, 4, 6, 7, 8, 10, 12)) or \
                                    (placement_grid[row + 1][col] in (1, 4, 5, 7, 8, 9, 10, 12)) or \
                                    ((placement_grid[row - 1][col] == 11) and Q_grid[row - 2][col] != -2) or \
                                    (placement_grid[row - 1][col] in (
                                            1, 2, 3, 6, 7, 9, 10,
                                            12))):  # Διόρθωση για να μην επιτρέπεται τοποθέτηση σε λάθος θέση
                                print(f"that's where i stopped2")
                                dropdown_x = square_x + col * square_size
                                dropdown_y = square_y + (row + 1) * square_size
                                dropdown_width = square_size
                                dropdown_height = square_size * len(available_icons)
                                dropdown_rect = pygame.Rect(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                dropdown_open = True
                                #selected_icon = None
                                if dropdown_open:
                                    pygame.draw.rect(screen, WHITE, dropdown_rect)
                                    pygame.draw.rect(screen, BLACK, dropdown_rect, 1)

                                    for i, icon in enumerate(available_icons):
                                        icon_scaled = pygame.transform.scale(icon, (square_size, square_size))
                                        dropdown_icon_rect = pygame.Rect(dropdown_x, dropdown_y + i * square_size,
                                                                         square_size, square_size)
                                        screen.blit(icon_scaled, dropdown_icon_rect)
                                        print(f"that's where i stopped3")
                        else:
                            dropdown_open = False
                            drawing_grid()
                            selected_icon = grid[row][col]
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and dropdown_open:
                if not dropdown_rect.collidepoint(event.pos):
                    dropdown_open = False
                    drawing_grid()
                    selected_icon = None
                else:
                    current_placement_grid = copy.deepcopy(placement_grid)
                    current_Q_grid = copy.deepcopy(Q_grid)
                    current_T_grid = copy.deepcopy(T_grid)
                    current_pipe_section_grid = copy.deepcopy(pipe_section_grid)
                    grid_versions.append({
                        'placement_grid': current_placement_grid,
                        'Q_grid': current_Q_grid,
                        'T_grid': current_T_grid,
                        'pipe_section_grid': current_pipe_section_grid
                    })

                    icon_index = (event.pos[1] - dropdown_y) // square_size
                    # selected_icon = icons[icon_index]
                    selected_icon = available_icons[icon_index]
                    icon_index = icons.index(selected_icon)
                    print("icon_index:", icon_index)
                    row = (dropdown_y - square_y - square_size) // square_size
                    print(f"The value of row2 is {row}")
                    col = (dropdown_x - square_x) // square_size
                    print(f"The value of col2 is {col}")
                    grid[row][col] = selected_icon
                    placement_grid[row][col] = icon_index
                    if dropdown_open == True and placed_new_item == False and 0 <= icon_index <= 9 and \
                            T_grid[pw_row[dataset] - 1][pw_col[dataset]] != 0:
                        if pipe_section_grid[row][col] == 0:
                            # things_around = 0  # things_around== Τα πράγματα με τα οποία μπορείς να συνδεθείς
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
                                        # things_around += 1
                                        things_around_left += 1
                                elif i == 1:
                                    ty = placement_grid[row - 1][col]
                                    trow = row - 1
                                    tcol = col
                                    # print(ty)
                                    ty_2 = ty
                                    if ty_2 > -1 and conn[i][icon_index] * conn[tx][ty] > 0:
                                        # things_around += 1
                                        things_around_up += 1
                                elif i == 2:
                                    ty = placement_grid[row][col + 1]
                                    trow = row
                                    tcol = col + 1
                                    # print(ty)
                                    ty_3 = ty
                                    if ty_3 > -1 and conn[i][icon_index] * conn[tx][ty] > 0:
                                        things_around_right += 1
                                elif i == 3:
                                    ty = placement_grid[row + 1][col]
                                    trow = row + 1
                                    tcol = col
                                    # print(ty)
                                    ty_4 = ty
                                    if ty_4 > -1 and conn[i][icon_index] * conn[tx][ty] > 0:
                                        # things_around += 1
                                        things_around_down += 1
                                things_around = things_around_left + things_around_up + things_around_right + things_around_down
                                if ty == -1: conn[tx][ty] = 0
                                if conn[i][icon_index] * conn[tx][ty] > 0 and things_around <= 1 and \
                                        placement_grid[row - 1][col] <= 9 and 0 <= icon_index <= 5:
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
                                        placement_grid[row - 1][col] > 9 and placement_grid[row - 1][
                                    col] != 10 and 0 <= icon_index <= 5:
                                    pipe_section += 1
                                    pipe_section_grid[row][col] = pipe_section
                                    Q[pipe_section_grid[row][col]] = Q_grid[row - 1][
                                        col]  # This does not allow wrong Q by the player. With  Q_grid[row - 2][col] it does.
                                    T[pipe_section_grid[row][col]] = [(min(T_grid[row - 1][col]) - Tloss_pipe[dataset])]
                                    # T[pipe_section_grid[row][col]] = min(T_grid[row - 1][col])
                                    T_grid[row][col] = T[pipe_section_grid[row][col]]
                                if conn[i][icon_index] * conn[tx][
                                    ty] > 0 and things_around > 1 and 0 <= icon_index <= 5 and \
                                        pipe_section_grid[row + 1][col] <= -11:
                                    pipe_section_grid[row][col] = pipe_section_grid[row - 1][
                                        col]  # min(element for element in[pipe_section_grid[row][col - 1],pipe_section_grid[row - 1][col], pipe_section_grid[row][col + 1], pipe_section_grid[row + 1][col]] if element > 0)
                                    Q_grid[row][col] = Q[pipe_section_grid[row][col]]
                                    #if Q_grid[row][col] != Q_grid[row + 1][col]:
                                        #game_over_Q_inconsistent()
                                        # Q_grid[row+1][col] = Q[pipe_section_grid[row][col]]
                                    # T[pipe_section_grid[row][col]] -= Tloss_pipe
                                    # sygrinw tin timi eisodou toy house me tin ypologismeni T_grid[row][col]
                                    # Q_grid[row + 1][col] = Q_grid[row][col]
                            Q_grid[row][col] = Q[pipe_section_grid[row][col]]
                            # T_grid[row][col] = T[pipe_section_grid[row][col]][-1] - Tloss_pipe
                        elif pipe_section_grid[row][col] != 0 and Q_grid[row][col] != 0 and 0 <= icon_index <= 5:
                            # things_around = 0  # things_around== Τα πράγματα με τα οποία μπορείς να συνδεθείς
                            # i: 0=left, 1=up, 2=right, 3=down
                            for i in range(0, 4):
                                tx = (i + 2) % 4
                                print(tx)
                                if i == 0:  # ti icon type exei to row-1
                                    ty = placement_grid[row][col - 1]
                                    trow = row
                                    tcol = col - 1
                                    ty_1 = ty
                                    if ty_1 > -1 and conn[i][icon_index] * conn[tx][ty] > 0:
                                        things_around_left += 1
                                elif i == 1:
                                    ty = placement_grid[row - 1][col]
                                    trow = row - 1
                                    tcol = col
                                    ty_2 = ty
                                    if ty_2 > -1 and conn[i][icon_index] * conn[tx][ty] > 0:
                                        things_around_up += 1
                                elif i == 2:
                                    ty = placement_grid[row][col + 1]
                                    trow = row
                                    tcol = col + 1
                                    ty_3 = ty
                                    if ty_3 > -1 and conn[i][icon_index] * conn[tx][ty] > 0:
                                        things_around_right += 1
                                elif i == 3:
                                    ty = placement_grid[row + 1][col]
                                    trow = row + 1
                                    tcol = col
                                    ty_4 = ty
                                    if ty_4 > -1 and conn[i][icon_index] * conn[tx][ty] > 0:
                                        things_around_down += 1
                            things_around = things_around_left + things_around_up + things_around_right + things_around_down
                            Q_grid[row][col] = Q[pipe_section_grid[row][col]]
                            T_grid[row][col] = float(T[pipe_section_grid[row][col]] - Tloss_pipe[dataset])
                            T[pipe_section_grid[row][col]] -= Tloss_pipe[dataset]
                            print("I was here3")
                        elif 0 <= icon_index <= 5:
                            Q_grid[row][col] = Q[pipe_section_grid[row][col]]
                            T_grid[row][col] = T[pipe_section_grid[row][col]][-1] - Tloss_pipe[dataset]
                            wait = input("wtf?")

                    if dropdown_open == True and placed_new_item == False and 0 <= icon_index <= 5 and \
                            T_grid[pw_row[dataset] - 1][pw_col[dataset]] == 0:
                        Q_grid[row][col] = Starting_Q
                        T_grid[row + 1][col] = Starting_T
                        T_grid[row][col] = float(Starting_T - Tloss_pipe[dataset])
                        T[pipe_section] = [T_grid[row][col]]
                        Q[pipe_section] = Q_grid[row][col]
                        print(Q[pipe_section])

                    if placement_grid[row][col - 1] > 9 or placement_grid[row][col + 1] > 9 or placement_grid[row - 1][
                        col] > 9 or placement_grid[row + 1][col] > 9:
                        # things_around -= 1
                        print(dropdown_open, placed_new_item, icon_index, things_around)
                    if dropdown_open == True and placed_new_item == False and icon_index == 6 and things_around == 1:
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

                                    # T of the triplet
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row + 1][col]][-1] - Tloss_pipe[dataset])

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

                                    # T of the triplet
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row][col - 1]][-1] - Tloss_pipe[dataset])

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
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row][col + 1]][-1] - Tloss_pipe[dataset])

                                Q_grid[row][col] = Q[
                                    min(pipe_section_grid[row + 1][col], pipe_section_grid[row][col - 1],
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
                    elif dropdown_open == True and placed_new_item == False and icon_index == 7 and things_around == 1:
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
                                    T[pipe_section] = [T[pipe_section_grid[row - 1][col]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row][col - 1]] = T[pipe_section]

                                    pipe_section += 1
                                    down_arrow_appears()  # Down arrow appears
                                    q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                    q = int(q)
                                    covering_the_arrow(screen)
                                    Q[pipe_section] = q
                                    Q_grid[row + 1][col] = Q[pipe_section]
                                    pipe_section_grid[row + 1][col] = pipe_section
                                    T[pipe_section] = [T[pipe_section_grid[row - 1][col]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row + 1][col]] = T[pipe_section]

                                    # T of the triplet
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row - 1][col]][-1] - Tloss_pipe[dataset])

                                elif placement_grid[row][col - 1] != -1:
                                    pipe_section += 1
                                    up_arrow_appears()  # Up arrow appears
                                    q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                    q = int(q)
                                    covering_the_arrow(screen)
                                    Q[pipe_section] = q
                                    Q_grid[row - 1][col] = Q[pipe_section]
                                    pipe_section_grid[row - 1][col] = pipe_section
                                    T[pipe_section] = [T[pipe_section_grid[row][col - 1]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row - 1][col]] = T[pipe_section]

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

                                    # T of the triplet
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row][col - 1]][-1] - Tloss_pipe[dataset])

                                elif placement_grid[row + 1][col] != -1:
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
                                    up_arrow_appears()  # Up arrow appears
                                    q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                    q = int(q)
                                    Q[pipe_section] = q
                                    Q_grid[row - 1][col] = Q[pipe_section]
                                    pipe_section_grid[row - 1][col] = pipe_section
                                    T[pipe_section] = [T[pipe_section_grid[row + 1][col]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row - 1][col]] = T[pipe_section]

                                    # T of the triplet
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row + 1][col]][-1] - Tloss_pipe[dataset])

                                Q_grid[row][col] = Q[
                                    min(pipe_section_grid[row - 1][col], pipe_section_grid[row][col - 1],
                                        pipe_section_grid[row + 1][col])]
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
                    elif dropdown_open == True and placed_new_item == False and icon_index == 8 and things_around == 1:
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
                                    T[pipe_section] = [T[pipe_section_grid[row - 1][col]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row][col - 1]] = T[pipe_section]

                                    pipe_section += 1
                                    right_arrow_appears()  # Right arrow appears
                                    q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                    q = int(q)
                                    covering_the_arrow(screen)
                                    Q[pipe_section] = q
                                    Q_grid[row][col + 1] = Q[pipe_section]
                                    pipe_section_grid[row][col + 1] = pipe_section
                                    T[pipe_section] = [T[pipe_section_grid[row - 1][col]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row][col + 1]] = T[pipe_section]

                                    # T of the triplet
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row - 1][col]][-1] - Tloss_pipe[dataset])

                                elif placement_grid[row][col - 1] != -1:
                                    pipe_section += 1
                                    up_arrow_appears()  # Up arrow appears
                                    q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                    q = int(q)
                                    covering_the_arrow(screen)
                                    Q[pipe_section] = q
                                    Q_grid[row - 1][col] = Q[pipe_section]
                                    pipe_section_grid[row - 1][col] = pipe_section
                                    T[pipe_section] = [T[pipe_section_grid[row][col - 1]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row - 1][col]] = T[pipe_section]

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

                                    # T of the triplet
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row][col - 1]][-1] - Tloss_pipe[dataset])


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
                                    up_arrow_appears()  # Down arrow appears
                                    q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                    q = int(q)
                                    covering_the_arrow(screen)
                                    Q[pipe_section] = q
                                    Q_grid[row - 1][col] = Q[pipe_section]
                                    pipe_section_grid[row - 1][col] = pipe_section
                                    T[pipe_section] = [T[pipe_section_grid[row][col + 1]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row - 1][col]] = T[pipe_section]

                                    # T of the triplet
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row][col + 1]][-1] - Tloss_pipe[dataset])

                                Q_grid[row][col] = Q[
                                    min(pipe_section_grid[row - 1][col], pipe_section_grid[row][col - 1],
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
                    elif dropdown_open == True and placed_new_item == False and icon_index == 9 and things_around == 1:
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
                                    T[pipe_section] = [T[pipe_section_grid[row - 1][col]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row][col + 1]] = T[pipe_section]

                                    pipe_section += 1
                                    down_arrow_appears()  # Down arrow appears
                                    q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                    q = int(q)
                                    covering_the_arrow(screen)
                                    Q[pipe_section] = q
                                    Q_grid[row + 1][col] = Q[pipe_section]
                                    pipe_section_grid[row + 1][col] = pipe_section
                                    T[pipe_section] = [T[pipe_section_grid[row - 1][col]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row + 1][col]] = T[pipe_section]

                                    # T of the triplet
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row - 1][col]][-1] - Tloss_pipe[dataset])

                                elif placement_grid[row][col + 1] != -1:
                                    pipe_section += 1
                                    up_arrow_appears()  # Up arrow appears
                                    q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                    q = int(q)
                                    covering_the_arrow(screen)
                                    Q[pipe_section] = q
                                    Q_grid[row - 1][col] = Q[pipe_section]
                                    pipe_section_grid[row - 1][col] = pipe_section
                                    T[pipe_section] = [T[pipe_section_grid[row][col + 1]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row - 1][col]] = T[pipe_section]

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
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row][col + 1]][-1] - Tloss_pipe[dataset])

                                elif placement_grid[row + 1][col] != -1:
                                    pipe_section += 1
                                    up_arrow_appears()  # Up arrow appears
                                    q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                    q = int(q)
                                    covering_the_arrow(screen)
                                    Q[pipe_section] = q
                                    Q_grid[row - 1][col] = Q[pipe_section]
                                    pipe_section_grid[row - 1][col] = pipe_section
                                    T[pipe_section] = [T[pipe_section_grid[row + 1][col]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row - 1][col]] = T[pipe_section]

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

                                    # T of the triplet
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row + 1][col]][-1] - Tloss_pipe[dataset])

                                Q_grid[row][col] = Q[
                                    min(pipe_section_grid[row - 1][col], pipe_section_grid[row][col + 1],
                                        pipe_section_grid[row + 1][col])]
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
                    elif dropdown_open == True and placed_new_item == False and icon_index == 6 and things_around == 2:
                        pipe_section += 1
                        if placement_grid[row + 1][col] != -1 and placement_grid[row][col - 1] != -1:
                            Q_grid[row][col + 1] = Q_grid[row + 1][col] + Q_grid[row][col - 1]
                            pipe_section_grid[row][col + 1] = pipe_section
                            Q[pipe_section] = Q_grid[row][col + 1]
                            Q_grid[row][col] = Q_grid[row + 1][col] + Q_grid[row][col - 1]
                            T[pipe_section_grid[row][col + 1]] = [
                                round(float((np.array(Q_grid[row + 1][col]) * T_grid[row + 1][col] +
                                             np.array(Q_grid[row][col - 1]) * T_grid[row][
                                                 col - 1]) / (Q_grid[row + 1][col] + Q_grid[row][
                                    col - 1]) - Tloss_pipe[dataset]), 1)]
                            T_grid[row][col] = T[pipe_section_grid[row][col + 1]]
                        if placement_grid[row + 1][col] != -1 and placement_grid[row][col + 1] != -1:
                            Q_grid[row][col - 1] = Q_grid[row + 1][col] + Q_grid[row][col + 1]
                            pipe_section_grid[row][col - 1] = pipe_section
                            Q[pipe_section] = Q_grid[row][col - 1]
                            Q_grid[row][col] = Q_grid[row + 1][col] + Q_grid[row][col + 1]
                            T[pipe_section_grid[row][col - 1]] = [
                                round(float((np.array(Q_grid[row + 1][col]) * T_grid[row + 1][col] +
                                             np.array(Q_grid[row][col + 1]) * T_grid[row][
                                                 col + 1]) / (
                                                    Q_grid[row + 1][col] + Q_grid[row][
                                                col + 1]) - Tloss_pipe[dataset]), 1)]
                            T_grid[row][col] = T[pipe_section_grid[row][col - 1]]
                        if placement_grid[row][col - 1] != -1 and placement_grid[row][col + 1] != -1:
                            Q_grid[row + 1][col] = Q_grid[row][col - 1] + Q_grid[row][col + 1]
                            pipe_section_grid[row + 1][col] = pipe_section
                            Q[pipe_section] = Q_grid[row + 1][col]
                            Q_grid[row][col] = Q_grid[row][col - 1] + Q_grid[row][col + 1]
                            T[pipe_section_grid[row + 1][col]] = [
                                round(float((np.array(Q_grid[row][col - 1]) * T_grid[row][col - 1] +
                                             np.array(Q_grid[row][col + 1]) * T_grid[row][
                                                 col + 1]) / (
                                                    Q_grid[row][col - 1] + Q_grid[row][
                                                col + 1]) - Tloss_pipe[dataset]), 1)]
                            T_grid[row][col] = T[pipe_section_grid[row + 1][col]]
                        pipe_section_grid[row][col] = -icon_index
                    elif dropdown_open == True and placed_new_item == False and icon_index == 7 and things_around == 2:
                        pipe_section += 1
                        if placement_grid[row + 1][col] != -1 and placement_grid[row][col - 1] != -1:
                            Q_grid[row - 1][col] = Q_grid[row + 1][col] + Q_grid[row][col - 1]
                            pipe_section_grid[row - 1][col] = pipe_section
                            Q[pipe_section] = Q_grid[row - 1][col]
                            Q_grid[row][col] = Q_grid[row + 1][col] + Q_grid[row][col - 1]
                            T[pipe_section_grid[row - 1][col]] = [
                                round(float((np.array(Q_grid[row + 1][col]) * T_grid[row + 1][col] +
                                             np.array(Q_grid[row][col - 1]) * T_grid[row][
                                                 col - 1]) / (
                                                    Q_grid[row + 1][col] + Q_grid[row][
                                                col - 1]) - Tloss_pipe[dataset]), 1)]
                            T_grid[row][col] = T[pipe_section_grid[row - 1][col]]
                        if placement_grid[row + 1][col] != -1 and placement_grid[row - 1][col] != -1:
                            Q_grid[row][col - 1] = Q_grid[row + 1][col] + Q_grid[row - 1][col]
                            pipe_section_grid[row][col - 1] = pipe_section
                            Q[pipe_section] = Q_grid[row][col - 1]
                            Q_grid[row][col] = Q_grid[row + 1][col] + Q_grid[row - 1][col]
                            T[pipe_section_grid[row][col - 1]] = [
                                round(float((np.array(Q_grid[row + 1][col]) * T_grid[row + 1][col] +
                                             np.array(Q_grid[row - 1][col]) * T_grid[row - 1][
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
                            T[pipe_section_grid[row + 1][col]] = [
                                round(float((np.array(Q_grid[row][col - 1]) * T_grid[row][col - 1] +
                                             np.array(Q_grid[row - 1][col]) * T_grid[row - 1][
                                                 col]) / (
                                                    Q_grid[row][col - 1] +
                                                    Q_grid[row - 1][
                                                        col]) - Tloss_pipe[dataset]), 1)]
                            T_grid[row][col] = T[pipe_section_grid[row + 1][col]]
                        pipe_section_grid[row][col] = -icon_index
                    elif dropdown_open == True and placed_new_item == False and icon_index == 8 and things_around == 2:
                        pipe_section += 1
                        if placement_grid[row - 1][col] != -1 and placement_grid[row][col - 1] != -1:
                            Q_grid[row][col + 1] = Q_grid[row - 1][col] + Q_grid[row][col - 1]
                            pipe_section_grid[row][col + 1] = pipe_section
                            Q[pipe_section] = Q_grid[row][col + 1]
                            Q_grid[row][col] = Q_grid[row - 1][col] + Q_grid[row][col - 1]
                            T[pipe_section_grid[row][col + 1]] = [
                                round(float((np.array(Q_grid[row - 1][col]) * T_grid[row - 1][col] +
                                             np.array(Q_grid[row][col - 1]) * T_grid[row][
                                                 col - 1]) / (
                                                    Q_grid[row - 1][col] + Q_grid[row][
                                                col - 1]) - Tloss_pipe[dataset]), 1)]
                            T_grid[row][col] = T[pipe_section_grid[row][col + 1]]
                        if placement_grid[row - 1][col] != -1 and placement_grid[row][col + 1] != -1:
                            Q_grid[row][col - 1] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                            pipe_section_grid[row][col - 1] = pipe_section
                            Q[pipe_section] = Q_grid[row][col - 1]
                            Q_grid[row][col] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                            T[pipe_section_grid[row][col - 1]] = [
                                round(float((np.array(Q_grid[row - 1][col]) * T_grid[row - 1][col] +
                                             np.array(Q_grid[row][col + 1]) * T_grid[row][col + 1]) / (
                                                    Q_grid[row - 1][col] + Q_grid[row][col + 1]) - Tloss_pipe[dataset]),
                                      1)]
                            T_grid[row][col] = T[pipe_section_grid[row][col - 1]]
                        if placement_grid[row][col - 1] != -1 and placement_grid[row][col + 1] != -1:
                            Q_grid[row - 1][col] = Q_grid[row][col - 1] + placement_grid[row][col + 1]
                            pipe_section_grid[row - 1][col] = pipe_section
                            Q[pipe_section] = Q_grid[row - 1][col]
                            Q_grid[row][col] = Q_grid[row][col - 1] + placement_grid[row][col + 1]
                            T[pipe_section_grid[row - 1][col]] = [
                                round(float((np.array(Q_grid[row][col - 1]) * T_grid[row][col - 1] +
                                             np.array(Q_grid[row][col + 1]) * T_grid[row][
                                                 col + 1]) / (
                                                    Q_grid[row][col - 1] + Q_grid[row][
                                                col + 1]) - Tloss_pipe[dataset]), 1)]
                            T_grid[row][col] = T[pipe_section_grid[row - 1][col]]
                        pipe_section_grid[row][col] = -icon_index
                    elif dropdown_open == True and placed_new_item == False and icon_index == 9 and things_around == 2:
                        pipe_section += 1
                        if placement_grid[row + 1][col] != -1 and placement_grid[row][col + 1] != -1:
                            Q_grid[row - 1][col] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                            pipe_section_grid[row - 1][col] = pipe_section
                            Q[pipe_section] = Q_grid[row - 1][col]
                            Q_grid[row][col] = Q_grid[row + 1][col] + Q_grid[row][col + 1]
                            T[pipe_section_grid[row - 1][col]] = [
                                round(float(np.array((Q_grid[row + 1][col]) * T_grid[row + 1][col] +
                                                     np.array(Q_grid[row][col + 1]) * T_grid[row][
                                                         col + 1]) / (
                                                    Q_grid[row + 1][col] + Q_grid[row][
                                                col + 1]) - Tloss_pipe[dataset]), 1)]
                            T_grid[row][col] = T[pipe_section_grid[row - 1][col]]
                        if placement_grid[row - 1][col] != -1 and placement_grid[row][col + 1] != -1:
                            Q_grid[row + 1][col] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                            pipe_section_grid[row + 1][col] = pipe_section
                            Q[pipe_section] = Q_grid[row + 1][col]
                            Q_grid[row][col] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                            T[pipe_section_grid[row + 1][col]] = [
                                round(float((np.array(Q_grid[row - 1][col]) * T_grid[row - 1][col] +
                                             np.array(Q_grid[row][col + 1]) * T_grid[row][
                                                 col + 1]) / (
                                                    Q_grid[row - 1][col] + Q_grid[row][
                                                col + 1]) - Tloss_pipe[dataset]), 1)]
                            T_grid[row][col] = T[pipe_section_grid[row + 1][col]]
                        if placement_grid[row - 1][col] != -1 and placement_grid[row + 1][col] != -1:
                            Q_grid[row][col + 1] = Q_grid[row - 1][col] + Q_grid[row + 1][col]
                            pipe_section_grid[row][col + 1] = pipe_section
                            Q[pipe_section] = Q_grid[row][col + 1]
                            Q_grid[row][col] = Q_grid[row - 1][col] + Q_grid[row + 1][col]
                            T[pipe_section_grid[row][col + 1]] = [
                                round(float((np.array(Q_grid[row + 1][col]) * T_grid[row + 1][col] +
                                             np.array(Q_grid[row - 1][col]) * T_grid[row - 1][
                                                 col]) / (
                                                    Q_grid[row + 1][col] +
                                                    Q_grid[row - 1][
                                                        col]) - Tloss_pipe[dataset]), 1)]
                            T_grid[row][col] = T[pipe_section_grid[row][col + 1]]
                        pipe_section_grid[row][col] = -icon_index
                    dropdown_open = False
                    number_of_items += 1
                    # Add the placed icon to the undo stack
                    undo_stack.append((row, col, icon_index))
                    print(icon_index)
                    drawing_grid()
                    placed_new_item = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and not dropdown_open:
                row = (event.pos[1] - square_y) // square_size
                col = (event.pos[0] - square_x) // square_size
                right_click_grid_cell_info(event, row, col)
            """elif budget_calculated < 0 and mistake_1 == 0:
                negative_point_counter -= 1
                mistake_1 = 1
                print(negative_point_counter)
                print(mistake_1)"""
                #game_over_budget()
            if Q_grid[rw_row[dataset] - 1][rw_col[dataset]] != -2 :
                if ((house0_col[dataset] > 0 and Q_grid[house0_row[dataset] - 1][house0_col[dataset]] < 0) or \
                        (house1_col[dataset] > 0 and Q_grid[house1_row[dataset] - 1][house1_col[dataset]] < 0) or \
                        (house2_col[dataset] > 0 and Q_grid[house2_row[dataset] - 1][house2_col[dataset]] < 0) or \
                        (greenhouse0_col[dataset] > 0 and Q_grid[greenhouse0_row[dataset] - 1][
                            greenhouse0_col[dataset]] < 0) or \
                        (greenhouse1_col[dataset] > 0 and Q_grid[greenhouse1_row[dataset] - 1][
                            greenhouse1_col[dataset]] < 0)) and mistake_2 == 0:
                    negative_point_counter -= 1
                    mistake_2 = 1
                    print(negative_point_counter)
                    print(mistake_2)
                    #game_over_users_not_satisfied()
                if budget_calculated < 0 and mistake_1 == 0:
                    negative_point_counter -= 1
                    mistake_1 = 1
                    print(negative_point_counter)
                    print(mistake_1)
                if ((things_around_up > 0 and pipe_section_grid[row - 1][col] > 0 and pipe_section_grid[row][
                    col] > 0 and
                     pipe_section_grid[row - 1][col] != pipe_section_grid[row][col]) or \
                    (things_around_right > 0 and pipe_section_grid[row][col + 1] > 0 and pipe_section_grid[row][
                        col] > 0 and
                     pipe_section_grid[row][col + 1] != pipe_section_grid[row][col]) or \
                    (things_around_down > 0 and pipe_section_grid[row + 1][col] > 0 and pipe_section_grid[row][
                        col] > 0 and
                     pipe_section_grid[row + 1][col] != pipe_section_grid[row][col]) or \
                    (things_around_left > 0 and pipe_section_grid[row][col - 1] > 0 and pipe_section_grid[row][
                        col] > 0 and
                     pipe_section_grid[row][col - 1] != pipe_section_grid[row][col])) and mistake_3 == 0:
                    # print("xxx xxx xxx xxx xxx xxx")
                    negative_point_counter -= 1
                    mistake_3 = 1
                    print(negative_point_counter)
                    print(mistake_3)
                if ((house0_row[dataset] > 0 and placement_grid[house0_row[dataset] - 1][house0_col[dataset]] != -1 and
                     Q_grid[house0_row[dataset] - 1][house0_col[dataset]] !=
                     Q_grid[house0_row[dataset]][house0_col[dataset]]) or \
                    (house1_row[dataset] > 0 and placement_grid[house1_row[dataset] - 1][house1_col[dataset]] != -1 and
                     Q_grid[house1_row[dataset] - 1][house1_col[dataset]] !=
                     Q_grid[house1_row[dataset]][house1_col[dataset]]) or \
                    (house2_row[dataset] > 0 and placement_grid[house2_row[dataset] - 1][house2_col[dataset]] != -1 and
                     Q_grid[house2_row[dataset] - 1][house2_col[dataset]] !=
                     Q_grid[house2_row[dataset]][house2_col[dataset]]) or \
                    (greenhouse0_row[dataset] > 0 and placement_grid[greenhouse0_row[dataset] - 1][
                        greenhouse0_col[dataset]] != -1 and
                     Q_grid[greenhouse0_row[dataset] - 1][greenhouse0_col[dataset]] !=
                     Q_grid[greenhouse0_row[dataset]][greenhouse0_col[dataset]]) or \
                    (greenhouse1_row[dataset] > 0 and placement_grid[greenhouse1_row[dataset] - 1][
                        greenhouse1_col[dataset]] != -1 and
                     Q_grid[greenhouse1_row[dataset] - 1][greenhouse1_col[dataset]] !=
                     Q_grid[greenhouse1_row[dataset]][greenhouse1_col[dataset]])) and mistake_4 == 0:
                    negative_point_counter -= 1
                    mistake_4 = 1
                    print(negative_point_counter)
                    print(f"I'm mistake 4{mistake_4}")
                if rw_row[dataset] > 0 and rw_existence == True and placement_grid[rw_row[dataset] - 1][
                    rw_col[dataset]] != -1:
                    game_over_ending_exam_mode()
                    return
                else:
                    if placement_grid[outflow_row[dataset] - 1][outflow_col[dataset]] != -1:
                        game_over_ending_exam_mode()
                        return
            """if ((things_around_up > 0 and pipe_section_grid[row - 1][col] > 0 and pipe_section_grid[row][col] > 0 and
                pipe_section_grid[row - 1][col] != pipe_section_grid[row][col]) or \
                    (things_around_right > 0 and pipe_section_grid[row][col + 1] > 0 and pipe_section_grid[row][
                        col] > 0 and
                     pipe_section_grid[row][col + 1] != pipe_section_grid[row][col]) or \
                    (things_around_down > 0 and pipe_section_grid[row + 1][col] > 0 and pipe_section_grid[row][
                        col] > 0 and
                     pipe_section_grid[row + 1][col] != pipe_section_grid[row][col]) or \
                    (things_around_left > 0 and pipe_section_grid[row][col - 1] > 0 and pipe_section_grid[row][
                        col] > 0 and
                     pipe_section_grid[row][col - 1] != pipe_section_grid[row][col])) and mistake_3 == 0:
                # print("xxx xxx xxx xxx xxx xxx")
                negative_point_counter -= 1
                mistake_3 = 1
                print(negative_point_counter)
                print(mistake_3)"""
                #game_over_triplet_issue()
            """if ((house0_row[dataset] > 0 and placement_grid[house0_row[dataset] - 1][house0_col[dataset]] != -1 and
                Q_grid[house0_row[dataset] - 1][house0_col[dataset]] !=
                            Q_grid[house0_row[dataset]][house0_col[dataset]]) or \
                (house1_row[dataset] > 0 and placement_grid[house1_row[dataset] - 1][house1_col[dataset]] != -1 and
                 Q_grid[house1_row[dataset] - 1][house1_col[dataset]] !=
                            Q_grid[house1_row[dataset]][house1_col[dataset]]) or \
                (house2_row[dataset] > 0 and placement_grid[house2_row[dataset] - 1][house2_col[dataset]] != -1 and
                 Q_grid[house2_row[dataset] - 1][house2_col[dataset]] !=
                            Q_grid[house2_row[dataset]][house2_col[dataset]]) or \
                (greenhouse0_row[dataset] > 0 and placement_grid[greenhouse0_row[dataset] - 1][greenhouse0_col[dataset]] != -1 and
                 Q_grid[greenhouse0_row[dataset] - 1][greenhouse0_col[dataset]] !=
                            Q_grid[greenhouse0_row[dataset]][greenhouse0_col[dataset]]) or \
                (greenhouse1_row[dataset] > 0 and placement_grid[greenhouse1_row[dataset] - 1][greenhouse1_col[dataset]] != -1 and
                 Q_grid[greenhouse1_row[dataset] - 1][greenhouse1_col[dataset]] !=
                            Q_grid[greenhouse1_row[dataset]][greenhouse1_col[dataset]])) and mistake_4 == 0:
                negative_point_counter -= 1
                mistake_4 = 1
                print(negative_point_counter)
                print(f"I'm mistake 4{mistake_4}")"""
                #game_over_Q_inconsistent()
            # Arrange the pipe_section_grid properly
            info_ghouse_blue_square()
            if house0_row[dataset] > 0: pipe_section_grid_for_icon_house0()
            if house1_row[dataset] > 0: pipe_section_grid_for_icon_house1()
            if house2_row[dataset] > 0: pipe_section_grid_for_icon_house2()
            if greenhouse0_row[dataset] > 0: pipe_section_grid_for_icon_greenhouse0()
            if greenhouse1_row[dataset] > 0: pipe_section_grid_for_icon_greenhouse1()

        #drawing_grid()

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
            print(T)
            print(Starting_Q)
            render_q2_dictionary(Q2, T, screen)
            print(username)
            print("things_around= ", things_around)
            print("things_around_left =", things_around_left)
            print("things_around_up= ", things_around_up)
            print("things_around_right= ", things_around_right)
            print("things_around_down= ", things_around_down)
            things_around_left = 0
            things_around_right = 0
            things_around_down = 0
            things_around_up = 0

        # Limit the frame rate to reduce blinking
        clock.tick(60)

        # Update the display
        pygame.display.update()

    # Quit Pygame
    pygame.quit()
    sys.exit()
has_the_exam_run = False
# Main game loop
def main_loop():
    global things_around_up, things_around_down, things_around_left, things_around_right, things_around, number_of_items, dropdown_open, Starting_Q, pipe_section, row, col, has_the_exam_run
    clock = pygame.time.Clock()
    """if has_the_exam_run:
        combined_start_function_RE()
        print("i'm in the main loop")
    else:
        pass"""
    #combined_start_function()
    starting_the_puzzle()
    screen.fill(BLUE)
    print(type(row), type(col), row, col)
    print(pipe_section_grid)
    "το πρόβλημα φαίνεται πως είναι ότι, για κάποιο λόγο μετά το retry το pipe_section_grid μετατρέπετε σε διαφορετικής μορφής array"
    #row = pw_row - 1
    #col = pw_col
    #reset_grid()
    initialize_grid()
    drawing_grid()
    if house0_row[dataset] > 0: pipe_section_grid_for_icon_house0()
    if house1_row[dataset] > 0: pipe_section_grid_for_icon_house1()
    if house2_row[dataset] > 0: pipe_section_grid_for_icon_house2()
    if greenhouse0_row[dataset] > 0: pipe_section_grid_for_icon_greenhouse0()
    if greenhouse1_row[dataset] > 0: pipe_section_grid_for_icon_greenhouse1()
    # Clear the screen
    running = True
    placed_new_item = False  # Flag to track if a new item is placed
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                undo()
                drawing_grid()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_grid()
                initialize_grid()
                drawing_grid()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                budget_explainer()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not dropdown_open:
                # Check if the button to reset the grid is clicked
                if reset_grid_button.is_clicked(pygame.mouse.get_pos()):
                    reset_grid()
                    initialize_grid()
                    drawing_grid()
                # Check if the button to undo is clicked
                elif undo_button.is_clicked(pygame.mouse.get_pos()):
                    undo()
                    drawing_grid()
                    # Check if the Retry button is clicked
                elif tip_button.is_clicked(pygame.mouse.get_pos()):
                    reset_grid()
                    Starting_Q = 0
                    initialize_grid()
                    main_loop()
                    #starting_the_puzzle()
                    # initialize_grid()
                    # tip_button_main_game_click()
                    # Pipe information cost
                elif button_for_menu.is_clicked(pygame.mouse.get_pos()):
                    display_for_pipe_cost()
                elif budget_explainer_button.is_clicked(pygame.mouse.get_pos()):
                    budget_explainer()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 64 <= event.pos[0] <= 544 + 64 and 64 <= event.pos[1] <= 544 + 64:  # The pixel "space" of the grid
                        print("I reached this part")

                        row = (event.pos[1] - square_y) // square_size
                        print(f"The value of row is {row}")
                        col = (event.pos[0] - square_x) // square_size
                        print(f"The value of col is {col}")
                        #available_icons = get_available_icons(row, col)
                        #get_available_icons(row, col)
                        #return get_available_icons
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
                                    0 <= neighbor_row < (grid_size - 1)
                                    and 0 <= neighbor_col < (grid_size - 1)
                                    and placement_grid[neighbor_row][neighbor_col] > -1
                            ):
                                # = [int(num) for num in my_string.split(',')]
                                icons2rem.append(na_icons[i][placement_grid[neighbor_row][neighbor_col]])
                        if len(icons2rem) != 0:
                            icons2rem = [int(j) for j in ",".join(icons2rem).split(',')]
                            icons2rem = list(set(icons2rem))
                            # print('in', icons2rem)
                            for j in icons2rem:
                                available_icons.remove(icons[j - 1])
                            if row == 0:
                                for i in [1, 4, 5, 7, 8, 9]:
                                    if icons[i] in available_icons:
                                        available_icons.remove(icons[i])
                            if col == 0:
                                for i in [0, 3, 4, 6, 7, 8]:
                                    if icons[i] in available_icons:
                                        available_icons.remove(icons[i])
                            if row == 16:  # error for last row
                                for i in [1, 2, 3, 6, 7, 9]:
                                    if icons[i] in available_icons:
                                        available_icons.remove(icons[i])
                            if col == 16:  # error for last column
                                for i in [0, 2, 5, 6, 8, 9]:
                                    if icons[i] in available_icons:
                                        available_icons.remove(icons[i])
                        print('out', available_icons)
                        print('out2', len(available_icons))
                        if placement_grid[row][col] == 11:
                            pass
                            """enhancer_system()
                            print(enhancer_usage)"""
                        print(f"that's where i stopped1")
                        if 0 <= row < (grid_size - 1) and 0 <= col < (grid_size - 1) and (
                                (row + 1 < (grid_size - 1) and (
                                        (placement_grid[row + 1][col] == 11 and 0 <= placement_grid[row + 2][
                                            col] <= 10) or (
                                                0 <= placement_grid[row + 1][col] <= 10))) or
                                (row - 1 >= 0 and (
                                        (placement_grid[row - 1][col] == 11 and 0 <= placement_grid[row - 2][
                                            col] <= 10) or (
                                                0 <= placement_grid[row - 1][col] <= 10))) or
                                (col - 1 >= 0 and (
                                        (placement_grid[row][col - 1] == 11 and 0 <= placement_grid[row][
                                            col - 2] <= 10) or (
                                                0 <= placement_grid[row][col - 1] <= 10))) or
                                (col + 1 < (grid_size - 1) and (
                                        (placement_grid[row][col + 1] == 11 and 0 <= placement_grid[row][
                                            col + 2] <= 10) or (
                                                0 <= placement_grid[row][col + 1] <= 10)))
                        ):
                            print(f"that's where i stopped1")
                            if placement_grid[row][col] == -1 and (
                                    (placement_grid[row][col - 1] in (0, 2, 5, 6, 8, 9, 10, 12)) or \
                                    (placement_grid[row][col + 1] in (0, 3, 4, 6, 7, 8, 10, 12)) or \
                                    (placement_grid[row + 1][col] in (1, 4, 5, 7, 8, 9, 10, 12)) or \
                                    ((placement_grid[row - 1][col] == 11) and Q_grid[row - 2][col] != -2) or \
                                    (placement_grid[row - 1][col] in (
                                            1, 2, 3, 6, 7, 9, 10,
                                            12))):  # Διόρθωση για να μην επιτρέπεται τοποθέτηση σε λάθος θέση
                                print(f"that's where i stopped2")
                                dropdown_x = square_x + col * square_size
                                dropdown_y = square_y + (row + 1) * square_size
                                dropdown_width = square_size
                                dropdown_height = square_size * len(available_icons)
                                dropdown_rect = pygame.Rect(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                dropdown_open = True
                                #selected_icon = None
                                if dropdown_open:
                                    pygame.draw.rect(screen, WHITE, dropdown_rect)
                                    pygame.draw.rect(screen, BLACK, dropdown_rect, 1)

                                    for i, icon in enumerate(available_icons):
                                        icon_scaled = pygame.transform.scale(icon, (square_size, square_size))
                                        dropdown_icon_rect = pygame.Rect(dropdown_x, dropdown_y + i * square_size,
                                                                         square_size, square_size)
                                        screen.blit(icon_scaled, dropdown_icon_rect)
                                        print(f"that's where i stopped3")
                        else:
                            dropdown_open = False
                            drawing_grid()
                            selected_icon = grid[row][col]
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and dropdown_open:
                if not dropdown_rect.collidepoint(event.pos):
                    dropdown_open = False
                    drawing_grid()
                    selected_icon = None
                else:
                    current_placement_grid = copy.deepcopy(placement_grid)
                    current_Q_grid = copy.deepcopy(Q_grid)
                    current_T_grid = copy.deepcopy(T_grid)
                    current_pipe_section_grid = copy.deepcopy(pipe_section_grid)
                    grid_versions.append({
                        'placement_grid': current_placement_grid,
                        'Q_grid': current_Q_grid,
                        'T_grid': current_T_grid,
                        'pipe_section_grid': current_pipe_section_grid
                    })

                    icon_index = (event.pos[1] - dropdown_y) // square_size
                    # selected_icon = icons[icon_index]
                    selected_icon = available_icons[icon_index]
                    icon_index = icons.index(selected_icon)
                    print("icon_index:", icon_index)
                    row = (dropdown_y - square_y - square_size) // square_size
                    print(f"The value of row2 is {row}")
                    col = (dropdown_x - square_x) // square_size
                    print(f"The value of col2 is {col}")
                    grid[row][col] = selected_icon
                    placement_grid[row][col] = icon_index
                    if dropdown_open == True and placed_new_item == False and 0 <= icon_index <= 9 and \
                            T_grid[pw_row[dataset] - 1][pw_col[dataset]] != 0:
                        if pipe_section_grid[row][col] == 0:
                            # things_around = 0  # things_around== Τα πράγματα με τα οποία μπορείς να συνδεθείς
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
                                        # things_around += 1
                                        things_around_left += 1
                                elif i == 1:
                                    ty = placement_grid[row - 1][col]
                                    trow = row - 1
                                    tcol = col
                                    # print(ty)
                                    ty_2 = ty
                                    if ty_2 > -1 and conn[i][icon_index] * conn[tx][ty] > 0:
                                        # things_around += 1
                                        things_around_up += 1
                                elif i == 2:
                                    ty = placement_grid[row][col + 1]
                                    trow = row
                                    tcol = col + 1
                                    # print(ty)
                                    ty_3 = ty
                                    if ty_3 > -1 and conn[i][icon_index] * conn[tx][ty] > 0:
                                        things_around_right += 1
                                elif i == 3:
                                    ty = placement_grid[row + 1][col]
                                    trow = row + 1
                                    tcol = col
                                    # print(ty)
                                    ty_4 = ty
                                    if ty_4 > -1 and conn[i][icon_index] * conn[tx][ty] > 0:
                                        # things_around += 1
                                        things_around_down += 1
                                things_around = things_around_left + things_around_up + things_around_right + things_around_down
                                if ty == -1: conn[tx][ty] = 0
                                if conn[i][icon_index] * conn[tx][ty] > 0 and things_around <= 1 and \
                                        placement_grid[row - 1][col] <= 9 and 0 <= icon_index <= 5:
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
                                        placement_grid[row - 1][col] > 9 and placement_grid[row - 1][
                                    col] != 10 and 0 <= icon_index <= 5:
                                    pipe_section += 1
                                    pipe_section_grid[row][col] = pipe_section
                                    Q[pipe_section_grid[row][col]] = Q_grid[row - 1][
                                        col]  # This does not allow wrong Q by the player. With  Q_grid[row - 2][col] it does.
                                    T[pipe_section_grid[row][col]] = [(min(T_grid[row - 1][col]) - Tloss_pipe[dataset])]
                                    # T[pipe_section_grid[row][col]] = min(T_grid[row - 1][col])
                                    T_grid[row][col] = T[pipe_section_grid[row][col]]
                                if conn[i][icon_index] * conn[tx][
                                    ty] > 0 and things_around > 1 and 0 <= icon_index <= 5 and \
                                        pipe_section_grid[row + 1][col] <= -11:
                                    pipe_section_grid[row][col] = pipe_section_grid[row - 1][
                                        col]  # min(element for element in[pipe_section_grid[row][col - 1],pipe_section_grid[row - 1][col], pipe_section_grid[row][col + 1], pipe_section_grid[row + 1][col]] if element > 0)
                                    Q_grid[row][col] = Q[pipe_section_grid[row][col]]
                                    #if Q_grid[row][col] != Q_grid[row + 1][col]:
                                        #game_over_Q_inconsistent()
                                        # Q_grid[row+1][col] = Q[pipe_section_grid[row][col]]
                                    # T[pipe_section_grid[row][col]] -= Tloss_pipe
                                    # sygrinw tin timi eisodou toy house me tin ypologismeni T_grid[row][col]
                                    # Q_grid[row + 1][col] = Q_grid[row][col]
                            Q_grid[row][col] = Q[pipe_section_grid[row][col]]
                            # T_grid[row][col] = T[pipe_section_grid[row][col]][-1] - Tloss_pipe
                        elif pipe_section_grid[row][col] != 0 and Q_grid[row][col] != 0 and 0 <= icon_index <= 5:
                            # things_around = 0  # things_around== Τα πράγματα με τα οποία μπορείς να συνδεθείς
                            # i: 0=left, 1=up, 2=right, 3=down
                            for i in range(0, 4):
                                tx = (i + 2) % 4
                                print(tx)
                                if i == 0:  # ti icon type exei to row-1
                                    ty = placement_grid[row][col - 1]
                                    trow = row
                                    tcol = col - 1
                                    ty_1 = ty
                                    if ty_1 > -1 and conn[i][icon_index] * conn[tx][ty] > 0:
                                        things_around_left += 1
                                elif i == 1:
                                    ty = placement_grid[row - 1][col]
                                    trow = row - 1
                                    tcol = col
                                    ty_2 = ty
                                    if ty_2 > -1 and conn[i][icon_index] * conn[tx][ty] > 0:
                                        things_around_up += 1
                                elif i == 2:
                                    ty = placement_grid[row][col + 1]
                                    trow = row
                                    tcol = col + 1
                                    ty_3 = ty
                                    if ty_3 > -1 and conn[i][icon_index] * conn[tx][ty] > 0:
                                        things_around_right += 1
                                elif i == 3:
                                    ty = placement_grid[row + 1][col]
                                    trow = row + 1
                                    tcol = col
                                    ty_4 = ty
                                    if ty_4 > -1 and conn[i][icon_index] * conn[tx][ty] > 0:
                                        things_around_down += 1
                            things_around = things_around_left + things_around_up + things_around_right + things_around_down
                            Q_grid[row][col] = Q[pipe_section_grid[row][col]]
                            T_grid[row][col] = float(T[pipe_section_grid[row][col]] - Tloss_pipe[dataset])
                            T[pipe_section_grid[row][col]] -= Tloss_pipe[dataset]
                            print("I was here3")
                        elif 0 <= icon_index <= 5:
                            Q_grid[row][col] = Q[pipe_section_grid[row][col]]
                            T_grid[row][col] = T[pipe_section_grid[row][col]][-1] - Tloss_pipe[dataset]
                            wait = input("wtf?")

                    if dropdown_open == True and placed_new_item == False and 0 <= icon_index <= 5 and \
                            T_grid[pw_row[dataset] - 1][pw_col[dataset]] == 0:
                        Q_grid[row][col] = Starting_Q
                        T_grid[row + 1][col] = Starting_T
                        T_grid[row][col] = float(Starting_T - Tloss_pipe[dataset])
                        T[pipe_section] = [T_grid[row][col]]
                        Q[pipe_section] = Q_grid[row][col]
                        print(Q[pipe_section])

                    if placement_grid[row][col - 1] > 9 or placement_grid[row][col + 1] > 9 or placement_grid[row - 1][
                        col] > 9 or placement_grid[row + 1][col] > 9:
                        # things_around -= 1
                        print(dropdown_open, placed_new_item, icon_index, things_around)
                    if dropdown_open == True and placed_new_item == False and icon_index == 6 and things_around == 1:
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

                                    # T of the triplet
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row + 1][col]][-1] - Tloss_pipe[dataset])

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

                                    # T of the triplet
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row][col - 1]][-1] - Tloss_pipe[dataset])

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
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row][col + 1]][-1] - Tloss_pipe[dataset])

                                Q_grid[row][col] = Q[
                                    min(pipe_section_grid[row + 1][col], pipe_section_grid[row][col - 1],
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
                    elif dropdown_open == True and placed_new_item == False and icon_index == 7 and things_around == 1:
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
                                    T[pipe_section] = [T[pipe_section_grid[row - 1][col]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row][col - 1]] = T[pipe_section]

                                    pipe_section += 1
                                    down_arrow_appears()  # Down arrow appears
                                    q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                    q = int(q)
                                    covering_the_arrow(screen)
                                    Q[pipe_section] = q
                                    Q_grid[row + 1][col] = Q[pipe_section]
                                    pipe_section_grid[row + 1][col] = pipe_section
                                    T[pipe_section] = [T[pipe_section_grid[row - 1][col]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row + 1][col]] = T[pipe_section]

                                    # T of the triplet
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row - 1][col]][-1] - Tloss_pipe[dataset])

                                elif placement_grid[row][col - 1] != -1:
                                    pipe_section += 1
                                    up_arrow_appears()  # Up arrow appears
                                    q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                    q = int(q)
                                    covering_the_arrow(screen)
                                    Q[pipe_section] = q
                                    Q_grid[row - 1][col] = Q[pipe_section]
                                    pipe_section_grid[row - 1][col] = pipe_section
                                    T[pipe_section] = [T[pipe_section_grid[row][col - 1]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row - 1][col]] = T[pipe_section]

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

                                    # T of the triplet
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row][col - 1]][-1] - Tloss_pipe[dataset])

                                elif placement_grid[row + 1][col] != -1:
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
                                    up_arrow_appears()  # Up arrow appears
                                    q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                    q = int(q)
                                    Q[pipe_section] = q
                                    Q_grid[row - 1][col] = Q[pipe_section]
                                    pipe_section_grid[row - 1][col] = pipe_section
                                    T[pipe_section] = [T[pipe_section_grid[row + 1][col]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row - 1][col]] = T[pipe_section]

                                    # T of the triplet
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row + 1][col]][-1] - Tloss_pipe[dataset])

                                Q_grid[row][col] = Q[
                                    min(pipe_section_grid[row - 1][col], pipe_section_grid[row][col - 1],
                                        pipe_section_grid[row + 1][col])]
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
                    elif dropdown_open == True and placed_new_item == False and icon_index == 8 and things_around == 1:
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
                                    T[pipe_section] = [T[pipe_section_grid[row - 1][col]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row][col - 1]] = T[pipe_section]

                                    pipe_section += 1
                                    right_arrow_appears()  # Right arrow appears
                                    q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                    q = int(q)
                                    covering_the_arrow(screen)
                                    Q[pipe_section] = q
                                    Q_grid[row][col + 1] = Q[pipe_section]
                                    pipe_section_grid[row][col + 1] = pipe_section
                                    T[pipe_section] = [T[pipe_section_grid[row - 1][col]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row][col + 1]] = T[pipe_section]

                                    # T of the triplet
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row - 1][col]][-1] - Tloss_pipe[dataset])

                                elif placement_grid[row][col - 1] != -1:
                                    pipe_section += 1
                                    up_arrow_appears()  # Up arrow appears
                                    q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                    q = int(q)
                                    covering_the_arrow(screen)
                                    Q[pipe_section] = q
                                    Q_grid[row - 1][col] = Q[pipe_section]
                                    pipe_section_grid[row - 1][col] = pipe_section
                                    T[pipe_section] = [T[pipe_section_grid[row][col - 1]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row - 1][col]] = T[pipe_section]

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

                                    # T of the triplet
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row][col - 1]][-1] - Tloss_pipe[dataset])


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
                                    up_arrow_appears()  # Down arrow appears
                                    q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                    q = int(q)
                                    covering_the_arrow(screen)
                                    Q[pipe_section] = q
                                    Q_grid[row - 1][col] = Q[pipe_section]
                                    pipe_section_grid[row - 1][col] = pipe_section
                                    T[pipe_section] = [T[pipe_section_grid[row][col + 1]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row - 1][col]] = T[pipe_section]

                                    # T of the triplet
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row][col + 1]][-1] - Tloss_pipe[dataset])

                                Q_grid[row][col] = Q[
                                    min(pipe_section_grid[row - 1][col], pipe_section_grid[row][col - 1],
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
                    elif dropdown_open == True and placed_new_item == False and icon_index == 9 and things_around == 1:
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
                                    T[pipe_section] = [T[pipe_section_grid[row - 1][col]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row][col + 1]] = T[pipe_section]

                                    pipe_section += 1
                                    down_arrow_appears()  # Down arrow appears
                                    q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                    q = int(q)
                                    covering_the_arrow(screen)
                                    Q[pipe_section] = q
                                    Q_grid[row + 1][col] = Q[pipe_section]
                                    pipe_section_grid[row + 1][col] = pipe_section
                                    T[pipe_section] = [T[pipe_section_grid[row - 1][col]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row + 1][col]] = T[pipe_section]

                                    # T of the triplet
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row - 1][col]][-1] - Tloss_pipe[dataset])

                                elif placement_grid[row][col + 1] != -1:
                                    pipe_section += 1
                                    up_arrow_appears()  # Up arrow appears
                                    q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                    q = int(q)
                                    covering_the_arrow(screen)
                                    Q[pipe_section] = q
                                    Q_grid[row - 1][col] = Q[pipe_section]
                                    pipe_section_grid[row - 1][col] = pipe_section
                                    T[pipe_section] = [T[pipe_section_grid[row][col + 1]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row - 1][col]] = T[pipe_section]

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
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row][col + 1]][-1] - Tloss_pipe[dataset])

                                elif placement_grid[row + 1][col] != -1:
                                    pipe_section += 1
                                    up_arrow_appears()  # Up arrow appears
                                    q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
                                    q = int(q)
                                    covering_the_arrow(screen)
                                    Q[pipe_section] = q
                                    Q_grid[row - 1][col] = Q[pipe_section]
                                    pipe_section_grid[row - 1][col] = pipe_section
                                    T[pipe_section] = [T[pipe_section_grid[row + 1][col]][-1] - Tloss_pipe[dataset]]
                                    T[pipe_section_grid[row - 1][col]] = T[pipe_section]

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

                                    # T of the triplet
                                    T_grid[row][col] = float(
                                        T[pipe_section_grid[row + 1][col]][-1] - Tloss_pipe[dataset])

                                Q_grid[row][col] = Q[
                                    min(pipe_section_grid[row - 1][col], pipe_section_grid[row][col + 1],
                                        pipe_section_grid[row + 1][col])]
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
                    elif dropdown_open == True and placed_new_item == False and icon_index == 6 and things_around == 2:
                        pipe_section += 1
                        if placement_grid[row + 1][col] != -1 and placement_grid[row][col - 1] != -1:
                            Q_grid[row][col + 1] = Q_grid[row + 1][col] + Q_grid[row][col - 1]
                            pipe_section_grid[row][col + 1] = pipe_section
                            Q[pipe_section] = Q_grid[row][col + 1]
                            Q_grid[row][col] = Q_grid[row + 1][col] + Q_grid[row][col - 1]
                            T[pipe_section_grid[row][col + 1]] = [
                                round(float((np.array(Q_grid[row + 1][col]) * T_grid[row + 1][col] +
                                             np.array(Q_grid[row][col - 1]) * T_grid[row][
                                                 col - 1]) / (Q_grid[row + 1][col] + Q_grid[row][
                                    col - 1]) - Tloss_pipe[dataset]), 1)]
                            T_grid[row][col] = T[pipe_section_grid[row][col + 1]]
                        if placement_grid[row + 1][col] != -1 and placement_grid[row][col + 1] != -1:
                            Q_grid[row][col - 1] = Q_grid[row + 1][col] + Q_grid[row][col + 1]
                            pipe_section_grid[row][col - 1] = pipe_section
                            Q[pipe_section] = Q_grid[row][col - 1]
                            Q_grid[row][col] = Q_grid[row + 1][col] + Q_grid[row][col + 1]
                            T[pipe_section_grid[row][col - 1]] = [
                                round(float((np.array(Q_grid[row + 1][col]) * T_grid[row + 1][col] +
                                             np.array(Q_grid[row][col + 1]) * T_grid[row][
                                                 col + 1]) / (
                                                    Q_grid[row + 1][col] + Q_grid[row][
                                                col + 1]) - Tloss_pipe[dataset]), 1)]
                            T_grid[row][col] = T[pipe_section_grid[row][col - 1]]
                        if placement_grid[row][col - 1] != -1 and placement_grid[row][col + 1] != -1:
                            Q_grid[row + 1][col] = Q_grid[row][col - 1] + Q_grid[row][col + 1]
                            pipe_section_grid[row + 1][col] = pipe_section
                            Q[pipe_section] = Q_grid[row + 1][col]
                            Q_grid[row][col] = Q_grid[row][col - 1] + Q_grid[row][col + 1]
                            T[pipe_section_grid[row + 1][col]] = [
                                round(float((np.array(Q_grid[row][col - 1]) * T_grid[row][col - 1] +
                                             np.array(Q_grid[row][col + 1]) * T_grid[row][
                                                 col + 1]) / (
                                                    Q_grid[row][col - 1] + Q_grid[row][
                                                col + 1]) - Tloss_pipe[dataset]), 1)]
                            T_grid[row][col] = T[pipe_section_grid[row + 1][col]]
                        pipe_section_grid[row][col] = -icon_index
                    elif dropdown_open == True and placed_new_item == False and icon_index == 7 and things_around == 2:
                        pipe_section += 1
                        if placement_grid[row + 1][col] != -1 and placement_grid[row][col - 1] != -1:
                            Q_grid[row - 1][col] = Q_grid[row + 1][col] + Q_grid[row][col - 1]
                            pipe_section_grid[row - 1][col] = pipe_section
                            Q[pipe_section] = Q_grid[row - 1][col]
                            Q_grid[row][col] = Q_grid[row + 1][col] + Q_grid[row][col - 1]
                            T[pipe_section_grid[row - 1][col]] = [
                                round(float((np.array(Q_grid[row + 1][col]) * T_grid[row + 1][col] +
                                             np.array(Q_grid[row][col - 1]) * T_grid[row][
                                                 col - 1]) / (
                                                    Q_grid[row + 1][col] + Q_grid[row][
                                                col - 1]) - Tloss_pipe[dataset]), 1)]
                            T_grid[row][col] = T[pipe_section_grid[row - 1][col]]
                        if placement_grid[row + 1][col] != -1 and placement_grid[row - 1][col] != -1:
                            Q_grid[row][col - 1] = Q_grid[row + 1][col] + Q_grid[row - 1][col]
                            pipe_section_grid[row][col - 1] = pipe_section
                            Q[pipe_section] = Q_grid[row][col - 1]
                            Q_grid[row][col] = Q_grid[row + 1][col] + Q_grid[row - 1][col]
                            T[pipe_section_grid[row][col - 1]] = [
                                round(float((np.array(Q_grid[row + 1][col]) * T_grid[row + 1][col] +
                                             np.array(Q_grid[row - 1][col]) * T_grid[row - 1][
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
                            T[pipe_section_grid[row + 1][col]] = [
                                round(float((np.array(Q_grid[row][col - 1]) * T_grid[row][col - 1] +
                                             np.array(Q_grid[row - 1][col]) * T_grid[row - 1][
                                                 col]) / (
                                                    Q_grid[row][col - 1] +
                                                    Q_grid[row - 1][
                                                        col]) - Tloss_pipe[dataset]), 1)]
                            T_grid[row][col] = T[pipe_section_grid[row + 1][col]]
                        pipe_section_grid[row][col] = -icon_index
                    elif dropdown_open == True and placed_new_item == False and icon_index == 8 and things_around == 2:
                        pipe_section += 1
                        if placement_grid[row - 1][col] != -1 and placement_grid[row][col - 1] != -1:
                            Q_grid[row][col + 1] = Q_grid[row - 1][col] + Q_grid[row][col - 1]
                            pipe_section_grid[row][col + 1] = pipe_section
                            Q[pipe_section] = Q_grid[row][col + 1]
                            Q_grid[row][col] = Q_grid[row - 1][col] + Q_grid[row][col - 1]
                            T[pipe_section_grid[row][col + 1]] = [
                                round(float((np.array(Q_grid[row - 1][col]) * T_grid[row - 1][col] +
                                             np.array(Q_grid[row][col - 1]) * T_grid[row][
                                                 col - 1]) / (
                                                    Q_grid[row - 1][col] + Q_grid[row][
                                                col - 1]) - Tloss_pipe[dataset]), 1)]
                            T_grid[row][col] = T[pipe_section_grid[row][col + 1]]
                        if placement_grid[row - 1][col] != -1 and placement_grid[row][col + 1] != -1:
                            Q_grid[row][col - 1] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                            pipe_section_grid[row][col - 1] = pipe_section
                            Q[pipe_section] = Q_grid[row][col - 1]
                            Q_grid[row][col] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                            T[pipe_section_grid[row][col - 1]] = [
                                round(float((np.array(Q_grid[row - 1][col]) * T_grid[row - 1][col] +
                                             np.array(Q_grid[row][col + 1]) * T_grid[row][col + 1]) / (
                                                    Q_grid[row - 1][col] + Q_grid[row][col + 1]) - Tloss_pipe[dataset]),
                                      1)]
                            T_grid[row][col] = T[pipe_section_grid[row][col - 1]]
                        if placement_grid[row][col - 1] != -1 and placement_grid[row][col + 1] != -1:
                            Q_grid[row - 1][col] = Q_grid[row][col - 1] + placement_grid[row][col + 1]
                            pipe_section_grid[row - 1][col] = pipe_section
                            Q[pipe_section] = Q_grid[row - 1][col]
                            Q_grid[row][col] = Q_grid[row][col - 1] + placement_grid[row][col + 1]
                            T[pipe_section_grid[row - 1][col]] = [
                                round(float((np.array(Q_grid[row][col - 1]) * T_grid[row][col - 1] +
                                             np.array(Q_grid[row][col + 1]) * T_grid[row][
                                                 col + 1]) / (
                                                    Q_grid[row][col - 1] + Q_grid[row][
                                                col + 1]) - Tloss_pipe[dataset]), 1)]
                            T_grid[row][col] = T[pipe_section_grid[row - 1][col]]
                        pipe_section_grid[row][col] = -icon_index
                    elif dropdown_open == True and placed_new_item == False and icon_index == 9 and things_around == 2:
                        pipe_section += 1
                        if placement_grid[row + 1][col] != -1 and placement_grid[row][col + 1] != -1:
                            Q_grid[row - 1][col] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                            pipe_section_grid[row - 1][col] = pipe_section
                            Q[pipe_section] = Q_grid[row - 1][col]
                            Q_grid[row][col] = Q_grid[row + 1][col] + Q_grid[row][col + 1]
                            T[pipe_section_grid[row - 1][col]] = [
                                round(float(np.array((Q_grid[row + 1][col]) * T_grid[row + 1][col] +
                                                     np.array(Q_grid[row][col + 1]) * T_grid[row][
                                                         col + 1]) / (
                                                    Q_grid[row + 1][col] + Q_grid[row][
                                                col + 1]) - Tloss_pipe[dataset]), 1)]
                            T_grid[row][col] = T[pipe_section_grid[row - 1][col]]
                        if placement_grid[row - 1][col] != -1 and placement_grid[row][col + 1] != -1:
                            Q_grid[row + 1][col] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                            pipe_section_grid[row + 1][col] = pipe_section
                            Q[pipe_section] = Q_grid[row + 1][col]
                            Q_grid[row][col] = Q_grid[row - 1][col] + Q_grid[row][col + 1]
                            T[pipe_section_grid[row + 1][col]] = [
                                round(float((np.array(Q_grid[row - 1][col]) * T_grid[row - 1][col] +
                                             np.array(Q_grid[row][col + 1]) * T_grid[row][
                                                 col + 1]) / (
                                                    Q_grid[row - 1][col] + Q_grid[row][
                                                col + 1]) - Tloss_pipe[dataset]), 1)]
                            T_grid[row][col] = T[pipe_section_grid[row + 1][col]]
                        if placement_grid[row - 1][col] != -1 and placement_grid[row + 1][col] != -1:
                            Q_grid[row][col + 1] = Q_grid[row - 1][col] + Q_grid[row + 1][col]
                            pipe_section_grid[row][col + 1] = pipe_section
                            Q[pipe_section] = Q_grid[row][col + 1]
                            Q_grid[row][col] = Q_grid[row - 1][col] + Q_grid[row + 1][col]
                            T[pipe_section_grid[row][col + 1]] = [
                                round(float((np.array(Q_grid[row + 1][col]) * T_grid[row + 1][col] +
                                             np.array(Q_grid[row - 1][col]) * T_grid[row - 1][
                                                 col]) / (
                                                    Q_grid[row + 1][col] +
                                                    Q_grid[row - 1][
                                                        col]) - Tloss_pipe[dataset]), 1)]
                            T_grid[row][col] = T[pipe_section_grid[row][col + 1]]
                        pipe_section_grid[row][col] = -icon_index
                    dropdown_open = False
                    number_of_items += 1
                    # Add the placed icon to the undo stack
                    undo_stack.append((row, col, icon_index))
                    print(icon_index)
                    drawing_grid()
                    placed_new_item = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and not dropdown_open:
                row = (event.pos[1] - square_y) // square_size
                col = (event.pos[0] - square_x) // square_size
                right_click_grid_cell_info(event, row, col)
            elif budget_calculated < 0:
                game_over_budget()
            elif Q_grid[rw_row[dataset] - 1][rw_col[dataset]] != -2:
                if (house0_col[dataset] > 0 and Q_grid[house0_row[dataset] - 1][house0_col[dataset]] < 0) or \
                        (house1_col[dataset] > 0 and Q_grid[house1_row[dataset] - 1][house1_col[dataset]] < 0) or \
                        (house2_col[dataset] > 0 and Q_grid[house2_row[dataset] - 1][house2_col[dataset]] < 0) or \
                        (greenhouse0_col[dataset] > 0 and Q_grid[greenhouse0_row[dataset] - 1][
                            greenhouse0_col[dataset]] < 0) or \
                        (greenhouse1_col[dataset] > 0 and Q_grid[greenhouse1_row[dataset] - 1][
                            greenhouse1_col[dataset]] < 0):
                    game_over_users_not_satisfied()
                else:
                    if rw_row[dataset] > 0 and rw_existence == True and placement_grid[rw_row[dataset] - 1][
                        rw_col[dataset]] != -1:
                        game_over_ending()
                    else:
                        if placement_grid[outflow_row[dataset] - 1][outflow_col[dataset]] != -1:
                            game_over_ending()
            if (things_around_up > 0 and pipe_section_grid[row - 1][col] > 0 and pipe_section_grid[row][col] > 0 and
                pipe_section_grid[row - 1][col] != pipe_section_grid[row][col]) or \
                    (things_around_right > 0 and pipe_section_grid[row][col + 1] > 0 and pipe_section_grid[row][
                        col] > 0 and
                     pipe_section_grid[row][col + 1] != pipe_section_grid[row][col]) or \
                    (things_around_down > 0 and pipe_section_grid[row + 1][col] > 0 and pipe_section_grid[row][
                        col] > 0 and
                     pipe_section_grid[row + 1][col] != pipe_section_grid[row][col]) or \
                    (things_around_left > 0 and pipe_section_grid[row][col - 1] > 0 and pipe_section_grid[row][
                        col] > 0 and
                     pipe_section_grid[row][col - 1] != pipe_section_grid[row][col]):
                # print("xxx xxx xxx xxx xxx xxx")
                game_over_triplet_issue()
            if (house0_row[dataset] > 0 and placement_grid[house0_row[dataset] - 1][house0_col[dataset]] != -1 and
                Q_grid[house0_row[dataset] - 1][house0_col[dataset]] !=
                            Q_grid[house0_row[dataset]][house0_col[dataset]]) or \
                (house1_row[dataset] > 0 and placement_grid[house1_row[dataset] - 1][house1_col[dataset]] != -1 and
                 Q_grid[house1_row[dataset] - 1][house1_col[dataset]] !=
                            Q_grid[house1_row[dataset]][house1_col[dataset]]) or \
                (house2_row[dataset] > 0 and placement_grid[house2_row[dataset] - 1][house2_col[dataset]] != -1 and
                 Q_grid[house2_row[dataset] - 1][house2_col[dataset]] !=
                            Q_grid[house2_row[dataset]][house2_col[dataset]]) or \
                (greenhouse0_row[dataset] > 0 and placement_grid[greenhouse0_row[dataset] - 1][greenhouse0_col[dataset]] != -1 and
                 Q_grid[greenhouse0_row[dataset] - 1][greenhouse0_col[dataset]] !=
                            Q_grid[greenhouse0_row[dataset]][greenhouse0_col[dataset]]) or \
                (greenhouse1_row[dataset] > 0 and placement_grid[greenhouse1_row[dataset] - 1][greenhouse1_col[dataset]] != -1 and
                 Q_grid[greenhouse1_row[dataset] - 1][greenhouse1_col[dataset]] !=
                            Q_grid[greenhouse1_row[dataset]][greenhouse1_col[dataset]]):
                game_over_Q_inconsistent()
            # Arrange the pipe_section_grid properly
            info_ghouse_blue_square()
            if house0_row[dataset] > 0: pipe_section_grid_for_icon_house0()
            if house1_row[dataset] > 0: pipe_section_grid_for_icon_house1()
            if house2_row[dataset] > 0: pipe_section_grid_for_icon_house2()
            if greenhouse0_row[dataset] > 0: pipe_section_grid_for_icon_greenhouse0()
            if greenhouse1_row[dataset] > 0: pipe_section_grid_for_icon_greenhouse1()

        #drawing_grid()

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
            print(T)
            print(Starting_Q)
            render_q2_dictionary(Q2, T, screen)
            print(username)
            print("things_around= ", things_around)
            print("things_around_left =", things_around_left)
            print("things_around_up= ", things_around_up)
            print("things_around_right= ", things_around_right)
            print("things_around_down= ", things_around_down)
            things_around_left = 0
            things_around_right = 0
            things_around_down = 0
            things_around_up = 0

        # Limit the frame rate to reduce blinking
        clock.tick(60)

        # Update the display
        pygame.display.update()

    # Quit Pygame
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    try:
        combined_start_function()
        main_loop()
    except SystemExit:
        pass  # Allow the program to exit normally
    except Exception as e:
        print(f"An error occurred: {e}")  # Optional: log the error for debugging
        sys.exit()