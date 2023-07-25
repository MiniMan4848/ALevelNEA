# Import modules
import pygame
import sys

# Initialise pygame
pygame.init()

# Creating the game window
screen = pygame.display.set_mode()
width, height = screen.get_size()
screen = pygame.display.set_mode((width, height/2))

# Fonts
GothamBlack = pygame.font.Font("Assets/Gotham Black.ttf", 100)

def gameLoop():
    # Loop for the game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fills the screen blue and says thats its the game loop
        screen.fill((0, 0, 100))
        GLtext = GothamBlack.render("This is the Game Loop", True, "white")

        # Center the text on the screen using the rectangle around the text
        text_rect = GLtext.get_rect(center=(width // 2, height // 4))
        screen.blit(GLtext, (text_rect))

        # Makes the game run at 60 FPS
        pygame.time.Clock().tick(60)
        pygame.display.update()

def mainMenu():
    # Loop for the main menu
    while True:
        for event in pygame.event.get():
            # If the mouse button is pressed, go to the game loop
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.display.set_caption("Blob Dodge - Game Loop")
                gameLoop()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fills the screen red and says thats its the main menu
        screen.fill((100, 0, 0))
        MMtext = GothamBlack.render("This is the Main Menu", True, "white")

        # Center the text on the screen using the rectangle around the text
        text_rect = MMtext.get_rect(center=(width // 2, height // 4))
        screen.blit(MMtext, (text_rect))

        # Makes the game run at 60 FPS
        pygame.time.Clock().tick(60)
        pygame.display.update()

mainMenu()