# Importing modules
import pygame
import sys

# Initialise pygame
pygame.init()

# Creating the game window
screen = pygame.display.set_mode()
width, height = screen.get_size()
screen = pygame.display.set_mode((width, height/2))

# Setting the caption on startup
pygame.display.set_caption("Blob Dodge - Main Menu")

# Fonts
GothamBlackHeader = pygame.font.Font("assets/Gotham Black.ttf", 100)
GothamBlackSmaller = pygame.font.Font("assets/Gotham Black.ttf", 50)

def gameLoop():
    # Loop for the game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fills the screen grey 
        screen.fill((40,43,48))

        # Makes the game run at 60 FPS
        pygame.time.Clock().tick(60)
        pygame.display.update()

def mainMenu():
    # importing classes used in the main menu to avoid a circular import error
    from classes.button import Button

    # All instances of main menu buttons
    playbutton = Button("PLAY", 620, 155, (242, 225, 36), (255, 192, 20), True)

    # Loop for the main menu
    while True:
        for event in pygame.event.get():
            # If the mouse button is pressed, go to the game loop
            if event.type == pygame.MOUSEBUTTONDOWN and playbutton.isClicked():
                pygame.display.set_caption("Blob Dodge - Game Loop")
                gameLoop()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fills the screen grey 
        screen.fill((40,43,48))
        playbutton.drawButton()
        playbutton.isHovered()

        # Puts the main menu text at the top of the screen
        MMtext = GothamBlackHeader.render("MAIN MENU", True, "white")
        main_menu_text_rect = MMtext.get_rect(center=(width // 2, height // 12))
        screen.blit(MMtext, (main_menu_text_rect))

        # Makes the game run at 60 FPS
        pygame.time.Clock().tick(60)
        pygame.display.update()

if __name__ == "__main__":
    mainMenu()