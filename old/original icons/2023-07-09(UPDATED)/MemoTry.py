import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Set up the window
window_size = (400, 200)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Inventory Memo")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Load your icon images (Replace "icons" with your directory containing the icon images)
icon_dir = "icons"
icons = []
for i in range(1, 11):
    icon_path = os.path.join(icon_dir, f"icon{i}.png")
    icon_image = pygame.image.load(icon_path).convert_alpha()
    icons.append(icon_image)

def create_inventory_memo(player_name, memo_title, icon_index, Q_value, T_value):
    font = pygame.font.Font(None, 28)

    # Clear the screen
    screen.fill(white)

    # Display player name and memo title
    player_text = font.render(f"Memo for {player_name}:", True, black)
    title_text = font.render(f"Title: {memo_title}", True, black)
    screen.blit(player_text, (20, 20))
    screen.blit(title_text, (20, 50))

    # Display the icon and Q, T information based on the icon_index
    icon_image = icons[icon_index - 1]  # Subtract 1 to get the correct index in the list
    screen.blit(icon_image, (20, 100))
    Q_text = font.render(f"Q: {Q_value}", True, black)
    T_text = font.render(f"T: {T_value}", True, black)
    screen.blit(Q_text, (80, 120))
    screen.blit(T_text, (180, 120))

    pygame.display.flip()

# Example usage:
player_name = "John"
memo_title = "Inventory Memo"
icon_index = 5  # Replace this with the desired icon index (1 to 10)
Q_value = 10
T_value = 5

# Run the memo display
create_inventory_memo(player_name, memo_title, icon_index, Q_value, T_value)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
