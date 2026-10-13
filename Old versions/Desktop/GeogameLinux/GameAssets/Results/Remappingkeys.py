import keyboard

# Define your custom key mappings
# If the device sends 'c' for key presses, remap them to other keys or actions
def remap_key(key):
    if key.name == 'c':  # If the key pressed is 'c'
        # Perform the action you want - e.g., send Alt+F4
        keyboard.press_and_release('alt+f4')
        print("Alt+F4 triggered by key press 'c'")c
# Listen for all key presses
keyboard.hook(remap_key)

# Keep the program running so it can listen for key presses
keyboard.wait('esc')  # This will exit the script when 'esc' is pressed
