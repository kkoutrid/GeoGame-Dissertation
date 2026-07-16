import pygame
import os
import numpy as np  # Numeric functions and arrays
import pandas as pd
import webbrowser
from openpyxl import load_workbook
import math
from exam_mode1 import run as run_exam_mode
from Geogame81 import run as run_exam_mode

os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'

# Initialize Pygame
pygame.init()

# Settings for the opening/loading screen
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
icons = []
icon_UKflag_path = os.path.join(icon_dir, "UKflag.png")
icon_UKflag = pygame.image.load(icon_UKflag_path).convert_alpha()
icon_Greeceflag_path = os.path.join(icon_dir, "Greeceflag.png")
icon_Greeceflag = pygame.image.load(icon_Greeceflag_path).convert_alpha()
icon_bug_report_path = os.path.join(icon_dir, "bug_report.png")
icon_bug_report = pygame.image.load(icon_bug_report_path).convert_alpha()
# Load the fonts
title_font = root_dir + "\GameAssets\Fonts\Handjet\static\Handjet-Light.ttf"
info_font = root_dir + "\GameAssets\Fonts\Roboto\Roboto-Medium.ttf"
info_font2 = root_dir + "\GameAssets\Fonts\PtSerif\PTSerif-Bold.ttf"

# pygame.time.wait(2000)

# Screen settings for normal game
screen_width = 1005
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SRCALPHA)

pygame.display.set_caption("Geogame")

for i in range(1, 11):
    icon_path = os.path.join(icon_dir, f"icon{i}.png")
    icon_image = pygame.image.load(icon_path).convert_alpha()
    icons.append(icon_image)
# Define the square properties
square_x = 64  # Grid top left x coordinate start
square_y = 64  # Grid top left y coordinate start

button_width = 100
button_height = 50

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
    training_mode_button = Button(screen_width // 2 - 100, screen_height // 2 - 50, 200, 50, "Play", RED, WHITE)
    exam_mode_button = Button(screen_width // 2 - 100, screen_height // 2 + 25, 200, 50, "Instructions", RED, WHITE)
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
                if training_mode_button.is_clicked(pygame.mouse.get_pos()):
                    Geogame81.run()
                elif exam_mode_button.is_clicked(pygame.mouse.get_pos()):
                    exam_mode1.run()
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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                return  # Exit the function to start the game
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                language_change()
            #elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                #exam()
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
        training_mode_button.draw(screen)
        exam_mode_button.draw(screen)
        language_button.draw(screen)
        bug_report_button.draw(screen)
        high_score_button.draw(screen)
        exam_mode_button.draw(screen)

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

#def exam():
    #exam_mode1.run()
def language_change():
    global language

    if language == 'en':
        language = 'gr'
    elif language == 'gr':
        language = 'en'
    return language


def bug_report_button_uploader_2():
    # Open GitHub Issues page in default web browser
    webbrowser.open('https://github.com/kkoutrid/Geogame-Downloader/issues')

transparent_surface_visible2 = False
if __name__ == "__main__":
    display_start_menu()