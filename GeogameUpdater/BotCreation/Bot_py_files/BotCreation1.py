import subprocess
import os
import pyautogui
import time
import threading

def run_python_file(file_path):
    try:
        subprocess.run(['python', file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def print_mouse_coordinates():
    while True:
        x, y = pyautogui.position()
        print(f"Mouse position: ({x}, {y})")
        time.sleep(1)

def locate_play_button():
    try:
        res = pyautogui.locateOnScreen("PlayButtonTemplate.png")
        if res is None:
            raise pyautogui.ImageNotFoundException(f"Image 'PlayButtonTemplate.png' not found on the screen.")
        print(res)
    except pyautogui.ImageNotFoundException as e:
        print(f"Error: {e}")
    return
def run_game(file_path):
    run_python_file(file_path)

# Example usage
root_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(root_dir, "Geogame71.py")
startingscreenpath = os.path.join(root_dir, "IconsForBotTrainging", "StartingScreen.png")
template_path = os.path.join(root_dir, "PlayButtonTemplate.png")
# Start the game in a separate thread
game_thread = threading.Thread(target=run_game, args=(file_path,))
game_thread.start()

locate_play_button()
# Wait for the game to open (you may need to adjust the sleep duration)
time.sleep(3)

# Get the coordinates (replace these values with your actual coordinates)
click_x = 1293
click_y = 688

# Perform the click
pyautogui.click(click_x, click_y)
pyautogui.press('enter')
pyautogui.write("BotSolver1")
print("I reached here")
