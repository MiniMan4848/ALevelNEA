# Importing modules
import pygame
import sys

# Initialise pygame
pygame.init()

# Creating the game window
screen = pygame.display.set_mode()
width, height = screen.get_size()
screen = pygame.display.set_mode((width, height/2))

# Constants
BGCOL = (40,43,48)

# Setting the caption on startup
pygame.display.set_caption("Blob Dodge - Main Menu")

# Fonts
fonts = {
    "Header":pygame.font.Font("assets/Gotham Black.ttf", 100),
    "Smaller":pygame.font.Font("assets/Gotham Black.ttf", 50),
    "Tiny":pygame.font.Font("assets/Gotham Black.ttf", 20)
}
            
def gameLoop():
    # Loop for the game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fills the screen grey 
        screen.fill(BGCOL)

        # Makes the game run at 60 FPS
        pygame.time.Clock().tick(60)
        pygame.display.update()

def mainMenu():
    # importing classes used in the main menu to avoid a circular import error
    from classes.button import Button

    # Popup flags
    settingsflag = False
    helpflag = False

    # All instances of main menu buttons, x pos is None because automatically centered on that axis
    playbutton = Button("PLAY", None, 155, (242, 225, 36), (255, 192, 20), fonts["Smaller"], 25, 10, True)
    settingsbutton = Button("SETTINGS", None, 240, (242, 225, 36), (255, 192, 20), fonts["Smaller"], 25, 10, True)
    helpbutton = Button("HELP", None, 360, (242, 225, 36), (255, 192, 20), fonts["Tiny"], 10, 5, True)

    # Loop for the main menu
    while True:
        for event in pygame.event.get():
            # If the mouse button is pressed, go to the game loop
            if event.type == pygame.MOUSEBUTTONDOWN and playbutton.isClicked():
                pygame.display.set_caption("Blob Dodge - Game Loop")
                gameLoop()

            # If the settings button is pressed, open the settings window
            if event.type == pygame.MOUSEBUTTONDOWN and settingsbutton.isClicked():
                settingsflag = True

            # If the help button is pressed, open the help window
            if event.type == pygame.MOUSEBUTTONDOWN and helpbutton.isClicked():
                helpflag = True

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fills the screen grey 
        screen.fill(BGCOL)
        
        # Calling the drawing and hovering methods to the play and settings button
        playbutton.drawButton()
        playbutton.isHovered()

        settingsbutton.drawButton()
        settingsbutton.isHovered()

        helpbutton.drawButton()
        helpbutton.isHovered()

        # Puts the main menu text at the top of the screen
        MMtext = fonts["Header"].render("MAIN MENU", True, "white")
        main_menu_text_rect = MMtext.get_rect(center=(width // 2, height // 12))
        screen.blit(MMtext, (main_menu_text_rect))

        if settingsflag == True:
            from classes.popup import Popup
            # Create an instance of a popup window
            SettingsPopup = Popup()
            SettingsPopup.drawPopup()
            SettingsPopup.backButton()
            
            # Disable the play and settings button when the popup is open
            playbutton = Button("PLAY", 620, 155, (242, 225, 36), (255, 192, 20), fonts["Smaller"], 25, 10, False)
            settingsbutton = Button("SETTINGS", 570, 240, (242, 225, 36), (255, 192, 20), fonts["Smaller"], 25, 10, False)

        if helpflag == True:
            from classes.popup import Popup
            # Create an instance of a popup window
            HelpPopup = Popup()
            HelpPopup.drawPopup()
            HelpPopup.backButton()

            # Disable the play and settings button when the popup is open
            playbutton = Button("PLAY", 620, 155, (242, 225, 36), (255, 192, 20), fonts["Smaller"], 25, 10, False)
            settingsbutton = Button("SETTINGS", 570, 240, (242, 225, 36), (255, 192, 20), fonts["Smaller"], 25, 10, False)

        # Makes the game run at 60 FPS
        pygame.time.Clock().tick(60)
        pygame.display.update()

if __name__ == "__main__":
    mainMenu()
